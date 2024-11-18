from PyQt6 import QtWidgets
from PyQt6.QtWidgets import (QTableWidget,
                             QPushButton, QVBoxLayout, QWidget, QStatusBar, QLabel)


def initUI(self):
    self.setWindowTitle('Поливайка')
    self.tableWidget = QTableWidget(self)

    self.tableWidget.setColumnCount(4)
    self.tableWidget.setHorizontalHeaderLabels(['ИД', 'Название', 'Информация', 'Периодичность полива'])
    self.tableWidget.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.Stretch)
    self.addButton = QPushButton('добавить', self)
    self.addButton.clicked.connect(self.adding)

    self.deleteButton = QPushButton('удалить', self)
    self.deleteButton.clicked.connect(self.delete_elem)

    self.statuslabel = QLabel()

    layout = QVBoxLayout()
    layout.addWidget(self.addButton)
    layout.addWidget(self.deleteButton)
    layout.addWidget(self.tableWidget)
    layout.addWidget(self.statuslabel)

    self.setLayout(layout)

    self.load_data()
