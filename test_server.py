#!/usr/bin/env python3
"""
Quick test script to verify server is working correctly
Run this after starting the server in another terminal
"""

import time
import requests
import sys

BASE_URL = "http://localhost:9000"
TIMEOUT = 5

def test_endpoints():
    print("🧪 Testing Solar System Physics Engine API\n")
    
    # Test 1: Root endpoint
    print("1️⃣  Testing root endpoint...")
    try:
        resp = requests.get(f"{BASE_URL}/", timeout=TIMEOUT)
        if resp.status_code == 200:
            print("   ✅ Root endpoint works")
            data = resp.json()
            print(f"   Status: {data.get('status')}\n")
        else:
            print(f"   ❌ Status code: {resp.status_code}\n")
            return False
    except Exception as e:
        print(f"   ❌ Error: {e}\n")
        return False
    
    # Test 2: Orbital velocity
    print("2️⃣  Testing orbital velocity calculation...")
    try:
        resp = requests.post(
            f"{BASE_URL}/api/orbital-velocity",
            json={"planet": "earth", "sun_mass_factor": 1.0, "gravity_factor": 1.0},
            timeout=TIMEOUT
        )
        if resp.status_code == 200:
            data = resp.json()
            print("   ✅ Orbital velocity works")
            print(f"   Earth orbital velocity: {data.get('velocity_kms', 0):.2f} km/s\n")
        else:
            print(f"   ❌ Status code: {resp.status_code}\n")
            return False
    except Exception as e:
        print(f"   ❌ Error: {e}\n")
        return False
    
    # Test 3: Escape velocity
    print("3️⃣  Testing escape velocity calculation...")
    try:
        resp = requests.post(
            f"{BASE_URL}/api/escape-velocity",
            json={"planet": "earth"},
            timeout=TIMEOUT
        )
        if resp.status_code == 200:
            data = resp.json()
            print("   ✅ Escape velocity works")
            print(f"   Earth escape velocity: {data.get('escape_velocity_kms', 0):.2f} km/s\n")
        else:
            print(f"   ❌ Status code: {resp.status_code}\n")
            return False
    except Exception as e:
        print(f"   ❌ Error: {e}\n")
        return False
    
    # Test 4: Gravitational force
    print("4️⃣  Testing gravitational force calculation...")
    try:
        resp = requests.post(
            f"{BASE_URL}/api/gravitational-force",
            json={"planet1": "sun", "planet2": "earth", "distance_au": 1.0},
            timeout=TIMEOUT
        )
        if resp.status_code == 200:
            data = resp.json()
            print("   ✅ Gravitational force works")
            print(f"   Sun-Earth force: {data.get('force_scientific', 'N/A')}\n")
        else:
            print(f"   ❌ Status code: {resp.status_code}\n")
            return False
    except Exception as e:
        print(f"   ❌ Error: {e}\n")
        return False
    
    # Test 5: HTML page
    print("5️⃣  Testing HTML page serving...")
    try:
        resp = requests.get(f"{BASE_URL}/", timeout=TIMEOUT)
        if resp.status_code == 200 and "index.html" not in resp.text:
            # If it's not serving HTML file, it's serving the JSON fallback
            print("   ⚠️  Root is serving API response (try visiting in browser)")
        else:
            print("   ✅ HTML page is being served\n")
    except Exception as e:
        print(f"   ❌ Error: {e}\n")
    
    # Test 6: solar_api.js
    print("6️⃣  Testing solar_api.js serving...")
    try:
        resp = requests.get(f"{BASE_URL}/solar_api.js", timeout=TIMEOUT)
        if resp.status_code == 200:
            print("   ✅ solar_api.js is accessible\n")
        else:
            print(f"   ❌ Status code: {resp.status_code}\n")
    except Exception as e:
        print(f"   ❌ Error: {e}\n")
    
    print("="*60)
    print("🎉 All tests completed!")
    print("="*60)
    return True

if __name__ == "__main__":
    print("\n⏳ Waiting a moment for server to initialize...\n")
    time.sleep(2)
    
    try:
        test_endpoints()
    except KeyboardInterrupt:
        print("\n\n⛔ Test interrupted")
        sys.exit(1)
