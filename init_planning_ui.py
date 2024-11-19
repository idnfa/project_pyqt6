from PyQt6.QtWidgets import QHBoxLayout, QCalendarWidget, QListWidget


def init_planning_ui(self):
    self.setWindowTitle('Расписание')
    self.setGeometry(100, 100, 800, 400)

    main_layout = QHBoxLayout()

    self.calendarWidget = QCalendarWidget()
    self.calendarWidget.setFixedSize(400, 300)
    self.calendarWidget.clicked.connect(self.show_events)

    main_layout.addWidget(self.calendarWidget)

    self.eventList = QListWidget()
    main_layout.addWidget(self.eventList)

    self.setLayout(main_layout)
