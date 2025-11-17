# -*- coding: utf-8 -*-
"""
事件系统
处理固定事件、条件事件和随机事件
"""

import random
from config import *


class EventSystem:
    """事件系统类"""
    
    def __init__(self, player):
        self.player = player
    
    def check_fixed_event(self, day):
        """检查是否有固定事件"""
        return FIXED_EVENTS.get(day, None)
    
    def check_condition_event(self, period):
        """Check condition events"""
        # Family care event
        if period == "Evening" and self.player.low_mood_days >= 3:
            return {
                "name": "Family Care",
                "description": "Your family called to check on you. Their concern warms your heart.",
                "options": [],
                "result": {"mood": 2}
            }
        return None
    
    def get_random_event(self, period):
        """获取随机事件"""
        if period not in RANDOM_EVENTS:
            return None
        
        events = RANDOM_EVENTS[period]
        
        # 根据心情调整事件权重
        mood = self.player.mood
        weights = []
        for event in events:
            if event["type"] == "好":
                weight = mood * 2  # 心情好更容易触发好事
            elif event["type"] == "坏":
                weight = (6 - mood) * 2  # 心情差更容易触发坏事
            else:
                weight = 5  # 中性事件固定权重
            weights.append(weight)
        
        # 随机选择事件
        event = random.choices(events, weights=weights)[0]
        return event.copy()
    
    def process_fixed_event(self, event, choice=None):
        """Process fixed event results"""
        results = {}
        
        if event["name"] == "Graduation Dinner":
            results["satiety"] = 50
            if self.player.mood >= 4:  # Happy or above
                results["satiety"] = 60
            results["message"] = "Had a great feast!"
        
        elif event["name"] == "Christmas Eve":
            if choice == "go_out":
                results["stamina"] = -20
                results["mood_set"] = 5  # Set to Ecstatic
                results["message"] = "Had a wonderful night with friends!"
            elif choice == "stay_home":
                results["stamina"] = 20
                results["message"] = "Had a good rest at home."
        
        return results
    
    def process_random_event(self, event, choice=None):
        """处理随机事件结果"""
        if not event.get("options"):
            # 无选项事件，直接返回结果
            return event.get("result", {})
        
        # 有选项的事件
        if choice and "results" in event:
            result_data = event["results"].get(choice)
            
            # 处理概率结果
            if isinstance(result_data, list):
                rand = random.random()
                cumulative = 0
                for outcome in result_data:
                    cumulative += outcome["probability"]
                    if rand <= cumulative:
                        return outcome["result"]
            else:
                return result_data
        
        return {}
    
    def apply_results(self, results):
        """Apply event results to player"""
        messages = []
        
        for key, value in results.items():
            if key == "stamina":
                self.player.update_stat("stamina", value, is_delta=True)
                if value > 0:
                    messages.append(f"Stamina +{value}")
                else:
                    messages.append(f"Stamina {value}")
            
            elif key == "mood":
                old_mood = self.player.get_mood_text()
                self.player.change_mood(value)
                new_mood = self.player.get_mood_text()
                if old_mood != new_mood:
                    messages.append(f"Mood: {old_mood} -> {new_mood}")
            
            elif key == "mood_set":
                old_mood = self.player.get_mood_text()
                self.player.update_stat("mood", value, is_delta=False)
                new_mood = self.player.get_mood_text()
                messages.append(f"Mood: {old_mood} -> {new_mood}")
            
            elif key == "health":
                self.player.update_stat("health", value, is_delta=True)
                if value > 0:
                    messages.append(f"Health +{value}")
                else:
                    messages.append(f"Health {value}")
            
            elif key == "satiety":
                self.player.update_stat("satiety", value, is_delta=True)
                if value > 0:
                    messages.append(f"Satiety +{value}")
            
            elif key == "money":
                self.player.update_stat("money", value, is_delta=True)
                if value > 0:
                    messages.append(f"Money +${value}")
                else:
                    messages.append(f"Money -${abs(value)}")
            
            elif key == "item":
                self.player.add_item(value, 1)
                messages.append(f"Obtained: {value}")
            
            elif key == "message":
                messages.append(value)
        
        return messages
