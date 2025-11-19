# Assets Directory

This directory contains all art and multimedia assets for the game.

## Directory Structure

```
assets/
├── images/          # Image assets (PNG, JPG)
├── sounds/          # Audio assets (WAV, MP3, OGG)
└── fonts/           # Font files (TTF, OTF)
```

## Getting Started

### Adding Your Assets

1. **Images**: Place image files in `images/` subdirectories:
   - `images/ui/` - UI elements, buttons, icons
   - `images/characters/` - Character sprites
   - `images/items/` - Food items, ingredients
   - `images/backgrounds/` - Scene backgrounds

2. **Sounds**: Place audio files in `sounds/` subdirectories:
   - `sounds/bgm/` - Background music
   - `sounds/sfx/` - Sound effects

3. **Fonts**: Place font files directly in `fonts/`

### Asset Naming Convention

Use lowercase with underscores:
- ✓ `instant_noodles.png`
- ✓ `click_sound.wav`
- ✗ `Instant Noodles.png`
- ✗ `Click Sound.wav`

## Recommended Asset Specifications

### Images

- **UI Elements**: PNG with transparency, 72-150 DPI
  - Buttons: 200x60 pixels (adjust as needed)
  - Icons: 64x64 or 128x128 pixels
  
- **Characters**: PNG with transparency
  - Sprite size: 64x64 to 128x128 pixels
  
- **Items**: PNG with transparency
  - Item icons: 64x64 pixels
  
- **Backgrounds**: JPG or PNG
  - Scene backgrounds: 1024x768 pixels (or higher)

### Audio

- **Sound Effects**: WAV format
  - Sample rate: 44100 Hz
  - Bit depth: 16-bit
  - Duration: < 2 seconds for most SFX
  
- **Background Music**: MP3 or OGG format
  - Bitrate: 128-192 kbps
  - Loopable (ensure seamless loop points)

### Fonts

- **Formats**: TTF or OTF
- **License**: Ensure fonts are licensed for game use
- **Recommended**: Include both regular and bold weights

## Example Assets List

Here's a suggested list of assets you might want to create:

### UI Assets (`images/ui/`)
- [ ] `button.png` - Default button
- [ ] `button_hover.png` - Button hover state
- [ ] `panel.png` - Background panel
- [ ] `icon_money.png` - Money icon
- [ ] `icon_stamina.png` - Stamina icon
- [ ] `icon_health.png` - Health icon
- [ ] `icon_satiety.png` - Satiety icon
- [ ] `icon_mood.png` - Mood icon

### Character Assets (`images/characters/`)
- [ ] `player.png` - Player character sprite
- [ ] `player_tired.png` - Tired state
- [ ] `player_happy.png` - Happy state

### Item Assets (`images/items/`)
- [ ] `instant_noodles.png`
- [ ] `egg.png`
- [ ] `tomato.png`
- [ ] `rice.png`
- [ ] `pork.png`
- [ ] `bento_a.png`
- [ ] `bento_b.png`

### Background Assets (`images/backgrounds/`)
- [ ] `dorm.png` - Dorm room
- [ ] `market.png` - Market scene
- [ ] `convenience_store.png` - Convenience store
- [ ] `kitchen.png` - Kitchen scene

### Sound Effects (`sounds/sfx/`)
- [ ] `click.wav` - Button click
- [ ] `purchase.wav` - Purchase confirmation
- [ ] `cooking.wav` - Cooking action
- [ ] `notification.wav` - Event notification
- [ ] `warning.wav` - Warning sound
- [ ] `gameover.wav` - Game over sound
- [ ] `victory.wav` - Victory sound

### Background Music (`sounds/bgm/`)
- [ ] `main_menu.mp3` - Main menu theme
- [ ] `gameplay.mp3` - Gameplay theme
- [ ] `tension.mp3` - Tense moments

### Fonts (`fonts/`)
- [ ] `game_font.ttf` - Main game font
- [ ] `title_font.ttf` - Title/header font

## Using Assets in Code

```python
from src.asset_loader import asset_loader

# Load an image
image = asset_loader.load_image('items/egg.png')

# Load a sound
sound = asset_loader.load_sound('sfx/click.wav')

# Load a font
font = asset_loader.load_font('game_font.ttf', 24)
```

For detailed usage, see [ASSET_GUIDE.md](../ASSET_GUIDE.md)

## Testing Assets

Run the asset example to test your assets:

```bash
python examples/asset_example.py
```

This will show which assets are loaded successfully and which are missing.

## Asset Sources

### Free Asset Resources

- **Graphics**:
  - [OpenGameArt.org](https://opengameart.org/)
  - [itch.io](https://itch.io/game-assets/free)
  - [Kenney.nl](https://kenney.nl/assets)

- **Sounds**:
  - [Freesound.org](https://freesound.org/)
  - [OpenGameArt.org](https://opengameart.org/)
  - [itch.io](https://itch.io/soundtracks/free)

- **Fonts**:
  - [Google Fonts](https://fonts.google.com/)
  - [DaFont](https://www.dafont.com/)
  - [FontSquirrel](https://www.fontsquirrel.com/)

**Important**: Always check the license before using any assets!

## Tips

1. **Organize assets early**: Set up your directory structure before creating assets
2. **Use consistent sizes**: Keep similar assets at the same dimensions
3. **Optimize file sizes**: Compress assets to reduce load times
4. **Test regularly**: Check that assets load correctly as you add them
5. **Keep backups**: Version control doesn't always work well with large binary files
6. **Document sources**: Keep track of where assets came from for licensing

## Need Help?

See the full documentation:
- [ASSET_GUIDE.md](../ASSET_GUIDE.md) - Detailed usage guide
- [PROJECT_STRUCTURE.md](../PROJECT_STRUCTURE.md) - Project organization

## License

Make sure all assets you add are appropriately licensed for use in this project.
