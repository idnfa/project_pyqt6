from PyQt6.QtWidgets import QPlainTextEdit, QPushButton, QVBoxLayout, QHBoxLayout, QLabel, QWidget


def init_add_mainer_form_ui(self):
    self.setWindowTitle('Добавить владельца')
    self.setGeometry(100, 100, 300, 300)
    self.setFixedSize(500, 500)

    self.name = QPlainTextEdit(self)
    self.name.setFixedHeight(30)

    self.pushButton = QPushButton('Добавить', self)
    self.pushButton.clicked.connect(self.get_adding_verdict)

    layout = QVBoxLayout()
    name_label = QHBoxLayout()
    self.label_1 = QLabel('Имя')
    name_label.addWidget(self.label_1)
    name_label.addWidget(self.name)
    layout.addLayout(name_label)

    layout.addWidget(self.pushButton)
    self.statuslabel = QLabel()
    layout.addWidget(self.statuslabel)
    container = QWidget()
    container.setLayout(layout)
    self.setCentralWidget(container)
