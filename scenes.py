# -*- coding: utf-8 -*-
"""
场景系统
包含常规场景、购物场景、厨房场景
"""

import pygame
from config import *
from ui import *


class Scene:
    """场景基类"""
    
    def __init__(self, game):
        self.game = game
        self.player = game.player
    
    def handle_event(self, event):
        """处理事件"""
        pass
    
    def update(self):
        """更新场景"""
        pass
    
    def draw(self, surface):
        """绘制场景"""
        pass


class MainScene(Scene):
    """主场景/常规场景"""
    
    def __init__(self, game):
        super().__init__(game)
        self.status_bars = self._create_status_bars()
        self.text_box = TextBox(50, 150, WINDOW_WIDTH - 100, 200, "", font_size=24)
        self.buttons = []
        self.current_text = ""
        self.event_data = None
    
    def _create_status_bars(self):
        """创建状态栏"""
        bars = []
        y_start = 20
        x_start = 50
        bar_width = 180
        bar_height = 30
        spacing = 200
        
        bars.append(StatusBar(x_start, y_start, bar_width, bar_height, 
                              "Stamina", self.player.stamina, STAT_MAX, GREEN))
        bars.append(StatusBar(x_start + spacing, y_start, bar_width, bar_height, 
                              "Health", self.player.health, STAT_MAX, GREEN))
        bars.append(StatusBar(x_start + spacing * 2, y_start, bar_width, bar_height, 
                              "Satiety", self.player.satiety, STAT_MAX, BLUE))
        
        return bars
    
    def set_content(self, text, buttons_data=None, event_data=None):
        """设置场景内容"""
        self.current_text = text
        self.text_box.set_text(text)
        self.event_data = event_data
        
        # 创建按钮
        self.buttons = []
        if buttons_data:
            button_width = 200
            button_height = 50
            x_start = (WINDOW_WIDTH - button_width * len(buttons_data) - 20 * (len(buttons_data) - 1)) // 2
            y_pos = 400
            
            for i, btn_data in enumerate(buttons_data):
                x = x_start + i * (button_width + 20)
                button = Button(x, y_pos, button_width, button_height, 
                              btn_data["text"], font_size=28)
                button.callback = btn_data.get("callback")
                button.data = btn_data.get("data")
                self.buttons.append(button)
    
    def handle_event(self, event):
        """处理事件"""
        for button in self.buttons:
            if button.handle_event(event):
                if button.callback:
                    button.callback(button.data)
                return True
        return False
    
    def update(self):
        """更新状态栏"""
        self.status_bars[0].update(self.player.stamina)
        self.status_bars[1].update(self.player.health)
        self.status_bars[2].update(self.player.satiety)
    
    def draw(self, surface):
        """绘制场景"""
        surface.fill(WHITE)
        
        # 绘制状态栏
        for bar in self.status_bars:
            bar.draw(surface)
        
        # Draw mood and money
        mood_text = f"Mood: {self.player.get_mood_text()}"
        money_text = f"Money: ${self.player.money}"
        day_text = f"Day {self.player.current_day}/{GAME_DAYS}"
        
        draw_text(surface, mood_text, 50, 70, 24, BLACK)
        draw_text(surface, money_text, 250, 70, 24, BLACK)
        draw_text(surface, day_text, 450, 70, 24, RED)
        
        # 绘制文本框
        self.text_box.draw(surface)
        
        # 绘制按钮
        for button in self.buttons:
            button.draw(surface)


class ShoppingScene(Scene):
    """购物场景"""
    
    def __init__(self, game):
        super().__init__(game)
        self.location = "菜市场"  # 菜市场/便利店/餐厅
        self.item_slots = []
        self.back_button = Button(50, WINDOW_HEIGHT - 100, 150, 50, "Back", font_size=28)
        self.buy_button = Button(WINDOW_WIDTH - 200, WINDOW_HEIGHT - 100, 150, 50, 
                                 "Buy", font_size=28, color=GREEN)
        self.selected_items = {}  # {物品名: 数量}
    
    def set_location(self, location):
        """Set shopping location"""
        self.location = location
        self.selected_items = {}
        self._create_item_slots()
    
    def _create_item_slots(self):
        """Create item slots"""
        self.item_slots = []
        available_items = []
        
        if self.location == "Restaurant":
            # Restaurant menu
            for name, data in RESTAURANT_MENU.items():
                available_items.append((name, data))
        else:
            # Filter ingredients by location
            for name, data in INGREDIENTS.items():
                if data["location"] == self.location:
                    available_items.append((name, data))
        
        # 创建物品槽
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
            
            price_text = f"{name} (${data['price']})"
            slot = ItemSlot(x, y, slot_width, slot_height, price_text, 0)
            slot.item_name = name
            slot.price = data["price"]
            self.item_slots.append(slot)
    
    def handle_event(self, event):
        """处理事件"""
        if self.back_button.handle_event(event):
            return "back"
        
        if self.buy_button.handle_event(event):
            return self._process_purchase()
        
        # 处理物品选择
        for slot in self.item_slots:
            if slot.handle_event(event):
                # 左键增加数量
                if event.button == 1:
                    item_name = slot.item_name
                    self.selected_items[item_name] = self.selected_items.get(item_name, 0) + 1
                    slot.count = self.selected_items[item_name]
                    slot.is_selected = True
                # 右键减少数量
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
        
        # Calculate total cost
        total_cost = 0
        for item_name, count in self.selected_items.items():
            if self.location == "Restaurant":
                total_cost += RESTAURANT_MENU[item_name]["price"] * count
            else:
                total_cost += INGREDIENTS[item_name]["price"] * count
        
        # Check money
        if total_cost > self.player.money:
            return {"result": "insufficient_money"}
        
        # Deduct money
        self.player.update_stat("money", -total_cost, is_delta=True)
        
        # Add items
        if self.location == "Restaurant":
            # Eat at restaurant
            for item_name, count in self.selected_items.items():
                effects = RESTAURANT_MENU[item_name]["effects"]
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
        total_cost = 0
        for item_name, count in self.selected_items.items():
            if self.location == "Restaurant":
                total_cost += RESTAURANT_MENU[item_name]["price"] * count
            else:
                total_cost += INGREDIENTS[item_name]["price"] * count
        
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
    """厨房场景"""
    
    def __init__(self, game):
        super().__init__(game)
        self.recipe_buttons = []
        self.back_button = Button(WINDOW_WIDTH // 2 - 75, WINDOW_HEIGHT - 100, 150, 50, 
                                  "Finish Cooking", font_size=28, color=RED)
        self._create_recipe_buttons()
    
    def _create_recipe_buttons(self):
        """创建食谱按钮"""
        self.recipe_buttons = []
        button_width = 220
        button_height = 80
        x_start = 50
        y_start = 150
        cols = 3
        x_spacing = 30
        y_spacing = 20
        
        for i, (name, data) in enumerate(RECIPES.items()):
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
        if self.player.stamina < recipe_data["stamina_cost"]:
            return False, "Not enough stamina"
        
        # Check ingredients
        for ingredient, count in recipe_data["ingredients"].items():
            if not self.player.has_item(ingredient, count):
                return False, f"Missing {ingredient}"
        
        return True, ""
    
    def _cook_recipe(self, recipe_name, recipe_data):
        """烹饪食谱"""
        can_cook, reason = self._can_cook(recipe_data)
        if not can_cook:
            return {"result": "failed", "reason": reason}
        
        # 消耗食材
        for ingredient, count in recipe_data["ingredients"].items():
            self.player.remove_item(ingredient, count)
        
        # 消耗体力
        self.player.update_stat("stamina", -recipe_data["stamina_cost"], is_delta=True)
        
        # 应用效果
        for stat, value in recipe_data["effects"].items():
            if stat == "mood":
                self.player.change_mood(value)
            else:
                self.player.update_stat(stat, value, is_delta=True)
        
        return {"result": "success", "recipe": recipe_name}
    
    def handle_event(self, event):
        """处理事件"""
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
            ingredients_text = ", ".join([f"{k}x{v}" for k, v in button.recipe_data["ingredients"].items()])
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
