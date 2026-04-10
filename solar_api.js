/**
 * Solar System APIs Client
 * Integration with Python FastAPI backend for physics calculations
 */

class SolarSystemAPI {
    constructor(baseURL = 'http://localhost:9000') {
        this.baseURL = baseURL;
        this.timeout = 10000;
    }

    /**
     * Calculate planet position at given date
     */
    async calculatePosition(planet, date = null, useNASA = false) {
        try {
            const params = {
                planet,
                use_nasa: useNASA
            };
            if (date) params.date = date;

            const response = await this.fetch('/api/calculate-position', 'POST', params);
            return response.data;
        } catch (error) {
            console.error('Position calculation error:', error);
            return null;
        }
    }

    /**
     * Calculate orbital velocity
     */
    async calculateOrbitalVelocity(planet, sunMassFactor = 1.0, gravityFactor = 1.0) {
        try {
            const response = await this.fetch('/api/orbital-velocity', 'POST', {
                planet,
                sun_mass_factor: sunMassFactor,
                gravity_factor: gravityFactor
            });
            return response;
        } catch (error) {
            console.error('Orbital velocity error:', error);
            return null;
        }
    }

    /**
     * Calculate gravitational force between two objects
     */
    async calculateGravitationalForce(planet1, planet2, distanceAU) {
        try {
            const response = await this.fetch('/api/gravitational-force', 'POST', {
                planet1,
                planet2,
                distance_au: distanceAU
            });
            return response;
        } catch (error) {
            console.error('Gravitational force error:', error);
            return null;
        }
    }

    /**
     * Calculate escape velocity
     */
    async calculateEscapeVelocity(planet) {
        try {
            const response = await this.fetch('/api/escape-velocity', 'POST', {
                planet
            });
            return response;
        } catch (error) {
            console.error('Escape velocity error:', error);
            return null;
        }
    }

    /**
     * Calculate position using Kepler orbital elements
     */
    async calculateKeplerPosition(planet, date = null) {
        try {
            const response = await this.fetch('/api/kepler-position', 'POST', {
                planet,
                date
            });
            return response;
        } catch (error) {
            console.error('Kepler position error:', error);
            return null;
        }
    }

    /**
     * Create a custom solar system
     */
    async createCustomSystem(name, planets, starMassFactor = 1.0, gravityFactor = 1.0) {
        try {
            const response = await this.fetch('/api/systems/create', 'POST', {
                name,
                planets: planets.map(p => ({
                    name: p.name,
                    distance: p.distance,
                    mass: p.mass,
                    radius: p.radius,
                    eccentricity: p.eccentricity || 0.0,
                    inclination: p.inclination || 0.0,
                    long_asc_node: p.long_asc_node || 0.0,
                    arg_perihelion: p.arg_perihelion || 0.0,
                    mean_anomaly: p.mean_anomaly || 0.0,
                    color: p.color || '#ffffff'
                })),
                star_mass_factor: starMassFactor,
                gravity_factor: gravityFactor
            });
            return response;
        } catch (error) {
            console.error('System creation error:', error);
            return null;
        }
    }

    /**
     * List all custom systems
     */
    async listCustomSystems() {
        try {
            const response = await this.fetch('/api/systems/list', 'GET');
            return response.systems || [];
        } catch (error) {
            console.error('List systems error:', error);
            return [];
        }
    }

    /**
     * Get a specific custom system
     */
    async getCustomSystem(systemId) {
        try {
            const response = await this.fetch(`/api/systems/${systemId}`, 'GET');
            return response.system;
        } catch (error) {
            console.error('Get system error:', error);
            return null;
        }
    }

    /**
     * Get comprehensive planet data
     */
    async getPlanetData(planet) {
        try {
            const response = await this.fetch(`/api/planet-data/${planet}`, 'GET');
            return response;
        } catch (error) {
            console.error('Planet data error:', error);
            return null;
        }
    }

    /**
     * Internal fetch method
     */
    async fetch(endpoint, method = 'GET', data = null) {
        let url = this.baseURL + endpoint;
        const options = {
            method,
            headers: {
                'Content-Type': 'application/json',
            },
            timeout: this.timeout
        };

        // For POST requests with data, append as query parameters
        if (data && method === 'POST') {
            const params = new URLSearchParams();
            for (const [key, value] of Object.entries(data)) {
                params.append(key, value);
            }
            url += '?' + params.toString();
        }

        try {
            const response = await fetch(url, options);
            if (!response.ok) {
                throw new Error(`API Error: ${response.status} ${response.statusText}`);
            }
            return await response.json();
        } catch (error) {
            console.error(`Fetch error (${endpoint}):`, error);
            throw error;
        }
    }
}

/**
 * Physics Calculator - Formulas and computations
 */
class PhysicsCalculator {
    static G = 6.67430e-11;  // Gravitational constant
    static AU = 1.496e11;     // AU in meters
    static EARTH_MASS = 5.972e24;

    /**
     * Calculate orbital period given semi-major axis and mass
     * T = 2π√(a³/GM)
     */
    static calculateOrbitalPeriod(semiMajorAxisAU, starMass) {
        const a = semiMajorAxisAU * this.AU;
        const period = 2 * Math.PI * Math.sqrt((a ** 3) / (this.G * starMass));
        return period / 86400;  // Convert to days
    }

    /**
     * Calculate Hill sphere (gravitational sphere of influence)
     */
    static calculateHillSphere(planetMass, distance, starMass) {
        const massFactor = (planetMass / starMass) / 3;
        const hillRadius = distance * (massFactor ** (1/3));
        return hillRadius;
    }

    /**
     * Calculate synodic period (time between conjunctions)
     */
    static calculateSynodicPeriod(period1, period2) {
        return Math.abs((period1 * period2) / (period1 - period2));
    }

    /**
     * Check for orbital resonance
     */
    static checkResonance(period1, period2, tolerance = 0.05) {
        const ratio = Math.max(period1, period2) / Math.min(period1, period2);
        return {
            ratio: ratio,
            possible: Math.abs(ratio - Math.round(ratio)) < tolerance,
            type: this.describeResonance(ratio)
        };
    }

    static describeResonance(ratio) {
        const resonances = {
            1: '1:1 (Same period)',
            2: '2:1 (Jupiter-Saturn like)',
            1.5: '3:2 (Pluto-Neptune like)',
            0.67: '2:3',
            0.5: '1:2'
        };

        // Find closest resonance
        let closest = null;
        let minDiff = Infinity;
        for (const [res, desc] of Object.entries(resonances)) {
            const diff = Math.abs(ratio - res);
            if (diff < minDiff) {
                minDiff = diff;
                closest = desc;
            }
        }
        return closest;
    }

    /**
     * Calculate tidal force
     */
    static calculateTidalForce(objectMass, distance, objectRadius) {
        const tidalForce = (2 * this.G * objectMass * objectRadius) / (distance ** 3);
        return tidalForce;
    }

    /**
     * Calculate Roche limit (fluid body)
     */
    static calculateRocheLimit(primaryMass, primaryRadius, satelliteMass, satelliteRadius, density = 1000) {
        // For fluid bodies
        const limit = 2.456 * primaryRadius * ((primaryMass / satelliteMass) ** (1/3));
        return limit;
    }
}

// Export for use in another module
if (typeof module !== 'undefined' && module.exports) {
    module.exports = { SolarSystemAPI, PhysicsCalculator };
}
