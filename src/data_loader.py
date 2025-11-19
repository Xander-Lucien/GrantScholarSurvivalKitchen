# -*- coding: utf-8 -*-
"""
Data Loader
Load and manage all JSON configuration files
"""

import json
import os
from pathlib import Path


class DataLoader:
    """Data loader for managing all game configuration"""
    
    _instance = None
    _data = {}
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DataLoader, cls).__new__(cls)
            cls._instance._load_all_data()
        return cls._instance
    
    def _load_all_data(self):
        """Load all JSON configuration files"""
        # Get the data directory path
        base_dir = Path(__file__).parent.parent
        data_dir = base_dir / "data"
        
        # Load all JSON files
        json_files = {
            "config": "config.json",
            "stats": "stats.json",
            "items": "items.json",
            "recipes": "recipes.json",
            "events": "events.json"
        }
        
        for key, filename in json_files.items():
            file_path = data_dir / filename
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    self._data[key] = json.load(f)
            except FileNotFoundError:
                print(f"Warning: {filename} not found. Using empty data.")
                self._data[key] = {}
            except json.JSONDecodeError as e:
                print(f"Error parsing {filename}: {e}")
                self._data[key] = {}
    
    def get(self, category, *keys, default=None):
        """
        Get configuration value
        
        Args:
            category: Data category (config, stats, items, recipes, events)
            *keys: Keys to traverse the nested dictionary
            default: Default value if key not found
            
        Returns:
            Configuration value
        """
        data = self._data.get(category, {})
        
        for key in keys:
            if isinstance(data, dict):
                data = data.get(key, default)
            else:
                return default
                
        return data if data is not None else default
    
    def get_all(self, category):
        """Get all data for a category"""
        return self._data.get(category, {})
    
    def reload(self):
        """Reload all configuration files"""
        self._data = {}
        self._load_all_data()


# Create singleton instance
data_loader = DataLoader()
