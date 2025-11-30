# -*- coding: utf-8 -*-
"""
Background drawing module
Contains functions to draw pixel-art style backgrounds for different scenes
"""

import pygame
from .config import *
from .asset_loader import AssetLoader

def draw_room_background(surface, x, y, width, height):
    """
    Draw room background using BgHome.png image
    Used for MainScene
    """
    asset_loader = AssetLoader()
    bg_image = asset_loader.load_image("backgrounds/BgHome.png", convert_alpha=True)
    
    if bg_image:
        # 缩放图片以适配窗口大小
        scaled_bg = pygame.transform.scale(bg_image, (width, height))
        surface.blit(scaled_bg, (x, y))
    else:
        # 如果图片加载失败，使用原来的像素风格背景作为后备
        # Define colors
        WALL_COLOR = (230, 230, 220)
        FLOOR_COLOR = (180, 160, 140)
        WINDOW_COLOR = (135, 206, 235)
        WINDOW_FRAME_COLOR = (100, 80, 60)
        TABLE_COLOR = (139, 69, 19)
        RUG_COLOR = (160, 82, 45)
        
        # Draw wall and floor
        # Floor takes up bottom 1/3
        floor_height = height // 3
        wall_height = height - floor_height
        
        # Wall
        pygame.draw.rect(surface, WALL_COLOR, (x, y, width, wall_height))
        # Floor
        pygame.draw.rect(surface, FLOOR_COLOR, (x, y + wall_height, width, floor_height))
        
        # Draw Window (Larger and centered)
        win_w = 200
        win_h = 160
        win_x = x + width // 2 - win_w // 2
        win_y = y + wall_height // 4
        
        # Window glass
        pygame.draw.rect(surface, WINDOW_COLOR, (win_x, win_y, win_w, win_h))
        # Window frame
        frame_thick = 10
        pygame.draw.rect(surface, WINDOW_FRAME_COLOR, (win_x, win_y, win_w, win_h), frame_thick)
        pygame.draw.rect(surface, WINDOW_FRAME_COLOR, (win_x, win_y + win_h//2, win_w, frame_thick)) # Horizontal bar
        pygame.draw.rect(surface, WINDOW_FRAME_COLOR, (win_x + win_w//2, win_y, frame_thick, win_h)) # Vertical bar
        
        # Draw Rug (On the floor)
        rug_w = 400
        rug_h = 100
        rug_x = x + width // 2 - rug_w // 2
        rug_y = y + wall_height + 50
        pygame.draw.ellipse(surface, RUG_COLOR, (rug_x, rug_y, rug_w, rug_h))
        
        # Draw Table (Centered, slightly above floor line to look like it's against the wall)
        table_w = 300
        table_h = 120
        table_x = x + width // 2 - table_w // 2
        # Position table so its legs are on the floor, but top is visible
        # Move it up so it's not covered by the text box (which is at bottom 220px)
        table_y = y + wall_height - 40 
        
        # Table top
        pygame.draw.rect(surface, TABLE_COLOR, (table_x, table_y, table_w, 30))
        # Table legs
        leg_w = 20
        pygame.draw.rect(surface, TABLE_COLOR, (table_x + 30, table_y + 30, leg_w, table_h))
        pygame.draw.rect(surface, TABLE_COLOR, (table_x + table_w - 30 - leg_w, table_y + 30, leg_w, table_h))

def draw_market_background(surface, x, y, width, height):
    """
    Draw market background using BgMarket.png image
    Used for ShoppingScene
    """
    asset_loader = AssetLoader()
    bg_image = asset_loader.load_image("backgrounds/BgMarket.png", convert_alpha=True)
    
    if bg_image:
        # 缩放图片以适配窗口大小
        scaled_bg = pygame.transform.scale(bg_image, (width, height))
        surface.blit(scaled_bg, (x, y))
    else:
        # 如果图片加载失败，使用原来的像素风格背景作为后备
        SKY_COLOR = (135, 206, 250)
        GROUND_COLOR = (210, 180, 140)
        STALL_COLOR = (205, 133, 63)
        AWNING_COLOR_1 = (255, 99, 71) # Red
        AWNING_COLOR_2 = (255, 255, 255) # White
        
        # Sky and Ground
        ground_h = height // 3
        sky_h = height - ground_h
        
        pygame.draw.rect(surface, SKY_COLOR, (x, y, width, sky_h))
        pygame.draw.rect(surface, GROUND_COLOR, (x, y + sky_h, width, ground_h))
        
        # Draw Stalls
        stall_w = 100
        stall_h = 80
        stall_gap = 40
        start_x = x + (width - (stall_w * 3 + stall_gap * 2)) // 2
        stall_y = y + sky_h - 40
        
        for i in range(3):
            curr_x = start_x + i * (stall_w + stall_gap)
            
            # Stall body
            pygame.draw.rect(surface, STALL_COLOR, (curr_x, stall_y, stall_w, stall_h))
            
            # Awning (striped)
            awning_h = 30
            awning_y = stall_y - awning_h
            pygame.draw.rect(surface, AWNING_COLOR_1, (curr_x - 10, awning_y, stall_w + 20, awning_h))
            
            # Stripes
            stripe_w = 15
            for j in range(0, stall_w + 20, stripe_w * 2):
                pygame.draw.rect(surface, AWNING_COLOR_2, (curr_x - 10 + j, awning_y, stripe_w, awning_h))

def draw_convenience_store_background(surface, x, y, width, height):
    """
    Draw convenience store background using BgConvenienceStore.png image
    Used for ShoppingScene when location is Convenience Store
    """
    asset_loader = AssetLoader()
    bg_image = asset_loader.load_image("backgrounds/BgConvenienceStore.png", convert_alpha=True)
    
    if bg_image:
        # 缩放图片以适配窗口大小
        scaled_bg = pygame.transform.scale(bg_image, (width, height))
        surface.blit(scaled_bg, (x, y))
    else:
        # 如果图片加载失败，使用简单的背景作为后备
        BG_COLOR = (240, 240, 240)
        SHELF_COLOR = (180, 180, 180)
        
        pygame.draw.rect(surface, BG_COLOR, (x, y, width, height))
        
        # Draw simple shelves
        for i in range(3):
            shelf_y = y + 150 + i * 150
            pygame.draw.rect(surface, SHELF_COLOR, (x + 50, shelf_y, width - 100, 80))

def draw_restaurant_background(surface, x, y, width, height):
    """
    Draw restaurant background using BgRestaurant.png image
    Used for ShoppingScene when location is Restaurant
    """
    asset_loader = AssetLoader()
    bg_image = asset_loader.load_image("backgrounds/BgRestaurant.png", convert_alpha=True)
    
    if bg_image:
        # 缩放图片以适配窗口大小
        scaled_bg = pygame.transform.scale(bg_image, (width, height))
        surface.blit(scaled_bg, (x, y))
    else:
        # 如果图片加载失败，使用简单的背景作为后备
        BG_COLOR = (255, 248, 240)
        TABLE_COLOR = (139, 69, 19)
        
        pygame.draw.rect(surface, BG_COLOR, (x, y, width, height))
        
        # Draw simple tables
        for i in range(2):
            table_x = x + 100 + i * 300
            table_y = y + height // 2
            pygame.draw.rect(surface, TABLE_COLOR, (table_x, table_y, 150, 100))

def draw_kitchen_background(surface, x, y, width, height):
    """
    Draw kitchen background using BgKitchen.png image
    Used for KitchenScene
    """
    asset_loader = AssetLoader()
    bg_image = asset_loader.load_image("backgrounds/BgKitchen.png", convert_alpha=True)
    
    if bg_image:
        # 缩放图片以适配窗口大小
        scaled_bg = pygame.transform.scale(bg_image, (width, height))
        surface.blit(scaled_bg, (x, y))
    else:
        # 如果图片加载失败，使用原来的像素风格背景作为后备
        WALL_COLOR = (240, 248, 255)
        TILE_COLOR = (200, 200, 200)
        COUNTER_COLOR = (169, 169, 169)
        STOVE_COLOR = (50, 50, 50)
        
        # Wall
        pygame.draw.rect(surface, WALL_COLOR, (x, y, width, height))
        
        # Tiles (grid pattern on lower half of wall)
        tile_start_y = y + height // 3
        tile_size = 40
        for ty in range(tile_start_y, y + height, tile_size):
            pygame.draw.line(surface, TILE_COLOR, (x, ty), (x + width, ty), 1)
        for tx in range(x, x + width, tile_size):
            pygame.draw.line(surface, TILE_COLOR, (tx, tile_start_y), (tx, y + height), 1)
            
        # Counter
        counter_h = 100
        counter_y = y + height - counter_h
        pygame.draw.rect(surface, COUNTER_COLOR, (x, counter_y, width, counter_h))
        
        # Stove
        stove_w = 120
        stove_h = 100 # Includes oven part
        stove_x = x + width // 2 - stove_w // 2
        stove_y = counter_y - 20 # Slightly above counter
        
        pygame.draw.rect(surface, STOVE_COLOR, (stove_x, stove_y, stove_w, stove_h))
        
        # Burners
        burner_color = (30, 30, 30)
        pygame.draw.circle(surface, burner_color, (stove_x + 30, stove_y + 15), 10)
        pygame.draw.circle(surface, burner_color, (stove_x + 90, stove_y + 15), 10)
        
        # Oven door
        oven_color = (70, 70, 70)
        pygame.draw.rect(surface, oven_color, (stove_x + 10, stove_y + 40, stove_w - 20, stove_h - 50))
