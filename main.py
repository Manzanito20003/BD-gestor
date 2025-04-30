from PyQt5.QtWidgets import QApplication, QWidget, QSplitter, QVBoxLayout
from PyQt5.QtCore import Qt
import sys

from TabLeftView import TabLeftView
from ShowTableView import ShowTableView
from QuerySQLView import QuerySQLView

def test_data():
    #SIMULA EXTRACCION DE DATOS
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
        self.resize(800, 400)
        self.initUI()

    def initUI(self):
        # Panel izquierdo
        #TEST DATA
        schemas = test_data()

        panel_izquierdo = TabLeftView(schemas)

        # Panel derecho con dos vistas una debajo de otra
        panel_derecho = QWidget()
        layout_derecho = QVBoxLayout()
        layout_derecho.setContentsMargins(0, 0, 0, 0)  # Opcional para ajustarse al borde

        layout_derecho.addWidget(QuerySQLView())
        layout_derecho.addWidget(ShowTableView())

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

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = Ventana()
    ventana.show()
    sys.exit(app.exec_())
