import random
import traceback

import enemy_generator


def check_pain(damage, enemy):
    if damage >= 150:
        enemy.pain_level += 2
    elif damage >= 200:
        enemy.pain_level += 3
    elif damage >= 300:
        enemy.pain_level += 4

    enemy.pain_level += 1
    damage -= 50
    while damage >= 100:
        damage -= 100
        enemy.pain_level += 1


def check_downed_limb(hit_place, enemy):
    if hit_place in [0, 6, 10]:
        enemy.injuries.append("СМЕРТЬ")
    elif hit_place in [1, 2]:
        enemy.injuries.append("Рука = 0")
        enemy.pain_level += 4
    elif hit_place in [3, 4]:
        enemy.injuries.append("Нога = 0")
        enemy.pain_level += 3
    else:
        enemy.injuries.append("Живот = 0")
        enemy.pain_level += 3


class DamageCounter:
    def __init__(self):
        self.random = random.Random()
        self.bullet_caliber_dict = {"9 * 18": [50, 5, -1], "9 * 19": [60, 15, -1], "7,62 * 25": [75, 15, 0], "5,7 * 28": [55, 25, 0],
                                    ".45 аср": [65, 25, 0], "9 * 21": [80, 20, 0], "СП-4": [95, 25, 0], "5,45 * 39": [80, 25, 0],
                                    "5,56 * 45": [75, 30, 0], "7,62 * 39": [90, 35, 2], "7,62 * 51": [100, 55, 2],
                                    "7,62 * 54": [110, 50, 2], "9 * 39": [80, 20, 2], "12,7 * 55": [95, 25, 3], "18 * 45": [70, 0, -20],
                                    "12 * 70 Картечь": [250, 5, 2], "12 * 70 Пуля": [115, 20, 2], "Аккумулятор": [250, 100, 3]}
        # Коэффициент урона, бронепробитие, кровотечение, бонус к доп травме, количество доп травм
        self.bullet_type_dict = {"Обычный": [1, 0, 0, 0, 1], "ЭП": [1.5, -15, 2, 30, 1], "БП": [1, 20, -1, -10, 1],
                                 "RIP": [3, -50, 4, 60, 2], "УБП": [1, 35, -2, -20, 1], "Разрывной": [3, -5, 8, 15, 2],
                                 "Зажигательный": [1, 0, -1, 0, 1]}
        self.body_part_indexes_dict = {"Левая нога": 3, "Правая нога": 4, "Левая рука": 1, "Правая рука": 2, "Живот": 5, "Грудь": 6, "Голова (защищено)": 0, "Голова (пустое место)": 10}
        self.armor_stages_dict = {"Целая": 1, "Немного повреждена": 2, "Повреждена": 3, "Сильно повреждена": 4, "Поломана": 5}

    def calculate_damage(self, enemy, damage_parameters, chosen_radio_button):
        try:
            if chosen_radio_button:
                bullet_damage = self.bullet_caliber_dict.get(damage_parameters[0])[0]
                bullet_piercing = self.bullet_caliber_dict.get(damage_parameters[0])[1]
                bullet_bleeding = self.bullet_caliber_dict.get(damage_parameters[0])[2]
                bullet_type = self.bullet_type_dict.get(damage_parameters[1])
                hit_place = self.body_part_indexes_dict.get(damage_parameters[2])

                if hit_place == 10:
                    enemy.injuries.append("СМЕРТЬ")
                    enemy.health_status[0] = "Голова: 0"
                    return

                bullet_damage *= bullet_type[0]
                bullet_piercing += bullet_type[1]

                armor_damage = bullet_damage
                enemy_armor_defence = int(enemy_generator.fullArmorDict.get(enemy.armor[0])[3].split("%")[0])
                if hit_place == 0: enemy_armor_defence = int(enemy_generator.fullHelmetDict.get(enemy.helmet[0])[3].split("%")[0])

                if "Живот = 0" in enemy.injuries: bullet_damage *= 1.5
                if hit_place in [1, 2, 3, 4]: bullet_piercing += 15

                if bullet_piercing > enemy_armor_defence:
                    armor_damage *= 1.5
                    if damage_parameters[0] == "9 * 39": bullet_damage += 20
                elif bullet_piercing < enemy_armor_defence:
                    armor_damage *= 0.5
                    if bullet_piercing + 20 <= enemy_armor_defence:
                        bullet_damage *= 0.1
                        if ((bullet_type[1] < -10 or damage_parameters[0] == "12 * 70 Картечь")
                                and damage_parameters[0] not in ["12 * 70 Пуля", "12,7 * 55", "9 * 39"]):
                            bullet_damage = 0
                        elif damage_parameters[0] in ["12 * 70 Пуля", "12,7 * 55", "9 * 39"] and bullet_type[1] > -10:
                            bullet_damage *= 3.3
                    else:
                        bullet_damage *= 1 - (((enemy_armor_defence - bullet_piercing) * 5) / 100)

                if damage_parameters[1] == "Зажигательный":
                    if (int(enemy_generator.fullArmorDict.get(enemy.armor[0])[5].split("%")[0]) +
                            int(enemy_generator.fullHelmetDict.get(enemy.helmet[0])[5].split("%")[0]) < 50):
                        enemy.injuries.append("Горит, 3")

                if bullet_damage >= 11:
                    self.check_additional_trauma(hit_place, bullet_damage, bullet_type, damage_parameters[0], enemy)

                if bullet_damage >= 50:
                    check_pain(bullet_damage, enemy)

                if bullet_piercing + 10 >= enemy_armor_defence:
                    self.check_bleeding(bullet_type, bullet_bleeding, enemy)

                if armor_damage >= enemy_generator.fullArmorDict.get(enemy.armor[0])[-1]: self.decrease_armor_stage(enemy, armor_damage)
                if armor_damage >= enemy_generator.fullHelmetDict.get(enemy.helmet[0])[-2]: self.decrease_helmet_stage(enemy, armor_damage)

                enemy.health_status[hit_place] = (enemy.health_status[hit_place].split(":")[0] + ": " +
                                                  str(int(int(enemy.health_status[hit_place].split(":")[1]) - bullet_damage)))
                enemy.full_hp -= bullet_damage
                if enemy.full_hp <= 0:
                    enemy.injuries.append("СМЕРТЬ")
                if int(enemy.health_status[hit_place].split(":")[1]) <= 0 < int(enemy.health_status[hit_place].split(":")[1]) + bullet_damage:
                    check_downed_limb(hit_place, enemy)
            else:
                try:
                    damage_amount = int(damage_parameters[3])
                except Exception:
                    traceback.print_exc()
                    return
                damage_type = damage_parameters[4]
                armor_piercing = int(damage_parameters[5].split("%")[0])
                enemy_armor_defence = 0

                if damage_amount >= enemy_generator.fullArmorDict.get(enemy.armor[0])[-1]: self.decrease_armor_stage(enemy, damage_amount)
                if damage_amount >= enemy_generator.fullHelmetDict.get(enemy.helmet[0])[-2]: self.decrease_helmet_stage(enemy, damage_amount)

                if damage_type == "Физический":
                    enemy_armor_defence = int(enemy_generator.fullArmorDict.get(enemy.armor[0])[3].split("%")[0])
                    enemy_armor_defence += int(enemy_generator.fullHelmetDict.get(enemy.helmet[0])[3].split("%")[0])
                elif damage_type == "Химический":
                    enemy_armor_defence = int(enemy_generator.fullArmorDict.get(enemy.armor[0])[4].split("%")[0])
                    enemy_armor_defence += int(enemy_generator.fullHelmetDict.get(enemy.helmet[0])[4].split("%")[0])
                elif damage_type == "Термический":
                    enemy_armor_defence = int(enemy_generator.fullArmorDict.get(enemy.armor[0])[5].split("%")[0])
                    enemy_armor_defence += int(enemy_generator.fullHelmetDict.get(enemy.helmet[0])[5].split("%")[0])
                elif damage_type == "Электрический":
                    enemy_armor_defence = int(enemy_generator.fullArmorDict.get(enemy.armor[0])[6].split("%")[0])
                    enemy_armor_defence += int(enemy_generator.fullHelmetDict.get(enemy.helmet[0])[6].split("%")[0])
                elif damage_type == "Радиационный":
                    enemy_armor_defence = int(enemy_generator.fullArmorDict.get(enemy.armor[0])[7].split("%")[0])
                    enemy_armor_defence += int(enemy_generator.fullHelmetDict.get(enemy.helmet[0])[7].split("%")[0])

                enemy_armor_defence -= armor_piercing
                if enemy_armor_defence < 0: enemy_armor_defence = 0

                damage_amount *= 1 - (enemy_armor_defence / 100)

                check_pain(damage_amount, enemy)

                enemy.full_hp -= damage_amount
                if enemy.full_hp <= 0:
                    enemy.injuries.append("СМЕРТЬ")

        except Exception:
            traceback.print_exc()

    def check_additional_trauma(self, hit_place, bullet_damage, bullet_type, bullet_name, enemy):
        add_trauma_count = 0
        if bullet_damage > 10:
            add_trauma_count = bullet_type[4]
            if bullet_name in ["12 * 70 Картечь", "12 * 70 Флешетты"]:
                add_trauma_count = int(bullet_damage / 50)
        while add_trauma_count:
            trauma_place = self.random.randint(1, 20)
            if hit_place == 0:
                if trauma_place in [1, 13, 17] and "Челюсть = 0" not in enemy.injuries:
                    enemy.injuries.append("Челюсть = 0")
                    enemy.pain_level += 4
                elif trauma_place == 3:
                    enemy.pain_level += 3
                elif trauma_place in [4, 14]:
                    enemy.injuries.append("Глаз = 0")
                    enemy.pain_level += 2
                elif trauma_place in [5, 11] and bullet_damage >= 40:
                    enemy.injuries.append("СМЕРТЬ")
                    enemy.injuries.append("Череп = 0")
                elif trauma_place in [6, 8]:
                    enemy.injuries.append("Нос = 0")
                    enemy.pain_level += 2
                elif trauma_place == 7:
                    enemy.bleedings.append("Сильное")
                elif trauma_place == 9:
                    enemy.bleedings.append("Экстремальное")
                elif trauma_place in [10, 18]:
                    enemy.injuries.append("Болевой шок")
                elif trauma_place == 15:
                    enemy.pain_level += 1
                elif trauma_place in [16, 20]:
                    enemy.injuries.append("Ухо = 0")
                    enemy.pain_level += 2
            elif hit_place in [1, 2, 3, 4]:
                if self.random.randint(1, 100) + bullet_type[3] >= 70:
                    if trauma_place in [3, 7, 10, 16, 18, 20]:
                        if hit_place in [1, 2]:
                            enemy.injuries.append("Перелом руки")
                        else:
                            enemy.injuries.append("Перелом ноги")
                        enemy.pain_level += 3
                    elif trauma_place in [9, 17]:
                        enemy.pain_level += 3
                    elif trauma_place in [5, 12, 14]:
                        enemy.pain_level += 1
            elif hit_place == 5:
                if self.random.randint(1, 100) + bullet_type[3] >= 30:
                    if trauma_place in [1, 20]:
                        enemy.injuries.append("Почка = 0")
                        enemy.pain_level += 8
                        enemy.bleedings.append("Экстремальное")
                    elif trauma_place in [3, 18]:
                        enemy.pain_level += 3
                    elif trauma_place == 1:
                        enemy.pain_level += 1
                    elif trauma_place in [4, 14]:
                        enemy.bleedings.append("Среднее")
                    elif trauma_place == 7:
                        enemy.bleedings.append("Сильное")
                    elif trauma_place in [5, 9, 12, 16]:
                        enemy.bleedings.append("Слабое")
                    elif trauma_place == 10:
                        enemy.injuries.append("СМЕРТЬ")
                        enemy.injuries.append("Печень = 0")
                    elif trauma_place == 17:
                        enemy.injuries.append("СМЕРТЬ")
                        enemy.injuries.append("Позвоночник = 0")
                    elif trauma_place == 6:
                        enemy.injuries.append("Желудок = 0")
                        enemy.pain_level += 8
                        enemy.bleedings.append("Сильное")
                    elif trauma_place == 8:
                        enemy.injuries.append("Болевой шок")
            elif hit_place == 6:
                if self.random.randint(1, 100) + bullet_type[3] >= 50:
                    if trauma_place == 1:
                        enemy.injuries.append("СМЕРТЬ")
                        enemy.injuries.append("Сердце = 0")
                    elif trauma_place in [3, 4, 6, 7, 12, 14, 16, 17]:
                        enemy.injuries.append("Легкое = 0")
                        enemy.pain_level += 5
                        enemy.bleedings.append("Сильное")
                    elif trauma_place == 20:
                        enemy.injuries.append("СМЕРТЬ")
                        enemy.injuries.append("Позвоночник = 0")
                    elif trauma_place in [9, 11]:
                        enemy.injuries.append("Болевой шок")
                    elif trauma_place == 10:
                        enemy.pain_level += 3
                    elif trauma_place in [5, 8, 15]:
                        enemy.bleedings.append("Слабое")
                    elif trauma_place in [13, 18]:
                        enemy.bleedings.append("Среднее")
            add_trauma_count -= 1

    def check_bleeding(self, bullet_type, bullet_bleeding, enemy):
        bleed_result = self.random.randint(1, 6) + bullet_type[2] + bullet_bleeding
        if bleed_result > 2:
            if bleed_result == 3:
                enemy.bleedings.append("Легкое")
            elif bleed_result in [4, 5]:
                enemy.bleedings.append("Среднее")
            elif bleed_result in [6, 7]:
                enemy.bleedings.append("Тяжелое")
            else:
                enemy.bleedings.append("Экстремальное")

    def decrease_armor_stage(self, enemy, damage):
        while damage > enemy_generator.fullArmorDict.get(enemy.armor[0])[-1] and self.armor_stages_dict.get(enemy.armor[1]) < 5:
            damage -= enemy_generator.fullArmorDict.get(enemy.armor[0])[-1]
            if self.armor_stages_dict.get(enemy.armor[1]) == 1:
                enemy.armor[1] = "Немного повреждена"
            elif self.armor_stages_dict.get(enemy.armor[1]) == 2:
                enemy.armor[1] = "Повреждена"
            elif self.armor_stages_dict.get(enemy.armor[1]) == 3:
                enemy.armor[1] = "Сильно повреждена"
            elif self.armor_stages_dict.get(enemy.armor[1]) == 4:
                enemy.armor[1] = "Поломана"

    def decrease_helmet_stage(self, enemy, damage):
        while damage > enemy_generator.fullHelmetDict.get(enemy.helmet[0])[-2] and self.armor_stages_dict.get(enemy.helmet[1]) < 5:
            damage -= enemy_generator.fullHelmetDict.get(enemy.helmet[0])[-2]
            if self.armor_stages_dict.get(enemy.armor[1]) == 1:
                enemy.armor[1] = "Немного повреждена"
            elif self.armor_stages_dict.get(enemy.armor[1]) == 2:
                enemy.armor[1] = "Повреждена"
            elif self.armor_stages_dict.get(enemy.armor[1]) == 3:
                enemy.armor[1] = "Сильно повреждена"
            elif self.armor_stages_dict.get(enemy.armor[1]) == 4:
                enemy.armor[1] = "Поломана"
