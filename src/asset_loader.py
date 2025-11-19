"""
Asset Loader Module
Singleton pattern asset manager for loading and caching game assets.
Supports: images, sounds, fonts
"""

import os
import pygame
from typing import Dict, Optional


class AssetLoader:
    """Singleton class for loading and caching game assets."""
    
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(AssetLoader, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if self._initialized:
            return
        
        self._initialized = True
        self.base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.assets_path = os.path.join(self.base_path, 'assets')
        
        # Cache dictionaries
        self._images: Dict[str, pygame.Surface] = {}
        self._sounds: Dict[str, pygame.mixer.Sound] = {}
        self._fonts: Dict[tuple, pygame.font.Font] = {}  # (font_path, size) -> Font
        
        # Ensure pygame is initialized
        if not pygame.get_init():
            pygame.init()
        if not pygame.mixer.get_init():
            pygame.mixer.init()
    
    def load_image(self, path: str, convert_alpha: bool = True) -> Optional[pygame.Surface]:
        """
        Load an image from assets/images/ directory.
        
        Args:
            path: Relative path within assets/images/ (e.g., 'ui/button.png')
            convert_alpha: Whether to convert with alpha transparency
            
        Returns:
            pygame.Surface or None if loading fails
        """
        if path in self._images:
            return self._images[path]
        
        full_path = os.path.join(self.assets_path, 'images', path)
        
        try:
            if not os.path.exists(full_path):
                print(f"Warning: Image not found: {full_path}")
                return None
            
            image = pygame.image.load(full_path)
            if convert_alpha:
                image = image.convert_alpha()
            else:
                image = image.convert()
            
            self._images[path] = image
            return image
        except pygame.error as e:
            print(f"Error loading image {full_path}: {e}")
            return None
    
    def load_sound(self, path: str) -> Optional[pygame.mixer.Sound]:
        """
        Load a sound from assets/sounds/ directory.
        
        Args:
            path: Relative path within assets/sounds/ (e.g., 'sfx/click.wav')
            
        Returns:
            pygame.mixer.Sound or None if loading fails
        """
        if path in self._sounds:
            return self._sounds[path]
        
        full_path = os.path.join(self.assets_path, 'sounds', path)
        
        try:
            if not os.path.exists(full_path):
                print(f"Warning: Sound not found: {full_path}")
                return None
            
            sound = pygame.mixer.Sound(full_path)
            self._sounds[path] = sound
            return sound
        except pygame.error as e:
            print(f"Error loading sound {full_path}: {e}")
            return None
    
    def load_font(self, path: Optional[str] = None, size: int = 24) -> pygame.font.Font:
        """
        Load a font from assets/fonts/ directory.
        
        Args:
            path: Relative path within assets/fonts/ (e.g., 'game_font.ttf')
                  If None, uses pygame's default font
            size: Font size in pixels
            
        Returns:
            pygame.font.Font object
        """
        cache_key = (path, size)
        if cache_key in self._fonts:
            return self._fonts[cache_key]
        
        try:
            if path is None:
                font = pygame.font.Font(None, size)
            else:
                full_path = os.path.join(self.assets_path, 'fonts', path)
                if not os.path.exists(full_path):
                    print(f"Warning: Font not found: {full_path}, using default font")
                    font = pygame.font.Font(None, size)
                else:
                    font = pygame.font.Font(full_path, size)
            
            self._fonts[cache_key] = font
            return font
        except pygame.error as e:
            print(f"Error loading font: {e}, using default font")
            font = pygame.font.Font(None, size)
            self._fonts[cache_key] = font
            return font
    
    def get_asset_path(self, category: str, filename: str) -> str:
        """
        Get the full path to an asset file.
        
        Args:
            category: Asset category ('images', 'sounds', 'fonts')
            filename: Filename within the category
            
        Returns:
            Full absolute path to the asset
        """
        return os.path.join(self.assets_path, category, filename)
    
    def clear_cache(self):
        """Clear all cached assets to free memory."""
        self._images.clear()
        self._sounds.clear()
        self._fonts.clear()
    
    def preload_assets(self, asset_list: Dict[str, list]):
        """
        Preload a batch of assets.
        
        Args:
            asset_list: Dictionary with keys 'images', 'sounds', 'fonts'
                       Each containing a list of paths to preload
                       Example:
                       {
                           'images': ['ui/button.png', 'characters/player.png'],
                           'sounds': ['sfx/click.wav'],
                           'fonts': [('game_font.ttf', 24), ('title_font.ttf', 48)]
                       }
        """
        if 'images' in asset_list:
            for img_path in asset_list['images']:
                self.load_image(img_path)
        
        if 'sounds' in asset_list:
            for sound_path in asset_list['sounds']:
                self.load_sound(sound_path)
        
        if 'fonts' in asset_list:
            for font_info in asset_list['fonts']:
                if isinstance(font_info, tuple):
                    path, size = font_info
                    self.load_font(path, size)
                else:
                    self.load_font(font_info)


# Global instance for easy access
asset_loader = AssetLoader()
