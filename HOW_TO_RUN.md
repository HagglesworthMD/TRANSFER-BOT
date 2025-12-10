# 🚀 HOW TO RUN - Quick Start Guide

## For Your Manager (Dashboard Only)

### **View the Live Dashboard:**
1. Open any web browser
2. Go to: **http://172.20.10.5:8502**
3. That's it! The dashboard updates automatically every 5 seconds

**Bookmark this URL** for instant access anytime!

---

## For You (Running the Bot)

### **Option 1: Quick Run (Testing)**

**Open Terminal in the folder:**
1. Right-click in the `TRANSFER BOT` folder
2. Select "Open Terminal Here" (or similar)
3. Run:
```bash
python distributor.py
```

**To stop:** Press `Ctrl+C`

---

### **Option 2: Background Service (Recommended for 24/7)**

**Start the bot in background:**
```bash
cd "/home/deck/Documents/TRANSFER BOT"
nohup python distributor.py > bot.log 2>&1 &
```

**Check if it's running:**
```bash
ps aux | grep distributor.py
```

**Stop the bot:**
```bash
pkill -f distributor.py
```

**View logs:**
```bash
tail -f bot.log
```

---

## Complete System Status

### **Check Dashboard:**
```bash
./dashboard_service.sh status
```

### **Restart Dashboard:**
```bash
./dashboard_service.sh restart
```

### **Check Both Running:**
```bash
# Dashboard
./dashboard_service.sh status

# Bot
ps aux | grep distributor.py
```

---

## What Each Component Does

### **1. Distributor Bot** (`distributor.py`)
- **Monitors** the SAMI mailbox
- **Assigns** emails to staff in round-robin
- **Logs** all activity to `daily_stats.csv`
- **Runs continuously** - needs to stay running

### **2. Dashboard** (`dashboard.py`)
- **Reads** the CSV log file
- **Displays** real-time analytics
- **Auto-refreshes** every 5 seconds
- **Already running** as a service

---

## Typical Workflow

### **Morning Setup:**
```bash
# Start the dashboard (if not already running)
./dashboard_service.sh start

# Start the bot
python distributor.py
```

### **During the Day:**
- Bot runs in background
- Dashboard accessible at http://172.20.10.5:8502
- Everything updates automatically

### **End of Day:**
- Bot keeps running (or stop with Ctrl+C)
- Dashboard keeps running 24/7
- Data accumulates in `daily_stats.csv`

---

## Troubleshooting

### **Dashboard not loading?**
```bash
./dashboard_service.sh restart
```

### **Bot not processing emails?**
- Check Outlook is open
- Check SAMI mailbox is accessible
- Check `staff.txt` has email addresses
- Look at console output for errors

### **No data showing?**
- Bot needs to process at least one email first
- Check `daily_stats.csv` has data
- Refresh browser (Ctrl+Shift+R)

---

## Quick Command Reference

```bash
# DASHBOARD
./dashboard_service.sh start     # Start dashboard
./dashboard_service.sh stop      # Stop dashboard
./dashboard_service.sh restart   # Restart dashboard
./dashboard_service.sh status    # Check status

# BOT (foreground)
python distributor.py            # Run bot (stay open)

# BOT (background)
nohup python distributor.py > bot.log 2>&1 &   # Start in background
pkill -f distributor.py                         # Stop background bot
tail -f bot.log                                 # View bot logs
```

---

## URLs to Remember

- **Dashboard (local):** http://localhost:8502
- **Dashboard (network):** http://172.20.10.5:8502
- **For manager:** http://172.20.10.5:8502

---

## Files Overview

| File | Purpose |
|------|---------|
| `distributor.py` | Email bot that assigns requests |
| `dashboard.py` | Analytics dashboard |
| `daily_stats.csv` | Activity log (auto-generated) |
| `staff.txt` | List of staff emails |
| `roster_state.json` | Current rotation position |
| `dashboard_service.sh` | Dashboard control script |

---

## Pro Tips

✅ **Keep bot running** during business hours  
✅ **Dashboard runs 24/7** (already set up)  
✅ **Check dashboard daily** to monitor performance  
✅ **Export CSV weekly** for archival  
✅ **Add to startup** if you want bot to auto-start  

---

**Need help? Check the other documentation:**
- `README.md` - Full system documentation
- `PREMIUM_FEATURES_GUIDE.md` - Dashboard features
- `MANAGER_CHEATSHEET.txt` - Quick reference for managers
