# 🌌 Solar System 3D - Enhanced Physics Model

A comprehensive, physics-based solar system simulation with NASA Horizons integration and real-time calculations.

## 📋 Features

### 🎨 Visual  Interface
- **3D Interactive Visualization**: Three.js-powered orbital simulation
- **2D Top-Down View**: Alternative visualization mode
- **Real-time Rendering**: Smooth 60 FPS animation
- **Multiple Camera Angles**: Follow planets, Earth-view, custom angles

### 🔬 Physics Engine
- **Kepler Orbital Mechanics**: Full 6-parameter orbital elements
- **Gravitational Calculations**: Newton's law of universal gravitation
- **Escape Velocity**: Calculate for any celestial body
- **Orbital Resonance Detection**: Identify harmonic relationships
- **Tidal Forces**: Calculate gravitational tidal effects
- **Roche Limit**: Determine planet fragmentation boundaries

### 🛰️ NASA Integration
- **Horizons API**: Real celestial body coordinates
- **Ephemeris Data**: Historical and predictive trajectories
- **Automatic Caching**: 24-hour cache for offline use

### 🎮 Interactive Panels
- **Physics Lab** 🔭: Calculate orbital velocities, gravitational forces, escape velocities
- **Experiment Station** 🔬: Weight calculations, size comparisons
- **Challenges** 🎮: Educational games and quizzes
- **Library** 📚: Historical events and NASA images

### 💾 User Features
- **Custom Solar Systems**: Create and save your own systems
- **Parameter Adjustment**: Modify sun mass, gravity factor, simulation speed
- **Real-time Calculations**: Backend physics engine integration
- **Database Storage**: SQLite persistence

---

## 🚀 Installation & Setup

### Prerequisites
- Python 3.8+
- Node.js 14+ (optional, if running frontend separately)
- Modern web browser (Chrome, Firefox, Edge)

### Step 1: Install Python Dependencies

```bash
# Navigate to project directory
cd "d:\tryyyyyyyyy solar2copy"

# Create virtual environment (recommended)
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install packages
pip install -r requirements.txt
```

### Step 2: Run the Backend Server

```bash
# Start FastAPI server
python app.py

# Server will start at http://localhost:8000
# API docs available at http://localhost:8000/docs
```

### Step 3: Open the Frontend

```bash
# Open in browser
# File path: file:///d:/tryyyyyyyyy%20solar2copy/templates/index.html
# Or if using a local server, point to: http://localhost:8000/templates/index.html
```

---

## 📡 API Endpoints

### Physics Calculations

#### 1. Calculate Orbital Position
```http
POST /api/calculate-position
Content-Type: application/json

{
  "planet": "earth",
  "date": "2026-04-09",
  "use_nasa": false
}
```

**Response:**
```json
{
  "success": true,
  "planet": "earth",
  "position": {"x": 0.983, "y": 0.184, "z": -0.001},
  "distance_au": 1.0
}
```

#### 2. Calculate Orbital Velocity
```http
POST /api/orbital-velocity
Content-Type: application/json

{
  "planet": "earth",
  "sun_mass_factor": 1.0,
  "gravity_factor": 1.0
}
```

**Response:**
```json
{
  "success": true,
  "planet": "earth",
  "velocity_ms": 29785.4,
  "velocity_kms": 29.79,
  "distance_au": 1.0
}
```

#### 3. Calculate Gravitational Force
```http
POST /api/gravitational-force
Content-Type: application/json

{
  "planet1": "sun",
  "planet2": "earth",
  "distance_au": 1.0
}
```

**Response:**
```json
{
  "success": true,
  "planet1": "sun",
  "planet2": "earth",
  "force_newtons": 3.54e22,
  "force_scientific": "3.54e+22 N"
}
```

#### 4. Calculate Escape Velocity
```http
POST /api/escape-velocity
Content-Type: application/json

{
  "planet": "earth"
}
```

**Response:**
```json
{
  "success": true,
  "planet": "earth",
  "escape_velocity_kms": 11.19,
  "radius_km": 6371.0
}
```

#### 5. Kepler Orbital Position (High Precision)
```http
POST /api/kepler-position
Content-Type: application/json

{
  "planet": "earth",
  "date": "2026-04-09"
}
```

### Custom Systems

#### 6. Create Custom System
```http
POST /api/systems/create
Content-Type: application/json

{
  "name": "My Binary Star System",
  "star_mass_factor": 2.0,
  "gravity_factor": 1.0,
  "planets": [
    {
      "name": "Planet A",
      "distance": 1.5,
      "mass": 1.0,
      "radius": 6371,
      "eccentricity": 0.1,
      "color": "#2277ff"
    }
  ]
}
```

#### 7. List Systems
```http
GET /api/systems/list
```

#### 8. Get System Details
```http
GET /api/systems/{system_id}
```

#### 9. Get Planet Data
```http
GET /api/planet-data/earth
```

---

## 🧮 Physics Formulas Used

### Kepler's Third Law
$$T^2 = \frac{4\pi^2 a^3}{GM}$$

Where:
- $T$ = Orbital period
- $a$ = Semi-major axis
- $G$ = Gravitational constant
- $M$ = Mass of central body

### Orbital Velocity
$$v = \sqrt{\frac{GM}{r}}$$

### Gravitational Force
$$F = G \frac{m_1 m_2}{r^2}$$

### Escape Velocity
$$v_e = \sqrt{\frac{2GM}{r}}$$

### Orbital Position (Kepler Elements)
- Input: Semi-major axis $a$, eccentricity $e$, inclination $i$, longitude of ascending node $\Omega$, argument of perihelion $\omega$, mean anomaly $M$
- Solves Kepler's equation to find true anomaly
- Applies 3D rotation transformations

---

## 💻 Using the Frontend

### Physics Lab Panel (🔭 Vật Lý)

1. **Orbital Velocity Calculator**
   - Select planet
   - Click "⚡ Tính tốc độ"
   - View orbital velocity in km/s

2. **Gravitational Force**
   - Select two celestial bodies
   - Set distance in AU
   - Click "💥 Tính lực"
   - View force in Newtons

3. **Escape Velocity**
   - Select planet/star
   - Click "🚀 Tính toán"
   - View escape velocity needed to leave surface

### Control Panel (⚙️ ĐIỀU CHỈNH VẬT LÝ)

- **Sun Mass Factor**: Scale the Sun's mass (0.5-2.5×)
- **Gravity Factor (G)**: Modify gravitational constant (0.2-2.0×)
- **Simulation Speed**: Time acceleration (0-3× normal)
- **Apply Physics**: Recalculate all orbits
- **Reset to Default**: Restore original parameters

---

## 📊 Planet Data Reference

| Planet | Distance (AU) | Period (Years) | Mass (Earth) | Radius (km) |
|--------|---------------|----------------|--------------|-------------|
| Mercury | 0.387 | 0.241 | 0.055 | 2,440 |
| Venus | 0.723 | 0.615 | 0.815 | 6,052 |
| Earth | 1.0 | 1.0 | 1.0 | 6,371 |
| Mars | 1.524 | 1.881 | 0.107 | 3,390 |
| Jupiter | 5.203 | 11.862 | 317.8 | 69,911 |
| Saturn | 9.537 | 29.457 | 95.2 | 58,232 |
| Uranus | 19.191 | 84.011 | 14.5 | 25,362 |
| Neptune | 30.069 | 164.79 | 17.1 | 24,622 |

---

## 🛠️ File Structure

```
d:\tryyyyyyyyy solar2copy\
├── app.py                 # FastAPI backend (physics engine)
├── config.py              # Configuration and presets
├── solar_api.js           # JavaScript API client
├── requirements.txt       # Python dependencies
├── solar_systems.db       # SQLite database (created on first run)
├── templates/
│   └── index.html         # Main frontend (Three.js visualization)
└── README.md              # This file
```

---

## 🧪 Example Usage

### Python Backend Example

```python
from app import PhysicsEngine

engine = PhysicsEngine()

# Calculate orbital velocity for Earth
velocity = engine.calculate_orbital_velocity(
    mass_sun=engine.SUN_MASS,
    distance=1.0,  # AU
    gravity_factor=1.0
)
print(f"Earth's orbital velocity: {velocity/1000:.2f} km/s")

# Calculate gravitational force
force = engine.calculate_gravitational_force(
    mass1=engine.SUN_MASS,
    mass2=engine.SUN_MASS * engine.PLANET_MASSES['earth'],
    distance=1.0  # AU
)
print(f"Sun-Earth force: {force:.2e} N")
```

### JavaScript Frontend Example

```javascript
const api = new SolarSystemAPI('http://localhost:8000');

// Calculate Jupiter's orbital velocity
const result = await api.calculateOrbitalVelocity('jupiter', 1.0, 1.0);
console.log(`Jupiter velocity: ${result.velocity_kms} km/s`);

// Create custom system
await api.createCustomSystem('My System', [
    {
        name: 'Planet 1',
        distance: 1.0,
        mass: 1.0,
        radius: 6371,
        color: '#2277ff'
    }
], 1.0, 1.0);
```

---

## 🔧 Troubleshooting

### Server Won't Start
```bash
# Check if port 8000 is in use
lsof -i :8000  # macOS/Linux

# Try different port
python app.py --port 8001
```

### API calls fail in browser
- Ensure backend is running (`python app.py`)
- Check CORS is enabled (default in app.py)
- Browser console should show errors
- Verify API URL in solar_api.js matches server

### Physics calculations seem wrong
- Check physics parameters in control panel
- Verify sun mass and gravity factors
- Reset to default values if uncertain

---

## 📚 Educational Resources

### Key Concepts
- **Orbital Mechanics**: Study of object motion around gravitational bodies
- **Kepler's Laws**: Three laws governing planetary motion
- **Gravitational Fields**: Physics of attractive forces between masses
- **Orbital Resonance**: When orbital periods create harmonic ratios

### Further Learning
- NASA Horizons API: https://ssd.jpl.nasa.gov/horizons/
- Three.js Documentation: https://threejs.org/docs/
- Orbital Mechanics Textbooks: "Fundamentals of Astrodynamics" by Bate, Mueller, White

---

## 💡 Future Enhancements

- [ ] Add collision physics
- [ ] Integrate real-time NASA data subscription
- [ ] Add exoplanet data
- [ ] Implement asteroid belt dynamics
- [ ] Create educational mission scenarios
- [ ] Add Lagrange point visualization
- [ ] Implement multi-body gravitational interactions
- [ ] Add solar flare animations
- [ ] Support for binary star systems

---

## 📄 License

This project is open-source and available for educational use.

## 👨‍💻 Author

Created as an enhanced physics simulation model for the NASA Eyes-style solar system visualization.

---

**Last Updated**: April 9, 2026
**Version**: 1.0.0
