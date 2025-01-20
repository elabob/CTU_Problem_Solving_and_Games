def read_classification_from_file (file_path) :
     """
    Nacita klasifikaciu emailov z textoveho suboru do slovnika.

    :param file_path: Cesta k textovemu suboru (napr. !truth.txt alebo !prediction.txt)
    :return: Slovnik, kde kluc je nazov suboru a hodnota je klasifikacia ('OK' alebo 'SPAM').
    """
     classification_dict = {}
     try :
         with open (file_path, "r", encoding = "utf-8") as file :
             for line in file :
                 parts = line.strip ().split ()
                 if len (parts) == 2 :
                     filename, classification = parts
                     classification_dict [filename] = classification
     except FileNotFoundError :
         print (f"Soubor {file_path} nebyl nalezen.")
     except Exception as e :
         print (f"Došlo k chybě při čtení souboru: {e}")

     return classification_dict


# Test funkce
if __name__ == "__main__" :
    # Testovací volání
    test_file_path = "test_truth.txt"
    classification = read_classification_from_file (test_file_path)
    print (classification)