import sys
import sqlite3

from PyQt6 import QtCore
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import (
    QApplication, QTableWidgetItem, QMessageBox, QWidget, QTabWidget, QHBoxLayout, QMainWindow,
)
from main_window_design import initUI
from adding_form_design import initAddingFormUI
import datetime


class InfoWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.statuslabel = None
        self.add_form = None
        self.tableWidget = None
        self.setMinimumSize(700, 700)
        initUI(self)

    def load_data(self):
        self.con = sqlite3.connect('plant_base.sqlite')
        cur = self.con.cursor()
        cur.execute("""
            SELECT id, name, info, watering_frequency FROM plants
        """)
        rows = cur.fetchall()
        self.tableWidget.setRowCount(0)
        try:
            self.tableWidget.cellChanged.disconnect(self.change_elem)
        except Exception as e:
            pass
        for row in rows:
            self.tableWidget.insertRow(self.tableWidget.rowCount())
            for col, item in enumerate(row):
                self.tableWidget.setItem(self.tableWidget.rowCount() - 1, col, QTableWidgetItem(str(item)))
                if col == 0:
                    self.tableWidget.item(self.tableWidget.rowCount() - 1, col).setFlags(Qt.ItemFlag.ItemIsEditable)
        self.tableWidget.cellChanged.connect(self.change_elem)

        self.tableWidget.resizeColumnsToContents()
        self.tableWidget.resizeRowsToContents()

    def delete_elem(self):
        rows = list(set([i.row() for i in self.tableWidget.selectedItems()]))
        ids = [self.tableWidget.item(i, 0).text() for i in rows]
        if not ids:
            self.statuslabel.setText('Не выбраны элементы для удаления')
        else:
            self.statuslabel.setText('')
            valid = QMessageBox.question(
                self, '', "Действительно удалить растения с ИД " + ",".join(ids),
                buttons=QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
            if valid == QMessageBox.StandardButton.Yes:
                self.tableWidget.cellChanged.disconnect(self.change_elem)
                cur = self.con.cursor()
                cur.execute("DELETE FROM plants WHERE id IN (" + ", ".join(
                    '?' * len(ids)) + ")", ids)
                self.con.commit()
                self.update_result()

    def change_elem(self, row, column):
        item = self.tableWidget.item(row, column)
        id_item = self.tableWidget.item(row, 0).text()
        new_value = item.text()
        valid = QMessageBox.question(
            self, '', 'Вы действительно хотите изменить запись?',
            buttons=QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if valid == QMessageBox.StandardButton.Yes:
            try:
                query_column = 'name' if column == 1 else 'info' if column == 2 else 'watering_frequency'
                cur = self.con.cursor()
                cur.execute(f"UPDATE plants SET {query_column} = ? WHERE id = ?", (new_value, id_item))
                self.con.commit()
            except Exception as e:
                QMessageBox.critical(self, 'Ошибка', f'Не удалось обновить запись: {str(e)}')
        self.tableWidget.cellChanged.disconnect(self.change_elem)
        self.update_result()

    def adding(self):
        self.add_form = AddWidget(self)
        self.add_form.show()

    def update_result(self):
        self.load_data()
        self.tableWidget.cellChanged.connect(self.change_elem)

    def closeEvent(self, event):
        self.con.close()


class AddWidget(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.statuslabel = None
        self.calendarWidget = None
        self.info = None
        self.title = None
        self.watering_frequency = None
        initAddingFormUI(self)

    def get_adding_verdict(self):
        title = self.title.toPlainText()
        info = self.info.toPlainText()
        watering_frequency = self.watering_frequency.value()
        first_watering_date = self.calendarWidget.selectedDate().toString('dd.MM.yyyy')
        day, month, year = [int(i) for i in first_watering_date.split('.')]

        if not title or watering_frequency == 0 or datetime.date.today() < datetime.date(year, month, day):
            self.statuslabel.setText('Неверно заполнена форма')
            return False

        try:
            self.con = sqlite3.connect('plant_base.sqlite')
            cursor = self.con.cursor()
            cursor.execute(
                "INSERT INTO plants (name, info, first_watering_date, watering_frequency) VALUES (?, ?, ?, ?)",
                (title, info, first_watering_date, watering_frequency))
            self.con.commit()
            QMessageBox.information(self, 'Успех', 'Растение успешно добавлено!')
            self.parent().tableWidget.cellChanged.disconnect(self.parent().change_elem)
            self.parent().update_result()
            self.close()
            return True

        except Exception as e:
            QMessageBox.critical(self, 'Ошибка', f'Не удалось добавить растение: {str(e)}')
            return False


class CalendarWidget(QWidget):
    ...


class MyWidget(QWidget):
    def __init__(self):
        super().__init__()
        main = QWidget(self)
        main.resize(700, 700)
        box = QHBoxLayout(main)
        main.setLayout(box)
        self.tabWidget = QTabWidget(self)
        inf = InfoWidget()
        self.tabWidget.addTab(inf, 'таблица')
        calend = CalendarWidget()
        self.tabWidget.addTab(calend, 'календарь')

        self.tabWidget.currentChanged.connect(self.tab_changed)
        self.tabWidget.resize(700, 700)
        box.addWidget(self.tabWidget)
        self.setLayout(box)
        self.add_widget = AddWidget()

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key.Key_F11:
            if self.isFullScreen():
                self.showNormal()
            else:
                self.showFullScreen()

    def tab_changed(self, index):
        ...

    def show_add_widget(self):
        self.add_widget.show()  # или self.add_widget.exec()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyWidget()
    window.setWindowIcon(QIcon('app.ico'))
    window.show()
    sys.exit(app.exec())
