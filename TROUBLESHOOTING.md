# 🔧 Troubleshooting Guide - Solar System 3D

## Installation Issues

### Error: "PIP upgrade failed" / "ERROR: To modify pip..."

**Problem:** Windows locks pip file when trying to upgrade it  
**This is NORMAL on Windows and doesn't prevent installation**

**Solution 1: Quick Install (Skip pip upgrade)** ✅ EASIEST
```bash
.\run_quick.bat
```

**Solution 2: Restart and Retry** 
```bash
# Close all terminal windows
# Right-click Command Prompt → "Run as Administrator"  
# Then:
.\run.bat
```

**Solution 3: Clean Install**
```bash
rmdir /s /q venv
powershell -ExecutionPolicy Bypass -File clean_install.ps1
.\run.bat
```

**Solution 4: Manual pip installation**
```bash
python -m venv venv
venv\Scripts\python.exe -m pip install -r requirements.txt --prefer-binary
venv\Scripts\python app.py
```

---

### Error: "ModuleNotFoundError: No module named 'distutils'"

**Problem:** Python 3.12 removed distutils which pip needs
**Solution:**
```bash
# Upgrade pip and install setuptools
python -m pip install --upgrade pip setuptools

# Then reinstall packages
pip install --prefer-binary -r requirements.txt
```

### Error: "pip install failed" / Dependency Installation Errors

**Causes:** Network issues, Python incompatibility, missing build tools

**Solutions:**

1. **Try with prebuilt wheels:**
```bash
pip install --prefer-binary -r requirements.txt
```

2. **Try without build isolation:**
```bash
pip install --no-build-isolation -r requirements.txt
```

3. **Upgrade pip first:**
```bash
python -m pip install --upgrade pip setuptools wheel
pip install -r requirements.txt
```

4. **Use Python 3.10/3.11 (not 3.12):**
   - Python 3.12 has fewer prebuilt packages
   - Download from: https://www.python.org/downloads
   - Recommended: Python 3.10 LTS

### Error: "Failed to create virtual environment"

**Solution:**
```bash
# Delete old venv and create new
rmdir /s /q venv
python -m venv venv
venv\Scripts\activate
pip install --upgrade pip setuptools
pip install --prefer-binary -r requirements.txt
```

Or use cleanup script:
```bash
powershell -ExecutionPolicy Bypass -File clean_install.ps1
```

---

## Runtime Issues

### Port 8000 Already in Use

**Problem:** Server can't start on localhost:8000
**Solution:**
```bash
# Find which process is using port 8000
netstat -ano | findstr :8000

# Kill the process (replace [PID] with the number you found)
taskkill /PID [PID] /F

# Now try running again
.\run.bat
```

### Server Starts But Browser Shows Black Screen

**Possible causes:**
1. Frontend still loading (normal, wait 10 seconds)
2. Browser cache issues
3. JavaScript file not loading

**Solutions:**
- **Wait longer** (10-15 seconds on first load)
- **Clear cache:** Ctrl+Shift+Delete → select all → clear
- **Hard refresh:** Ctrl+F5
- **Check browser console:** Press F12, look for red errors
- **Try different browser:** Chrome/Firefox/Edge

### API Calls Failing / "Cannot GET /api/..."

**Problem:** Physics Lab calculations don't work
**Causes:** 
- Server not running
- Browser lost connection to server
- CORS issues

**Solutions:**

1. **Check server is still running:**
   - Look for "⭐ Solar System Server" window
   - Check it's not showing red error messages

2. **Restart server:**
   - Close "⭐ Solar System Server" window
   - Open new terminal: `.\run.bat`
   - Wait 8 seconds for startup
   - Refresh browser (F5)

3. **Check server health:**
   - Open developer tools (F12)
   - Check Console tab for errors
   - Visit http://localhost:8000/docs to verify API works

4. **Try manual server startup:**
```bash
.\run_manual.bat
```

### Browser Hangs or Unresponsive

**Cause:** 3D rendering performance issues
**Solutions:**
- Reduce simulation speed (⚙️ Settings panel → Simulation Speed slider)
- Close other browser tabs
- Restart browser completely
- Try different browser

### Physics Results Look Wrong

**Possible issues:**
- NASA API gave cached bad data
- Incorrect planet selected
- Physics parameters were modified

**Solutions:**
- Click reset button (♻️) in settings
- Clear cache: `powershell clean_install.ps1`
- Select "Earth" planet as default test

---

## Connection Problems

### NASA API Not Responding

**Cause:** NASA Horizons API is down or unreachable
**Behavior:** Calculations still work (using local formulas)
**Solution:** None needed - fallback calculations are automatic

### No Internet Connection

**Impact:** NASA API won't work, but all calculations still function
**What works:**
- 3D visualization ✅
- Physics calculations ✅  
- Local data ✅

**What doesn't work:**
- Real NASA ephemeris data ❌

---

## Performance Issues

### Frame Rate Drops / Laggy Animation

**Causes:** Too many objects, graphics card can't keep up, other apps using CPU

**Solutions:**
1. **Reduce objects:** Hide asteroids or limit planet count
2. **Lower graphics quality:** Disable shadows (if available)
3. **Close other apps:** Free up RAM and CPU
4. **Check GPU:** Use dedicated graphics card (check NVIDIA/AMD settings)

### Program Uses Too Much Memory

**Solutions:**
- Close and restart: `.\run.bat`
- Use 64-bit Python (not 32-bit)
- Close other browser tabs
- Restart your computer

---

## Database Issues

### "Cannot open database file" Error

**Cause:** Database file corrupted or permission issues
**Solution:**
```bash
# Delete old database (it will recreate automatically)
del solar_systems.db

# Restart server
.\run.bat
```

### Lost Custom Systems

**Recovery:**
- Check if `solar_systems.db` file exists
- If deleted, create new systems again (data can't be recovered)
- Consider backing up `solar_systems.db` file after creating systems

---

## Script Issues

### run.bat Won't Execute

**Causes:** Execution policy, antivirus blocking, file corrupted

**Solutions:**

1. **If file won't open:**
   - Right-click `run.bat` → Edit
   - Should open in Notepad
   - Save without changes
   - Try running again

2. **If execution blocked by policy:**
```bash
# Use PowerShell with bypass
powershell -ExecutionPolicy Bypass -Command "& '.\run.bat'"
```

3. **If PowerShell scripts blocked:**
```bash
# Allow script execution temporarily
powershell -ExecutionPolicy Bypass -File clean_install.ps1
```

### "timeout" command doesn't work

**Cause:** Some Windows versions use different sleep command

**Manual workaround:**
```bash
# Edit run.bat, replace:
timeout /t 8 /nobreak

# With:
ping localhost -n 9 >nul
```

---

## Debugging Steps

**If something goes wrong, try troubleshooting in this order:**

1. **Check Python version:**
```bash
python --version
# Should be 3.9 or higher
```

2. **Check server is running:**
```bash
# New terminal/PowerShell:
curl http://localhost:8000
# Should return HTML or JSON, not connection error
```

3. **Check dependencies:**
```bash
venv\Scripts\pip list
# Should show: fastapi, uvicorn, numpy, scipy, requests, etc.
```

4. **Check logs:**
   - Look in "⭐ Solar System Server" window for red error messages
   - Check browser console (F12) for JavaScript errors

5. **Clean install:**
```bash
powershell -ExecutionPolicy Bypass -File clean_install.ps1
.\run.bat
```

6. **Try manual server:**
```bash
.\run_manual.bat
```

---

## Getting Help

**Before asking for help, please provide:**

1. Your Python version: `python --version`
2. Full error message (copy entire traceback)
3. What you were doing when error occurred
4. Which startup method you used (run.bat vs manual vs PowerShell)
5. Your Windows version (Win10/Win11)
6. Browser type and version

---

## Contact & Support

For more help, check:
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Three.js Documentation](https://threejs.org/docs/)
- [Python Package Index](https://pypi.org/)

---

**Last Updated:** April 2026
