from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QLabel, QHBoxLayout



def test_data():
    #aqui crearemos data de prueba
    # TEST DATA
    # columnas e índices para las tablas

    # Diccionario de tablas dentro del esquema "ventas"
    name_table = "productos"
    rows = 10
    index = 3
    Tabla = {
        "name_table": name_table,
        "rows": rows,
        "index": index,
        "columns": ["id", "name", "precio", "estado","Null1","Null2"],

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
        ]}



    return Tabla


class ShowTableView(QWidget):
    def __init__(self,parent=None):
        super().__init__()
        self.parent = parent

        self.data_tabla = []
        self.data_index = []

        self.active_tab = None
        self.table_name = None
        self.table_rows = None
        self.table_index = None

        self.initUI()

    def initUI(self):
        # Crear tabla
        layout_info= QHBoxLayout()
        self.table_name= QLabel("Nombre de la tabla:")
        self.table_rows= QLabel("# rows:")
        self.table_index= QLabel("# index:")
        layout_info.addWidget(self.table_name)
        layout_info.addWidget(self.table_rows)
        layout_info.addWidget(self.table_index)


        self.table = QTableWidget()
        self.table.setColumnCount(3)  # Puedes ajustarlo luego
        self.table.setHorizontalHeaderLabels(['Col 1', 'Col 2', 'Col 3'])

        # Layout
        layout = QVBoxLayout()
        layout.addLayout(layout_info)
        layout.addWidget(self.table)
        self.setLayout(layout)

        #teste load_Data
        data = test_data()
        self.load_data(data)

    def load_data(self, data):
        print("load_data", data )
        # Limpiar la tabla antes de cargar nuevos datos
        self.table.clear()
        self.table.setRowCount(0)
        self.table.setColumnCount(0)

        # Configurar columnas
        self.table.setColumnCount(len(data["columns"]))
        self.table.setHorizontalHeaderLabels(data["columns"])

        # Cargar filas
        for row_index, row_data in enumerate(data["data"]):
            self.table.insertRow(row_index)
            for col_index, value in enumerate(row_data):
                item = QTableWidgetItem(str(value))
                self.table.setItem(row_index, col_index, item)

        # Extraer y mostrar información adicional
        info = data

        self.table_name.setText("Table: "+info.get("name_table", ""))
        self.table_rows.setText("#Rows: "+str(info.get("rows", len(data["data"]))))
        self.table_index.setText("#Index: "+str(info.get("index", 0)))

