# -*- coding: utf-8 -*-
"""
Configuration constants
Loads from JSON and provides convenient access
"""

from .data_loader import data_loader


# Window settings
WINDOW_WIDTH = data_loader.get("config", "window", "width", default=1024)
WINDOW_HEIGHT = data_loader.get("config", "window", "height", default=768)
FPS = data_loader.get("config", "window", "fps", default=60)
TITLE = data_loader.get("config", "window", "title", default="Grant Scholar's Survival Kitchen")

# Colors
def get_color(name):
    """Get color tuple from configuration"""
    color = data_loader.get("config", "colors", name, default=[255, 255, 255])
    return tuple(color)

WHITE = get_color("white")
BLACK = get_color("black")
GRAY = get_color("gray")
LIGHT_GRAY = get_color("light_gray")
RED = get_color("red")
GREEN = get_color("green")
BLUE = get_color("blue")
YELLOW = get_color("yellow")
ORANGE = get_color("orange")

# Game settings
GAME_DAYS = data_loader.get("config", "game", "total_days", default=30)
START_YEAR = data_loader.get("config", "game", "start_year", default=2025)
START_MONTH = data_loader.get("config", "game", "start_month", default=12)
START_DAY = data_loader.get("config", "game", "start_day", default=2)
TIME_PERIODS = data_loader.get("config", "game", "time_periods", default=[])

# Stat settings
STAT_MIN = data_loader.get("stats", "stat_ranges", "min", default=0)
STAT_MAX = data_loader.get("stats", "stat_ranges", "max", default=100)
INITIAL_MONEY = data_loader.get("stats", "initial_values", "money", default=1500)

# Data access helpers
def get_ingredients():
    """Get all ingredients data"""
    return data_loader.get_all("items").get("ingredients", {})

def get_restaurant_menu():
    """Get restaurant menu"""
    return data_loader.get_all("items").get("restaurant_menu", {})

def get_recipes():
    """Get all recipes"""
    return data_loader.get_all("recipes").get("recipes", {})

def get_fixed_events():
    """Get fixed events"""
    return data_loader.get_all("events").get("fixed_events", {})

def get_random_events():
    """Get random events"""
    return data_loader.get_all("events").get("random_events", {})

def get_condition_events():
    """Get condition events"""
    return data_loader.get_all("events").get("condition_events", {})

def get_intro_events():
    """Get intro events"""
    return data_loader.get_all("events").get("intro_events", {})
