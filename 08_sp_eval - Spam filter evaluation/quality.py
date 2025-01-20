from confmat import BinaryConfusionMatrix
from utils import read_classification_from_file


def quality_score (tp, tn, fp, fn) :
    """
    Spočítá skóre kvality na základě matice záměn.

    :param tp: Počet True Positives
    :param tn: Počet True Negatives
    :param fp: Počet False Positives
    :param fn: Počet False Negatives
    :return: Skóre kvality filtru (hodnota mezi 0 a 1)
    """
    denominator = tp + tn + 10 * fp + fn
    if denominator == 0 :
        return 0  # Zajistíme, že nedojde k dělení nulou
    return (tp + tn) / denominator


def compute_quality_for_corpus (corpus_dir) :
    """
    Spočítá kvalitu filtru na základě souborů v daném adresáři korpusu.

    :param corpus_dir: Adresář obsahující soubory !truth.txt a !prediction.txt.
    :return: Skóre kvality filtru (hodnota mezi 0 a 1)
    """
    # Načteme správné a predikované klasifikace
    truth_dict = read_classification_from_file (f"{corpus_dir}/!truth.txt")
    pred_dict = read_classification_from_file (f"{corpus_dir}/!prediction.txt")

    # Vytvoříme instanci matice záměn
    cm = BinaryConfusionMatrix (pos_tag = "SPAM", neg_tag = "OK")

    # Spočítáme matici záměn na základě načtených slovníků
    cm.compute_from_dicts (truth_dict, pred_dict)

    # Získáme hodnoty TP, TN, FP, FN
    tp, tn, fp, fn = cm.tp, cm.tn, cm.fp, cm.fn

    # Spočítáme kvalitu filtru
    return quality_score (tp, tn, fp, fn)
