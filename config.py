"""
Configuration and utilities for the Solar System backend
"""

import os
from typing import Dict

# API Configuration
API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:9000")
API_TIMEOUT = 10

# NASA Horizons Configuration
NASA_API_ENABLED = os.getenv("NASA_API_ENABLED", "true").lower() == "true"
NASA_API_CACHE_DURATION = 86400  # 24 hours

# Database Configuration
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///solar_systems.db")
DATABASE_FILE = "solar_systems.db"

# Physics Presets
PHYSICS_PRESETS: Dict[str, Dict] = {
    "realistic": {
        "sun_mass_factor": 1.0,
        "gravity_factor": 1.0,
        "simulation_speed": 1.0,
        "name": "Realistic Solar System"
    },
    "high_gravity": {
        "sun_mass_factor": 1.5,
        "gravity_factor": 1.5,
        "simulation_speed": 1.0,
        "name": "High Gravity Universe"
    },
    "fast_orbits": {
        "sun_mass_factor": 1.0,
        "gravity_factor": 1.0,
        "simulation_speed": 10.0,
        "name": "Time-Accelerated (10x)"
    },
    "binary_star": {
        "sun_mass_factor": 2.0,
        "gravity_factor": 1.0,
        "simulation_speed": 1.0,
        "name": "Binary Star System"
    },
    "low_gravity": {
        "sun_mass_factor": 0.5,
        "gravity_factor": 0.5,
        "simulation_speed": 1.0,
        "name": "Low Gravity Universe"
    }
}

# Planet color mapping (for frontend)
PLANET_COLORS: Dict[str, str] = {
    'sun': '#ffaa33',
    'mercury': '#aaaaaa',
    'venus': '#e6b800',
    'earth': '#2277ff',
    'mars': '#cc5533',
    'jupiter': '#d8a27a',
    'saturn': '#e8d4a8',
    'uranus': '#afdbdb',
    'neptune': '#4a6da8'
}

# Logging Configuration
DEBUG = os.getenv("DEBUG", "false").lower() == "true"
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

# ---  Models for common requests ---
PLANET_NAMES = [
    'mercury', 'venus', 'earth', 'mars',
    'jupiter', 'saturn', 'uranus', 'neptune'
]

def get_preset(preset_name: str) -> Dict:
    """Get physics preset by name"""
    return PHYSICS_PRESETS.get(preset_name.lower(), PHYSICS_PRESETS["realistic"])

def get_planet_color(planet: str) -> str:
    """Get color for a planet"""
    return PLANET_COLORS.get(planet.lower(), '#ffffff')
