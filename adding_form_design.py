from PyQt6.QtWidgets import (
    QPushButton, QVBoxLayout, QPlainTextEdit, QHBoxLayout, QLabel,
    QCalendarWidget, QSpinBox, QWidget, QComboBox)


def init_adding_form_ui(self):
    self.setWindowTitle('Добавить элемент')
    self.setGeometry(100, 100, 300, 300)
    self.setFixedSize(600, 600)

    self.title = QPlainTextEdit(self)
    self.title.setFixedHeight(30)
    self.info = QPlainTextEdit(self)
    self.info.setFixedHeight(30)

    self.calendarWidget = QCalendarWidget()
    self.calendarWidget.setFixedSize(400, 300)

    self.watering_frequency = QSpinBox(self)

    self.mainer_name = QComboBox()
    self.mainer_name.addItems(self.parent().result)

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

    mainer_label = QHBoxLayout()
    self.label_4 = QLabel('Имя владельца')
    mainer_label.addWidget(self.label_4)
    mainer_label.addWidget(self.mainer_name)
    layout.addLayout(mainer_label)

    first_watering_date_label = QHBoxLayout()
    self.label_5 = QLabel('Дата последнего полива')
    first_watering_date_label.addWidget(self.label_5)
    first_watering_date_label.addWidget(self.calendarWidget)
    layout.addLayout(first_watering_date_label)

    layout.addWidget(self.pushButton)
    self.statuslabel = QLabel()
    layout.addWidget(self.statuslabel)
    container = QWidget()
    container.setLayout(layout)
    self.setCentralWidget(container)
