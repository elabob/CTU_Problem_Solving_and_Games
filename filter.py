from basefilter import BaseFilter
from utils import read_classification_from_file
import os
import re
import math
from collections import Counter, defaultdict
from typing import Dict, Set

class MyFilter(BaseFilter):
    def __init__(self):
        self.word_scores = defaultdict(float)
        self.spam_prior = 0.5
        self.min_word_length = 2
        
        # Vyrazne zvysene vahy pre spam slova
        self.spam_words = {
            'win': 4.0, 'cash': 4.5, 'prize': 4.0, 'lottery': 4.5,
            'urgent': 3.5, 'free': 3.0, 'offer': 3.0, 'click': 4.0,
            'buy': 3.0, 'investment': 3.5, 'viagra': 5.0, 'money': 4.0,
            'guarantee': 3.5, 'credit': 3.5, 'loan': 4.0, 'debt': 3.5,
            'casino': 4.5, 'bonus': 3.5, 'discount': 3.0, 'limited': 3.0,
            'subscribe': 3.0, 'promotion': 3.5, 'winner': 4.0, 'pills': 4.0,
            'dollars': 3.5, 'prices': 3.0, 'income': 3.5, 'earn': 3.8,
            'spam': 5.0, 'advertisement': 3.5, 'marketing': 3.0,
            'pharmacy': 4.5, 'medication': 4.0, 'cure': 3.5, 'weight': 3.0,
            'success': 3.0, 'millions': 4.0, 'guaranteed': 3.5, 'unlimited': 3.5,
            'risk-free': 4.0, 'investment': 3.5, 'opportunity': 3.0
        }
        
        self.stop_words = {
            'the', 'be', 'to', 'of', 'and', 'a', 'in', 'that', 'have', 'i', 
            'it', 'for', 'not', 'on', 'with', 'he', 'as', 'you', 'do', 'at',
            'this', 'but', 'his', 'by', 'from', 'they', 'we', 'say', 'her'
        }
        
        # Pridane bigramy pre lepsiu detekciu
        self.spam_bigrams = {
            'click here': 4.0, 'buy now': 4.0, 'limited time': 3.5,
            'special offer': 3.5, 'act now': 3.5, 'money back': 3.5,
            'credit card': 3.0, 'free trial': 3.5
        }

    def _clean_text(self, text: str) -> str:
        text = text.lower()
        # Zachovanie dolára a ďalších menových symbolov
        text = text.replace('$', ' dollar ')
        text = text.replace('€', ' euro ')
        text = text.replace('£', ' pound ')
        # Odstránenie URL
        text = re.sub(r'http[s]?://\S+', ' URL ', text)
        # Odstránenie HTML
        text = re.sub(r'<[^>]+>', ' HTML ', text)
        # Nahradenie čísel
        text = re.sub(r'\d+(?:\.\d+)?%', ' PERCENTAGE ', text)
        text = re.sub(r'\d+(?:\.\d+)?', ' NUMBER ', text)
        # Odstránenie špeciálnych znakov ale zachovanie exclamation marks
        text = re.sub(r'!+', ' EXCLAMATION ', text)
        text = re.sub(r'[^\w\s]', ' ', text)
        return ' '.join(text.split())

    def _get_features(self, text: str):
        words = text.split()
        features = Counter()
        
        # Unikátne slová
        for word in set(words):
            if len(word) >= self.min_word_length and word not in self.stop_words:
                features[word] += 1
        
        # Bigramy
        for i in range(len(words) - 1):
            bigram = f"{words[i]} {words[i+1]}"
            if bigram in self.spam_bigrams:
                features[bigram] += 1
        
        # Špeciálne features
        features['EXCLAMATION_COUNT'] = text.count('EXCLAMATION')
        features['URL_COUNT'] = text.count('URL')
        features['NUMBER_COUNT'] = text.count('NUMBER')
        
        return features

    def train(self, training_dir: str):
        try:
            truth_path = os.path.join(training_dir, '!truth.txt')
            truth_data = read_classification_from_file(truth_path)

            spam_features = Counter()
            ham_features = Counter()
            total_spam, total_ham = 0, 0

            # Trénovanie
            for filename, label in truth_data.items():
                file_path = os.path.join(training_dir, filename)
                if not os.path.isfile(file_path):
                    continue

                with open(file_path, 'r', encoding='utf-8') as f:
                    content = self._clean_text(f.read())
                features = self._get_features(content)

                if label == 'SPAM':
                    spam_features.update(features)
                    total_spam += 1
                else:
                    ham_features.update(features)
                    total_ham += 1

            self.spam_prior = (total_spam + 1) / (total_spam + total_ham + 2)

            # Výpočet skóre pre features
            all_features = set(spam_features) | set(ham_features)
            for feature in all_features:
                # Agresívnejší Laplace smoothing
                spam_freq = spam_features[feature] + 0.1
                ham_freq = ham_features[feature] + 0.1
                
                # Normalizácia
                spam_prob = spam_freq / (total_spam + 0.1)
                ham_prob = ham_freq / (total_ham + 0.1)
                
                score = math.log(spam_prob / ham_prob)
                
                # Aplikácia váh pre známe spam slová a bigramy
                if feature in self.spam_words:
                    score *= self.spam_words[feature]
                elif feature in self.spam_bigrams:
                    score *= self.spam_bigrams[feature]
                
                self.word_scores[feature] = score

        except Exception as e:
            print(f"Error during training: {e}")

    def _predict_email(self, directory: str, filename: str) -> str:
        try:
            file_path = os.path.join(directory, filename)
            with open(file_path, 'r', encoding='utf-8') as f:
                content = self._clean_text(f.read())
            
            features = self._get_features(content)
            
            # Výpočet celkového skóre
            score = 0
            feature_count = 0
            
            for feature, count in features.items():
                if feature in self.word_scores:
                    feature_score = self.word_scores[feature] * count
                    # Penalizácia pre ham features
                    if feature_score < 0:
                        feature_score *= 0.8
                    score += feature_score
                    feature_count += count
            
            # Normalizácia a aplikácia agresívnejšieho prahu
            if feature_count > 0:
                score = score / math.sqrt(feature_count)
            
            # Agresívnejší prah
            threshold = math.log(self.spam_prior / (1 - self.spam_prior)) - 0.3
            
            return 'SPAM' if score > threshold else 'OK'

        except Exception as e:
            print(f"Error processing {filename}: {e}")
            return 'OK'
        