# 🚀 Solar System 3D - Installation Guide

## Quick Start (Windows)

**Easiest Method: Just Double-Click**
```bash
.\run.bat
```

**If pip upgrade fails:**
```bash
.\run_quick.bat
```

---

## 🔧 Manual Installation

If `run.bat` fails, try these steps:

### 1. Create Virtual Environment
```bash
python -m venv venv
```

### 2. Activate Virtual Environment
```bash
venv\Scripts\activate
```

### 3. Upgrade pip and install setuptools (Important for Python 3.12+)
```bash
python -m pip install --upgrade pip setuptools wheel
```

### 4. Install Dependencies
```bash
pip install --prefer-binary -r requirements.txt
```

Or with no build isolation (if above fails):
```bash
pip install --no-build-isolation -r requirements.txt
```

### 5. Run Server
```bash
python app.py
```

### 6. Open Browser
Visit: **http://localhost:8000**

---

## ❌ Troubleshooting

### Error: "PIP upgrade failed" / "To modify pip, please run..."
**Cause:** Windows file lock (pip can't upgrade itself)
**Solutions (try in order):**

1. **Quick method (skip pip upgrade):**
   ```bash
   .\run_quick.bat
   ```

2. **Close everything and retry:**
   - Close all Python/terminal windows
   - Right-click Command Prompt → "Run as Administrator"
   - Delete venv: `rmdir /s /q venv`
   - Run: `.\run.bat`

3. **Manual installation:**
   ```bash
   rmdir /s /q venv
   python -m venv venv
   venv\Scripts\python.exe -m pip install -r requirements.txt --prefer-binary
   ```

4. **PowerShell clean install:**
   ```powershell
   powershell -ExecutionPolicy Bypass -File clean_install.ps1
   ```

### Error: `ModuleNotFoundError: No module named 'distutils'`
**Solution:**
```bash
python -m pip install --upgrade setuptools
.\run_quick.bat
```

---

## 📋 System Requirements

- **Python**: 3.9 or higher
- **RAM**: 512 MB minimum (1 GB recommended)
- **Disk Space**: 500 MB for dependencies
- **Browser**: Chrome, Firefox, Edge, Safari (modern version)
- **Network**: Internet connection for NASA API (optional, will use calculated data as fallback)

---

## ✅ After Installation

1. **Physics Lab** - Click 🔭 button to access calculations
2. **Planet Info** - Click any planet to see details
3. **Settings** - Adjust physics parameters on right panel
4. **3D Controls**:
   - Drag to rotate
   - Scroll to zoom
   - Right-click to pan

---

## 📞 Support

If you encounter issues:

1. Check error messages in "Solar System Server" terminal window
2. Review logs in browser console (F12)
3. Verify Python version: `python --version`
4. Check port availability: `netstat -ano | findstr :8000`

**Happy exploring! 🌌**
