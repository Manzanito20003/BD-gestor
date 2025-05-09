from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel,
    QLineEdit, QPushButton, QWidget, QScrollArea, QSizePolicy
)
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtCore import Qt

from Backend.tools import chatbot_conect

class ChatbotDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Chatbot")
        self.setFixedSize(420, 460)
        self.setStyleSheet("background-color: #f0f0f0; border-radius: px;")

        # === Encabezado azul con texto ===
        header = QLabel("Talk with Utechi")
        header.setAlignment(Qt.AlignCenter) # aliniar
        header.setStyleSheet("""
            QLabel {
                background-color: #1976d2;
                color: white;
                font-size: 16px;
                font-weight: bold;
                padding: 10px;
                border-top-left-radius: 10px;
                border-top-right-radius: 10px;
            }
        """)

        # === Área de chat con scroll ===
        self.chat_area = QVBoxLayout()
        self.chat_area.setAlignment(Qt.AlignTop) # apila los mensajes desde arriba hacia abajo
        self.chat_area.setSpacing(12) # espacio vertical entre mensaje

        chat_container = QWidget()
        chat_container.setLayout(self.chat_area) # asignamos el layout de mensajes al contenedor visual

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setWidget(chat_container)
        scroll.setStyleSheet("border: none; background-color: #e0e0e0;")

        # === Entrada + botón (estilo moderno) ===
        self.input_box = QLineEdit()
        self.input_box.setPlaceholderText("Compose your message...")
        self.input_box.setStyleSheet("""
            QLineEdit {
                border: 1px solid #ccc;
                border-radius: 18px;
                padding: 8px 14px;
                background-color: white;
                font-size: 13px;
            }
        """)

        self.send_button = QPushButton()
        self.send_button.setFixedSize(36, 36)
        self.send_button.setIcon(QIcon("./Fronted/icon/enviar.png"))  # el lugar de donde se pone es de donde se ejecuta el main

        self.send_button.setStyleSheet("""
            QPushButton {
                background-color: #1976d2;
                border-radius: 18px;
            }
        """)
        self.send_button.clicked.connect(self.send_message)

        input_layout = QHBoxLayout()
        input_layout.addWidget(self.input_box)
        input_layout.addWidget(self.send_button)

        # === Layout principal ===
        main_layout = QVBoxLayout()
        main_layout.setSpacing(0)
        main_layout.setContentsMargins(0, 0, 0, 6)
        main_layout.addWidget(header)
        main_layout.addWidget(scroll)
        main_layout.addLayout(input_layout)
        self.setLayout(main_layout)

    def send_message(self):
        user_text = self.input_box.text().strip()
        if user_text:
            response=chatbot_conect(user_text)

            self.add_user_bubble(user_text)

            self.add_bot_bubble(response)
            self.input_box.clear()

    def add_bot_bubble(self, text):
        bubble_layout = QHBoxLayout()
        bubble_layout.setAlignment(Qt.AlignLeft)

        # Avatar y nombre
        avatar = QLabel()

        avatar.setFixedSize(30, 30)
        avatar.setPixmap(QPixmap("./Fronted/icon/utechi.png"))
        avatar.setScaledContents(True)
        avatar.setStyleSheet("""
            QLabel {
                border-radius: 15px;         /* mitad del tamaño → círculo */
                border: 2px solid transparent;
                background-color: white;
            }
        """)

        avatar.setScaledContents(True)

        name = QLabel("Bot")
        name.setStyleSheet("font-size: 10px; color: gray;")

        left_column = QVBoxLayout()
        left_column.setAlignment(Qt.AlignTop)
        left_column.addWidget(avatar)
        left_column.addWidget(name)

        # Burbuja
        bubble = QLabel(text)
        bubble.setTextFormat(Qt.RichText)

        bubble.setWordWrap(True)
        bubble.setStyleSheet("""
            QLabel {
                background-color: #eeeeee;
                color: black;
                border-radius: 12px;
                padding: 10px 14px;
                font-size: 13px;
                max-width: 200px;
            }
        """)

        bubble_layout.addLayout(left_column)
        bubble_layout.addWidget(bubble)

        wrapper = QWidget()
        wrapper.setLayout(bubble_layout)
        self.chat_area.addWidget(wrapper)

    def add_user_bubble(self, text):
        bubble_layout = QVBoxLayout()
        bubble_layout.setAlignment(Qt.AlignRight)

        # Burbuja del usuario
        bubble = QLabel(text)
        bubble.setWordWrap(True)
        bubble.setStyleSheet("""
            QLabel {
                background-color: #1976d2;
                color: white;
                border-radius: 12px;
                padding: 10px 14px;
                font-size: 13px;
                max-width: 200px;
            }
        """)
        bubble.adjustSize()


        # Simula "✔ Message read"
        footer = QLabel("✓ Message read")
        footer.setStyleSheet("font-size: 10px; color: gray;")

        bubble_layout.addWidget(bubble)
        bubble_layout.addWidget(footer, alignment=Qt.AlignRight)

        wrapper = QWidget()
        wrapper.setLayout(bubble_layout)
        self.chat_area.addWidget(wrapper)
