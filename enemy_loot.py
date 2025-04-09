import random

food_table = {
    1: {  # Уровень 1 (слабые противники)
        1: ["Хлеб", "Вода", "Кустарное пиво", "Самокрутка"],
        2: ["Хлеб", "Вода", "Консервы", "Колбаса", "Энергетик", "Самокрутка"],
        3: ["Хлеб", "Консервы", "Колбаса", "Сахар", "Энергетик", "Самокрутка"],
        4: ["Консервы", "Колбаса", "Кофе", "Пиво 'Лей не жалей'", "Самокрутка"]
    },
    2: {  # Уровень 2 (средние противники)
        1: ["Хлеб", "Вода", "Консервы", "Колбаса", "Энергетик", "Самокрутка"],
        2: ["Хлеб", "Консервы", "Колбаса", "Энергетик", "Кофе", "Самокрутка"],
        3: ["Консервы", "Колбаса", "Энергетик", "Кофе", "Протеин", "Самокрутка"],
        4: ["Консервы", "Колбаса", "Кофе", "Плитка шоколада", "Сигареты 'Египетская сила'"]
    },
    3: {  # Уровень 3 (сильные противники)
        1: ["Консервы", "Колбаса", "Кофе", "Энергетик", "Сигареты 'Египетская сила'"],
        2: ["Консервы", "Колбаса", "Кофе", "Протеин", "Сигареты 'Египетская сила'"],
        3: ["Кофе", "Протеин", "Плитка шоколада", "Вино", "Сигареты 'Гибралтарский пролив'"],
        4: ["Плитка шоколада", "Вино", "Сигареты 'Гибралтарский пролив'", "Сигареты 'Петр Второй'", "Сигары"]
    },
    4: {  # Уровень 4 (элитные противники)
        1: ["Кофе", "Протеин", "Вино", "Сигареты 'Гибралтарский пролив'"],
        2: ["Протеин", "Плитка шоколада", "Вино", "Сигареты 'Гибралтарский пролив'", "Сигареты 'Петр Второй'"],
        3: ["Плитка шоколада", "Вино", "Сигареты 'Петр Второй'", "Сигары"],
        4: ["Вино", "Сигары", "Самогон"]
    }
}
devices_table = {
    1: {  # Уровень 1 (слабые противники)
        1: ["Фонарь", "Рация", "КПК", "Напильник", "Мультитул"],
        2: ["Бинокль", "Фонарь", "Набор инструментов Оружейника (Упрощёные) 2", "Плоскогубцы"],
        3: ["Рация", "КПК", "Плоскогубцы", "Набор инструментов Оружейника (Упрощёные) 5"],
        4: ["КПК", "Набор инструментов Оружейника (Упрощёные) 2", "Мультитул"]
    },
    2: {  # Уровень 2 (средние противники)
        1: ["Фонарь улучшенный", "Рация", "КПК", "Бинокль", "Ножницы"],
        2: ["Фонарь улучшенный", "КПК", "Бинокль с дальномером", "Шлифовальные инструменты 5"],
        3: ["Рация", "КПК", "Шприц пистолет", "Паяльные инструменты 3", "Мультитул"],
        4: ["Шприц пистолет", "Фонарь улучшенный", "КПК", "Набор инструментов Оружейника (Стандартные) 2"]
    },
    3: {  # Уровень 3 (сильные противники)
        1: ["Бинокль ночной", "Гитара", "Светящаяся палочка", "Набор инструментов Бронника (Упрощёные) 1"],
        2: ["Бинокль с дальномером", "КПК", "Шприц пистолет", "Гитара", "Набор инструментов Охотника 5"],
        3: ["Фонарь улучшенный", "Бинокль ночной", "КПК", "Шприц пистолет", "Набор инструментов Оружейника (Расширенные) 4"],
        4: ["Светящаяся палочка", "КПК", "Бинокль с дальномером", "Шприц пистолет", "Набор инструментов Охотника 5", "Мультитул"]
    },
    4: {  # Уровень 4 (элитные противники)
        1: ["КПК", "Гитара", "Светящаяся палочка", "Радио", "Набор инструментов Бронника (Стандартные) 2"],
        2: ["Палатка", "Светящаяся палочка", "КПК", "Бинокль ночной", "Набор инструментов Хирурга 3"],
        3: ["Батарейки", "Фонарь улучшенный", "Шприц пистолет", "Гитара", "Набор инструментов Бронника (Расширенные) 3"],
        4: ["КПК", "Фонарь улучшенный", "Светящаяся палочка", "Бинокль с дальномером", "Гитара", "Набор инструментов Врача 5", "Мультитул"]
    }
}
med_table = {
    1: {  # Уровень 1 (слабые противники)
        1: ["Обычные"],
        2: ["Обычные"],
        3: ["Обычные", "Обычные", "Обычные", "Редкие"],
        4: ["Обычные", "Обычные", "Редкие"]
    },
    2: {  # Уровень 2 (средние противники)
        1: ["Обычные", "Обычные", "Редкие"],
        2: ["Обычные", "Редкие"],
        3: ["Обычные", "Редкие", "Редкие"],
        4: ["Обычные", "Редкие", "Редкие", "Редкие"]
    },
    3: {  # Уровень 3 (сильные противники)
        1: ["Обычные", "Редкие", "Редкие", "Редкие"],
        2: ["Обычные", "Редкие", "Редкие", "Редкие", "Очень редкие"],
        3: ["Редкие", "Редкие", "Редкие", "Очень редкие"],
        4: ["Редкие", "Редкие", "Очень редкие", "Очень редкие"]
    },
    4: {  # Уровень 4 (элитные противники)
        1: ["Редкие", "Редкие", "Очень редкие", "Очень редкие"],
        2: ["Редкие", "Очень редкие", "Очень редкие"],
        3: ["Редкие", "Очень редкие", "Очень редкие", "Очень редкие"],
        4: ["Очень редкие"]
    }
}
opponent_medicines = {
    "Обычные": [
        "Бинт",
        "Жгут",
        "Антисептический тампон",
        "Ампула Оксицела",
        "Пластырь с гемостатиком",
        "Плитка Гематогена",
        "Пакет физраствора",
        "Шина",
        "Ампула Тромбина-Л",
        "Пенициллин (Таблетка)",
        "Настойка мяты",
        "Самопальный стимпак",
        "Настойка подорожника",
        "Ибупрофен (Таблетка)",
        "Аспирин (Таблетка)",
        "Ампула Антирад-А",
        "Анальгин (Таблетка)",
        "Бутылек нашатыря",
        "Настойка боярышника",
        "Активированный уголь (Таблетка)",
        "Антирад. Препарат 'Йод-Плюс' (Таблетка)",
        "Очищенная настойка коры"
    ],
    "Редкие": [
        "Ампула Тромбина",
        "Шина Шарнирова",
        "Ампула Глобулина",
        "Аугментин (Таблетка)",
        "Сангвинил (Таблетка)",
        "Стимулятор 'Полукровка'",
        "Пластырь 'Стазис'",
        "Ампула Адреналина",
        "Ампула Антирад-Б",
        "Регенеративный стимулятор Альфа",
        "Препарат 'Радист'-Л",
        "Стимулятор 'Психолог-М'",
        "Стимулятор 'Грация'",
        "Стимулятор Скала",
        "Стимулятор Морковчатник",
        "Военный стимпак",
        "Препарат 02",
        "Стимулятор Болид",
        "Стимулятор Покой",
        "Пакет крови",
        "Подавитель эмоций"
    ],
    "Очень редкие": [
        "Ампула Эпинефрина",
        "Стимулятор 'Орёл'",
        "Стимулятор Воля",
        "Стимулятор Гора",
        "Стимулятор Гора-Д",
        "Стимулятор Скала-Н",
        "Стимулятор Викинг",
        "Стимулятор Варвар",
        "Препарат 'Радист'",
        "Ампула Антирад-Г",
        "Регенеративный стимулятор Звезда",
        "Регенеративный стимулятор Бета",
        "Научный стимпак",
        "Стимулятор Мозгоправ",
        "Стимулятор Психолог-М",
        "Стимулятор 'Котик'",
        "Препарат К.О.Д.",
        "Военный стимулятор ПЧеЛа",
        "Стимулятор Воля-Н",
        "Научный стимулятор Волкодав",
        "Кровоостанавливающее 'Желе'",
        "Кровоостанавливающее 'Хлопок'",
        "Антирад. Препарат 'Радогон'",
        "Противорадиационное 'Брезент'-ПБ",
        "Стимулятор Шумодав"
    ]
}
opponent_rags = {
    1: {  # Уровень 1 (слабые противники)
        1: ["Ничего"],  # Богатство 1
        2: ["Ничего", "4В77"],  # Богатство 2
        3: ["Ничего", "4В77", "Жилет 'Взломщик'"],  # Богатство 3
        4: ["Ничего", "Жилет 'Взломщик'"]  # Богатство 4
    },
    2: {  # Уровень 2 (средние противники)
        1: ["Ничего", "Жилет 'Стрелок'"],  # Богатство 1
        2: ["Ничего", "4В227", "ВиТ-101"],  # Богатство 2
        3: ["Ничего", "Жилет 'Стрелок'", "4В227"],  # Богатство 3
        4: ["Ничего", "ВиТ-101", "Разгрузка 'Тактик'"]  # Богатство 4
    },
    3: {  # Уровень 3 (сильные противники)
        1: ["Ничего", "Жилет 'Охотник'"],  # Богатство 1
        2: ["Ничего", "Жилет 'Гора'", "Тактик"],  # Богатство 2
        3: ["Ничего", "Жилет 'Гора'", "Тактик"],  # Богатство 3
        4: ["Ничего", "Разгрузка 'Черногорец'"]  # Богатство 4
    },
    4: {  # Уровень 4 (элитные противники)
        1: ["Ничего", "Жилет 'Охотник'"],  # Богатство 1
        2: ["Ничего", "Жилет 'Гора'", "Тактик"],  # Богатство 2
        3: ["Ничего", "Разгрузка 'Черногорец'"],  # Богатство 3
        4: ["Ничего", "СБДЖ"]  # Богатство 4
    }
}
opponent_headphones = {
    1: {  # Уровень 1 (слабые противники)
        1: ["Ничего"],  # Богатство 1
        2: ["Ничего", "Беруши"],  # Богатство 2
        3: ["Ничего", "Беруши", "ГСШ-01"],  # Богатство 3
        4: ["Ничего", "ГСШ-01", "ПроУши"]  # Богатство 4
    },
    2: {  # Уровень 2 (средние противники)
        1: ["Ничего", "ГСШ-01"],  # Богатство 1
        2: ["Ничего", "ПроУши", "Стрелок-2"],  # Богатство 2
        3: ["Ничего", "Стрелок-2", "ЗащУш"],  # Богатство 3
        4: ["Ничего", "ПроУши", "ТактикКiт"]  # Богатство 4
    },
    3: {  # Уровень 3 (сильные противники)
        1: ["Ничего", "Стрелок-2"],  # Богатство 1
        2: ["Ничего", "ТактикКiт", "ГСШ-01"],  # Богатство 2
        3: ["Ничего", "ТактикКiт", "Стрелок-2"],  # Богатство 3
        4: ["Ничего", "ХватаюШи"]  # Богатство 4
    },
    4: {  # Уровень 4 (элитные противники)
        1: ["Ничего", "ТактикКiт"],  # Богатство 1
        2: ["Ничего", "ПроУши", "ХватаюШи"],  # Богатство 2
        3: ["Ничего", "ХватаюШи", "ЗащУш"],  # Богатство 3
        4: ["Ничего", "ХватаюШи", "ТактикКiт"]  # Богатство 4
    }
}
opponent_misc_items = {
    1: {  # Уровень 1 (слабые противники)
        1: [
            "Игральные карты", "Игральная кость", "Стеклянная бутылка",
            "Свисток", "Зажигалка", "Компас", "Шприц", "Марля", "Бумага", "Спички", "Мыло"
        ],  # Богатство 1
        2: [
            "Игральные карты", "Игральная кость", "Стеклянная бутылка",
            "Пластиковая бутылка", "Бинокль", "Свисток", "Зажигалка",
            "Шприц", "Марля", "Клей", "Резина", "Фольга", "Скотч", "Порох", "Химические материалы",
            "Медицинские материалы", "Батарейки"
        ],  # Богатство 2
        3: [
            "Игральные карты", "Игральная кость", "Стеклянная бутылка",
            "Пластиковая бутылка", "Бинокль", "Гитара", "Рация", "Свисток",
            "Зажигалка", "Компас", "Шприц", "Марля", "Бумага", "Скотч", "Порох",
            "Химические материалы", "Медицинские материалы", "Электронные материалы"
        ],  # Богатство 3
        4: [
            "Игральные карты", "Игральная кость", "Стеклянная бутылка",
            "Пластиковая бутылка", "Бинокль", "Гитара", "Рация", "Свисток",
            "Зажигалка", "Компас", "Шприц", "Марля", "Бумага", "Клей", "Резина",
            "Скотч", "Порох", "Химические материалы", "Медицинские материалы",
            "Электронные материалы", "Флешка с информацией о навыке", "Батарейки"
        ],  # Богатство 4
    },
    2: {  # Уровень 2 (средние противники)
        1: [
            "Игральные карты", "Игральная кость", "Стеклянная бутылка",
            "Свисток", "Зажигалка", "Компас", "Шприц", "Марля", "Бумага", "Спички", "Мыло"
        ],  # Богатство 1
        2: [
            "Игральные карты", "Игральная кость", "Стеклянная бутылка",
            "Пластиковая бутылка", "Бинокль", "Свисток", "Зажигалка",
            "Шприц", "Марля", "Клей", "Резина", "Фольга", "Скотч", "Порох", "Химические материалы",
            "Медицинские материалы", "Батарейки"
        ],  # Богатство 2
        3: [
            "Игральные карты", "Игральная кость", "Стеклянная бутылка",
            "Пластиковая бутылка", "Бинокль", "Гитара", "Рация", "Свисток",
            "Зажигалка", "Компас", "Шприц", "Марля", "Бумага", "Скотч", "Порох",
            "Химические материалы", "Медицинские материалы", "Электронные материалы"
        ],  # Богатство 3
        4: [
            "Игральные карты", "Игральная кость", "Стеклянная бутылка",
            "Пластиковая бутылка", "Бинокль", "Гитара", "Рация", "Свисток",
            "Зажигалка", "Компас", "Шприц", "Марля", "Бумага", "Клей", "Резина",
            "Скотч", "Порох", "Химические материалы", "Медицинские материалы",
            "Электронные материалы", "Флешка с информацией о навыке", "Батарейки"
        ],  # Богатство 4
    },
    3: {  # Уровень 3 (сильные противники)
        1: [
            "Игральные карты", "Игральная кость", "Стеклянная бутылка",
            "Свисток", "Зажигалка", "Компас", "Шприц", "Марля", "Бумага", "Спички", "Мыло"
        ],  # Богатство 1
        2: [
            "Игральные карты", "Игральная кость", "Стеклянная бутылка",
            "Пластиковая бутылка", "Бинокль", "Свисток", "Зажигалка",
            "Шприц", "Марля", "Клей", "Резина", "Фольга", "Скотч", "Порох", "Химические материалы",
            "Медицинские материалы", "Батарейки"
        ],  # Богатство 2
        3: [
            "Игральные карты", "Игральная кость", "Стеклянная бутылка",
            "Пластиковая бутылка", "Бинокль", "Гитара", "Рация", "Свисток",
            "Зажигалка", "Компас", "Шприц", "Марля", "Бумага", "Скотч", "Порох",
            "Химические материалы", "Медицинские материалы", "Электронные материалы"
        ],  # Богатство 3
        4: [
            "Игральные карты", "Игральная кость", "Стеклянная бутылка",
            "Пластиковая бутылка", "Бинокль", "Гитара", "Рация", "Свисток",
            "Зажигалка", "Компас", "Шприц", "Марля", "Бумага", "Клей", "Резина",
            "Скотч", "Порох", "Химические материалы", "Медицинские материалы",
            "Электронные материалы", "Флешка с информацией о навыке", "Батарейки"
        ],  # Богатство 4
    },
    4: {  # Уровень 4 (элитные противники)
        1: [
            "Игральные карты", "Игральная кость", "Стеклянная бутылка",
            "Свисток", "Зажигалка", "Компас", "Шприц", "Марля", "Бумага", "Спички", "Мыло"
        ],  # Богатство 1
        2: [
            "Игральные карты", "Игральная кость", "Стеклянная бутылка",
            "Пластиковая бутылка", "Бинокль", "Свисток", "Зажигалка",
            "Шприц", "Марля", "Клей", "Резина", "Фольга", "Скотч", "Порох", "Химические материалы",
            "Медицинские материалы", "Батарейки"
        ],  # Богатство 2
        3: [
            "Игральные карты", "Игральная кость", "Стеклянная бутылка",
            "Пластиковая бутылка", "Бинокль", "Гитара", "Рация", "Свисток",
            "Зажигалка", "Компас", "Шприц", "Марля", "Бумага", "Скотч", "Порох",
            "Химические материалы", "Медицинские материалы", "Электронные материалы"
        ],  # Богатство 3
        4: [
            "Игральные карты", "Игральная кость", "Стеклянная бутылка",
            "Пластиковая бутылка", "Бинокль", "Гитара", "Рация", "Свисток",
            "Зажигалка", "Компас", "Шприц", "Марля", "Бумага", "Клей", "Резина",
            "Скотч", "Порох", "Химические материалы", "Медицинские материалы",
            "Электронные материалы", "Флешка с информацией о навыке", "Батарейки"
        ],  # Богатство 4
    }
}
opponent_backpacks = {
    1: {  # Уровень 1 (слабые противники)
        1: ["Ничего", "Сумка"],  # Богатство 1
        2: ["Ничего", "Сумка", "Вещмешок"],  # Богатство 2
        3: ["Сумка", "Вещмешок", "Спортивный рюкзак"],  # Богатство 3
        4: ["Вещмешок", "Спортивный рюкзак", "Рюкзак"],  # Богатство 4
    },
    2: {  # Уровень 2 (средние противники)
        1: ["Ничего", "Сумка"],  # Богатство 1
        2: ["Сумка", "Вещмешок", "Спортивный рюкзак"],  # Богатство 2
        3: ["Вещмешок", "Спортивный рюкзак", "Рюкзак"],  # Богатство 3
        4: ["Спортивный рюкзак", "Рюкзак", "Большой рюкзак"],  # Богатство 4
    },
    3: {  # Уровень 3 (сильные противники)
        1: ["Сумка", "Вещмешок"],  # Богатство 1
        2: ["Вещмешок", "Спортивный рюкзак", "Рюкзак"],  # Богатство 2
        3: ["Спортивный рюкзак", "Рюкзак", "Разгрузочный рюкзак"],  # Богатство 3
        4: ["Рюкзак", "Разгрузочный рюкзак", "Большой рюкзак"],  # Богатство 4
    },
    4: {  # Уровень 4 (элитные противники)
        1: ["Вещмешок", "Спортивный рюкзак"],  # Богатство 1
        2: ["Спортивный рюкзак", "Рюкзак", "Разгрузочный рюкзак"],  # Богатство 2
        3: ["Рюкзак", "Разгрузочный рюкзак", "Большой рюкзак"],  # Богатство 3
        4: ["Разгрузочный рюкзак", "Большой рюкзак", "БФРР"],  # Богатство 4
    }
}

class EnemyLoot:
    def __init__(self, enemy, enemy_generate_info):
        self.random = random.Random()
        self.enemy = enemy
        self.level = int(enemy_generate_info[1].split(".")[0])
        self.wealth = int(enemy_generate_info[2].split(".")[0])
        self.rag = self.generate_rag()
        self.headphones = self.generate_headphones()
        self.backpack = self.generate_backpack()
        self.loot = self.generate_loot()

    def generate_rag(self):
        return random.choice(opponent_rags.get(self.level).get(self.wealth))

    def generate_headphones(self):
        return random.choice(opponent_headphones.get(self.level).get(self.wealth))

    def generate_loot(self):
        enemy_meds = []
        enemy_food = []
        enemy_devices = random.choice(devices_table.get(self.level).get(self.wealth))
        enemy_misc = random.choice(opponent_misc_items.get(self.level).get(self.wealth))
        enemy_bullets = self.get_bullets()
        enemy_meds.append(self.get_meds())
        enemy_meds.append(self.get_meds())
        enemy_food.append(random.choice(food_table.get(self.level).get(self.wealth)))
        enemy_food.append(random.choice(food_table.get(self.level).get(self.wealth)))
        enemy_money = self.get_money()
        return [enemy_bullets, enemy_meds, enemy_food, enemy_devices, enemy_misc, enemy_money]

    def generate_backpack(self):
        return random.choice(opponent_backpacks.get(self.level).get(self.wealth))

    def get_meds(self):
        return random.choice(opponent_medicines.get(random.choice(med_table.get(self.level).get(self.wealth))))

    def get_bullets(self):
        return random.randint(int(self.enemy.weapon[1] / 3), int(self.enemy.weapon[1])) * self.wealth * self.level

    def get_money(self):
        return int(random.randint(500, 2500) * self.wealth * self.level / 4)