# Project Structure

This document describes the structure and organization of the Grant Scholar's Survival Kitchen project.

## Directory Structure

```
GrantScholarSurvivalKitchen/
├── data/                      # Game configuration data (JSON)
│   ├── config.json           # Window, colors, game settings
│   ├── stats.json            # Player attributes configuration
│   ├── items.json            # Ingredients and restaurant menu
│   ├── recipes.json          # Cooking recipes
│   └── events.json           # Game events data
│
├── src/                       # Source code
│   ├── __init__.py           # Package initialization
│   ├── data_loader.py        # JSON data loader (Singleton)
│   ├── config.py             # Configuration constants
│   ├── player.py             # Player class
│   ├── events.py             # Event system
│   ├── scenes.py             # Scene management
│   ├── ui.py                 # UI components
│   └── game.py               # Main game controller
│
├── main.py                    # Program entry point
├── requirements.txt           # Python dependencies
├── setup.py                   # Package setup script
├── pyproject.toml            # Modern Python project configuration
├── MANIFEST.in               # Package manifest
├── .gitignore                # Git ignore rules
├── README.md                 # Project documentation
└── PROJECT_STRUCTURE.md      # This file
```

## Module Description

### Data Layer (`data/`)

All game configuration is stored in JSON format for easy modification by designers and planners:

- **config.json**: Window settings, colors, game parameters
- **stats.json**: Initial values, stat ranges, mood levels, warnings
- **items.json**: Ingredients (with price, location, shelf life), restaurant menu
- **recipes.json**: Cooking recipes (ingredients, effects, stamina cost)
- **events.json**: Fixed events, condition events, random events

### Core Layer (`src/`)

#### `data_loader.py`
- Singleton pattern data loader
- Loads all JSON configuration files at startup
- Provides unified interface for accessing configuration data
- Supports nested key access: `data_loader.get("config", "window", "width")`

#### `config.py`
- Loads configuration from JSON files
- Provides convenient constants (WINDOW_WIDTH, COLORS, etc.)
- Helper functions for accessing different data types

#### `player.py`
- Player class managing all attributes
- Inventory management
- Expired item checking
- Status warning system
- All numerical values loaded from configuration

#### `events.py`
- Event system managing three types of events:
  - Fixed events (triggered on specific days)
  - Condition events (triggered when conditions met)
  - Random events (weighted random selection)
- Event result processing and application

#### `scenes.py`
- Three scene types:
  - **MainScene**: Regular game flow and event display
  - **ShoppingScene**: Market, convenience store, restaurant
  - **KitchenScene**: Cooking interface
- All item data loaded from JSON configuration

#### `ui.py`
- UI components: Button, TextBox, StatusBar, ItemSlot
- Text rendering helpers
- Event handling

#### `game.py`
- Main game controller
- Time period flow management
- Scene switching
- Game state management (playing/win/lose)

## Configuration Modification Guide

### For Designers/Planners

You can modify game balance and content by editing JSON files in the `data/` directory:

#### 1. Adjust Player Stats (`stats.json`)
```json
{
  "initial_values": {
    "money": 1500,    // Starting money
    "stamina": 100,   // Starting stamina
    // ...
  }
}
```

#### 2. Add/Modify Items (`items.json`)
```json
{
  "ingredients": {
    "New Item": {
      "price": 10,
      "location": "Market",
      "shelf_life": 5,
      "description": "Description"
    }
  }
}
```

#### 3. Create New Recipes (`recipes.json`)
```json
{
  "recipes": {
    "New Recipe": {
      "ingredients": {"Item1": 1, "Item2": 1},
      "effects": {"satiety": 40, "health": 5},
      "stamina_cost": 10,
      "description": "Recipe description"
    }
  }
}
```

#### 4. Add Events (`events.json`)
```json
{
  "random_events": {
    "Morning": [
      {
        "name": "New Event",
        "type": "good",
        "description": "Event description",
        "result": {"stamina": 10, "mood": 1}
      }
    ]
  }
}
```

## Development Guide

### Adding New Features

1. **Add new data structure**: Create/modify JSON files in `data/`
2. **Update data loader**: Add getter methods in `config.py` if needed
3. **Implement logic**: Add functionality in appropriate modules
4. **Update UI**: Modify scenes or create new UI components

### Code Style

- Use docstrings for all classes and functions
- Follow PEP 8 style guide
- Keep functions focused and modular
- Use meaningful variable names

### Testing

After modifications, test:
1. Game launches without errors
2. All configurations load correctly
3. Game flow works as expected
4. Save/load functionality (if implemented)

## Build and Distribution

### Development Mode
```bash
pip install -e .
```

### Build Package
```bash
python setup.py sdist bdist_wheel
```

### Install Package
```bash
pip install dist/grant-scholar-survival-kitchen-1.0.0.tar.gz
```

## Future Improvements

Potential areas for enhancement:
- [ ] Save/load system
- [ ] Achievement system
- [ ] More events and recipes
- [ ] Sound effects and music
- [ ] Localization support
- [ ] Difficulty levels
- [ ] Extended gameplay modes
