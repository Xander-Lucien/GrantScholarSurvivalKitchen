# -*- coding: utf-8 -*-
"""
游戏配置文件
包含游戏常量、事件数据、食材数据等
"""

# Window Settings
WINDOW_WIDTH = 1024
WINDOW_HEIGHT = 768
FPS = 60
TITLE = "Grant Scholar's Survival Kitchen"

# 颜色定义
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)
LIGHT_GRAY = (200, 200, 200)
RED = (220, 50, 50)
GREEN = (50, 200, 50)
BLUE = (50, 100, 200)
YELLOW = (255, 215, 0)
ORANGE = (255, 165, 0)

# 属性范围
STAT_MIN = 0
STAT_MAX = 100
INITIAL_MONEY = 1500

# Mood Levels
MOOD_LEVELS = {
    5: "Ecstatic",
    4: "Happy",
    3: "Calm",
    2: "Depressed",
    1: "Desperate"
}

# 游戏时间设置
GAME_DAYS = 30
START_YEAR = 2025
START_MONTH = 12
START_DAY = 2  # 12月2日开始，到12月31日结束

# Time Periods
TIME_PERIODS = [
    "Morning",    # 0
    "Daytime",    # 1
    "Shopping",   # 2
    "Cooking",    # 3
    "Evening",    # 4
    "Sleep"       # 5
]

# Fixed Events
FIXED_EVENTS = {
    12: {  # Dec 12
        "name": "Graduation Dinner",
        "period": "Daytime",
        "description": "Today is the graduation dinner organized by the department. Everyone is happy!",
        "options": [],
        "auto_result": True
    },
    24: {  # Dec 24
        "name": "Christmas Eve",
        "period": "Daytime",
        "description": "It's Christmas Eve! Do you want to go out with friends to celebrate?",
        "options": [
            {"text": "Go out with friends", "id": "go_out"},
            {"text": "Stay home", "id": "stay_home"}
        ],
        "auto_result": False
    }
}

# Random Events
RANDOM_EVENTS = {
    "Morning": [
        {
            "name": "Overslept",
            "type": "bad",
            "description": "Oh no! Your alarm didn't go off and you overslept!",
            "options": [],
            "result": {"stamina": -10, "mood": -1}
        },
        {
            "name": "Sweet Dream",
            "type": "good",
            "description": "You had a wonderful dream. You feel refreshed!",
            "options": [],
            "result": {"stamina": 5, "mood": 1}
        },
        {
            "name": "Normal Morning",
            "type": "neutral",
            "description": "Just another ordinary day.",
            "options": [],
            "result": {}
        }
    ],
    "Daytime": [
        {
            "name": "Storm Warning",
            "type": "neutral",
            "description": "Typhoon signal No.8 issued! Heavy rain and strong winds outside.",
            "options": [
                {"text": "Lock doors and windows", "id": "lock"},
                {"text": "Go outside", "id": "go_out"}
            ],
            "results": {
                "lock": {"stamina": -10, "mood": 1},
                "go_out": [
                    {"probability": 0.3, "result": {"money": -10, "item": "Bento A"}},
                    {"probability": 0.7, "result": {"stamina": -20, "health": -5, "mood": -1}}
                ]
            }
        },
        {
            "name": "Supervisor Meeting",
            "type": "bad",
            "description": "Your supervisor wants to talk about your thesis progress...",
            "options": [],
            "result": {"stamina": -15, "mood": -1}
        },
        {
            "name": "Package Delivery",
            "type": "good",
            "description": "You received an unexpected package! Snacks from a friend.",
            "options": [],
            "result": {"mood": 1, "satiety": 10}
        }
    ],
    "Evening": [
        {
            "name": "Watch Movie",
            "type": "good",
            "description": "You watched a great movie online. Feeling good!",
            "options": [],
            "result": {"mood": 1, "stamina": -5}
        },
        {
            "name": "Thesis Anxiety",
            "type": "bad",
            "description": "Suddenly remembered how much work is left on your thesis...",
            "options": [],
            "result": {"mood": -1}
        }
    ]
}

# Ingredients
INGREDIENTS = {
    "Instant Noodles": {
        "price": 5,
        "location": "Market",
        "shelf_life": 30,
        "description": "Cheap instant food"
    },
    "Egg": {
        "price": 2,
        "location": "Market",
        "shelf_life": 7,
        "description": "Fresh eggs"
    },
    "Tomato": {
        "price": 4,
        "location": "Market",
        "shelf_life": 5,
        "description": "Red tomatoes"
    },
    "Rice": {
        "price": 3,
        "location": "Market",
        "shelf_life": 30,
        "description": "Cooked rice"
    },
    "Pork": {
        "price": 15,
        "location": "Market",
        "shelf_life": 3,
        "description": "Fresh pork"
    },
    "Bento A": {
        "price": 20,
        "location": "Convenience Store",
        "shelf_life": 3,
        "description": "Regular bento"
    },
    "Bento B": {
        "price": 30,
        "location": "Convenience Store",
        "shelf_life": 3,
        "description": "Deluxe bento"
    }
}

# Recipes
RECIPES = {
    "Boiled Noodles": {
        "ingredients": {"Instant Noodles": 1},
        "effects": {"satiety": 30},
        "stamina_cost": 5,
        "description": "Quick and simple"
    },
    "Noodles with Egg": {
        "ingredients": {"Instant Noodles": 1, "Egg": 1},
        "effects": {"satiety": 40, "health": 3},
        "stamina_cost": 8,
        "description": "More nutritious with egg"
    },
    "Tomato Scrambled Eggs": {
        "ingredients": {"Tomato": 1, "Egg": 1},
        "effects": {"satiety": 35, "mood": 1, "health": 5},
        "stamina_cost": 12,
        "description": "Classic home cooking"
    },
    "Clay Pot Rice": {
        "ingredients": {"Rice": 1, "Pork": 1},
        "effects": {"satiety": 50, "mood": 1, "health": 3},
        "stamina_cost": 15,
        "description": "Fragrant clay pot rice"
    },
    "Eat Bento A": {
        "ingredients": {"Bento A": 1},
        "effects": {"satiety": 30, "health": 3},
        "stamina_cost": 2,
        "description": "Ready to eat"
    },
    "Eat Bento B": {
        "ingredients": {"Bento B": 1},
        "effects": {"satiety": 40, "health": 4},
        "stamina_cost": 2,
        "description": "Deluxe ready-to-eat"
    }
}

# Restaurant Menu
RESTAURANT_MENU = {
    "Roast Goose Rice": {
        "price": 40,
        "effects": {"satiety": 50, "mood": 2, "health": 5},
        "description": "Delicious roast goose rice"
    }
}

# 每日饱腹度下降速率（每个时间段）
SATIETY_DECAY_RATE = 8

# Sleep Stamina Recovery
SLEEP_STAMINA_RECOVERY = {
    "Early Sleep": 60,
    "Normal Sleep": 50,
    "Stay Up Late": 30
}
