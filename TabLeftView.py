from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QListWidget, QScrollArea, QTreeWidget, QTreeWidgetItem


# Clase que representa las tablas dentro de un esquema
class TableView(QWidget):
    def __init__(self, table_names):
        super().__init__()
        self.table_names = table_names
        self.initUI()

    def initUI(self):
        self.list_widget = QListWidget()
        self.list_widget.addItems(self.table_names)

        layout = QVBoxLayout()
        layout.addWidget(self.list_widget)
        self.setLayout(layout)

    def on_table_selected(self, callback):
        self.list_widget.itemClicked.connect(lambda item: callback(item.text()))


# Clase que representa un esquema individual con su lista de tablas
class SchemaView(QWidget):
    def __init__(self, schema_name, table_names):
        super().__init__()
        self.schema_name = schema_name
        self.table_names = table_names
        self.initUI()

    def initUI(self):
        label = QLabel(f"Esquema: {self.schema_name}")
        self.table_view = TableView(self.table_names)

        layout = QVBoxLayout()
        layout.addWidget(label)
        layout.addWidget(self.table_view)
        self.setLayout(layout)

    def set_table_click_callback(self, callback):
        self.table_view.on_table_selected(callback)


# Clase contenedora que muestra todos los esquemas
class TabLeftView(QWidget):
    def __init__(self, schemas_data):
        super().__init__()
        self.schemas_data = schemas_data
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        self.tree = QTreeWidget()
        self.tree.setHeaderHidden(True)  # Oculta encabezado

        # Llenar el árbol con esquemas, tablas, columnas e índices
        for schema_name, tables in self.schemas_data.items():
            schema_item = QTreeWidgetItem([schema_name])

            for table_name, table_info in tables.items():
                table_item = QTreeWidgetItem([table_name])
                schema_item.addChild(table_item)

                # Columnas
                columnas_item = QTreeWidgetItem(["Columnas"])
                for column_name in table_info.get("columnas", []):
                    columnas_item.addChild(QTreeWidgetItem([column_name]))
                table_item.addChild(columnas_item)

                # Índices
                index_item = QTreeWidgetItem(["Índices"])
                for index_name in table_info.get("index", []):
                    index_item.addChild(QTreeWidgetItem([index_name]))
                table_item.addChild(index_item)

            self.tree.addTopLevelItem(schema_item)

            schema_item.setExpanded(False)  # Que esté colapsado por defecto
            self.tree.addTopLevelItem(schema_item)

        self.tree.itemClicked.connect(self.on_item_clicked)

        layout.addWidget(self.tree)
        self.setLayout(layout)

    def on_item_clicked(self, item, column):
        if item.parent():  # Si tiene padre, es una tabla (no un esquema)
            table_name = item.text(0)
            schema_name = item.parent().text(0).replace("Esquema: ", "")
            print(f"Tabla seleccionada: {schema_name}.{table_name}")
            # Aquí puedes emitir señal o llamar método para actualizar la vista derecha

