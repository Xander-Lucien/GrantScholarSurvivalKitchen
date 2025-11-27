# Grant Scholar's Survival Kitchen

A survival simulation game built with Pygame.

## Game Overview

Grant Scholar has only 30 days until graduation, but only $1500 left for living expenses! Help him manage his diet, balance various attributes, and survive these 30 days to graduate successfully.

## Project Features

### 🎯 Professional Engineering Structure
- **Data-Driven Design**: All game configurations use JSON files for easy balancing
- **Asset Management System**: Complete art resource loading and caching system supporting images, audio, and fonts
- **Modular Architecture**: Code organized by functionality for easy maintenance and extension
- **Singleton Data Loader**: Unified management of all configuration file loading and access
- **Standard Python Package**: Includes setup.py, pyproject.toml and other standard configurations

### 🎮 Game Features
- **Five-Attribute System**: Stamina, Mood, Health, Satiety, Money
- **Rich Event System**: Fixed events, conditional events, random events
- **Cooking System**: Purchase ingredients and prepare various dishes
- **Time Management**: Each day divided into six periods: Morning, Daytime, Shopping, Cooking, Evening, Sleep

## Project Structure

```
GrantScholarSurvivalKitchen/
├── assets/                # Art and multimedia assets
│   ├── images/           # Image resources
│   ├── sounds/           # Audio resources
│   └── fonts/            # Font files
├── data/                  # Game configuration data (JSON format)
│   ├── config.json       # Window, colors, game settings
│   ├── stats.json        # Player attributes configuration
│   ├── items.json        # Ingredients and restaurant menu
│   ├── recipes.json      # Cooking recipes
│   ├── events.json       # Game events
│   └── assets.json       # Asset path configuration
├── src/                   # Source code
│   ├── data_loader.py    # Data loader
│   ├── asset_loader.py   # Asset loader
│   ├── config.py         # Configuration constants
│   ├── player.py         # Player class
│   ├── events.py         # Event system
│   ├── scenes.py         # Scene management
│   ├── ui.py             # UI components
│   └── game.py           # Main game controller
├── main.py               # Program entry point
└── ...
```

For detailed information, see [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md)

## Art Assets

### Asset Directory Structure

The game supports a complete art asset system. Asset files are stored in the `assets/` directory:

- `assets/images/` - Image resources (UI, characters, items, backgrounds)
- `assets/sounds/` - Audio resources (background music, sound effects)
- `assets/fonts/` - Font files

### Adding Assets

1. Place image files in the appropriate `assets/images/` subdirectory
2. Place audio files in the appropriate `assets/sounds/` subdirectory
3. Place font files in the `assets/fonts/` directory

Using assets in code:
```python
from src.asset_loader import asset_loader

# Load image
image = asset_loader.load_image('items/egg.png')

# Load sound
sound = asset_loader.load_sound('sfx/click.wav')

# Load font
font = asset_loader.load_font('game_font.ttf', 24)
```

For detailed guides:
- [assets/README.md](assets/README.md) - Asset directory documentation
- [ASSET_GUIDE.md](ASSET_GUIDE.md) - Complete usage guide

## Quick Start for Game Designers

### Modifying Game Values

All game data is stored in JSON files in the `data/` directory. You can directly edit:

1. **Adjust player initial attributes** (`data/stats.json`)
2. **Add new ingredients** (`data/items.json`)
3. **Create new recipes** (`data/recipes.json`)
4. **Design new events** (`data/events.json`)
5. **Modify game parameters** (`data/config.json`)

### Example: Adding New Ingredient

Edit `data/items.json`:
```json
{
  "ingredients": {
    "New Ingredient": {
      "price": 10,
      "location": "Market",
      "shelf_life": 5,
      "description": "Description"
    }
  }
}
```

Changes take effect immediately - no recompilation needed!

For detailed configuration guide, see [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md)

## Installation

### Method 1: Direct Installation

1. Clone the repository:
```bash
git clone https://github.com/Xander-Lucien/GrantScholarSurvivalKitchen.git
cd GrantScholarSurvivalKitchen
```

2. Create virtual environment (recommended):
```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# Linux/Mac
source .venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run the game:
```bash
python main.py
```

### Method 2: Install as Package

```bash
# Install in development mode
pip install -e .

# Or install directly
pip install .

# Run the game
grant-scholar
```

## Running the Game

### Windows
```bash
# Using virtual environment Python
.venv\Scripts\python.exe main.py

# Or double-click to run
run_game.bat
```

### Linux/Mac
```bash
python main.py
```

## Gameplay

### Attributes

- **Stamina (0-100)**: Consumed by cooking and other activities, restored by sleep
- **Mood (5 levels)**: Affects random event trigger probability
- **Health (0-100)**: Game over when it reaches zero
- **Satiety (0-100)**: Decreases over time, continuous health damage when zero
- **Money**: Spent on purchasing ingredients

### Daily Flow

1. **Morning**: Check status, trigger random events
2. **Daytime**: Encounter fixed events or random events
3. **Shopping**: Choose Market, Convenience Store, Restaurant, or skip shopping
4. **Cooking**: Cook dishes with available ingredients (multiple times)
5. **Evening**: Sleep early / Relax / Stay up late
6. **Sleep**: Restore stamina, proceed to next day

### Ingredients & Recipes

#### Ingredients
- Instant Noodles, Egg, Tomato, Rice, Pork (Market)
- Bento A, Bento B (Convenience Store)
- Roast Goose Rice (Restaurant - direct consumption)

#### Recipes
- Boiled Noodles, Noodles with Egg
- Tomato Scrambled Eggs, Clay Pot Rice
- Bento A/B (direct consumption)

### Game Objective

Keep health above zero for 30 days to graduate successfully!

## Controls

- Left Mouse Button: Select options / Purchase items
- Right Mouse Button (Shopping interface): Cancel selected items

## Development Info

- Language: Python
- Engine: Pygame
- Version: 1.0

## Notes

- Ingredients have expiration dates and will be automatically discarded when expired
- Running out of stamina forces sleep and deducts mood and health
- Three consecutive days of low mood triggers family care event
- Plan your budget carefully to avoid running out of money

Enjoy the game!
