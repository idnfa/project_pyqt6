from PyQt6.QtWidgets import (
    QPushButton, QVBoxLayout, QPlainTextEdit, QHBoxLayout, QLabel,
    QCalendarWidget, QSpinBox, QWidget)


def initAddingFormUI(self):
    self.setWindowTitle('Добавить элемент')
    self.setGeometry(100, 100, 300, 300)
    self.setFixedSize(500, 500)

    self.title = QPlainTextEdit(self)
    self.title.setFixedHeight(30)
    self.info = QPlainTextEdit(self)
    self.info.setFixedHeight(30)

    self.calendarWidget = QCalendarWidget()
    self.calendarWidget.setFixedSize(400, 300)

    self.watering_frequency = QSpinBox(self)

    self.pushButton = QPushButton('Добавить', self)
    self.pushButton.clicked.connect(self.get_adding_verdict)

    layout = QVBoxLayout()
    name_label = QHBoxLayout()
    self.label_1 = QLabel('Название')
    name_label.addWidget(self.label_1)
    name_label.addWidget(self.title)
    layout.addLayout(name_label)

    info_label = QHBoxLayout()
    self.label_2 = QLabel('Краткое описание')
    info_label.addWidget(self.label_2)
    info_label.addWidget(self.info)
    layout.addLayout(info_label)

    frequency_label = QHBoxLayout()
    self.label_3 = QLabel('Периодичность полива (в днях)')
    frequency_label.addWidget(self.label_3)
    frequency_label.addWidget(self.watering_frequency)
    layout.addLayout(frequency_label)

    first_watering_date_label = QHBoxLayout()
    self.y = QLabel('Дата последнего полива')
    first_watering_date_label.addWidget(self.y)
    first_watering_date_label.addWidget(self.calendarWidget)
    layout.addLayout(first_watering_date_label)

    layout.addWidget(self.pushButton)
    self.statuslabel = QLabel()
    layout.addWidget(self.statuslabel)
    container = QWidget()
    container.setLayout(layout)
    self.setCentralWidget(container)
