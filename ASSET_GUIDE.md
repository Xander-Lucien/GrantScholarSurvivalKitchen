# Asset Usage Guide

This guide shows you how to use the asset loader system to integrate art assets into the game.

## Quick Start

```python
from src.asset_loader import asset_loader

# Load an image
button_image = asset_loader.load_image('ui/button.png')

# Load a sound
click_sound = asset_loader.load_sound('sfx/click.wav')

# Load a font
title_font = asset_loader.load_font('title_font.ttf', 48)
```

## Asset Organization

### Directory Structure

```
assets/
├── images/
│   ├── ui/              # UI elements
│   ├── characters/      # Character sprites
│   ├── items/           # Food items
│   └── backgrounds/     # Scene backgrounds
├── sounds/
│   ├── bgm/             # Background music
│   └── sfx/             # Sound effects
└── fonts/               # Font files
```

### Adding Assets

1. Place your asset files in the appropriate subdirectory
2. Update `data/assets.json` with the asset path (optional, but recommended)
3. Load the asset using the asset loader

## Usage Examples

### Loading Images

```python
from src.asset_loader import asset_loader

# Load with alpha transparency (for PNG with transparency)
button = asset_loader.load_image('ui/button.png')

# Load without alpha (for JPG or opaque images)
background = asset_loader.load_image('backgrounds/dorm.jpg', convert_alpha=False)

# Draw to screen
screen.blit(button, (100, 100))
```

### Loading Sounds

```python
from src.asset_loader import asset_loader

# Load sound effect
click_sound = asset_loader.load_sound('sfx/click.wav')

# Play sound
click_sound.play()

# Set volume (0.0 to 1.0)
click_sound.set_volume(0.5)

# Load background music
pygame.mixer.music.load(asset_loader.get_asset_path('sounds', 'bgm/gameplay.mp3'))
pygame.mixer.music.play(-1)  # Loop indefinitely
```

### Loading Fonts

```python
from src.asset_loader import asset_loader

# Load custom font
title_font = asset_loader.load_font('title_font.ttf', 48)
normal_font = asset_loader.load_font('game_font.ttf', 24)

# Use default pygame font
default_font = asset_loader.load_font(None, 20)

# Render text
text_surface = title_font.render('Game Title', True, (255, 255, 255))
screen.blit(text_surface, (100, 50))
```

## Preloading Assets

For better performance, preload assets at game startup:

```python
from src.asset_loader import asset_loader

# Preload multiple assets at once
assets_to_preload = {
    'images': [
        'ui/button.png',
        'ui/button_hover.png',
        'characters/player.png',
        'items/instant_noodles.png'
    ],
    'sounds': [
        'sfx/click.wav',
        'sfx/purchase.wav'
    ],
    'fonts': [
        ('game_font.ttf', 24),
        ('title_font.ttf', 48)
    ]
}

asset_loader.preload_assets(assets_to_preload)
```

## Configuration in assets.json

Define asset paths in `data/assets.json` for easier management:

```json
{
  "ui": {
    "button": "ui/button.png",
    "button_hover": "ui/button_hover.png"
  },
  "items": {
    "egg": "items/egg.png"
  }
}
```

Then load from data loader:

```python
from src.data_loader import data_loader
from src.asset_loader import asset_loader

# Get path from config
button_path = data_loader.get('assets', 'ui', 'button')
button_image = asset_loader.load_image(button_path)
```

## Error Handling

The asset loader handles errors gracefully:

```python
# If asset doesn't exist, returns None for images/sounds
image = asset_loader.load_image('nonexistent.png')
if image is None:
    # Use fallback or default
    image = create_placeholder_surface()

# For fonts, falls back to default pygame font
font = asset_loader.load_font('nonexistent.ttf', 24)
# Always returns a valid font object
```

## Memory Management

```python
# Clear all cached assets to free memory
asset_loader.clear_cache()

# This is useful when transitioning between major game states
# (e.g., from menu to gameplay)
```

## Integration with UI Components

Example: Creating an image button

```python
from src.asset_loader import asset_loader
import pygame

class ImageButton:
    def __init__(self, x, y, image_path, hover_image_path=None):
        self.rect = pygame.Rect(x, y, 0, 0)
        self.normal_image = asset_loader.load_image(image_path)
        self.hover_image = asset_loader.load_image(hover_image_path) if hover_image_path else self.normal_image
        
        if self.normal_image:
            self.rect.size = self.normal_image.get_size()
        
        self.is_hovered = False
    
    def draw(self, screen):
        image = self.hover_image if self.is_hovered else self.normal_image
        if image:
            screen.blit(image, self.rect)
    
    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.is_hovered = self.rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if self.is_hovered:
                return True  # Button clicked
        return False
```

## Best Practices

1. **Organize assets logically**: Keep similar assets in the same directory
2. **Use consistent naming**: `item_name.png`, `item_name_hover.png`
3. **Optimize file sizes**: Compress images and audio files appropriately
4. **Preload frequently used assets**: Reduces loading time during gameplay
5. **Use configuration files**: Makes it easier to manage asset paths
6. **Test missing assets**: Ensure your code handles missing files gracefully
7. **Clear cache when needed**: Free memory when switching between game states

## Recommended File Formats

- **Images**: PNG (with transparency), JPG (photos/backgrounds)
- **Audio**: WAV (sound effects), MP3/OGG (background music)
- **Fonts**: TTF, OTF

## Example: Full Asset Setup

```python
# In game initialization
from src.asset_loader import asset_loader
from src.data_loader import data_loader

class Game:
    def __init__(self):
        # Preload assets from configuration
        preload_config = data_loader.get('assets', 'preload')
        if preload_config:
            asset_loader.preload_assets(preload_config)
        
        # Load UI assets
        self.button_img = asset_loader.load_image('ui/button.png')
        self.panel_img = asset_loader.load_image('ui/panel.png')
        
        # Load fonts
        self.title_font = asset_loader.load_font('title_font.ttf', 48)
        self.normal_font = asset_loader.load_font('game_font.ttf', 24)
        
        # Load sounds
        self.click_sound = asset_loader.load_sound('sfx/click.wav')
        
        # Load background music
        pygame.mixer.music.load(
            asset_loader.get_asset_path('sounds', 'bgm/gameplay.mp3')
        )
```
