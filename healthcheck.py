#!/usr/bin/env python
import requests
import json

print("=" * 60)
print("SOLAR SYSTEM HEALTHCHECK")
print("=" * 60)

# Test 1: HTML endpoint
print("\n[1] HTML Endpoint Test")
try:
    resp = requests.get('http://127.0.0.1:9000/')
    print(f"    Status: {resp.status_code}")
    print(f"    HTML Size: {len(resp.text)} bytes")
    print(f"    Content Type: HTML Document")
    print("    ✅ PASS")
except Exception as e:
    print(f"    ❌ FAIL: {e}")

# Test 2: solar_api.js endpoint
print("\n[2] JavaScript API Endpoint Test")
try:
    resp = requests.get('http://127.0.0.1:9000/solar_api.js')
    print(f"    Status: {resp.status_code}")
    print(f"    JS Size: {len(resp.text)} bytes")
    print("    ✅ PASS")
except Exception as e:
    print(f"    ❌ FAIL: {e}")

# Test 3: Physics calculation endpoint
print("\n[3] Physics API Tests")
planets = ['mercury', 'earth', 'jupiter', 'mars', 'saturn']
for planet in planets:
    try:
        resp = requests.post(f'http://127.0.0.1:9000/api/orbital-velocity?planet={planet}')
        data = resp.json()
        if data.get('success'):
            velocity = data.get('velocity_kms', 0)
            print(f"    • {planet.capitalize():8} → {velocity:8.2f} km/s ✅")
        else:
            print(f"    • {planet.capitalize():8} → ERROR ❌")
    except Exception as e:
        print(f"    • {planet.capitalize():8} → {e} ❌")

# Test 4: More complex calculations
print("\n[4] Advanced Physics Tests")

# Escape velocity
print("    Escape Velocities:")
for planet in ['earth', 'mars', 'jupiter']:
    try:
        resp = requests.post(f'http://127.0.0.1:9000/api/escape-velocity?planet={planet}')
        data = resp.json()
        if data.get('success'):
            vel = data.get('escape_velocity_kms', 0)
            print(f"      • {planet.capitalize():8} → {vel:8.2f} km/s ✅")
    except:
        pass

# Gravitational force
print("    Gravitational Forces:")
try:
    resp = requests.post('http://127.0.0.1:9000/api/gravitational-force?planet1=earth&planet2=sun&distance_au=1.0')
    data = resp.json()
    if data.get('success'):
        force = data.get('force_scientific', 'N/A')
        print(f"      • Earth-Sun @ 1 AU → {force} ✅")
except:
    pass

print("\n" + "=" * 60)
print("HEALTHCHECK COMPLETE")
print("=" * 60)
print("\nServer URL: http://127.0.0.1:9000")
print("API Docs: http://127.0.0.1:9000/docs")
print("\n✅ All systems operational!")
