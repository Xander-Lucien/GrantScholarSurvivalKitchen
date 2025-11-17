# -*- coding: utf-8 -*-
"""
玩家类
管理玩家的所有属性和状态
"""

from config import *


class Player:
    """玩家类，管理所有属性"""
    
    def __init__(self):
        # 基础属性
        self.stamina = 100  # 体力
        self.mood = 3  # 心情（1-5）
        self.health = 100  # 健康
        self.satiety = 80  # 饱腹度
        self.money = INITIAL_MONEY  # 金钱
        
        # 库存
        self.inventory = {}  # {食材名: {"count": 数量, "buy_day": 购买天数}}
        
        # 游戏状态
        self.current_day = 1  # 当前天数
        self.low_mood_days = 0  # 连续低心情天数
        
    def update_stat(self, stat_name, value, is_delta=True):
        """更新属性值
        
        Args:
            stat_name: 属性名称
            value: 变化值或绝对值
            is_delta: True表示增减，False表示设置绝对值
        """
        if is_delta:
            setattr(self, stat_name, getattr(self, stat_name) + value)
        else:
            setattr(self, stat_name, value)
        
        # 限制范围
        if stat_name in ["stamina", "health", "satiety"]:
            current = getattr(self, stat_name)
            setattr(self, stat_name, max(STAT_MIN, min(STAT_MAX, current)))
        elif stat_name == "mood":
            self.mood = max(1, min(5, self.mood))
        elif stat_name == "money":
            self.money = max(0, self.money)
    
    def change_mood(self, delta):
        """改变心情等级"""
        self.update_stat("mood", delta, is_delta=True)
    
    def add_item(self, item_name, count=1):
        """添加物品到库存"""
        if item_name in self.inventory:
            self.inventory[item_name]["count"] += count
        else:
            self.inventory[item_name] = {
                "count": count,
                "buy_day": self.current_day
            }
    
    def remove_item(self, item_name, count=1):
        """从库存移除物品"""
        if item_name in self.inventory:
            self.inventory[item_name]["count"] -= count
            if self.inventory[item_name]["count"] <= 0:
                del self.inventory[item_name]
            return True
        return False
    
    def has_item(self, item_name, count=1):
        """检查是否有足够的物品"""
        if item_name in self.inventory:
            return self.inventory[item_name]["count"] >= count
        return False
    
    def check_expired_items(self):
        """检查并移除过期食材"""
        expired = []
        for item_name, data in list(self.inventory.items()):
            if item_name in INGREDIENTS:
                shelf_life = INGREDIENTS[item_name]["shelf_life"]
                days_passed = self.current_day - data["buy_day"]
                if days_passed > shelf_life:
                    expired.append(item_name)
                    del self.inventory[item_name]
        return expired
    
    def decay_satiety(self):
        """饱腹度随时间下降"""
        self.update_stat("satiety", -SATIETY_DECAY_RATE, is_delta=True)
        
        # 如果饱腹度为0，健康值下降
        if self.satiety <= 0:
            self.update_stat("health", -5, is_delta=True)
    
    def check_mood_streak(self):
        """检查连续低心情天数"""
        if self.mood <= 2:
            self.low_mood_days += 1
        else:
            self.low_mood_days = 0
    
    def is_alive(self):
        """检查玩家是否存活"""
        return self.health > 0
    
    def force_sleep(self):
        """体力耗尽强制昏睡"""
        self.stamina = 30  # 恢复少量体力
        self.update_stat("mood", -1, is_delta=True)
        self.update_stat("health", -10, is_delta=True)
    
    def sleep(self, sleep_type="消磨时间"):
        """睡觉恢复体力"""
        recovery = SLEEP_STAMINA_RECOVERY.get(sleep_type, 50)
        self.update_stat("stamina", recovery, is_delta=True)
        self.current_day += 1
        self.check_mood_streak()
    
    def get_mood_text(self):
        """获取心情文字描述"""
        return MOOD_LEVELS.get(self.mood, "未知")
    
    def get_status_summary(self):
        """Get status summary"""
        warnings = []
        if self.stamina < 30:
            warnings.append("Low Stamina")
        if self.health < 40:
            warnings.append("Poor Health")
        if self.satiety < 30:
            warnings.append("Very Hungry")
        if self.money < 100:
            warnings.append("Low Budget")
        if self.mood <= 2:
            warnings.append("Bad Mood")
        
        return warnings
