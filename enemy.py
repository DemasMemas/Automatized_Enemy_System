from enemy_loot import EnemyLoot

enemy_loot = EnemyLoot

class Enemy:
    def __init__(self, enemy_id):
        self.enemy_id = enemy_id
        self.enemy_name = ["Иван", "Одиночки"]
        # Оружие: Название, прочность, максимальная прочность, бронебойность, урон, очередь
        self.weapon = ["Пистолет Зосимова", 8, 100, 100, "5%", 50, 1]
        self.grenade = ["РГД-5", "1"]
        # Броня: Название, стадия прочности
        self.armor = ["Куртка Новичка", "Целая"]
        self.helmet = ["Без шлема", "Целая"]
        self.mobility_debuff = 0
        self.initiative = 10
        self.health_status = ["Голова: 50", "Левая рука: 90", "Правая рука: 90", "Левая нога: 100", "Правая нога: 100", "Живот: 120", "Грудь: 150"]
        self.blood_status = "Норма"
        self.pain_level = 0
        self.skills = ["Стрелковые навыки: 10", "Сила: 10", "Ловкость: 10", "Воля: 10", "Ближний бой: 10", "Внимательность: 10", "Тактика: 10", "Скрытность: 10", "Медицина: 10"]
        self.bleedings = []
        self.injuries = []
        self.enemy_loot = enemy_loot
