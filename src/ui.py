# -*- coding: utf-8 -*-
"""
UI components
Contains buttons, text boxes and other UI elements
"""

import pygame
from .config import *


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
        # 绘制阴影
        shadow_rect = self.rect.copy()
        shadow_rect.x += 4
        shadow_rect.y += 4
        pygame.draw.rect(surface, (50, 50, 50), shadow_rect, border_radius=5)
        
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
    
    def __init__(self, x, y, width, height, text="", font_size=24, 
                 bg_color=(30, 30, 40, 230), text_color=(255, 255, 255), padding=20):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font = pygame.font.Font(None, font_size)
        self.bg_color = bg_color
        self.text_color = text_color
        self.padding = padding
        self.line_spacing = 8  # 行距
        self.wrapped_lines = []
        self._wrap_text()
    
    def set_text(self, text):
        """设置文本"""
        self.text = text
        self._wrap_text()
        
    def _wrap_text(self):
        """处理文本自动换行"""
        self.wrapped_lines = []
        if not self.text:
            return
            
        # 可用宽度
        max_width = self.rect.width - self.padding * 2
        
        # 按换行符分割段落
        paragraphs = self.text.split('\n')
        
        for paragraph in paragraphs:
            words = paragraph.split(' ')
            current_line = []
            
            for word in words:
                # 尝试添加单词
                test_line = ' '.join(current_line + [word])
                # 检查宽度
                if self.font.size(test_line)[0] <= max_width:
                    current_line.append(word)
                else:
                    # 如果当前行不为空，先保存当前行
                    if current_line:
                        self.wrapped_lines.append(' '.join(current_line))
                        current_line = [word]
                    else:
                        # 单词本身太长
                        self.wrapped_lines.append(word)
                        current_line = []
            
            # 添加最后一行
            if current_line:
                self.wrapped_lines.append(' '.join(current_line))
    
    def draw(self, surface):
        """绘制文本框"""
        # 1. 绘制半透明背景
        s = pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA)
        
        # 填充背景色
        if len(self.bg_color) == 4:
            s.fill(self.bg_color)
        else:
            s.fill((*self.bg_color, 255))
            
        # 绘制边框
        pygame.draw.rect(s, (200, 200, 200), s.get_rect(), 2, border_radius=10)
        
        # 将surface blit到主屏幕
        surface.blit(s, (self.rect.x, self.rect.y))
        
        # 2. 绘制文本
        y_offset = self.rect.y + self.padding
        line_height = self.font.get_height() + self.line_spacing
        
        for line in self.wrapped_lines:
            # 检查是否超出高度
            if y_offset + line_height > self.rect.bottom - self.padding:
                break
                
            text_surface = self.font.render(line, True, self.text_color)
            surface.blit(text_surface, (self.rect.x + self.padding, y_offset))
            y_offset += line_height


class StatusBar:
    """状态栏类"""
    
    def __init__(self, x, y, width, height, label, value, max_value, 
                 bar_color=GREEN, bg_color=(60, 60, 60), icon_text=""):
        self.rect = pygame.Rect(x, y, width, height)
        self.label = label
        self.value = value
        self.max_value = max_value
        self.bar_color = bar_color
        self.bg_color = bg_color
        self.icon_text = icon_text
        self.font = pygame.font.Font(None, 22)
    
    def update(self, value):
        """更新数值"""
        self.value = value
    
    def draw(self, surface):
        """绘制状态栏"""
        # 绘制背景容器 (圆角)
        pygame.draw.rect(surface, self.bg_color, self.rect, border_radius=8)
        pygame.draw.rect(surface, (200, 200, 200), self.rect, 2, border_radius=8)
        
        # 内部进度条区域
        padding = 4
        inner_width = self.rect.width - padding * 2
        inner_height = self.rect.height - padding * 2
        inner_x = self.rect.x + padding
        inner_y = self.rect.y + padding
        
        # 绘制槽位背景
        pygame.draw.rect(surface, (30, 30, 30), 
                        (inner_x, inner_y, inner_width, inner_height), 
                        border_radius=4)
        
        # 绘制进度条
        if self.max_value > 0:
            progress = min(1.0, max(0.0, self.value / self.max_value))
            bar_width = int(inner_width * progress)
            
            if bar_width > 0:
                bar_rect = pygame.Rect(inner_x, inner_y, bar_width, inner_height)
                
                # 根据数值改变颜色 (低数值变红)
                color = self.bar_color
                if progress < 0.3:
                    color = (220, 60, 60) # 红色警告
                
                pygame.draw.rect(surface, color, bar_rect, border_radius=4)
                
                # 添加高光 (上半部分半透明白)
                highlight_rect = pygame.Rect(inner_x, inner_y, bar_width, inner_height // 2)
                highlight_surf = pygame.Surface((bar_width, inner_height // 2), pygame.SRCALPHA)
                highlight_surf.fill((255, 255, 255, 60))
                surface.blit(highlight_surf, highlight_rect)
        
        # 绘制文字 (带阴影)
        text = f"{self.icon_text} {self.label}: {int(self.value)}/{int(self.max_value)}"
        
        # 阴影
        text_shadow = self.font.render(text, True, (0, 0, 0))
        text_rect_shadow = text_shadow.get_rect(center=(self.rect.centerx + 1, self.rect.centery + 1))
        surface.blit(text_shadow, text_rect_shadow)
        
        # 正文
        text_surface = self.font.render(text, True, WHITE)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)


class InfoBadge:
    """信息徽章类 (用于心情和金钱)"""
    
    def __init__(self, x, y, width, height, label, value_text, 
                 color=(100, 100, 255), icon_text=""):
        self.rect = pygame.Rect(x, y, width, height)
        self.label = label
        self.value_text = value_text
        self.color = color
        self.icon_text = icon_text
        self.font = pygame.font.Font(None, 22)
    
    def update(self, value_text, color=None):
        self.value_text = value_text
        if color:
            self.color = color
            
    def draw(self, surface):
        # 背景 (带边框)
        pygame.draw.rect(surface, self.color, self.rect, border_radius=8)
        pygame.draw.rect(surface, WHITE, self.rect, 2, border_radius=8)
        
        # 高光
        highlight_rect = pygame.Rect(self.rect.x, self.rect.y, self.rect.width, self.rect.height // 2)
        highlight_surf = pygame.Surface((self.rect.width, self.rect.height // 2), pygame.SRCALPHA)
        highlight_surf.fill((255, 255, 255, 40))
        surface.blit(highlight_surf, highlight_rect)
        
        # 文字
        text = f"{self.icon_text} {self.label}: {self.value_text}"
        
        # 阴影
        text_shadow = self.font.render(text, True, (0, 0, 0))
        text_rect_shadow = text_shadow.get_rect(center=(self.rect.centerx + 1, self.rect.centery + 1))
        surface.blit(text_shadow, text_rect_shadow)
        
        # 正文
        text_surf = self.font.render(text, True, WHITE)
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)


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
