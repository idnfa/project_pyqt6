import sys
import sqlite3

from PyQt6 import QtCore
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import (
    QApplication, QTableWidgetItem, QMessageBox, QWidget, QTabWidget, QMainWindow,
    QVBoxLayout, QComboBox,
)
from main_window_design import init_ui
from adding_form_design import init_adding_form_ui
from mainer_info_design import init_mainer_form_ui
from adding_mainer_design import init_add_mainer_form_ui
from init_planning_ui import init_planning_ui
import datetime
from main_palette import PALETTES


class InfoWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.con = None
        self.result = None
        self.statuslabel = None
        self.add_form = None
        self.tableWidget = None
        self.setMinimumSize(700, 700)
        init_ui(self)

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
                try:
                    self.tableWidget.cellChanged.disconnect(self.change_elem)
                except Exception as e:
                    pass
                self.tableWidget.setItem(self.tableWidget.rowCount() - 1, col, QTableWidgetItem(str(item)))
                if col == 0:
                    self.tableWidget.item(self.tableWidget.rowCount() - 1, col).setFlags(Qt.ItemFlag.ItemIsEditable)

        self.tableWidget.resizeRowsToContents()
        self.tableWidget.cellChanged.connect(self.change_elem)

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
        self.con = sqlite3.connect('plant_base.sqlite')
        cursor = self.con.cursor()
        self.result = [name[0] for name in cursor.execute("""SELECT name FROM mainers""").fetchall()]

        if not self.result:
            self.statuslabel.setText('Сначала добавьте владельцев')
            return False
        self.statuslabel.setText('')
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
        self.con = None
        self.mainer_name = None
        self.statuslabel = None
        self.calendarWidget = None
        self.info = None
        self.title = None
        self.watering_frequency = None
        init_adding_form_ui(self)

    def get_adding_verdict(self):
        title = self.title.toPlainText()
        info = self.info.toPlainText()
        watering_frequency = self.watering_frequency.value()
        first_watering_date = self.calendarWidget.selectedDate().toString('dd.MM.yyyy')
        day, month, year = [int(i) for i in first_watering_date.split('.')]

        mainer_name = self.mainer_name.currentText()
        self.con = sqlite3.connect('plant_base.sqlite')
        cursor = self.con.cursor()
        mainer_id = int(cursor.execute("""SELECT id FROM mainers WHERE name = ?""", (mainer_name,)).fetchone()[0])

        if not title or watering_frequency == 0 or datetime.date.today() < datetime.date(year, month, day):
            self.statuslabel.setText('Неверно заполнена форма')
            return False

        try:
            self.con = sqlite3.connect('plant_base.sqlite')
            cursor = self.con.cursor()
            cursor.execute(
                "INSERT INTO plants (name, info, first_watering_date, watering_frequency, mainer) VALUES"
                " (?, ?, ?, ?, ?)",
                (title, info, first_watering_date, watering_frequency, mainer_id))
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
    def __init__(self):
        super().__init__()
        self.eventList = None
        self.calendarWidget = None
        init_planning_ui(self)
        self.event = None

    def show_events(self):
        self.event = {}
        self.eventList.clear()
        selected_date = self.calendarWidget.selectedDate().toString('dd.MM.yyyy')
        selected_date_as_dt = datetime.date(*[int(i) for i in selected_date.split('.')[::-1]])
        connect = sqlite3.connect('plant_base.sqlite')
        cur = connect.cursor()
        plants_data = cur.execute(
            """SELECT name, first_watering_date, watering_frequency, mainer FROM plants """).fetchall()

        for plant in plants_data:
            plant_name = plant[0]
            plant_first_watering_date = datetime.date(*[int(i) for i in plant[1].split('.')[::-1]])
            plant_watering_frequency = plant[2]
            plant_mainer = cur.execute("""SELECT name FROM mainers 
            WHERE id = ?""", (plant[3],)).fetchone()[0]
            if abs((selected_date_as_dt - plant_first_watering_date).days) % plant_watering_frequency == 0:
                if plant_mainer in self.event:
                    self.event[plant_mainer].append(plant_name)
                else:
                    self.event[plant_mainer] = [plant_name]
        if not self.event:
            self.eventList.addItem('Нет растений требующих полива')
        else:
            for mainer, plant_list in self.event.items():
                self.eventList.addItem(f'{mainer} должен(а) полить цветы: {", ".join(plant_list)}')


class MainerInfoWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.statuslabel = None
        self.add_form = None
        self.tableWidget = None
        self.setMinimumSize(700, 700)
        init_mainer_form_ui(self)

    def load_data(self):
        self.con = sqlite3.connect('plant_base.sqlite')
        cur = self.con.cursor()
        cur.execute("""
               SELECT id, name FROM mainers
           """)
        rows = cur.fetchall()
        self.tableWidget.setRowCount(0)
        self.tableWidget.setEnabled(False)
        for row in rows:
            self.tableWidget.insertRow(self.tableWidget.rowCount())
            for col, item in enumerate(row):
                self.tableWidget.setItem(self.tableWidget.rowCount() - 1, col, QTableWidgetItem(str(item)))
        self.tableWidget.resizeRowsToContents()

    def adding(self):
        self.add_form = AddMainerWidget(self)
        self.add_form.show()

    def update_result(self):
        self.load_data()


class AddMainerWidget(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.name = None
        self.statuslabel = None
        self.calendarWidget = None
        self.info = None
        self.title = None
        self.watering_frequency = None
        init_add_mainer_form_ui(self)

    def get_adding_verdict(self):
        name = self.name.toPlainText()
        if not name:
            self.statuslabel.setText('Неверно заполнена форма')
            return False
        self.con = sqlite3.connect('plant_base.sqlite')
        cursor = self.con.cursor()
        result = cursor.execute("""SELECT name FROM mainers 
            WHERE name = ?""", (name,)).fetchall()
        if result:
            self.statuslabel.setText('Владелец с таким именем уже существует')
            return False
        try:
            cursor.execute(
                "INSERT INTO mainers (name) VALUES (?)",
                (name,))
            self.con.commit()
            QMessageBox.information(self, 'Успех', 'Владелец успешно добавлен!')
            self.statuslabel.setText('')
            self.parent().update_result()
            self.close()
            return True

        except Exception as e:
            QMessageBox.critical(self, 'Ошибка', f'Не удалось добавить владельца: {str(e)}')
            return False


class MyWidget(QWidget):
    def __init__(self):
        super().__init__()
        main = QWidget(self)
        main.resize(700, 700)
        box = QVBoxLayout(main)
        main.setLayout(box)

        self.tabWidget = QTabWidget(self)

        self.inf = InfoWidget()

        self.palette_btn = QComboBox(self)
        self.palette_btn.addItems(PALETTES.keys())
        self.palette_btn.currentTextChanged.connect(self.change_palette)

        self.tabWidget.addTab(self.inf, 'таблица')

        self.calend = CalendarWidget()
        self.tabWidget.addTab(self.calend, 'календарь')

        self.mainers = MainerInfoWidget()
        self.tabWidget.addTab(self.mainers, 'владельцы')

        self.tabWidget.currentChanged.connect(self.tab_changed)
        self.tabWidget.resize(700, 700)
        box.addWidget(self.palette_btn)
        box.addWidget(self.tabWidget)

        self.setLayout(box)

    def change_palette(self):
        palette = PALETTES[self.palette_btn.currentText()]
        QApplication.setPalette(palette)

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key.Key_F11:
            if self.isFullScreen():
                self.showNormal()
            else:
                self.showFullScreen()

    def tab_changed(self, index):
        if index == 0:
            self.inf.update_result()
        elif index == 1:
            self.calend.show_events()
        elif index == 2:
            self.mainers.load_data()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setPalette(PALETTES['light'])
    app.setStyle('windowsvista')
    window = MyWidget()
    window.setWindowIcon(QIcon('app.ico'))
    window.show()
    sys.exit(app.exec())
