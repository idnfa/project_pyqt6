from PyQt6 import QtWidgets
from PyQt6.QtWidgets import QTableWidget, QPushButton, QLabel, QVBoxLayout


def init_mainer_form_ui(self):
    self.setWindowTitle('Владельцы')
    self.tableWidget = QTableWidget(self)

    self.tableWidget.setColumnCount(2)
    self.tableWidget.setHorizontalHeaderLabels(['ИД', 'Имя'])
    self.tableWidget.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.Stretch)

    self.addButton = QPushButton('добавить', self)
    self.addButton.clicked.connect(self.adding)

    self.statuslabel = QLabel()

    layout = QVBoxLayout()
    layout.addWidget(self.addButton)
    layout.addWidget(self.tableWidget)
    layout.addWidget(self.statuslabel)

    self.setLayout(layout)
    self.load_data()
