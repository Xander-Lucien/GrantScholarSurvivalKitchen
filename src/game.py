# -*- coding: utf-8 -*-
"""
Game main control class
Manages game flow, time period switching, scene switching
"""

import pygame
import sys
from .config import *
from .player import Player
from .events import EventSystem
from .scenes import MainScene, ShoppingScene, KitchenScene, StoryScene


class Game:
    """Game main class"""
    
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        self.running = True
        
        # Initialize game objects
        self.player = Player()
        self.event_system = EventSystem(self.player)
        
        # Scenes
        self.main_scene = MainScene(self)
        self.shopping_scene = ShoppingScene(self)
        self.kitchen_scene = KitchenScene(self)
        self.story_scene = StoryScene(self)
        self.current_scene = self.main_scene
        self.previous_scene = None
        
        # Game state
        self.current_period = 0
        self.game_state = "playing"  # playing/win/lose
        
        # Start game
        self.start_new_day()
    
    def start_new_day(self, data=None):
        """Start new day"""
        self.current_period = 0
        
        # Check expired items
        expired = self.player.check_expired_items()
        if expired:
            expired_text = ", ".join(expired)
            self.show_message(f"Expired items discarded: {expired_text}")
        
        # Morning period
        self.process_morning()
    
    def process_morning(self, data=None):
        """Process morning period"""
        # Decay satiety
        self.player.decay_satiety()
        
        # Generate status summary
        warnings = self.player.get_status_summary()
        warning_text = ", ".join(warnings) if warnings else "All stats OK"
        
        date_text = f"{START_MONTH}/{START_DAY + self.player.current_day - 1}/{START_YEAR}"
        summary = f"{date_text}\nDay {self.player.current_day}, {GAME_DAYS - self.player.current_day + 1} days until graduation.\n{warning_text}"
        
        # Trigger morning random event
        event = self.event_system.get_random_event("Morning")
        if event:
            self.show_event(event, summary)
        else:
            self.show_message(summary, [{"text": "Continue", "callback": self.next_period}])
    
    def process_daytime(self, data=None):
        """Process daytime period"""
        # Decay satiety
        self.player.decay_satiety()
        
        # Check fixed events
        day_of_month = START_DAY + self.player.current_day - 1
        fixed_event = self.event_system.check_fixed_event(day_of_month)
        
        if fixed_event:
            self.show_fixed_event(fixed_event)
        else:
            # Trigger random event
            event = self.event_system.get_random_event("Daytime")
            if event:
                self.show_event(event)
            else:
                self.show_message("A peaceful day...", [{"text": "Continue", "callback": self.next_period}])
    
    def process_shopping(self, data=None):
        """Process shopping period"""
        self.player.decay_satiety()
        
        text = "Shopping Time: Where do you want to buy food?"
        buttons = [
            {"text": "Market", "callback": self.go_shopping, "data": "Market"},
            {"text": "Convenience Store", "callback": self.go_shopping, "data": "Convenience Store"},
            {"text": "Restaurant", "callback": self.go_shopping, "data": "Restaurant"},
            {"text": "Skip Shopping", "callback": self.next_period}
        ]
        self.main_scene.set_content(text, buttons)
        self.current_scene = self.main_scene
    
    def process_cooking(self, data=None):
        """Process cooking period"""
        self.player.decay_satiety()
        
        # Switch to kitchen scene
        self.current_scene = self.kitchen_scene
    
    def process_night(self, data=None):
        """Process evening period"""
        self.player.decay_satiety()
        
        # Check condition events
        condition_event = self.event_system.check_condition_event("Evening")
        if condition_event:
            self.show_event(condition_event)
            return
        
        # Choose evening activity
        text = "Evening: What do you want to do tonight?"
        buttons = [
            {"text": "Sleep Early", "callback": self.go_sleep, "data": "Early Sleep"},
            {"text": "Relax", "callback": self.night_activity, "data": "Normal Sleep"},
            {"text": "Stay Up Late", "callback": self.night_activity, "data": "Stay Up Late"}
        ]
        self.main_scene.set_content(text, buttons)
        self.current_scene = self.main_scene
    
    def night_activity(self, activity_type):
        """Evening activity"""
        # Trigger evening random event
        event = self.event_system.get_random_event("Evening")
        if event:
            # Process event then sleep
            results = self.event_system.process_random_event(event)
            messages = self.event_system.apply_results(results)
            
            event_text = event["description"] + "\n\n" + "\n".join(messages)
            
            # Check for story pages
            if "story_pages" in results:
                self.play_story(results["story_pages"], 
                              lambda: self.show_message(event_text, [{"text": "Sleep", "callback": self.go_sleep, "data": activity_type}]))
            else:
                self.show_message(event_text, [{"text": "Sleep", "callback": self.go_sleep, "data": activity_type}])
        else:
            self.go_sleep(activity_type)
    
    def go_sleep(self, sleep_type):
        """Go to sleep"""
        # Check stamina
        if self.player.stamina <= 0:
            self.player.force_sleep()
            text = "Stamina depleted! You passed out..."
        else:
            self.player.sleep(sleep_type)
            text = f"Good night! ({sleep_type})"
        
        # Check game end conditions
        if not self.player.is_alive():
            self.game_over(False)
            return
        
        if self.player.current_day > GAME_DAYS:
            self.game_over(True)
            return
        
        # Start new day
        self.show_message(text, [{"text": "New Day", "callback": self.start_new_day}])
    
    def go_shopping(self, location):
        """Go shopping"""
        self.shopping_scene.set_location(location)
        self.current_scene = self.shopping_scene
    
    def show_event(self, event, prefix_text=""):
        """Show event"""
        text = prefix_text + "\n\n" + event["description"] if prefix_text else event["description"]
        
        if event.get("options"):
            # Event with options
            buttons = []
            for option in event["options"]:
                buttons.append({
                    "text": option["text"],
                    "callback": self.handle_event_choice,
                    "data": {"event": event, "choice": option["id"]}
                })
            self.main_scene.set_content(text, buttons, event)
        else:
            # Auto-process event
            results = self.event_system.process_random_event(event)
            messages = self.event_system.apply_results(results)
            result_text = text + "\n\n" + "\n".join(messages)
            
            # Check for story pages
            if "story_pages" in results:
                self.play_story(results["story_pages"], 
                              lambda: self.show_message(result_text, [{"text": "Continue", "callback": self.next_period}]))
            else:
                self.show_message(result_text, [{"text": "Continue", "callback": self.next_period}])
        
        self.current_scene = self.main_scene
    
    def show_fixed_event(self, event):
        """Show fixed event"""
        if event.get("auto_result"):
            # Auto-process result
            results = self.event_system.process_fixed_event(event)
            messages = self.event_system.apply_results(results)
            text = event["description"] + "\n\n" + "\n".join(messages)
            
            # Check for story pages
            if "story_pages" in results:
                self.play_story(results["story_pages"], 
                              lambda: self.show_message(text, [{"text": "Continue", "callback": self.next_period}]))
            else:
                self.show_message(text, [{"text": "Continue", "callback": self.next_period}])
        else:
            # Need to choose
            buttons = []
            for option in event["options"]:
                buttons.append({
                    "text": option["text"],
                    "callback": self.handle_fixed_event_choice,
                    "data": {"event": event, "choice": option["id"]}
                })
            self.main_scene.set_content(event["description"], buttons)
        
        self.current_scene = self.main_scene
    
    def handle_event_choice(self, data):
        """Handle event choice"""
        event = data["event"]
        choice = data["choice"]
        
        results = self.event_system.process_random_event(event, choice)
        messages = self.event_system.apply_results(results)
        
        result_text = "\n".join(messages)
        
        # Check for story pages
        if "story_pages" in results:
            self.play_story(results["story_pages"], 
                          lambda: self.show_message(result_text, [{"text": "Continue", "callback": self.next_period}]))
        else:
            self.show_message(result_text, [{"text": "Continue", "callback": self.next_period}])
    
    def handle_fixed_event_choice(self, data):
        """Handle fixed event choice"""
        event = data["event"]
        choice = data["choice"]
        
        results = self.event_system.process_fixed_event(event, choice)
        messages = self.event_system.apply_results(results)
        
        result_text = "\n".join(messages)
        
        # Check for story pages
        if "story_pages" in results:
            self.play_story(results["story_pages"], 
                          lambda: self.show_message(result_text, [{"text": "Continue", "callback": self.next_period}]))
        else:
            self.show_message(result_text, [{"text": "Continue", "callback": self.next_period}])
    
    def show_message(self, text, buttons=None):
        """Show message"""
        if buttons is None:
            buttons = [{"text": "OK", "callback": self.next_period}]
        self.main_scene.set_content(text, buttons)
        self.current_scene = self.main_scene
    
    def next_period(self, data=None):
        """Enter next time period"""
        self.current_period += 1
        
        if self.current_period >= len(TIME_PERIODS):
            self.current_period = 0
            self.start_new_day()
            return
        
        period_name = TIME_PERIODS[self.current_period]
        
        if period_name == "Morning":
            self.process_morning()
        elif period_name == "Daytime":
            self.process_daytime()
        elif period_name == "Shopping":
            self.process_shopping()
        elif period_name == "Cooking":
            self.process_cooking()
        elif period_name == "Evening":
            self.process_night()
    
    def game_over(self, win):
        """Game over"""
        self.game_state = "win" if win else "lose"
        
        if win:
            text = f"Congratulations! You survived {GAME_DAYS} days and graduated!\n\n"
            text += f"Final Money: ${self.player.money}\n"
            text += f"Final Health: {int(self.player.health)}\n"
            text += f"Final Mood: {self.player.get_mood_text()}"
        else:
            text = "Game Over! Your health reached zero...\n\n"
            text += f"Survived: {self.player.current_day - 1}/{GAME_DAYS} days"
        
        self.show_message(text, [{"text": "Quit Game", "callback": self.quit_game}])
    
    def quit_game(self, data=None):
        """Quit game"""
        self.running = False
    
    def handle_events(self):
        """Handle events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            
            # Scene event handling
            result = self.current_scene.handle_event(event)
            
            # Handle shopping scene return
            if isinstance(result, str) and result == "back":
                if self.current_scene == self.shopping_scene:
                    self.process_shopping()
                elif self.current_scene == self.kitchen_scene:
                    self.next_period()
            
            # Handle shopping result
            elif isinstance(result, dict):
                if self.current_scene == self.shopping_scene:
                    if result.get("result") == "success":
                        location = result.get("location")
                        cost = result.get("cost")
                        if location == "Restaurant":
                            text = f"Spent ${cost}, had a great meal!"
                            self.show_message(text, [{"text": "Continue", "callback": self.next_period}])
                        else:
                            text = f"Purchase successful! Spent ${cost}"
                            self.show_message(text, [{"text": "Continue", "callback": self.process_shopping}])
                    elif result.get("result") == "insufficient_money":
                        self.show_message("Insufficient money!", [{"text": "Back", "callback": self.process_shopping}])
                
                elif self.current_scene == self.kitchen_scene:
                    if result.get("result") == "success":
                        recipe = result.get("recipe")
                        text = f"Successfully cooked {recipe}!"
                        self.show_message(text, [{"text": "Cook More", "callback": self.process_cooking},
                                                {"text": "Finish Cooking", "callback": self.next_period}])
                    elif result.get("result") == "failed":
                        reason = result.get("reason")
                        self.show_message(f"Cannot cook: {reason}", 
                                        [{"text": "Back", "callback": self.process_cooking}])
    
    def update(self):
        """Update game"""
        self.current_scene.update()
    
    def draw(self):
        """Draw game"""
        self.current_scene.draw(self.screen)
        pygame.display.flip()
    
    def play_story(self, pages, on_finish=None):
        """Play story"""
        self.previous_scene = self.current_scene
        self.story_scene.set_story(pages, on_finish)
        self.current_scene = self.story_scene
        
    def return_from_story(self):
        """Return from story scene"""
        if self.previous_scene:
            self.current_scene = self.previous_scene
            self.previous_scene = None
    
    def run(self):
        """Run game main loop"""
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)
        
        pygame.quit()
        sys.exit()
