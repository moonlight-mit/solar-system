"""
🌌 Solar System 3D - Backend Server
Physics-based simulation with NASA Horizons API integration
"""

from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import List, Optional, Dict
import numpy as np
from datetime import datetime, timedelta
import sqlite3
import json
import os
from pathlib import Path

# ==================== PHYSICS ENGINE ====================
class PhysicsEngine:
    """
    Realistic orbital mechanics calculations
    """
    # Constants
    G = 6.67430e-11  # Gravitational constant (m³/kg·s²)
    AU = 1.496e11    # Astronomical Unit (meters)
    DAY = 86400      # Seconds in a day
    YEAR = 365.25 * DAY  # Seconds in a year
    
    # Solar masses (kg)
    SUN_MASS = 1.989e30
    
    # Planet masses relative to Earth
    PLANET_MASSES = {
        'mercury': 0.055,
        'venus': 0.815,
        'earth': 1.0,
        'mars': 0.107,
        'jupiter': 317.8,
        'saturn': 95.2,
        'uranus': 14.5,
        'neptune': 17.1
    }
    
    # Semi-major axes (AU)
    ORBITAL_DISTANCES = {
        'mercury': 0.387,
        'venus': 0.723,
        'earth': 1.0,
        'mars': 1.524,
        'jupiter': 5.203,
        'saturn': 9.537,
        'uranus': 19.191,
        'neptune': 30.069
    }
    
    # Orbital periods (Earth years)
    ORBITAL_PERIODS = {
        'mercury': 0.241,
        'venus': 0.615,
        'earth': 1.0,
        'mars': 1.881,
        'jupiter': 11.862,
        'saturn': 29.457,
        'uranus': 84.011,
        'neptune': 164.79
    }
    
    # Planet radii (km)
    PLANET_RADII = {
        'sun': 696000,
        'mercury': 2440,
        'venus': 6052,
        'earth': 6371,
        'mars': 3390,
        'jupiter': 69911,
        'saturn': 58232,
        'uranus': 25362,
        'neptune': 24622
    }
    
    @staticmethod
    def calculate_distance(a: float, e: float, true_anomaly: float) -> float:
        """
        Calculate distance from focus (Sun) using orbital equation
        Parameters:
            a: Semi-major axis (AU)
            e: Eccentricity
            true_anomaly: True anomaly (radians)
        Returns: Distance in AU
        """
        return a * (1 - e**2) / (1 + e * np.cos(true_anomaly))
    
    @staticmethod
    def calculate_orbital_velocity(mass_sun: float, distance: float, gravity_factor: float = 1.0) -> float:
        """
        Calculate orbital velocity using Kepler's law
        v = sqrt(G*M/r)
        """
        distance_m = distance * PhysicsEngine.AU
        velocity = np.sqrt(gravity_factor * PhysicsEngine.G * mass_sun / distance_m)
        return velocity
    
    @staticmethod
    def calculate_gravitational_force(mass1: float, mass2: float, distance: float) -> float:
        """
        Calculate gravitational force between two bodies
        F = G * m1 * m2 / r²
        """
        distance_m = distance * PhysicsEngine.AU
        force = PhysicsEngine.G * mass1 * mass2 / (distance_m ** 2)
        return force
    
    @staticmethod
    def calculate_escape_velocity(mass: float, radius: float) -> float:
        """
        Calculate escape velocity
        v = sqrt(2GM/r)
        """
        return np.sqrt(2 * PhysicsEngine.G * mass / radius)
    
    @staticmethod
    def kepler_orbital_position(
        semi_major_axis: float,
        eccentricity: float,
        inclination: float,
        long_asc_node: float,
        arg_perihelion: float,
        mean_anomaly: float
    ) -> Dict[str, float]:
        """
        Calculate 3D Cartesian coordinates from Keplerian orbital elements
        
        Returns: {x, y, z} in AU
        """
        # Solve Kepler's equation for eccentric anomaly (E)
        # Using Newton-Raphson method
        E = mean_anomaly
        for _ in range(10):
            E = mean_anomaly + eccentricity * np.sin(E)
        
        # Calculate true anomaly
        true_anomaly = 2 * np.arctan2(
            np.sqrt(1 + eccentricity) * np.sin(E/2),
            np.sqrt(1 - eccentricity) * np.cos(E/2)
        )
        
        # Distance from focus
        r = semi_major_axis * (1 - eccentricity**2) / (1 + eccentricity * np.cos(true_anomaly))
        
        # Position in orbital plane
        x_orb = r * np.cos(true_anomaly)
        y_orb = r * np.sin(true_anomaly)
        z_orb = 0
        
        # Apply orbital element rotations (3D transformation)
        # 1. Rotation about z-axis by argument of perihelion
        cos_w = np.cos(arg_perihelion)
        sin_w = np.sin(arg_perihelion)
        x_rot1 = cos_w * x_orb - sin_w * y_orb
        y_rot1 = sin_w * x_orb + cos_w * y_orb
        z_rot1 = z_orb
        
        # 2. Rotation about x-axis by inclination
        cos_i = np.cos(inclination)
        sin_i = np.sin(inclination)
        x_rot2 = x_rot1
        y_rot2 = cos_i * y_rot1 - sin_i * z_rot1
        z_rot2 = sin_i * y_rot1 + cos_i * z_rot1
        
        # 3. Rotation about z-axis by longitude of ascending node
        cos_Ω = np.cos(long_asc_node)
        sin_Ω = np.sin(long_asc_node)
        x = cos_Ω * x_rot2 - sin_Ω * y_rot2
        y = sin_Ω * x_rot2 + cos_Ω * y_rot2
        z = z_rot2
        
        return {'x': x, 'y': y, 'z': z, 'distance': r}


# ==================== NASA HORIZONS API ====================
class NASAHorizonsClient:
    """
    Interface with NASA Horizons API for real celestial body data
    """
    def __init__(self):
        self.base_url = "https://ssd.jpl.nasa.gov/api/horizons.api"
        self.cache_file = "nasa_horizons_cache.json"
        self.cache_duration = 86400  # 24 hours
    
    def get_planet_coordinates(
        self,
        planet_id: str,
        date: Optional[datetime] = None
    ) -> Dict[str, float]:
        """
        Fetch real planet coordinates from NASA Horizons
        Planet IDs: 1=Mercury, 2=Venus, 3=Earth, 4=Mars, 5=Jupiter, etc.
        """
        if date is None:
            date = datetime.utcnow()
        
        try:
            import requests
            
            planet_map = {
                'mercury': '1', 'venus': '2', 'earth': '399',
                'mars': '4', 'jupiter': '5', 'saturn': '6',
                'uranus': '7', 'neptune': '8', 'sun': '10'
            }
            
            obj_id = planet_map.get(planet_id.lower(), '399')
            
            params = {
                'format': 'json',
                'COMMAND': f"'{obj_id}'",
                'EPHEM_TYPE': 'vectors',
                'OUT_UNITS': 'AU-D',
                'QUANTITIES': '1,2,3',  # 1=position, 2=velocity, 3=range
                'CSV_FORMAT': 'YES',
                'SCENE': 'heliocentre',
                'REF_SYSTEM': 'ICRF',
                'VECT_TABLE': '2',
                'START_TIME': date.strftime('%Y-%m-%d'),
                'STOP_TIME': (date + timedelta(days=1)).strftime('%Y-%m-%d'),
                'STEP_SIZE': '1d'
            }
            
            response = requests.get(self.base_url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            if data.get('result'):
                result = data['result'].split('\n')
                # Parse vector data (X, Y, Z)
                for line in result:
                    if ',' in line and not line.startswith('$$'):
                        coords = line.split(',')[3:6]
                        return {
                            'x': float(coords[0]),
                            'y': float(coords[1]),
                            'z': float(coords[2]),
                            'source': 'NASA Horizons',
                            'date': date.isoformat()
                        }
        
        except Exception as e:
            print(f"NASA API Error: {e}")
            return None
    
    def get_planet_ephemeris(self, planet_id: str, days: int = 30) -> List[Dict]:
        """
        Get ephemeris data for planet trajectory
        """
        ephemeris_data = []
        current_date = datetime.utcnow()
        
        for i in range(0, days, 7):  # Get weekly data
            data = self.get_planet_coordinates(planet_id, current_date + timedelta(days=i))
            if data:
                ephemeris_data.append(data)
        
        return ephemeris_data


# ==================== DATABASE ====================
class Database:
    """SQLite database for storing user-created systems"""
    
    def __init__(self, db_file: str = "solar_systems.db"):
        self.db_file = db_file
        self.init_db()
    
    def init_db(self):
        """Initialize database tables"""
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_systems (
                id INTEGER PRIMARY KEY,
                name TEXT UNIQUE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                data TEXT,
                star_mass REAL DEFAULT 1.0,
                gravity_factor REAL DEFAULT 1.0
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_planets (
                id INTEGER PRIMARY KEY,
                system_id INTEGER,
                name TEXT,
                distance REAL,
                mass REAL,
                radius REAL,
                eccentricity REAL DEFAULT 0.0,
                inclination REAL DEFAULT 0.0,
                color TEXT,
                FOREIGN KEY(system_id) REFERENCES user_systems(id)
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def save_system(self, name: str, data: Dict, star_mass: float = 1.0, gravity_factor: float = 1.0) -> int:
        """Save a custom solar system"""
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        
        try:
            cursor.execute(
                'INSERT INTO user_systems (name, data, star_mass, gravity_factor) VALUES (?, ?, ?, ?)',
                (name, json.dumps(data), star_mass, gravity_factor)
            )
            conn.commit()
            system_id = cursor.lastrowid
            return system_id
        except sqlite3.IntegrityError:
            raise ValueError(f"System '{name}' already exists")
        finally:
            conn.close()
    
    def load_system(self, system_id: int) -> Optional[Dict]:
        """Load a custom solar system"""
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM user_systems WHERE id = ?', (system_id,))
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return {
                'id': row[0],
                'name': row[1],
                'created_at': row[2],
                'data': json.loads(row[3]),
                'star_mass': row[4],
                'gravity_factor': row[5]
            }
        return None
    
    def list_systems(self) -> List[Dict]:
        """List all user systems"""
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        cursor.execute('SELECT id, name, created_at, star_mass, gravity_factor FROM user_systems')
        rows = cursor.fetchall()
        conn.close()
        
        return [
            {
                'id': row[0],
                'name': row[1],
                'created_at': row[2],
                'star_mass': row[3],
                'gravity_factor': row[4]
            }
            for row in rows
        ]


# ==================== FASTAPI APP ====================
app = FastAPI(
    title="🌌 Solar System Physics Engine",
    description="Real physics-based orbital simulation with NASA Horizons integration",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files (templates, js, css)
templates_dir = Path(__file__).parent / "templates"
if templates_dir.exists():
    app.mount("/static", StaticFiles(directory=str(templates_dir)), name="static")

# Initialize components
physics = PhysicsEngine()
nasa_client = NASAHorizonsClient()
db = Database()


# ==================== MODELS ====================
class PlanetData(BaseModel):
    """Planet configuration"""
    name: str
    distance: float  # AU
    mass: float      # Earth masses
    radius: float    # km
    eccentricity: float = 0.0
    inclination: float = 0.0
    long_asc_node: float = 0.0
    arg_perihelion: float = 0.0
    mean_anomaly: float = 0.0
    color: str = "#ffffff"


class CustomSystem(BaseModel):
    """Custom solar system"""
    name: str
    planets: List[PlanetData]
    star_mass_factor: float = 1.0
    gravity_factor: float = 1.0


# ==================== ENDPOINTS ====================

@app.get("/solar_api.js")
async def serve_solar_api():
    """Serve solar_api.js"""
    api_file = Path(__file__).parent / "solar_api.js"
    if api_file.exists():
        return FileResponse(str(api_file), media_type="application/javascript")
    raise HTTPException(status_code=404, detail="solar_api.js not found")


@app.get("/")
async def root():
    """Serve main HTML file"""
    html_file = Path(__file__).parent / "templates" / "index.html"
    
    if html_file.exists():
        try:
            return FileResponse(str(html_file), media_type="text/html")
        except Exception as e:
            print(f"FileResponse error: {e}")
            import traceback
            traceback.print_exc()
    
    # Fallback API response
    return {
        "status": "🌌 Solar System Physics Engine Running",
        "version": "1.0.0",
        "features": [
            "Real orbital mechanics",
            "NASA Horizons API integration",
            "Custom system creation",
            "Physics simulations"
        ]
    }


@app.post("/api/calculate-position")
async def calculate_position(
    planet: str,
    date: Optional[str] = None,
    use_nasa: bool = False
):
    """
    Calculate planet position at given date
    
    Parameters:
    - planet: Planet name (mercury, venus, earth, etc.)
    - date: ISO format date (default: now)
    - use_nasa: Use NASA Horizons API (default: False)
    """
    try:
        if use_nasa:
            try:
                date_obj = datetime.fromisoformat(date) if date else None
                coords = nasa_client.get_planet_coordinates(planet, date_obj)
                if coords:
                    return {"success": True, "data": coords}
            except Exception as e:
                print(f"NASA API failed, falling back to calculation: {e}")
        
        # Calculate from orbital elements
        distance = physics.ORBITAL_DISTANCES.get(planet.lower(), 1.0)
        period = physics.ORBITAL_PERIODS.get(planet.lower(), 1.0)
        
        # Current date
        if date:
            current_date = datetime.fromisoformat(date)
        else:
            current_date = datetime.utcnow()
        
        # Time since epoch (days)
        days_since_epoch = (current_date - datetime(2000, 1, 1)).days
        
        # Mean anomaly (radians per day)
        mean_anomaly = (days_since_epoch * 2 * np.pi) / (period * 365.25)
        
        # Use simplified circular orbit for fast calculation
        x = distance * np.cos(mean_anomaly)
        y = distance * np.sin(mean_anomaly)
        z = 0
        
        return {
            "success": True,
            "planet": planet,
            "date": current_date.isoformat(),
            "position": {"x": float(x), "y": float(y), "z": float(z)},
            "distance_au": float(distance),
            "source": "calculated"
        }
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/api/orbital-velocity")
async def calculate_orbital_velocity(
    planet: str,
    sun_mass_factor: float = 1.0,
    gravity_factor: float = 1.0
):
    """Calculate orbital velocity of a planet"""
    try:
        distance = physics.ORBITAL_DISTANCES.get(planet.lower(), 1.0)
        sun_mass = physics.SUN_MASS * sun_mass_factor
        
        velocity = physics.calculate_orbital_velocity(sun_mass, distance, gravity_factor)
        
        return {
            "success": True,
            "planet": planet.capitalize(),
            "velocity_ms": float(velocity),
            "velocity_kms": float(velocity / 1000),
            "distance_au": float(distance)
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


@app.post("/api/gravitational-force")
async def calculate_force(
    planet1: str,
    planet2: str,
    distance_au: float
):
    """Calculate gravitational force between two planets"""
    try:
        masses = {
            'sun': physics.SUN_MASS,
            'mercury': physics.SUN_MASS * physics.PLANET_MASSES['mercury'],
            'venus': physics.SUN_MASS * physics.PLANET_MASSES['venus'],
            'earth': physics.SUN_MASS * physics.PLANET_MASSES['earth'],
            'mars': physics.SUN_MASS * physics.PLANET_MASSES['mars'],
            'jupiter': physics.SUN_MASS * physics.PLANET_MASSES['jupiter'],
            'saturn': physics.SUN_MASS * physics.PLANET_MASSES['saturn'],
            'uranus': physics.SUN_MASS * physics.PLANET_MASSES['uranus'],
            'neptune': physics.SUN_MASS * physics.PLANET_MASSES['neptune'],
        }
        
        mass1 = masses.get(planet1.lower())
        mass2 = masses.get(planet2.lower())
        
        if not mass1 or not mass2:
            return {"success": False, "error": "Invalid planet names"}
        
        force = physics.calculate_gravitational_force(mass1, mass2, distance_au)
        
        return {
            "success": True,
            "planet1": planet1.capitalize(),
            "planet2": planet2.capitalize(),
            "distance_au": distance_au,
            "force_newtons": float(force),
            "force_scientific": f"{force:.2e} N"
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


@app.post("/api/escape-velocity")
async def calculate_escape_velocity(planet: str):
    """Calculate escape velocity from a planet's surface"""
    try:
        mass_map = {
            'sun': physics.SUN_MASS,
            **{name: physics.SUN_MASS * mass for name, mass in physics.PLANET_MASSES.items()}
        }
        
        mass = mass_map.get(planet.lower())
        radius = physics.PLANET_RADII.get(planet.lower())
        
        if not mass or not radius:
            return {"success": False, "error": f"Unknown planet: {planet}"}
        
        escape_vel = physics.calculate_escape_velocity(mass, radius * 1000)
        
        return {
            "success": True,
            "planet": planet.capitalize(),
            "escape_velocity_ms": float(escape_vel),
            "escape_velocity_kms": float(escape_vel / 1000),
            "radius_km": float(radius)
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


@app.post("/api/kepler-position")
async def kepler_position(
    planet: str,
    date: Optional[str] = None,
    physical_params: Optional[dict] = None
):
    """
    Calculate position using full Keplerian orbital elements
    For high-precision calculations
    """
    try:
        # Default orbital elements for planets (simplified)
        orbital_elements = {
            'mercury': {'a': 0.387, 'e': 0.206, 'i': 0.122, 'Ω': 0.843, 'ω': 0.508, 'M': 4.402},
            'venus': {'a': 0.723, 'e': 0.007, 'i': 0.059, 'Ω': 1.338, 'ω': 2.296, 'M': 3.176},
            'earth': {'a': 1.0, 'e': 0.017, 'i': 0.0, 'Ω': 0.0, 'ω': 1.991, 'M': 1.796},
            'mars': {'a': 1.524, 'e': 0.093, 'i': 0.032, 'Ω': 0.865, 'ω': 5.865, 'M': 6.203},
        }
        
        elements = orbital_elements.get(planet.lower())
        if not elements:
            raise ValueError(f"Orbital data not available for {planet}")
        
        # If date provided, adjust mean anomaly
        if date:
            date_obj = datetime.fromisoformat(date)
            days_since_epoch = (date_obj - datetime(2000, 1, 1)).days
            period_years = physics.ORBITAL_PERIODS.get(planet.lower(), 1.0)
            elements['M'] += (days_since_epoch / 365.25) * (2 * np.pi / period_years)
        
        position = physics.kepler_orbital_position(
            elements['a'], elements['e'], elements['i'],
            elements['Ω'], elements['ω'], elements['M']
        )
        
        return {
            "success": True,
            "planet": planet,
            "position": position,
            "date": date or datetime.utcnow().isoformat(),
            "method": "Kepler orbital elements"
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/api/systems/create")
async def create_custom_system(system: CustomSystem):
    """Create and save a custom solar system"""
    try:
        system_data = {
            'planets': [planet.dict() for planet in system.planets],
            'star_mass_factor': system.star_mass_factor,
            'gravity_factor': system.gravity_factor
        }
        
        system_id = db.save_system(
            system.name,
            system_data,
            system.star_mass_factor,
            system.gravity_factor
        )
        
        return {
            "success": True,
            "system_id": system_id,
            "name": system.name,
            "planet_count": len(system.planets),
            "message": f"System '{system.name}' created successfully"
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/api/systems/list")
async def list_systems():
    """List all saved custom systems"""
    try:
        systems = db.list_systems()
        return {
            "success": True,
            "systems": systems,
            "count": len(systems)
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/api/systems/{system_id}")
async def get_system(system_id: int):
    """Get a specific custom system"""
    try:
        system = db.load_system(system_id)
        if not system:
            raise HTTPException(status_code=404, detail="System not found")
        return {"success": True, "system": system}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/api/planet-data/{planet}")
async def get_planet_data(planet: str):
    """Get comprehensive data for a planet"""
    try:
        planet_lower = planet.lower()
        
        if planet_lower not in physics.ORBITAL_DISTANCES:
            raise HTTPException(status_code=404, detail=f"Planet '{planet}' not found")
        
        return {
            "success": True,
            "planet": planet,
            "distance_au": physics.ORBITAL_DISTANCES.get(planet_lower),
            "period_years": physics.ORBITAL_PERIODS.get(planet_lower),
            "mass_earth_masses": physics.PLANET_MASSES.get(planet_lower),
            "radius_km": physics.PLANET_RADII.get(planet_lower),
            "orbital_velocity_ms": physics.calculate_orbital_velocity(
                physics.SUN_MASS,
                physics.ORBITAL_DISTANCES.get(planet_lower)
            )
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# ==================== MAIN ====================
if __name__ == "__main__":
    import uvicorn
    import sys
    import os
    # Fix Unicode encoding for Windows console
    if sys.platform == "win32":
        # Use UTF-8 encoding for stdout
        import io
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    
    print("[*] Starting Solar System Physics Engine...")
    print("[*] Server running at: http://127.0.0.1:9000")
    uvicorn.run(
        app,
        host="127.0.0.1",
        port=9000,
        log_level="info",
        access_log=False
    )
