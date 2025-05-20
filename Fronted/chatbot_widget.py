from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel,
    QLineEdit, QPushButton, QWidget, QScrollArea, QSizePolicy
)
from PyQt5.QtGui import QPixmap, QIcon, QMovie
from PyQt5.QtCore import Qt

from Backend.tools import chatbot_conect

class ChatbotDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Chatbot")
        self.setFixedSize(420, 460)
        self.setStyleSheet("background-color: #f0f0f0;")

        header = QLabel("Talk with Utechi")
        header.setAlignment(Qt.AlignCenter)
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

        self.chat_area = QVBoxLayout()
        self.chat_area.setAlignment(Qt.AlignTop)
        self.chat_area.setSpacing(12)

        chat_container = QWidget()
        chat_container.setLayout(self.chat_area)

        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setWidget(chat_container)
        self.scroll.setStyleSheet("border: none; background-color: #e0e0e0;")

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
        self.send_button.setIcon(QIcon("./Fronted/icon/enviar.png"))
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

        # Indicador de carga (invisible inicialmente)
        self.loading_label = QLabel()
        self.loading_label.setFixedSize(24, 24)
        self.loading_label.setVisible(False)
        # Puedes usar un gif animado de carga o un texto simple
        # Ejemplo con gif animado:
        self.loading_movie = QMovie("./Fronted/icon/loading.gif")  # Pon aquí el gif que tengas
        self.loading_label.setMovie(self.loading_movie)

        input_layout.addWidget(self.loading_label)

        main_layout = QVBoxLayout()
        main_layout.setSpacing(0)
        main_layout.setContentsMargins(0, 0, 0, 6)
        main_layout.addWidget(header)
        main_layout.addWidget(self.scroll)
        main_layout.addLayout(input_layout)
        self.setLayout(main_layout)

    def send_message(self):
        user_text = self.input_box.text().strip()
        if user_text:
            self.add_user_bubble(user_text)
            self.input_box.clear()
            self.send_button.setEnabled(False)

            # Mostrar indicador carga
            self.loading_label.setVisible(True)
            self.loading_movie.start()

            # Aquí ideal usar threading para no bloquear UI
            # Para ejemplo simple, llamamos directo
            response = chatbot_conect(user_text)

            self.add_bot_bubble(response)

            # Ocultar indicador carga
            self.loading_movie.stop()
            self.loading_label.setVisible(False)
            self.send_button.setEnabled(True)

    def add_bot_bubble(self, text):
        bubble_layout = QHBoxLayout()
        bubble_layout.setAlignment(Qt.AlignLeft)

        avatar = QLabel()
        avatar.setFixedSize(30, 30)
        avatar.setPixmap(QPixmap("./Fronted/icon/utechi.png"))
        avatar.setScaledContents(True)
        avatar.setStyleSheet("""
            QLabel {
                border-radius: 15px;
                border: 2px solid transparent;
                background-color: white;
            }
        """)

        name = QLabel("Bot")
        name.setStyleSheet("font-size: 10px; color: gray;")

        left_column = QVBoxLayout()
        left_column.setAlignment(Qt.AlignTop)
        left_column.addWidget(avatar)
        left_column.addWidget(name)

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
                max-width: 350px;
                min-width: 150px;
            }
        """)

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(bubble)
        scroll_area.setMaximumWidth(380)
        scroll_area.setMaximumHeight(200)

        bubble_layout.addLayout(left_column)
        bubble_layout.addWidget(scroll_area)

        wrapper = QWidget()
        wrapper.setLayout(bubble_layout)
        wrapper.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.chat_area.addWidget(wrapper)

        self.scroll.verticalScrollBar().setValue(self.scroll.verticalScrollBar().maximum())

    def add_user_bubble(self, text):
        bubble_layout = QVBoxLayout()
        bubble_layout.setAlignment(Qt.AlignRight)
        bubble_layout.setContentsMargins(0, 0, 0, 0)
        bubble_layout.setSpacing(4)

        bubble = QLabel(text)
        bubble.setWordWrap(True)
        bubble.setStyleSheet("""
            QLabel {
                background-color: #1976d2;
                color: white;
                border-radius: 15px;
                padding: 12px 18px;
                font-size: 13px;
                max-width: 450px;   # más ancho
                min-width: 180px;
                margin-left: 60px;
            }
        """)
        bubble.adjustSize()
        bubble.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)

        # Opcional: encapsular en scroll para evitar corte
        # scroll_area = QScrollArea()
        # scroll_area.setWidgetResizable(True)
        # scroll_area.setWidget(bubble)
        # scroll_area.setMaximumWidth(460)
        # scroll_area.setMaximumHeight(150)
        # bubble_layout.addWidget(scroll_area)

        # Si no usas scroll, agregar directamente:
        bubble_layout.addWidget(bubble)

        footer = QLabel("✓ Message read")
        footer.setStyleSheet("""
            font-size: 10px;
            color: gray;
            margin-right: 60px;
        """)
        footer.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)
        footer.setMaximumWidth(150)
        footer.adjustSize()

        bubble_layout.addWidget(footer, alignment=Qt.AlignRight)

        wrapper = QWidget()
        wrapper.setLayout(bubble_layout)
        wrapper.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.chat_area.addWidget(wrapper)

        self.scroll.verticalScrollBar().setValue(self.scroll.verticalScrollBar().maximum())
