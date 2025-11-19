# -*- coding: utf-8 -*-
"""
Player class
Manages all player attributes and state
"""

from .data_loader import data_loader


class Player:
    """Player class managing all attributes"""
    
    def __init__(self):
        # Load initial values from configuration
        initial = data_loader.get("stats", "initial_values", default={})
        stat_range = data_loader.get("stats", "stat_ranges", default={})
        
        # Basic attributes
        self.stamina = initial.get("stamina", 100)
        self.mood = initial.get("mood", 3)
        self.health = initial.get("health", 100)
        self.satiety = initial.get("satiety", 80)
        self.money = initial.get("money", 1500)
        
        # Stat ranges
        self.stat_min = stat_range.get("min", 0)
        self.stat_max = stat_range.get("max", 100)
        
        # Inventory
        self.inventory = {}  # {item_name: {"count": count, "buy_day": day}}
        
        # Game state
        self.current_day = 1
        self.low_mood_days = 0
        
    def update_stat(self, stat_name, value, is_delta=True):
        """Update attribute value"""
        if is_delta:
            setattr(self, stat_name, getattr(self, stat_name) + value)
        else:
            setattr(self, stat_name, value)
        
        # Limit ranges
        if stat_name in ["stamina", "health", "satiety"]:
            current = getattr(self, stat_name)
            setattr(self, stat_name, max(self.stat_min, min(self.stat_max, current)))
        elif stat_name == "mood":
            self.mood = max(1, min(5, self.mood))
        elif stat_name == "money":
            self.money = max(0, self.money)
    
    def change_mood(self, delta):
        """Change mood level"""
        self.update_stat("mood", delta, is_delta=True)
    
    def add_item(self, item_name, count=1):
        """Add item to inventory"""
        if item_name in self.inventory:
            self.inventory[item_name]["count"] += count
        else:
            self.inventory[item_name] = {
                "count": count,
                "buy_day": self.current_day
            }
    
    def remove_item(self, item_name, count=1):
        """Remove item from inventory"""
        if item_name in self.inventory:
            self.inventory[item_name]["count"] -= count
            if self.inventory[item_name]["count"] <= 0:
                del self.inventory[item_name]
            return True
        return False
    
    def has_item(self, item_name, count=1):
        """Check if has enough items"""
        if item_name in self.inventory:
            return self.inventory[item_name]["count"] >= count
        return False
    
    def check_expired_items(self):
        """Check and remove expired items"""
        items_data = data_loader.get("items", "ingredients", default={})
        expired = []
        
        for item_name, data in list(self.inventory.items()):
            if item_name in items_data:
                shelf_life = items_data[item_name].get("shelf_life", 30)
                days_passed = self.current_day - data["buy_day"]
                if days_passed > shelf_life:
                    expired.append(item_name)
                    del self.inventory[item_name]
        
        return expired
    
    def decay_satiety(self):
        """Satiety decreases over time"""
        decay_rate = data_loader.get("config", "game", "satiety_decay_rate", default=8)
        self.update_stat("satiety", -decay_rate, is_delta=True)
        
        # If satiety is 0, health decreases
        if self.satiety <= 0:
            self.update_stat("health", -5, is_delta=True)
    
    def check_mood_streak(self):
        """Check consecutive low mood days"""
        if self.mood <= 2:
            self.low_mood_days += 1
        else:
            self.low_mood_days = 0
    
    def is_alive(self):
        """Check if player is alive"""
        return self.health > 0
    
    def force_sleep(self):
        """Forced sleep when stamina depleted"""
        self.stamina = 30
        self.update_stat("mood", -1, is_delta=True)
        self.update_stat("health", -10, is_delta=True)
    
    def sleep(self, sleep_type="Normal Sleep"):
        """Sleep to recover stamina"""
        sleep_recovery = data_loader.get("stats", "sleep_recovery", default={})
        recovery = sleep_recovery.get(sleep_type, 50)
        self.update_stat("stamina", recovery, is_delta=True)
        self.current_day += 1
        self.check_mood_streak()
    
    def get_mood_text(self):
        """Get mood text description"""
        mood_levels = data_loader.get("stats", "mood_levels", default={})
        return mood_levels.get(str(self.mood), "Unknown")
    
    def get_status_summary(self):
        """Get status summary"""
        thresholds = data_loader.get("stats", "warning_thresholds", default={})
        warnings = []
        
        if self.stamina < thresholds.get("stamina_low", 30):
            warnings.append("Low Stamina")
        if self.health < thresholds.get("health_low", 40):
            warnings.append("Poor Health")
        if self.satiety < thresholds.get("satiety_low", 30):
            warnings.append("Very Hungry")
        if self.money < thresholds.get("money_low", 100):
            warnings.append("Low Budget")
        if self.mood <= thresholds.get("mood_low", 2):
            warnings.append("Bad Mood")
        
        return warnings
