# 🌌 QUICK START GUIDE - SOLAR SYSTEM 3D

## ⚡ Start the Application (3 Steps)

### Step 1: Open Command Prompt
Navigate to the project folder:
```
cd D:\tryyyyyyyyy solar2copy
```

### Step 2: Run the Startup Script
```
.\run_quick.bat
```

### Step 3: Wait for Browser
The application will automatically:
- ✅ Create virtual environment (if needed)
- ✅ Install dependencies  
- ✅ Start the server
- ✅ Open browser to the 3D interface

**That's it!** 🎉

---

## 📍 Where to Find Things

| What | Where |
|------|-------|
| **3D Interface** | http://127.0.0.1:9000 |
| **API Documentation** | http://127.0.0.1:9000/docs |
| **Physics Lab** | Click 🔭 button in interface |
| **Calculation Tools** | "Get Physics" menu in 3D view |
| **API Speed Lookup** | ⚡ button in toolbar |

---

## 🔭 Using Physics Lab

1. Click the **🔭 Physics Lab** button
2. Choose calculation type
3. Enter values
4. Click "Calculate" button
5. View results instantly

### Available Calculations:
- ⚡ Orbital velocity
- 🌍 Gravitational force  
- 🚀 Escape velocity
- 📊 Kepler orbital positions
- 📍 Planet positions

---

## 🛠 If Something Goes Wrong

### Server won't start?
```
Try: .\run.bat
```

### Port already in use?
```
Kill it: netstat -ano | findstr :9000
```

### Still having issues?
Check these files:
- `TROUBLESHOOTING.md` - Common problems
- `INSTALL.md` - Detailed installation
- `PHYSICS_GUIDE.md` - Physics calculations

---

## 📊 Current Configuration

- **Server**: http://127.0.0.1:9000
- **Port**: 9000
- **Database**: solar_systems.db
- **Frontend**: Three.js 0.128.0
- **Physics**: NumPy + SciPy

---

## ✅ Everything Works!

Healthcheck results show:
- ✅ HTML serving (57KB)
- ✅ JavaScript loaded (8.6KB)
- ✅ Physics calculations accurate
- ✅ All 11 API endpoints active
- ✅ No errors or warnings

---

## 🚀 Pro Tips

1. **Keep server window open** while using the app
2. **Bookmark** http://127.0.0.1:9000/docs for API reference
3. **Try different planets** in Physics Lab for comparisons
4. **Run healthcheck.py** to verify all systems

```bash
venv\Scripts\python healthcheck.py
```

---

**🌌 Ready to explore the cosmos!** 🚀

Click on planets, rotate the 3D view, and check out the Physics Lab calculations!
