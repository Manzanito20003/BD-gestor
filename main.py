from PyQt5.QtWidgets import QApplication, QWidget, QSplitter, QVBoxLayout
from PyQt5.QtCore import Qt
import sys

from Fronted.TabLeftView import TabLeftView
from Fronted.ShowTableView import ShowTableView
from Fronted.QuerySQLView import QuerySQLView
from Fronted.HttpClient import HttpClient

from PyQt5.QtWidgets import QPushButton, QDialog

from Fronted.chatbot_widget import ChatbotDialog


def my_test():

    # SIMULA EXTRACCION DE DATOS
    # TEST DATA

    # columnas e índices para las tablas
    columnas = ["id", "fecha", "cliente", "total"]
    index = ["id_B++", "total_BRIN"]

    # Diccionario de tablas dentro del esquema "ventas"
    Tablas = {
        "facturas": {"columnas": columnas, "index": index},
        "productos": {"columnas": columnas, "index": index}
    }

    # Diccionario de esquemas
    Schemas = {
        "ventas": Tablas,
        "admin": {
            "usuarios": {"columnas": columnas, "index": index},
            "roles": {"columnas": columnas, "index": index},
            "permisos": {"columnas": columnas, "index": index}
        }
    }
    print("Test schema:",Schemas)
    return Schemas

class Ventana(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("División con QSplitter")
        self.resize(1000, 600)


        # Crear el cliente HTTP
        self.http_client = HttpClient()

        self.table_selected = None
        self.schema_selected = None
        #----------
        self.QuerySQLView=QuerySQLView(self,)
        self.ShowTableView=ShowTableView(self,)
        self.initUI()
    def initUI(self):
        # Panel izquierdo
        #TEST DATA
        schemas = my_test()
        #schemas= self.http_client.make_get_request("http://127.0.0.1:8000/show_schema_info")
        panel_izquierdo = TabLeftView(schemas)

        # Panel derecho con dos vistas una debajo de otra
        panel_derecho = QWidget()
        layout_derecho = QVBoxLayout()
        layout_derecho.setContentsMargins(0, 0, 0, 0)  # Opcional para ajustarse al borde

        layout_derecho.addWidget(self.QuerySQLView)
        layout_derecho.addWidget(self.ShowTableView)



        panel_derecho.setLayout(layout_derecho)

        # Splitter
        splitter = QSplitter(Qt.Orientation.Horizontal)
        splitter.addWidget(panel_izquierdo)
        splitter.addWidget(panel_derecho)
        splitter.setSizes([200, 600])  # Ancho inicial de cada panel



        # Layout principal
        layout = QVBoxLayout()
        layout.addWidget(splitter)
        self.setLayout(layout)


        # === Botón flotante ===
        self.chat_button = QPushButton("💬", self)
        self.chat_button.setFixedSize(50, 50)
        self.chat_button.setStyleSheet("""
                    QPushButton {
                        border-radius: 25px;
                        background-color: #0078D7;
                        color: white;
                        font-size: 20px;
                    }
                """)
        self.chat_button.clicked.connect(self.abrir_chat)
        self.chat_button.raise_()  # Asegura que esté por encima

    def abrir_chat(self,):
        dialog = ChatbotDialog(self)
        dialog.exec_()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        # Reposiciona el botón en cada cambio de tamaño
        self.chat_button.move(self.width() - 70, self.height() - 70)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = Ventana()
    ventana.show()
    sys.exit(app.exec_())
