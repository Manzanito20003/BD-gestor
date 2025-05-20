from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QLabel,
    QHBoxLayout, QPushButton, QSpacerItem, QSizePolicy
)

def test_data():
    name_table = "productos"
    rows = 10
    index = 3
    Tabla = {
        "name_table": name_table,
        "rows": rows,
        "index": index,
        "columns": ["id", "name", "precio", "estado"],
        "data": [
            [0, "ARÁNDANOS", 10.0, "activo"],
            [1, "MANZANA", 5.5, "inactivo"],
            [2, "PLÁTANO", 3.0, "activo"],
            [3, "NARANJA", 4.2, "activo"],
            [4, "KIWI", 8.0, "inactivo"],
            [5, "FRESA", 12.5, "activo"],
            [6, "MANGO", 7.8, "activo"],
            [7, "UVA", 6.3, "activo"],
            [8, "PIÑA", 9.4, "inactivo"],
            [9, "PAPAYA", 11.0, "activo"]
        ]
    }
    return Tabla


class ShowTableView(QWidget):
    def __init__(self, parent=None):
        super().__init__()
        self.parent = parent

        self.data_tabla = None  # Datos totales (diccionario con data)
        self.current_page = 0   # Página actual
        self.page_size = 20      # Tamaño de página (ejemplo: 3 registros por página)

        # Widgets de info
        self.table_name = QLabel("Table:")
        self.table_rows = QLabel("Rows:")
        self.table_time = QLabel("Time(ms):")
        self.page_info = QLabel("Página 0 de 0")

        # Tabla para mostrar datos
        self.table = QTableWidget()

        # Botones para paginación
        self.prev_button = QPushButton("Anterior")
        self.next_button = QPushButton("Siguiente")

        self.initUI()

    def initUI(self):
        layout_info = QHBoxLayout()
        layout_info.addWidget(self.table_name)
        layout_info.addWidget(self.table_rows)
        layout_info.addWidget(self.table_time)
        layout_info.addStretch()
        layout_info.addWidget(self.page_info)

        # Layout para botones
        layout_buttons = QHBoxLayout()
        layout_buttons.addWidget(self.prev_button)
        layout_buttons.addWidget(self.next_button)

        # Layout principal vertical
        layout = QVBoxLayout()
        layout.addLayout(layout_info)
        layout.addWidget(self.table)
        layout.addLayout(layout_buttons)
        self.setLayout(layout)

        # Conectar botones
        self.prev_button.clicked.connect(self.previous_page)
        self.next_button.clicked.connect(self.next_page)

        # Cargar datos de prueba
        data = test_data()
        self.load_data(data)

    def load_data(self, data, time_execution=None):
        self.data_tabla = data
        self.current_page = 0

        self.table_name.setText("Table: " + data.get("name_table", ""))
        self.table_rows.setText("Rows: " + str(data.get("rows", len(data["data"]))))
        self.table_time.setText("Time(ms): " + str(time_execution if time_execution is not None else "N/A"))

        self.display_page()

    def display_page(self):
        self.table.clear()
        self.table.setRowCount(0)
        self.table.setColumnCount(0)

        # Configurar columnas
        columns = self.data_tabla["columns"]
        self.table.setColumnCount(len(columns))
        self.table.setHorizontalHeaderLabels(columns)

        # Calcular rango de filas a mostrar
        start = self.current_page * self.page_size
        end = start + self.page_size
        page_data = self.data_tabla["data"][start:end]

        # Cargar filas actuales
        for row_index, row_data in enumerate(page_data):
            self.table.insertRow(row_index)
            for col_index, value in enumerate(row_data):
                item = QTableWidgetItem(str(value))
                self.table.setItem(row_index, col_index, item)

        # Actualizar etiqueta de página
        total_pages = self.total_pages()
        self.page_info.setText(f"Página {self.current_page + 1} de {total_pages}")

        # Habilitar/deshabilitar botones según página
        self.prev_button.setEnabled(self.current_page > 0)
        self.next_button.setEnabled(self.current_page < total_pages - 1)

    def total_pages(self):
        total_records = len(self.data_tabla["data"])
        return max(1, (total_records + self.page_size - 1) // self.page_size)

    def next_page(self):
        if (self.current_page + 1) < self.total_pages():
            self.current_page += 1
            self.display_page()

    def previous_page(self):
        if self.current_page > 0:
            self.current_page -= 1
            self.display_page()
