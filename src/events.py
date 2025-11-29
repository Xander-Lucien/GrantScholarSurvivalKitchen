# -*- coding: utf-8 -*-
"""
Event system
Handles fixed events, condition events and random events
"""

import random
from .config import get_fixed_events, get_random_events, get_condition_events, get_intro_events


class EventSystem:
    """Event system class"""
    
    def __init__(self, player):
        self.player = player
    
    def check_fixed_event(self, day):
        """Check if there's a fixed event"""
        fixed_events = get_fixed_events()
        return fixed_events.get(str(day), None)
    
    def check_condition_event(self, period):
        """Check condition events"""
        condition_events = get_condition_events()
        
        # Family care event
        family_care = condition_events.get("family_care", {})
        if period == "Evening" and self.player.low_mood_days >= 3:
            return {
                "name": family_care.get("name", "Family Care"),
                "description": family_care.get("description", ""),
                "options": family_care.get("options", []),
                "result": family_care.get("result", {})
            }
        return None
    
    def get_intro_event(self):
        """Get intro event"""
        intro_events = get_intro_events()
        return intro_events.get("diary", None)
    
    def get_random_event(self, period):
        """Get random event"""
        random_events = get_random_events()
        events = random_events.get(period, [])
        
        if not events:
            return None
        
        # Adjust event weights based on mood
        mood = self.player.mood
        weights = []
        for event in events:
            event_type = event.get("type", "neutral")
            if event_type == "good":
                weight = mood * 2  # Higher mood = more good events
            elif event_type == "bad":
                weight = (6 - mood) * 2  # Lower mood = more bad events
            else:
                weight = 5  # Neutral events fixed weight
            weights.append(weight)
        
        # Randomly select event
        event = random.choices(events, weights=weights)[0]
        return event.copy()
    
    def process_fixed_event(self, event, choice=None):
        """Process fixed event results"""
        results = {}
        event_name = event.get("name", "")
        event_results = event.get("results", {})
        
        if event_name == "Graduation Dinner":
            base_result = event_results.get("base", {})
            results.update(base_result)
            
            # Check mood bonus
            mood_bonus = event_results.get("mood_bonus", {})
            if self.player.mood >= 4:
                results["satiety"] = results.get("satiety", 0) + mood_bonus.get("satiety", 0)
        
        elif event_name == "Christmas Eve":
            if choice in event_results:
                results = event_results[choice].copy()
        
        return results
    
    def process_random_event(self, event, choice=None):
        """Process random event results"""
        if not event.get("options"):
            # No options event, return result directly
            return event.get("result", {})
        
        # Event with options
        if choice and "results" in event:
            result_data = event["results"].get(choice)
            
            # Handle probability results
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
