# -*- coding: utf-8 -*-
"""
Scene system
Contains regular scene, shopping scene, kitchen scene
"""

import pygame
from .config import *
from .ui import *
from .backgrounds import *


class Scene:
    """Scene base class"""
    
    def __init__(self, game):
        self.game = game
        self.player = game.player
    
    def handle_event(self, event):
        """Handle events"""
        pass
    
    def update(self):
        """Update scene"""
        pass
    
    def draw(self, surface):
        """Draw scene"""
        pass


class MainScene(Scene):
    """Main scene / Regular scene"""
    
    def __init__(self, game):
        super().__init__(game)
        self.status_bars = self._create_status_bars()
        
        # 创建心情和金钱徽章
        self.mood_badge = InfoBadge(20, 20 + 45 * 3, 250, 35, "Mood", 
                                  self.player.get_mood_text(), color=(147, 112, 219), icon_text="Mood")
        self.money_badge = InfoBadge(20, 20 + 45 * 4, 250, 35, "Money", 
                                   f"${self.player.money}", color=(218, 165, 32), icon_text="$")
                                   
        # 对话框移到界面下方，增加高度以容纳更多文本
        self.text_box = TextBox(50, WINDOW_HEIGHT - 310, WINDOW_WIDTH - 100, 240, "", 
                              font_size=22, bg_color=(20, 20, 35, 230))
        self.buttons = []
        self.current_text = ""
        self.event_data = None
    
    def _create_status_bars(self):
        """Create status bars"""
        # 五种属性移到左上角垂直排布
        bars = []
        x_pos = 20  # 左侧位置
        y_start = 20  # 起始Y坐标
        bar_width = 250  # 状态栏宽度
        bar_height = 35  # 状态栏高度
        spacing = 45  # 垂直间距
        
        # 体力 (绿色)
        bars.append(StatusBar(x_pos, y_start, bar_width, bar_height, 
                              "Stamina", self.player.stamina, STAT_MAX, 
                              bar_color=(50, 205, 50), icon_text="HP"))
        # 健康 (红色)
        bars.append(StatusBar(x_pos, y_start + spacing, bar_width, bar_height, 
                              "Health", self.player.health, STAT_MAX, 
                              bar_color=(255, 80, 80), icon_text="HT"))
        # 饱腹 (橙色)
        bars.append(StatusBar(x_pos, y_start + spacing * 2, bar_width, bar_height, 
                              "Satiety", self.player.satiety, STAT_MAX, 
                              bar_color=(255, 165, 0), icon_text="FD"))
        
        return bars
    
    def set_content(self, text, buttons_data=None, event_data=None):
        """Set scene content"""
        self.current_text = text
        self.text_box.set_text(text)
        self.event_data = event_data
        
        # Create buttons - 按钮放在对话框上方
        self.buttons = []
        if buttons_data:
            button_width = 200
            button_height = 50
            x_start = (WINDOW_WIDTH - button_width * len(buttons_data) - 20 * (len(buttons_data) - 1)) // 2
            y_pos = WINDOW_HEIGHT - 370  # 在对话框上方
            
            for i, btn_data in enumerate(buttons_data):
                x = x_start + i * (button_width + 20)
                button = Button(x, y_pos, button_width, button_height, 
                              btn_data["text"], font_size=28)
                button.callback = btn_data.get("callback")
                button.data = btn_data.get("data")
                self.buttons.append(button)
    
    def handle_event(self, event):
        """Handle events"""
        for button in self.buttons:
            if button.handle_event(event):
                if button.callback:
                    button.callback(button.data)
                return True
        return False
    
    def update(self):
        """Update status bars"""
        self.status_bars[0].update(self.player.stamina)
        self.status_bars[1].update(self.player.health)
        self.status_bars[2].update(self.player.satiety)
        
        # 更新徽章
        self.mood_badge.update(self.player.get_mood_text())
        self.money_badge.update(f"${self.player.money}")
    
    def draw(self, surface):
        """Draw scene"""
        surface.fill(WHITE)
        
        # 绘制全屏像素背景
        draw_room_background(surface, 0, 0, WINDOW_WIDTH, WINDOW_HEIGHT)
        
        # Draw status bars (左上角垂直排布)
        for bar in self.status_bars:
            bar.draw(surface)
        
        # Draw mood and money badges
        self.mood_badge.draw(surface)
        self.money_badge.draw(surface)
        
        # Draw day counter (右上角)
        day_text = f"Day {self.player.current_day}/{GAME_DAYS}"
        draw_text(surface, day_text, WINDOW_WIDTH - 150, 20, 28, RED)
        
        # Draw text box (界面下方)
        self.text_box.draw(surface)
        
        # Draw buttons (对话框上方)
        for button in self.buttons:
            button.draw(surface)


class ShoppingScene(Scene):
    """Shopping scene"""
    
    def __init__(self, game):
        super().__init__(game)
        self.location = "Market"
        self.item_slots = []
        self.back_button = Button(50, WINDOW_HEIGHT - 100, 150, 50, "Back", font_size=28)
        self.buy_button = Button(WINDOW_WIDTH - 200, WINDOW_HEIGHT - 100, 150, 50, 
                                 "Buy", font_size=28, color=GREEN)
        self.selected_items = {}
    
    def set_location(self, location):
        """Set shopping location"""
        self.location = location
        self.selected_items = {}
        self._create_item_slots()
    
    def _create_item_slots(self):
        """Create item slots"""
        self.item_slots = []
        available_items = []
        
        ingredients = get_ingredients()
        restaurant_menu = get_restaurant_menu()
        
        if self.location == "Restaurant":
            # Restaurant menu
            for name, data in restaurant_menu.items():
                available_items.append((name, data))
        else:
            # Filter ingredients by location
            for name, data in ingredients.items():
                if data.get("location") == self.location:
                    available_items.append((name, data))
        
        # Create item slots
        slot_width = 200
        slot_height = 60
        x_start = 50
        y_start = 120
        cols = 4
        x_spacing = 20
        y_spacing = 10
        
        for i, (name, data) in enumerate(available_items):
            row = i // cols
            col = i % cols
            x = x_start + col * (slot_width + x_spacing)
            y = y_start + row * (slot_height + y_spacing)
            
            price_text = f"{name} (${data.get('price', 0)})"
            slot = ItemSlot(x, y, slot_width, slot_height, price_text, 0)
            slot.item_name = name
            slot.price = data.get("price", 0)
            self.item_slots.append(slot)
    
    def handle_event(self, event):
        """Handle events"""
        if self.back_button.handle_event(event):
            return "back"
        
        if self.buy_button.handle_event(event):
            return self._process_purchase()
        
        # Handle item selection
        for slot in self.item_slots:
            if slot.handle_event(event):
                # Left click adds item
                if event.button == 1:
                    item_name = slot.item_name
                    self.selected_items[item_name] = self.selected_items.get(item_name, 0) + 1
                    slot.count = self.selected_items[item_name]
                    slot.is_selected = True
                # Right click removes item
                elif event.button == 3:
                    item_name = slot.item_name
                    if item_name in self.selected_items and self.selected_items[item_name] > 0:
                        self.selected_items[item_name] -= 1
                        if self.selected_items[item_name] == 0:
                            del self.selected_items[item_name]
                            slot.is_selected = False
                        slot.count = self.selected_items.get(item_name, 0)
        
        return None
    
    def _process_purchase(self):
        """Process purchase"""
        if not self.selected_items:
            return None
        
        ingredients = get_ingredients()
        restaurant_menu = get_restaurant_menu()
        
        # Calculate total cost
        total_cost = 0
        for item_name, count in self.selected_items.items():
            if self.location == "Restaurant":
                total_cost += restaurant_menu[item_name]["price"] * count
            else:
                total_cost += ingredients[item_name]["price"] * count
        
        # Check money
        if total_cost > self.player.money:
            return {"result": "insufficient_money"}
        
        # Deduct money
        self.player.update_stat("money", -total_cost, is_delta=True)
        
        # Add items
        if self.location == "Restaurant":
            # Eat at restaurant
            for item_name, count in self.selected_items.items():
                effects = restaurant_menu[item_name]["effects"]
                for _ in range(count):
                    for stat, value in effects.items():
                        if stat == "mood":
                            self.player.change_mood(value)
                        else:
                            self.player.update_stat(stat, value, is_delta=True)
        else:
            # Buy ingredients
            for item_name, count in self.selected_items.items():
                self.player.add_item(item_name, count)
        
        return {"result": "success", "cost": total_cost, "location": self.location}
    
    def draw(self, surface):
        """Draw scene"""
        surface.fill(WHITE)
        
        # Draw background
        draw_market_background(surface, 0, 0, WINDOW_WIDTH, WINDOW_HEIGHT)
        
        # Title
        title = f"{self.location}"
        draw_text(surface, title, WINDOW_WIDTH // 2, 30, 36, BLACK, center=True)
        
        # Money display
        money_text = f"Money: ${self.player.money}"
        draw_text(surface, money_text, WINDOW_WIDTH // 2, 70, 28, GREEN, center=True)
        
        # Draw item slots
        for slot in self.item_slots:
            slot.draw(surface)
        
        # Draw total cost
        ingredients = get_ingredients()
        restaurant_menu = get_restaurant_menu()
        
        total_cost = 0
        for item_name, count in self.selected_items.items():
            if self.location == "Restaurant":
                total_cost += restaurant_menu[item_name]["price"] * count
            else:
                total_cost += ingredients[item_name]["price"] * count
        
        if total_cost > 0:
            cost_text = f"Total: ${total_cost}"
            color = RED if total_cost > self.player.money else BLACK
            draw_text(surface, cost_text, WINDOW_WIDTH // 2, WINDOW_HEIGHT - 150, 32, color, center=True)
        
        # Hint
        hint_text = "Left click to select, Right click to cancel"
        draw_text(surface, hint_text, WINDOW_WIDTH // 2, WINDOW_HEIGHT - 180, 20, GRAY, center=True)
        
        # Draw buttons
        self.back_button.draw(surface)
        self.buy_button.draw(surface)


class KitchenScene(Scene):
    """Kitchen scene"""
    
    def __init__(self, game):
        super().__init__(game)
        self.recipe_buttons = []
        self.back_button = Button(WINDOW_WIDTH // 2 - 75, WINDOW_HEIGHT - 100, 150, 50, 
                                  "Finish Cooking", font_size=28, color=RED)
        self._create_recipe_buttons()
    
    def _create_recipe_buttons(self):
        """Create recipe buttons"""
        self.recipe_buttons = []
        recipes = get_recipes()
        
        button_width = 220
        button_height = 80
        x_start = 50
        y_start = 150
        cols = 3
        x_spacing = 30
        y_spacing = 20
        
        for i, (name, data) in enumerate(recipes.items()):
            row = i // cols
            col = i % cols
            x = x_start + col * (button_width + x_spacing)
            y = y_start + row * (button_height + y_spacing)
            
            button = Button(x, y, button_width, button_height, name, font_size=22)
            button.recipe_name = name
            button.recipe_data = data
            self.recipe_buttons.append(button)
    
    def _can_cook(self, recipe_data):
        """Check if can cook this recipe"""
        # Check stamina
        if self.player.stamina < recipe_data.get("stamina_cost", 0):
            return False, "Not enough stamina"
        
        # Check ingredients
        for ingredient, count in recipe_data.get("ingredients", {}).items():
            if not self.player.has_item(ingredient, count):
                return False, f"Missing {ingredient}"
        
        return True, ""
    
    def _cook_recipe(self, recipe_name, recipe_data):
        """Cook recipe"""
        can_cook, reason = self._can_cook(recipe_data)
        if not can_cook:
            return {"result": "failed", "reason": reason}
        
        # Consume ingredients
        for ingredient, count in recipe_data.get("ingredients", {}).items():
            self.player.remove_item(ingredient, count)
        
        # Consume stamina
        self.player.update_stat("stamina", -recipe_data.get("stamina_cost", 0), is_delta=True)
        
        # Apply effects
        for stat, value in recipe_data.get("effects", {}).items():
            if stat == "mood":
                self.player.change_mood(value)
            else:
                self.player.update_stat(stat, value, is_delta=True)
        
        return {"result": "success", "recipe": recipe_name}
    
    def handle_event(self, event):
        """Handle events"""
        if self.back_button.handle_event(event):
            return "back"
        
        for button in self.recipe_buttons:
            if button.handle_event(event):
                result = self._cook_recipe(button.recipe_name, button.recipe_data)
                return result
        
        return None
    
    def draw(self, surface):
        """Draw scene"""
        surface.fill(WHITE)
        
        # Draw background
        draw_kitchen_background(surface, 0, 0, WINDOW_WIDTH, WINDOW_HEIGHT)
        
        # Title
        draw_text(surface, "Kitchen - Choose Recipe", WINDOW_WIDTH // 2, 30, 36, BLACK, center=True)
        
        # Show current status
        status_text = f"Stamina: {int(self.player.stamina)}/{STAT_MAX}  Satiety: {int(self.player.satiety)}/{STAT_MAX}"
        draw_text(surface, status_text, WINDOW_WIDTH // 2, 80, 24, BLACK, center=True)
        
        # Draw recipe buttons
        for button in self.recipe_buttons:
            # Check if can cook
            can_cook, reason = self._can_cook(button.recipe_data)
            if not can_cook:
                button.color = GRAY
            else:
                button.color = GREEN
            
            button.draw(surface)
            
            # Show ingredient requirements
            ingredients_text = ", ".join([f"{k}x{v}" for k, v in button.recipe_data.get("ingredients", {}).items()])
            draw_text(surface, ingredients_text, button.rect.centerx, button.rect.bottom + 5, 
                     16, GRAY, center=True)
        
        # Show inventory
        inventory_y = 500
        draw_text(surface, "Current Inventory:", 50, inventory_y, 24, BLACK)
        inventory_text = ", ".join([f"{k}x{v['count']}" for k, v in self.player.inventory.items()])
        if not inventory_text:
            inventory_text = "None"
        draw_text(surface, inventory_text, 50, inventory_y + 30, 20, GRAY)
        
        # Draw back button
        self.back_button.draw(surface)

class StoryScene(Scene):
    """Story playback scene"""
    
    def __init__(self, game):
        super().__init__(game)
        self.pages = []
        self.current_page_index = 0
        self.on_finish_callback = None
        self.font = pygame.font.Font(None, 32)
        self.instruction_font = pygame.font.Font(None, 24)
        
    def set_story(self, pages, on_finish_callback=None):
        """Set story content"""
        self.pages = pages
        self.current_page_index = 0
        self.on_finish_callback = on_finish_callback
        
    def handle_event(self, event):
        """Handle events"""
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Left click to next page
            if event.button == 1:
                self.current_page_index += 1
                if self.current_page_index >= len(self.pages):
                    # Story finished
                    if self.on_finish_callback:
                        self.on_finish_callback()
                    self.game.return_from_story()
                return True
        return False
        
    def draw(self, surface):
        """Draw scene"""
        # Black background
        surface.fill(BLACK)
        
        if 0 <= self.current_page_index < len(self.pages):
            text = self.pages[self.current_page_index]
            
            # Draw text centered
            draw_multiline_text(surface, text, 100, 200, WINDOW_WIDTH - 200, 
                              font_size=32, color=WHITE)
            
            # Draw instruction
            instruction = "Click to continue..."
            if self.current_page_index == len(self.pages) - 1:
                instruction = "Click to finish"
                
            text_surf = self.instruction_font.render(instruction, True, GRAY)
            text_rect = text_surf.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT - 50))
            surface.blit(text_surf, text_rect)
