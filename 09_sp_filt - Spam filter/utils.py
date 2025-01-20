def read_classification_from_file(file_path):
    classification_dict = {}
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            for line in file:
                parts = line.strip().split()
                if len(parts) != 2:
                    print(f"Warning: Malformed line in {file_path}: {line}")
                    continue
                filename, classification = parts
                classification_dict[filename] = classification
    except FileNotFoundError:
        print(f"File {file_path} not found.")
    except Exception as e:
        print(f"Error reading file: {e}")

    return classification_dict
