class MyVector:
    def __init__(self, elements):
        # Konstruktor uklada prvky vektorov
        self.elements = elements

    def get_vector(self):
        # Vracia zoznam prvkov vektorov
        return self.elements

    def __mul__(self, other):
        # Skalárny súčin: súčet súčinov odpovedajúcich prvkov
        result = 0
        for a, b in zip (self.elements, other.get_vector ()):
            result += a * b
        return result


# Kontrola kódu
if __name__ == "__main__":
    vec1 = MyVector ([1, 2, 3])
    vec2 = MyVector ([3, 4, 5])

    print (vec1.get_vector ())  # Výstup: [1, 2, 3]
    dot_product = vec1 * vec2  # Výpočet skalárného súčinu
    print (dot_product)  # Výstup: 26
