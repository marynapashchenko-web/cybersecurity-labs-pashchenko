class CipherAnalysis:
    def __init__(self):
        self.ukrainian_alphabet = 'АБВГҐДЕЄЖЗИІЇЙКЛМНОПРСТУФХЦЧШЩЬЮЯ'
    
    # ========== ШИФР ЦЕЗАРЯ ==========
    def generate_caesar_key(self, birth_date):
        """Генерація ключа з дати народження (сума цифр)"""
        digits = [int(d) for d in birth_date if d.isdigit()]
        return sum(digits)
    
    def caesar_encrypt(self, text, shift):
        """Шифрування методом Цезаря"""
        result = []
        for char in text:
            upper_char = char.upper()
            if upper_char in self.ukrainian_alphabet:
                old_index = self.ukrainian_alphabet.index(upper_char)
                new_index = (old_index + shift) % len(self.ukrainian_alphabet)
                new_char = self.ukrainian_alphabet[new_index]
                result.append(new_char.lower() if char.islower() else new_char)
            else:
                result.append(char)
        return ''.join(result)
    
    def caesar_decrypt(self, text, shift):
        """Розшифрування методом Цезаря"""
        return self.caesar_encrypt(text, -shift)
    
    # ========== ШИФР ВІЖЕНЕРА ==========
    def vigenere_encrypt(self, text, key):
        """Шифрування методом Віженера"""
        result = []
        key_upper = key.upper()
        key_index = 0
        
        for char in text:
            upper_char = char.upper()
            if upper_char in self.ukrainian_alphabet:
                text_index = self.ukrainian_alphabet.index(upper_char)
                key_char = key_upper[key_index % len(key_upper)]
                key_shift = self.ukrainian_alphabet.index(key_char)
                new_index = (text_index + key_shift) % len(self.ukrainian_alphabet)
                new_char = self.ukrainian_alphabet[new_index]
                result.append(new_char.lower() if char.islower() else new_char)
                key_index += 1
            else:
                result.append(char)
        return ''.join(result)
    
    def vigenere_decrypt(self, text, key):
        """Розшифрування методом Віженера"""
        result = []
        key_upper = key.upper()
        key_index = 0
        
        for char in text:
            upper_char = char.upper()
            if upper_char in self.ukrainian_alphabet:
                text_index = self.ukrainian_alphabet.index(upper_char)
                key_char = key_upper[key_index % len(key_upper)]
                key_shift = self.ukrainian_alphabet.index(key_char)
                new_index = (text_index - key_shift) % len(self.ukrainian_alphabet)
                new_char = self.ukrainian_alphabet[new_index]
                result.append(new_char.lower() if char.islower() else new_char)
                key_index += 1
            else:
                result.append(char)
        return ''.join(result)
    
    # ========== АНАЛІЗ ==========
    def analyze_cipher(self, original, encrypted, key_complexity):
        """Аналіз результатів шифрування"""
        unique_chars = len(set(c for c in encrypted if c.upper() in self.ukrainian_alphabet))
        
        # Оцінка читабельності(чи схожий на український текст)
        common_bigrams = ['НА', 'ПО', 'ПР', 'СТ', 'ВІ']
        readability_score = sum(1 for bg in common_bigrams if bg in encrypted.upper())
        readability = "Низька" if readability_score < 2 else "Середня" if readability_score < 4 else "Висока"
        
        return {
            'довжина': len(encrypted),
            'унікальних_символів': unique_chars,
            'читабельність': readability,
            'складність_ключа': key_complexity
        }
    
    def print_comparison_table(self, caesar_analysis, vigenere_analysis):
        """Виведення порівняльної таблиці"""
        print("\n" + "="*70)
        print("ПОРІВНЯЛЬНА ТАБЛИЦЯ РЕЗУЛЬТАТІВ".center(70))
        print("="*70)
        print(f"{'Параметр':<30} {'Цезар':<20} {'Віженер':<20}")
        print("-"*70)
        print(f"{'Довжина результату':<30} {caesar_analysis['довжина']:<20} {vigenere_analysis['довжина']:<20}")
        print(f"{'Унікальних символів':<30} {caesar_analysis['унікальних_символів']:<20} {vigenere_analysis['унікальних_символів']:<20}")
        print(f"{'Читабельність':<30} {caesar_analysis['читабельність']:<20} {vigenere_analysis['читабельність']:<20}")
        print(f"{'Складність ключа':<30} {caesar_analysis['складність_ключа']:<20} {vigenere_analysis['складність_ключа']:<20}")
        print("="*70)


# ========== ДЕМОНСТРАЦІЯ РОБОТИ ==========
def main():
    cipher = CipherAnalysis()
    
    print("╔" + "="*68 + "╗")
    print("║" + "ПОРІВНЯЛЬНИЙ АНАЛІЗ ШИФРІВ ЦЕЗАРЯ ТА ВІЖЕНЕРА".center(68) + "║")
    print("╚" + "="*68 + "╝")
    
    # Введення персональних даних
    print("\nВВЕДЕННЯ ПЕРСОНАЛЬНИХ ДАНИХ:")
    surname = input("Введіть прізвище (для ключа Віженера): ").strip() or "Шевченко"
    birth_date = input("Введіть дату народження (дд.мм.рррр): ").strip() or "15.03.2000"
    
    # Тестовий текст
    text = input("\nВведіть текст для шифрування (або Enter для прикладу): ").strip()
    if not text:
        text = "Захист інформації – важлива дисципліна"
    
    print("\n" + "-"*70)
    print(f"Оригінальний текст: {text}")
    print("-"*70)
    
    # ========== ЦЕЗАР ==========
    caesar_key = cipher.generate_caesar_key(birth_date)
    print(f"\nКЛЮЧ ЦЕЗАРЯ: {caesar_key} (сума цифр дати: {birth_date})")
    
    caesar_encrypted = cipher.caesar_encrypt(text, caesar_key)
    print(f"Зашифровано: {caesar_encrypted}")
    
    caesar_decrypted = cipher.caesar_decrypt(caesar_encrypted, caesar_key)
    print(f"Розшифровано: {caesar_decrypted}")
    print(f"Перевірка: {'OK' if caesar_decrypted == text else 'ПОМИЛКА'}")
    
    # ========== ВІЖЕНЕР ==========
    print(f"\nКЛЮЧ ВІЖЕНЕРА: {surname}")
    
    vigenere_encrypted = cipher.vigenere_encrypt(text, surname)
    print(f"Зашифровано: {vigenere_encrypted}")
    
    vigenere_decrypted = cipher.vigenere_decrypt(vigenere_encrypted, surname)
    print(f"Розшифровано: {vigenere_decrypted}")
    print(f"Перевірка: {'OK' if vigenere_decrypted == text else 'ПОМИЛКА'}")
    
    # ========== АНАЛІЗ ==========
    caesar_analysis = cipher.analyze_cipher(text, caesar_encrypted, f"Число {caesar_key}")
    vigenere_analysis = cipher.analyze_cipher(text, vigenere_encrypted, f"Слово ({len(surname)} літер)")
    
    cipher.print_comparison_table(caesar_analysis, vigenere_analysis)
    
    # ========== ВИСНОВКИ ==========
    print("\nВИСНОВКИ ПРО СТІЙКІСТЬ МЕТОДІВ:")
    print("-"*70)
    print("1. ШИФР ЦЕЗАРЯ:")
    print("   • Простий у реалізації та використанні")
    print("   • Низька стійкість (легко зламати перебором - 33 варіанти)")
    print("   • Ключ генерується з дати (може бути передбачуваним)")
    print("   • Зберігає частоту появи символів")
    
    print("\n2. ШИФР ВІЖЕНЕРА:")
    print("   • Складніший у реалізації")
    print("   • Вища стійкість (залежить від довжини ключа)")
    print("   • Ключ на основі прізвища (можна вгадати)")
    print("   • Краще маскує частоти символів")
    
    print("\n3. ЗАГАЛЬНИЙ ВИСНОВОК:")
    print("   Віженер є стійкішим, але обидва шифри вважаються застарілими")
    print("   для сучасного захисту інформації. Для реального використання")
    print("   потрібні сучасні алгоритми (AES, RSA тощо).")
    print("="*70)


if __name__ == "__main__":
    main()
