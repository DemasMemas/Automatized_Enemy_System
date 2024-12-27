import sys

from PyQt6 import uic
from PyQt6.QtWidgets import QApplication, QMainWindow, QMessageBox, QWidget

from enemy_coder import EnemyCoder
from enemy_generator import EnemyGenerator

enemy_coder = EnemyCoder()
enemy_list = []
enemy_generator = EnemyGenerator()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = uic.loadUi('main.ui', self)

        # Привязка кнопок к действиям
        self.ui.enemy_add_btn.clicked.connect(self.open_add_enemy_dialog)
        self.ui.clear_tracker_btn.clicked.connect(self.clear_tracker)

        self.ui.initiativeTracker.itemDoubleClicked.connect(self.open_enemy_loot)

    def open_enemy_loot(self, item):
        # Заглушка, нужно открывать другое окно с лутом персонажа
        QMessageBox.information(self, "Info", item.text())

    def open_add_enemy_dialog(self):
        dlg = CreateEnemyDialog(self)
        dlg.show()

    def add_enemy(self, enemy_generate_info):
        new_enemy = enemy_generator.generate_enemy(enemy_generate_info)
        enemy_list.append(new_enemy)
        self.ui.initiativeTracker.addItem(enemy_coder.code_enemy(new_enemy))

    def clear_tracker(self):
        self.ui.initiativeTracker.clear()
        enemy_list.clear()
        enemy_generator.last_id = 0


class CreateEnemyDialog(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.ui = uic.loadUi('createEnemyDialog.ui', self)
        self.main_window = main_window

        self.fractions_list = ["Одиночки", "Бандиты", "Наемники", "Военные", "Ученые", "Монолит", "Ренегаты", "Неопознанные"]
        self.difficulty_list = ["1. Противник новичок", "2. Противник опытный", "3. Противник ветеран", "4. Противник мастер"]
        self.wealth_list = ["1. Беден", "2. Средний класс", "3. В достатке", "4. Богат"]
        self.ui.fraction_box.addItems(self.fractions_list)
        self.ui.difficult_box.addItems(self.difficulty_list)
        self.ui.wealth_box.addItems(self.wealth_list)

        self.ui.ok_btn.clicked.connect(self.get_generated_enemy_info)
        self.ui.cancel_btn.clicked.connect(self.cancel_enemy_creation)

    def get_generated_enemy_info(self):
        if (self.ui.fraction_box.currentText() in self.fractions_list
            and self.ui.difficult_box.currentText() in self.difficulty_list
            and self.ui.wealth_box.currentText() in self.wealth_list):
            self.main_window.add_enemy([self.ui.fraction_box.currentText(), self.ui.difficult_box.currentText(), self.ui.wealth_box.currentText()])
            self.close()
        else:
            QMessageBox.information(self, "Ошибка", "Не выбрано значение")

    def cancel_enemy_creation(self):
        self.close()


app = QApplication([])
window = MainWindow()
window.show()
sys.exit(app.exec())
