class EnemyCoder:
    def __init__(self):
        pass

    @staticmethod
    def code_enemy(enemy):
        enemy_string = ", ".join(enemy.enemy_name) + "\n"
        enemy_string += "Оружие: " + enemy.weapon[0] + ", Кол-во патронов: " + str(enemy.weapon[1]) + ", Бронепробитие: " + str(enemy.weapon[4]) + ", Урон: " + str(enemy.weapon[5]) + "\n"
        if enemy.grenade[0] != "Ничего" and enemy.grenade[1] != 0:
            enemy_string += "Гранаты: " + enemy.grenade[0] + " - " + str(enemy.grenade[1]) + "\n"
        enemy_string += "Броня: " + enemy.armor[0] + ", Прочность: " + str(enemy.armor[1]) + "\n"
        enemy_string += "Шлем: " + enemy.helmet[0] + ", Прочность: " + str(enemy.helmet[1]) + "\n"
        enemy_string += "Штраф перемещения: " + str(enemy.mobility_debuff) + "\n"
        enemy_string += "Инициатива: " + str(enemy.initiative) + "\n"
        if enemy.health_status != ["Голова: 50", "Левая рука: 90", "Правая рука: 90", "Левая нога: 100", "Правая нога: 100", "Живот: 120", "Грудь: 150"]:
            enemy_string += "Статус здоровья:\n" + "\n".join(enemy.health_status) + "\n"
        if enemy.blood_status != "Норма":
            enemy_string += "Статус кровопотери: " + enemy.blood_status + "\n"
        if enemy.pain_level != 0:
            enemy_string += "Уровень боли: " + str(enemy.pain_level) + "\n"
        enemy_string += ", ".join(enemy.skills[0:4]) + "\n"
        enemy_string += ", ".join(enemy.skills[5:8]) + "\n"
        if enemy.bleedings:
            enemy_string += "Кровотечения:\n" + "\n".join(enemy.bleedings) + "\n"
        if enemy.injuries:
            enemy_string += "Травмы:\n" + "\n".join(enemy.injuries) + "\n"
        enemy_string += "--------------------------------------------------------------------------------------------------------#" + str(enemy.enemy_id)
        return enemy_string
