import random
import sys
import traceback

from PyQt6 import uic
from PyQt6.QtWidgets import QApplication, QMainWindow, QMessageBox, QWidget, QButtonGroup

import damage_counter
from enemy_coder import EnemyCoder
from enemy_generator import EnemyGenerator

enemy_coder = EnemyCoder()
enemy_list = []
enemy_generator = EnemyGenerator()
random = random.Random()
d_counter = damage_counter.DamageCounter

def check_enemy_health_status(enemy):
    if "СМЕРТЬ" not in enemy.injuries:
        """if "Горит, 3" in enemy.injuries or "Горит, 2" in enemy.injuries or "Горит, 1" in enemy.injuries:
            for injury in enemy.injuries:
                if injury == "Горит, 1":
                    enemy.injuries.remove(injury)
            for injury in enemy.injuries:
                if injury == "Горит, 2":
                    enemy.injuries.remove(injury)
                    enemy.injuries.append("Горит, 1")
            for injury in enemy.injuries:
                if injury == "Горит, 3":
                    enemy.injuries.remove(injury)
                    enemy.injuries.append("Горит, 2")
            if (int(enemy_generator.fullArmorDict.get(enemy.armor[0])[5].split("%")[0]) +
                    int(enemy_generator.fullHelmetDict.get(enemy.helmet[0])[5].split("%")[0]) < 35):
                enemy.full_hp -= 50
                enemy.pain_level += 3"""

        will_bonus = ((int(enemy.skills[3].split(": ")[1]) - 10) // 2)
        if "Болевой шок" in enemy.injuries:
            if random.randint(1, 20) < 12 - will_bonus:
                enemy.injuries.remove("Болевой шок")
        else:
            if enemy.pain_level >= 5:
                if ("Болевой шок" not in enemy.injuries and random.randint(1, 20)
                        < enemy.pain_level * 2 - will_bonus):
                    enemy.injuries.append("Болевой шок")
        if enemy.bleedings:
            bleed_check_hard = will_bonus
            if enemy.blood_status == "Легкая":
                bleed_check_hard -= 1
            elif enemy.blood_status == "Средняя":
                bleed_check_hard -= 2
            elif enemy.blood_status == "Тяжелая":
                bleed_check_hard -= 3
            elif enemy.blood_status == "Критическая":
                bleed_check_hard -= 4
            for bleeding in enemy.bleedings:
                if bleeding == "Легкое":
                    bleed_check_hard += 1
                elif bleeding == "Среднее":
                    bleed_check_hard += 3
                elif bleeding == "Тяжелое":
                    bleed_check_hard += 5
                elif bleeding == "Экстремальное":
                    bleed_check_hard += 8

            if random.randint(1, 20) < bleed_check_hard:
                if enemy.blood_status == "Норма":
                    enemy.blood_status = "Легкая"
                if enemy.blood_status == "Легкая":
                    enemy.blood_status = "Средняя"
                elif enemy.blood_status == "Средняя":
                    enemy.blood_status = "Тяжелая"
                    enemy.mobility_debuff += 1
                    enemy.skills[1] = "Сила: " + str(int(enemy.skills[1].split(": ")[1]) - 1)
                    enemy.skills[2] = "Ловкость: " + str(int(enemy.skills[2].split(": ")[1]) - 1)
                elif enemy.blood_status == "Тяжелая":
                    enemy.blood_status = "Критическая"
                    enemy.mobility_debuff += 2
                    enemy.skills[1] = "Сила: " + str(int(enemy.skills[1].split(": ")[1]) - 2)
                    enemy.skills[2] = "Ловкость: " + str(int(enemy.skills[2].split(": ")[1]) - 2)
                elif enemy.blood_status == "Критическая":
                    enemy.blood_status = "СМЕРТЬ"
                    enemy.injuries.append("СМЕРТЬ")

        if enemy.full_hp <= 0:
            enemy.injuries.append("СМЕРТЬ")


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = uic.loadUi('main.ui', self)

        # Привязка кнопок к действиям
        self.ui.enemy_add_btn.clicked.connect(self.open_add_enemy_dialog)
        self.ui.clear_tracker_btn.clicked.connect(self.clear_tracker)
        self.ui.initiative_sort_btn.clicked.connect(self.sort_tracker)
        self.ui.next_turn_btn.clicked.connect(self.next_turn)
        self.ui.delete_enemy_btn.clicked.connect(self.delete_enemy)

        self.ui.enemy_add_rand_1.clicked.connect(self.add_1_random_enemy)
        self.ui.enemy_add_rand_3.clicked.connect(self.add_3_random_enemies)

        self.ui.grenade_btn.clicked.connect(self.throw_grenade)
        self.ui.shoot_btn.clicked.connect(self.shoot)
        self.ui.reload_btn.clicked.connect(self.reload)
        self.ui.inventory_btn.clicked.connect(self.open_inventory)
        self.ui.get_damage_btn.clicked.connect(self.get_damage)

        self.ui.initiativeTracker.itemDoubleClicked.connect(self.open_chose_dialog)

    def get_damage(self):
        try:
            dlg = CreateDamageDialog(self.get_current_enemy(), self)
            dlg.show()
        except Exception:
            traceback.print_exc()

    def get_current_enemy(self):
        try:
            enemy_id = int(self.ui.initiativeTracker.itemAt(0, 0).text().split("#")[1])
            for enemy in enemy_list:
                if enemy.enemy_id == enemy_id:
                    return enemy
        except Exception:
            traceback.print_exc()
            return enemy_list[-1]

    def open_inventory(self):
        dlg = LootDialog(self, self.get_current_enemy())
        dlg.show()

    def reload(self):
        enemy = self.get_current_enemy()
        enemy.weapon[1] = enemy_generator.fullWeaponDict.get(enemy.weapon[0])[-2]

    def shoot(self):
        try:
            dlg = CreateShootingDialog(self)
            dlg.show()
        except Exception:
            traceback.print_exc()

    def throw_grenade(self):
        try:
            enemy = self.get_current_enemy()
            if enemy.grenade[1] > 0:
                enemy.grenade[1] -= 1
                base_difficulty = 8 - ((int(enemy.skills[1].split(": ")[1]) - 10) // 2) - ((int(enemy.skills[2].split(": ")[1]) - 10) // 2) - (((int(enemy.skills[6].split(": ")[1]) - 10) // 2) * 2)

                QMessageBox.information(self, "Граната", enemy.enemy_name[0] + " кинул гранату " + enemy.grenade[0] +
                                        " с базовой сложностью = " + str(base_difficulty) +
                                        "\nЗначение броска метания: " + str(random.randint(1, 20)) +
                                        "\nДобавьте дальность к сложности.\nДобавьте 3/8 к сложности, если он сидит/лежит.\nДобавьте сложность препятствия 1/3/5, если она есть")
            self.refresh_current_enemy()
        except Exception:
            traceback.print_exc()

    def delete_enemy(self):
        enemy = self.get_current_enemy()
        self.ui.initiativeTracker.takeItem(0)
        enemy_list.remove(enemy)

    def add_3_random_enemies(self):
        self.add_1_random_enemy()
        self.add_1_random_enemy()
        self.add_1_random_enemy()

    def add_1_random_enemy(self):
        dlg = CreateEnemyDialog(self)
        dlg.random_enemy_creation()
        dlg.get_generated_enemy_info()

    def open_chose_dialog(self, item):
        enemy_id = int(item.text().split("#")[1])
        for enemy in enemy_list:
            if enemy.enemy_id == enemy_id:
                dlg = ChooseDialog(enemy, self)
                dlg.show()
                break

    def open_add_enemy_dialog(self):
        dlg = CreateEnemyDialog(self)
        dlg.show()

    def add_enemy(self, enemy_generate_info):
        try:
            new_enemy = enemy_generator.generate_enemy(enemy_generate_info)
            enemy_list.append(new_enemy)
            self.ui.initiativeTracker.addItem(enemy_coder.code_enemy(new_enemy))
        except Exception:
            traceback.print_exc()

    def clear_tracker(self):
        self.ui.initiativeTracker.clear()
        enemy_list.clear()
        enemy_generator.last_id = 0

    def sort_tracker(self):
        enemy_list.sort(key=lambda x: x.initiative, reverse=True)
        self.ui.initiativeTracker.clear()
        for enemy in enemy_list:
            self.ui.initiativeTracker.addItem(enemy_coder.code_enemy(enemy))

    def next_turn(self):
        try:
            enemy = self.get_current_enemy()
            self.ui.initiativeTracker.takeItem(0)
            check_enemy_health_status(enemy)
            self.ui.initiativeTracker.addItem(enemy_coder.code_enemy(enemy))
        except Exception:
            traceback.print_exc()

    def refresh_current_enemy(self):
        enemy = self.get_current_enemy()
        self.ui.initiativeTracker.takeItem(0)
        self.ui.initiativeTracker.insertItem(0, enemy_coder.code_enemy(enemy))


class ChooseDialog(QWidget):
    def __init__(self, enemy, main):
        super().__init__()
        self.main = main
        self.enemy = enemy
        self.ui = uic.loadUi('loot_or_damage.ui', self)

        self.ui.inventory_btn.clicked.connect(self.open_inventory)
        self.ui.get_damage_btn.clicked.connect(self.get_damage)

    def get_damage(self):
        try:
            dlg = CreateDamageDialog(self.enemy, self.main)
            dlg.show()
        except Exception:
            traceback.print_exc()
        self.close()

    def open_inventory(self):
        try:
            dlg = LootDialog(self.main, self.enemy)
            dlg.show()
        except Exception:
            traceback.print_exc()
        self.close()


class CreateDamageDialog(QWidget):
    def __init__(self, enemy, main):
        super().__init__()
        self.main = main
        self.enemy = enemy
        self.damage_parameters = []
        self.ui = uic.loadUi('createDamageDialog.ui', self)

        self.radio_group = QButtonGroup()
        self.radio_group.addButton(self.ui.bulletRadio)
        self.radio_group.addButton(self.ui.otherDamageRadio)
        self.ui.get_damage_btn.clicked.connect(self.get_damage)

        self.caliber_list = ["9 * 18", "9 * 19", "7,62 * 25", "5,7 * 28", ".45 аср", "9 * 21", "СП-4", "5,45 * 39",
                             "5,56 * 45", "7,62 * 39", "7,62 * 51", "7,62 * 54", "9 * 39", "12,7 * 55", "18 * 45",
                             "12 * 70 Картечь", "12 * 70 Пуля", "Аккумулятор"]
        self.bullet_type_list = ["Обычный", "ЭП", "БП", "RIP", "УБП", "Разрывной", "Зажигательный"]
        self.hit_place_list = ["Левая нога", "Правая нога", "Левая рука", "Правая рука", "Живот", "Грудь", "Голова (защищено)", "Голова (пустое место)"]
        self.damage_type_list = ["Физический", "Термический", "Химический", "Электрический", "Радиационный"]
        self.armor_piercing_list = ["0%", "5%", "10%", "15%", "20%", "25%", "30%", "35%", "40%", "45%", "50%", "55%",
                                    "60%", "65%", "70%", "75%", "80%", "85%", "90%", "95%", "100%"]

        self.ui.caliber_box.addItems(self.caliber_list)
        self.ui.bullet_type_box.addItems(self.bullet_type_list)
        self.ui.hit_place_box.addItems(self.hit_place_list)
        self.ui.damage_type_box.addItems(self.damage_type_list)
        self.ui.armor_piercing_box.addItems(self.armor_piercing_list)

    def get_damage(self):
        chosen_radio_button = self.ui.bulletRadio.isChecked()

        self.damage_parameters = [self.ui.caliber_box.currentText(),
        self.ui.bullet_type_box.currentText(),
        self.ui.hit_place_box.currentText(),
        self.ui.damage_amount_line.text(),
        self.ui.damage_type_box.currentText(),
        self.ui.armor_piercing_box.currentText()]

        dmg_counter = damage_counter.DamageCounter()
        dmg_counter.calculate_damage(self.enemy, self.damage_parameters, chosen_radio_button)

        self.main.refresh_current_enemy()
        self.close()


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
        self.ui.random_btn.clicked.connect(self.random_enemy_creation)

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

    def random_enemy_creation(self):
        self.ui.fraction_box.setCurrentIndex(random.randint(0, len(self.fractions_list)-1))
        self.ui.difficult_box.setCurrentIndex(random.randint(0, len(self.difficulty_list)-1))
        self.ui.wealth_box.setCurrentIndex(random.randint(0, len(self.wealth_list)-1))


class CreateShootingDialog(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.ui = uic.loadUi('createShootingDialog.ui', self)
        self.main_window = main_window

        self.bullet_type_list = ["Обычный", "ЭП", "БП", "RIP", "УБП", "Разрывной", "Зажигательный"]
        self.shooting_type_list = ["Неприцельный", "Беглый", "Прицельный", "Очередь", "Прицельный Голова", "Прицельный ноги на ходу"]
        self.cover_list = ["Нет укрытия", "Укрытие на 1/2", "Укрытие на 3/4"]
        self.ui.bullet_type_box.addItems(self.bullet_type_list)
        self.ui.shooting_type_box.addItems(self.shooting_type_list)
        self.ui.cover_box.addItems(self.cover_list)

        self.ui.shoot_btn.clicked.connect(self.shoot)

    def shoot(self):
        try:
            enemy = self.main_window.get_current_enemy()
            enemy_weapon = enemy_generator.fullWeaponDict.get(enemy.weapon[0])
            base_difficulty = 10 - ((int(enemy.skills[0].split(": ")[1]) - 10) // 2) - enemy_weapon[6]

            if self.ui.shooting_type_box.currentText() == "Беглый":
                base_difficulty += 4
            elif self.ui.shooting_type_box.currentText() == "Прицельный":
                base_difficulty -= 3
            elif self.ui.shooting_type_box.currentText() == "Прицельный Голова":
                base_difficulty += 8
            elif self.ui.shooting_type_box.currentText() == "Прицельный ноги на ходу":
                base_difficulty += 6

            if self.ui.enemy_movement_check.isChecked():
                base_difficulty += 1
            if self.ui.over_distance_check.isChecked():
                base_difficulty += 1
            if self.ui.shooter_movement_check.isChecked():
                base_difficulty += 1

            if self.ui.cover_box.currentText() == "Укрытие на 1/2":
                base_difficulty += 2
            elif self.ui.cover_box.currentText() == "Укрытие на 3/4":
                base_difficulty += 1

            if self.ui.shooting_type_box.currentText() != "Очередь":
                enemy.weapon[1] -= 1
                QMessageBox.information(self, "Выстрел", enemy.enemy_name[0] + " выстрелил с уроном: " +
                                        str(enemy_weapon[4]) + " и бронебойностью: " + str(enemy_weapon[3]) +
                                        "\nТип патрона = " + self.ui.bullet_type_box.currentText() +
                                        "\nБазовая сложность = " + str(base_difficulty) +
                                        "\nЗначение броска стрельбы: " + str(random.randint(1, 20)) +
                                        "\nЗначение броска для помех/преимущества: " + str(random.randint(1, 20)))
            else:

                enemy.weapon[1] -= enemy_weapon[5]
                message = (enemy.enemy_name[0] + " выстрелил с уроном: " + str(enemy_weapon[4]) + " и бронебойностью: "
                           + str(enemy_weapon[3]) + "\nТип патрона = " + self.ui.bullet_type_box.currentText()
                           + "\nСложность первого выстрела = " + str(base_difficulty) + "\nБазовая сложность = "
                           + str(base_difficulty + enemy_weapon[-1]))
                for i in range(1, enemy_weapon[5] + 1, 1):
                    message += ("\nЗначение броска стрельбы: " + str(random.randint(1, 20))
                                + "\nЗначение броска для помех/преимущества: " + str(random.randint(1, 20)))
                QMessageBox.information(self, "Выстрел", message)
        except Exception:
            traceback.print_exc()
        self.main_window.refresh_current_enemy()
        self.close()

class LootDialog(QWidget):
    def __init__(self, main_window, enemy):
        super().__init__()
        self.ui = uic.loadUi('lootWindow.ui', self)
        self.main_window = main_window
        self.enemy = enemy

        self.ui.weaponLabel.setText("Оружие: " + enemy.weapon[0] + " " + str(enemy.weapon[2]) + "/" + str(enemy.weapon[3]))
        self.ui.nameLabel.setText(", ".join(enemy.enemy_name))
        self.ui.armorLabel.setText("Броня: " + ", ".join(enemy.armor))
        self.ui.helmetLabel.setText("Шлем: " + ", ".join(enemy.helmet))
        self.ui.ragLabel.setText("Разгрузка: " + enemy.enemy_loot.rag)
        self.ui.headphonesLabel.setText("Наушники: " + enemy.enemy_loot.headphones)
        self.ui.backpackLabel.setText("Рюкзак: " + enemy.enemy_loot.backpack)
        self.ui.foodLabel.setText("Еда: " + ", ".join(enemy.enemy_loot.loot[2]))
        self.ui.medLabel.setText("Медикаменты: " + ", ".join(enemy.enemy_loot.loot[1]))
        self.ui.miscLabel.setText("Прочее: " + enemy.enemy_loot.loot[3] + ", " + enemy.enemy_loot.loot[4])
        self.ui.bulletLabel.setText("Патроны: " + str(enemy.enemy_loot.loot[0]))
        self.ui.moneyLabel.setText("Деньги: " + str(enemy.enemy_loot.loot[5]))

app = QApplication([])
window = MainWindow()
window.show()
sys.exit(app.exec())
