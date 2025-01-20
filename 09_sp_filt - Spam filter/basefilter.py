import os

class BaseFilter:
    def train(self, training_dir):
        pass
    
    def test(self, testing_dir):
        predictions = self._make_predictions(testing_dir)
        self._save_predictions(testing_dir, predictions)
    
    def _make_predictions(self, directory):
        predictions = {}
        for filename in os.listdir(directory):
            if filename.startswith('!'):
                continue
            predictions[filename] = self._predict_email(directory, filename)
        return predictions
    
    def _predict_email(self, directory, filename):
        raise NotImplementedError
    
    def _save_predictions(self, directory, predictions):
        prediction_path = os.path.join(directory, '!prediction.txt')
        try:
            with open(prediction_path, 'w', encoding='utf-8') as f:
                for filename, prediction in sorted(predictions.items()):
                    f.write(f'{filename} {prediction}\n')
        except Exception as e:
            print(f"Error saving predictions to {prediction_path}: {e}")
