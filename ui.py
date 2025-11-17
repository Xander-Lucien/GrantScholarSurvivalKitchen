# -*- coding: utf-8 -*-
"""
UI组件
包含按钮、文本框等UI元素
"""

import pygame
from config import *


class Button:
    """按钮类"""
    
    def __init__(self, x, y, width, height, text, font_size=24, 
                 color=BLUE, hover_color=LIGHT_GRAY, text_color=WHITE):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font = pygame.font.Font(None, font_size)
        self.color = color
        self.hover_color = hover_color
        self.text_color = text_color
        self.is_hovered = False
    
    def draw(self, surface):
        """绘制按钮"""
        color = self.hover_color if self.is_hovered else self.color
        pygame.draw.rect(surface, color, self.rect, border_radius=5)
        pygame.draw.rect(surface, BLACK, self.rect, 2, border_radius=5)
        
        text_surface = self.font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)
    
    def handle_event(self, event):
        """处理事件"""
        if event.type == pygame.MOUSEMOTION:
            self.is_hovered = self.rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if self.is_hovered:
                return True
        return False


class TextBox:
    """文本框类"""
    
    def __init__(self, x, y, width, height, text="", font_size=20, 
                 bg_color=WHITE, text_color=BLACK, padding=10):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font = pygame.font.Font(None, font_size)
        self.bg_color = bg_color
        self.text_color = text_color
        self.padding = padding
    
    def set_text(self, text):
        """设置文本"""
        self.text = text
    
    def draw(self, surface):
        """绘制文本框"""
        pygame.draw.rect(surface, self.bg_color, self.rect, border_radius=5)
        pygame.draw.rect(surface, BLACK, self.rect, 2, border_radius=5)
        
        # 绘制文本（支持多行）
        lines = self.text.split('\n')
        y_offset = self.padding
        for line in lines:
            text_surface = self.font.render(line, True, self.text_color)
            surface.blit(text_surface, (self.rect.x + self.padding, self.rect.y + y_offset))
            y_offset += self.font.get_height() + 2


class StatusBar:
    """状态栏类"""
    
    def __init__(self, x, y, width, height, label, value, max_value, 
                 bar_color=GREEN, bg_color=GRAY):
        self.rect = pygame.Rect(x, y, width, height)
        self.label = label
        self.value = value
        self.max_value = max_value
        self.bar_color = bar_color
        self.bg_color = bg_color
        self.font = pygame.font.Font(None, 20)
    
    def update(self, value):
        """更新数值"""
        self.value = value
    
    def draw(self, surface):
        """绘制状态栏"""
        # 绘制背景
        pygame.draw.rect(surface, self.bg_color, self.rect)
        
        # 绘制进度条
        if self.max_value > 0:
            progress = min(1.0, self.value / self.max_value)
            bar_width = int(self.rect.width * progress)
            bar_rect = pygame.Rect(self.rect.x, self.rect.y, bar_width, self.rect.height)
            
            # 根据数值改变颜色
            if progress < 0.3:
                color = RED
            elif progress < 0.6:
                color = ORANGE
            else:
                color = self.bar_color
            
            pygame.draw.rect(surface, color, bar_rect)
        
        # 绘制边框
        pygame.draw.rect(surface, BLACK, self.rect, 2)
        
        # 绘制标签和数值
        text = f"{self.label}: {int(self.value)}/{int(self.max_value)}"
        text_surface = self.font.render(text, True, WHITE)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)


class ItemSlot:
    """物品槽类"""
    
    def __init__(self, x, y, width, height, item_name, count, font_size=18):
        self.rect = pygame.Rect(x, y, width, height)
        self.item_name = item_name
        self.count = count
        self.font = pygame.font.Font(None, font_size)
        self.is_hovered = False
        self.is_selected = False
    
    def draw(self, surface):
        """绘制物品槽"""
        # 背景色
        if self.is_selected:
            bg_color = YELLOW
        elif self.is_hovered:
            bg_color = LIGHT_GRAY
        else:
            bg_color = WHITE
        
        pygame.draw.rect(surface, bg_color, self.rect, border_radius=3)
        pygame.draw.rect(surface, BLACK, self.rect, 2, border_radius=3)
        
        # 物品名称
        text = f"{self.item_name} x{self.count}"
        text_surface = self.font.render(text, True, BLACK)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)
    
    def handle_event(self, event):
        """处理事件"""
        if event.type == pygame.MOUSEMOTION:
            self.is_hovered = self.rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if self.is_hovered:
                return True
        return False


def draw_text(surface, text, x, y, font_size=24, color=BLACK, center=False):
    """绘制文本的辅助函数"""
    font = pygame.font.Font(None, font_size)
    text_surface = font.render(text, True, color)
    if center:
        text_rect = text_surface.get_rect(center=(x, y))
        surface.blit(text_surface, text_rect)
    else:
        surface.blit(text_surface, (x, y))


def draw_multiline_text(surface, text, x, y, width, font_size=20, color=BLACK):
    """绘制多行文本"""
    font = pygame.font.Font(None, font_size)
    words = text.split(' ')
    lines = []
    current_line = []
    
    for word in words:
        current_line.append(word)
        line_text = ' '.join(current_line)
        if font.size(line_text)[0] > width:
            if len(current_line) > 1:
                current_line.pop()
                lines.append(' '.join(current_line))
                current_line = [word]
            else:
                lines.append(line_text)
                current_line = []
    
    if current_line:
        lines.append(' '.join(current_line))
    
    y_offset = y
    for line in lines:
        text_surface = font.render(line, True, color)
        surface.blit(text_surface, (x, y_offset))
        y_offset += font.get_height() + 2
