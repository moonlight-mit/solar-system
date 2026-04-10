#!/usr/bin/env python3
"""
🌌 Solar System 3D - Quick Start Script
Automatically sets up and runs the solar system simulation
"""

import os
import sys
import subprocess
import webbrowser
from pathlib import Path


def check_python_version():
    """Check if Python version is 3.8+"""
    if sys.version_info < (3, 8):
        print(f"❌ Python 3.8+ required. You have {sys.version_info.major}.{sys.version_info.minor}")
        sys.exit(1)
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor}")


def create_venv():
    """Create virtual environment if it doesn't exist"""
    venv_path = Path('venv')
    if not venv_path.exists():
        print("📦 Creating virtual environment...")
        subprocess.run([sys.executable, '-m', 'venv', 'venv'], check=True)
        print("✅ Virtual environment created")
    else:
        print("✅ Virtual environment already exists")


def activate_venv():
    """Get the Python executable in venv"""
    venv_python = Path('venv') / ('Scripts' if sys.platform == 'win32' else 'bin') / ('python.exe' if sys.platform == 'win32' else 'python')
    return str(venv_python)


def install_requirements(python_exe):
    """Install required packages"""
    print("📥 Installing dependencies...")
    subprocess.run([python_exe, '-m', 'pip', 'install', '-q', '-r', 'requirements.txt'], check=True)
    print("✅ Dependencies installed")


def run_server(python_exe):
    """Run the FastAPI server"""
    print("\n🚀 Starting Solar System Physics Engine...\n")
    print("=" * 60)
    print("🌌 Server running at: http://localhost:9000")
    print("📚 API Documentation: http://localhost:9000/docs")
    print("=" * 60)
    print("\n🌐 Opening frontend in browser...")
    
    # Open browser
    try:
        webbrowser.open('file:///' + os.path.abspath('templates/index.html').replace('\\', '/'))
    except:
        print("⚠️ Could not auto-open browser. Manually open:")
        print(f"   file:///{os.path.abspath('templates/index.html').replace(chr(92), '/')}")
    
    # Run server
    subprocess.run([python_exe, 'app.py'], check=False)


def main():
    """Main setup and run function"""
    print("🌌 Solar System 3D - Quick Start\n")
    
    # Check Python version
    check_python_version()
    
    # Create virtual environment
    create_venv()
    
    # Get venv Python
    python_exe = activate_venv()
    
    # Install requirements
    install_requirements(python_exe)
    
    # Run server
    run_server(python_exe)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Server stopped")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)
