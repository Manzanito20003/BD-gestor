import logging
import time

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QDragEnterEvent, QDropEvent
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QTextEdit, QPushButton, QLabel, QFileDialog, QMessageBox
from .HttpClient import HttpClient
class QuerySQLView(QWidget):
    def __init__(self, parent=None):
        super().__init__()
        self.parent = parent

        self.query_input = None
        self.result_output = None
        self.execute_button = None
        self.initUI()

        self.http=HttpClient()



    def initUI(self):
        # Cuadro de texto para escribir la consulta SQL
        self.query_input = QTextEdit()
        self.query_input.setPlaceholderText("SELECT * FROM LIFE ...")

        # Botones
        self.execute_button = QPushButton("Ejecutar")
        self.execute_button.clicked.connect(self.action_execute_button)


        # Layout de botones (vertical)
        layout_botones = QVBoxLayout()
        layout_botones.addWidget(self.execute_button)


        botones_widget = QWidget()
        botones_widget.setLayout(layout_botones)

        # Drop area
        self.drop_area = DropArea()
        layout_right = QVBoxLayout()
        layout_right.addWidget(self.drop_area)
        layout_right.addWidget(botones_widget)

        layout_right_widget = QWidget()
        layout_right_widget.setLayout(layout_right)

        # Layout horizontal principal
        layout_principal = QHBoxLayout()
        layout_principal.addWidget(self.query_input)
        layout_principal.addWidget(layout_right_widget)

        layout_principal.setStretch(0, 3) # recibe el index,factor 3+1 =4 partes el horinzontal
        layout_principal.setStretch(1, 1) # 75%  index 0    y 25% index 1

        self.setLayout(layout_principal)
        self.setStyleSheet("""
            QWidget {
            }
        """)

    def action_execute_button(self):
        try:
            # Obtener la consulta desde el input
            sql_text = self.query_input.toPlainText().strip()
            if not sql_text:
                QMessageBox.warning(self, "Consulta vacía", "Ingrese una consulta SQL antes de ejecutar.")
                logging.warning("Se intentó ejecutar una consulta vacía.")
                return

            logging.info(f"Consulta enviada: {sql_text}")
            start_time = time.time()

            # Ejecutar consulta
            result_output = self.http.make_post_request(sql_text)

            if result_output["status"]!=200:
                QMessageBox.warning(self, "Error",
                                    "Al ejecutar la consulta. Probelmas en el servidor.")
                logging.error(f"La consulta fallo: {result_output['error']}. code:{result_output['status']}")
                return

            # Medir tiempo de ejecución
            elapsed_ms = (time.time() - start_time) * 1000
            logging.info(f"Consulta ejecutada en {elapsed_ms:.2f} ms")

            # Mostrar resultado en tabla
            self.parent.ShowTableView.load_data(result_output, elapsed_ms)

        except Exception as e:
            logging.exception("Excepción durante la ejecución de consulta SQL:")
            QMessageBox.critical(self, "Error", f"Error al ejecutar la consulta:\n{str(e)}")


class DropArea(QWidget):
    def __init__(self):
        super().__init__()
        self.setAcceptDrops(True) # habilitar el drag and drop

        #limitaremos el tamaño
        self.setFixedSize(200,200)

        self.container = QWidget()
        # Estilo visual
        self.container.setStyleSheet("""
                    QLabel {
                        border: 2px dashed gray;
                        padding: 40px;
                        font-size: 14px;
                    }
                   
                """)
        # Texto
        self.label = QLabel("Arrastra un \n archivo .txt")
        self.label.setAlignment(Qt.AlignCenter)# centrar el label

        # Botón para carga manual
        self.button = QPushButton("Cargar")
        self.button.clicked.connect(self.cargar_manual)

        # Layout vertical
        layout = QVBoxLayout() # creamos el layout
        layout.addWidget(self.label) # add los widget , label and button
        layout.addWidget(self.button)
        self.container.setLayout(layout)   # asignar el layout al diseño actual la class principal


        # layout principal
        layout=QVBoxLayout()
        layout.addWidget(self.container)
        self.setLayout(layout)

    def dragEnterEvent(self, event: QDragEnterEvent):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event: QDropEvent):
        urls = event.mimeData().urls()
        if urls:
            filepath = urls[0].toLocalFile()
            self.label.setText(f"Archivo recibido:\n{filepath}")
            print("Archivo recibido:", filepath)
            # Aquí podrías almacenar el filepath para usarlo luego



    def cargar_manual(self):
        filepath, _ = QFileDialog.getOpenFileName(self, "Seleccionar archivo")
        if filepath:
            file = filepath.split("/")[-1]

            if file.split(".")[-1] != "txt":
                QMessageBox.warning(self, "Error", "El archivo debe ser un .txt")
                return

            self.label.setText(f"Archivo cargado manualmente:\n{file}")
            print("Archivo cargado manualmente:", filepath)

    def load_sql_from_file(self, path):


        pass
