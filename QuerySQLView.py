from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QTextEdit, QPushButton, QLabel


class QuerySQLView(QWidget):
    def __init__(self):
        super().__init__()
        self.query_input = None
        self.result_output = None
        self.execute_button = None
        self.initUI()

    def initUI(self):
        # Cuadro de texto para escribir la consulta SQL
        self.query_input = QTextEdit()
        self.query_input.setPlaceholderText("SELECT * FROM LIFE ...")

        # Botones
        self.execute_button = QPushButton("Ejecutar")
        self.execute_button.clicked.connect(self.action_execute_button)

        self.open_file = QPushButton("Cambiar archivo")

        # Layout de botones (vertical)
        layout_botones = QVBoxLayout()
        layout_botones.addWidget(self.execute_button)
        layout_botones.addWidget(self.open_file)

        # Layout horizontal principal
        layout_principal = QHBoxLayout()
        layout_principal.addWidget(self.query_input)

        # Para agregar un layout dentro de otro, necesitamos usar un widget contenedor
        botones_widget = QWidget()
        botones_widget.setLayout(layout_botones)

        layout_principal.addWidget(botones_widget)

        self.setLayout(layout_principal)

    def action_execute_button(self):
        print("Ejecutar consulta SQL")
