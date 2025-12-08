from PIL import Image
import numpy as np
import os


class Steganography:
    def __init__(self, bits=2):
        self.BITS = bits                
        self.END = "<<<END>>>"           # Маркер завершення (ASCII)
        self.DEFAULT_IMAGE = "original.jpg"

        if not os.path.exists(self.DEFAULT_IMAGE):
            self._create_default_image()

    # ================================================================
    #  ДОПОМОЖНІ МЕТОДИ
    # ================================================================

    def _create_default_image(self):
        """Створює дефолтне зображення 400×300 з легким шумом."""
        img = Image.new("RGB", (400, 300), (120, 180, 200))
        arr = np.array(img)

        noise = np.random.randint(-20, 20, arr.shape)
        arr = np.clip(arr + noise, 0, 255).astype(np.uint8)

        Image.fromarray(arr).save(self.DEFAULT_IMAGE)
        print(f"[INFO] Автоматично створено {self.DEFAULT_IMAGE}")

    def text_to_bits(self, text):
        """
        Перетворює текст у рядок бітів.
        1) Кодуємо текст у UTF-8 байти.
        2) Кожен байт перетворюємо у 8-бітове двійкове представлення.
        """
        data = text.encode("utf-8")
        return ''.join(f"{b:08b}" for b in data)

    def bits_to_text(self, bits):
        """
        Перетворює бітовий рядок у текст, інтерпретуючи його як UTF-8.
        Цей метод зараз не використовується напряму, але залишений для зручності.
        """
        data = bytearray()
        for i in range(0, len(bits), 8):
            byte = bits[i:i + 8]
            if len(byte) < 8:
                break
            data.append(int(byte, 2))
        return data.decode("utf-8", errors="ignore")

    def xor(self, text, password):
        """Просте XOR-шифрування/розшифрування рядка з паролем."""
        if not password:
            return text
        return ''.join(
            chr(ord(text[i]) ^ ord(password[i % len(password)]))
            for i in range(len(text))
        )

    # ================================================================
    #  ПРИХОВУВАННЯ
    # ================================================================

    def hide(self, message, password="", input_img=None, output_img="hidden.png"):
        if input_img is None:
            input_img = self.DEFAULT_IMAGE

        print("\n[1] Завантаження зображення...")
        img = Image.open(input_img).convert("RGB")
        arr = np.array(img).reshape(-1)
        print(f"    Файл: {input_img}")

        print("[2] Підготовка повідомлення...")
        # Шифруємо вихідний текст (у вигляді Python-рядка/Unicode)
        encrypted = self.xor(message, password)
        # Додаємо ASCII-маркер завершення
        full_text = encrypted + self.END
        # Кодуємо як UTF-8 - байти - біти
        bits = self.text_to_bits(full_text)
        print(f"    Символів у вихідному повідомленні: {len(message)}")
        print(f"    Бітів для запису (з шифруванням і END): {len(bits)}")

        capacity = len(arr) * self.BITS
        print(f"[3] Місткість зображення: {capacity} біт")
        if len(bits) > capacity:
            raise ValueError("Повідомлення занадто велике для цього зображення!")

        print("[4] Запис LSB...")
        mask = 0xFF & ~((1 << self.BITS) - 1)
        bit_i = 0

        for i in range(len(arr)):
            if bit_i >= len(bits):
                break

            # Беремо наступні BITS бітів
            end_i = min(bit_i + self.BITS, len(bits))
            chunk = bits[bit_i:end_i]

            # Дозаповнюємо нулями, якщо chunk коротший
            if len(chunk) < self.BITS:
                chunk += "0" * (self.BITS - len(chunk))

            arr[i] = (arr[i] & mask) | int(chunk, 2)
            bit_i += self.BITS

        # Повертаємо форму та зберігаємо
        arr = arr.reshape(img.size[1], img.size[0], 3).astype(np.uint8)
        Image.fromarray(arr).save(output_img, "PNG")

        print(f"[5] Готово! Створено файл: {output_img}")

    # ================================================================
    #  ВИТЯГУВАННЯ
    # ================================================================

    def extract(self, input_img="hidden.png", password=""):
        print("\n[1] Зчитування зображення...")
        img = Image.open(input_img).convert("RGB")
        arr = np.array(img).reshape(-1)
        print(f"    Файл: {input_img}")

        print("[2] Витягування бітів...")
        mask = (1 << self.BITS) - 1
        bitstream = ""
        data_bytes = bytearray()
        end_bytes = self.END.encode("utf-8")   # Маркер у вигляді байтів

        for px in arr:
            # Витягуємо BITS молодших бітів і додаємо у бітовий потік
            bitstream += f"{px & mask:0{self.BITS}b}"

            # З бітового потоку формуємо байти (8 біт)
            while len(bitstream) >= 8:
                byte = bitstream[:8]
                bitstream = bitstream[8:]
                data_bytes.append(int(byte, 2))

                # Перевіряємо, чи є вже послідовність END у байтах
                if end_bytes in data_bytes:
                    all_data = bytes(data_bytes)

                    # Усе, що ДО END — це зашифрований текст
                    encrypted_bytes = all_data.split(end_bytes)[0]

                    # Повертаємо зашифрований текст, який був після XOR
                    encrypted_text = encrypted_bytes.decode("utf-8", errors="strict")

                    # Розшифровуємо, якщо задано пароль
                    if password:
                        decoded = self.xor(encrypted_text, password)
                    else:
                        decoded = encrypted_text

                    print("[3] Повідомлення успішно витягнуто!")
                    return decoded

        print("[!] Маркер END не знайдено — повідомлення пошкоджене або неправильний пароль.")
        return ""


# ================================================================
#  ПРИКЛАД ВИКОРИСТАННЯ
# ================================================================
if __name__ == "__main__":
    steg = Steganography(bits=2)

    message = "Це приховане повідомлення від Пащенко Марини."
    steg.hide(message=message, password="1234")

    extracted = steg.extract("hidden.png", password="1234")

    print("\n>>> Витягнуте повідомлення:")
    print(extracted)
