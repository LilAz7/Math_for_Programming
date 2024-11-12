import random
import sys
from sympy import mod_inverse, isprime
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
from PyQt5.QtGui import QFont  # Импортируем QFont

# Функция для генерации простого числа заданного размера (в битах)
def generate_prime(bits):
    while True:
        prime_candidate = random.getrandbits(bits)
        if isprime(prime_candidate):
            return prime_candidate

# Генерация ключей для RSA
def generate_rsa_keys(bits=128):
    p = generate_prime(bits)
    q = generate_prime(bits)
    n = p * q
    phi_n = (p - 1) * (q - 1)
    e = 65537
    if phi_n % e == 0:
        e = 3
    d = mod_inverse(e, phi_n)
    return (e, n), (d, n)

# Шифрование
def rsa_encrypt(message, public_key):
    e, n = public_key
    message_int = int.from_bytes(message.encode('utf-8'), byteorder='big')
    cipher_int = pow(message_int, e, n)
    return cipher_int

# Дешифрование
def rsa_decrypt(cipher_int, private_key):
    d, n = private_key
    message_int = pow(cipher_int, d, n)
    message_bytes = message_int.to_bytes((message_int.bit_length() + 7) // 8, byteorder='big')
    return message_bytes.decode('utf-8')

# Главный класс приложения
class RSACipherApp(QWidget):
    def __init__(self):
        super().__init__()

        # Генерация ключей RSA
        self.public_key, self.private_key = generate_rsa_keys()

        # Инициализация интерфейса
        self.init_ui()

    def init_ui(self):
        # Основной layout
        main_layout = QVBoxLayout()

        # Поля для ввода и вывода
        font_size = 14

        # Создание объекта QFont
        font = QFont("Arial", font_size)

        # Ввод сообщения для шифрования
        self.message_label = QLabel("Введите сообщение для шифрования:")
        self.message_label.setFont(font)  # Устанавливаем шрифт
        self.entry_message = QLineEdit()
        self.entry_message.setFont(font)  # Устанавливаем шрифт
        main_layout.addWidget(self.message_label)
        main_layout.addWidget(self.entry_message)

        # Зашифрованное сообщение
        self.cipher_label = QLabel("Зашифрованное сообщение:")
        self.cipher_label.setFont(font)  # Устанавливаем шрифт
        self.entry_cipher = QLineEdit()
        self.entry_cipher.setFont(font)  # Устанавливаем шрифт
        self.entry_cipher.setReadOnly(True)
        main_layout.addWidget(self.cipher_label)
        main_layout.addWidget(self.entry_cipher)

        # Расшифрованное сообщение
        self.decrypted_label = QLabel("Расшифрованное сообщение:")
        self.decrypted_label.setFont(font)  # Устанавливаем шрифт
        self.entry_decrypted = QLineEdit()
        self.entry_decrypted.setFont(font)  # Устанавливаем шрифт
        self.entry_decrypted.setReadOnly(True)
        main_layout.addWidget(self.decrypted_label)
        main_layout.addWidget(self.entry_decrypted)

        # Кнопки для шифрования и дешифрования
        button_layout = QHBoxLayout()

        self.btn_encrypt = QPushButton("Зашифровать")
        self.btn_encrypt.setFont(font)  # Устанавливаем шрифт
        self.btn_encrypt.clicked.connect(self.encrypt_message)
        button_layout.addWidget(self.btn_encrypt)

        self.btn_decrypt = QPushButton("Расшифровать")
        self.btn_decrypt.setFont(font)  # Устанавливаем шрифт
        self.btn_decrypt.clicked.connect(self.decrypt_message)
        button_layout.addWidget(self.btn_decrypt)

        main_layout.addLayout(button_layout)

        # Устанавливаем главный layout
        self.setLayout(main_layout)

        # Настройки окна
        self.setWindowTitle("RSA Шифратор/Дешифратор")
        self.setGeometry(100, 100, 600, 300)

    def encrypt_message(self):
        message = self.entry_message.text()
        if not message:
            QMessageBox.warning(self, "Ошибка", "Введите сообщение!")
            return
        cipher_text = rsa_encrypt(message, self.public_key)
        self.entry_cipher.setText(str(cipher_text))

    def decrypt_message(self):
        cipher_text = self.entry_cipher.text()
        if not cipher_text:
            QMessageBox.warning(self, "Ошибка", "Введите зашифрованное сообщение!")
            return
        try:
            decrypted_message = rsa_decrypt(int(cipher_text), self.private_key)
            self.entry_decrypted.setText(decrypted_message)
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", "Невозможно расшифровать сообщение!")

# Запуск приложения
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = RSACipherApp()
    window.show()
    sys.exit(app.exec_())
