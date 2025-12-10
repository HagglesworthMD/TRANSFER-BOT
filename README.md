# 🚀 SAMI Transfer Bot - Live Dashboard

## Overview
Real-time monitoring dashboard for the email transfer bot that handles round-robin distribution of SAMI transfer requests to staff members.

## ✨ Features

### 📊 **Real-Time Metrics**
- **Total requests processed today**
- **Active staff count** with utilization
- **Completion rate** tracking
- **Average workload per staff member**
- **Last activity** timestamp

### 📈 **Advanced Analytics**
- **Workload Distribution Chart** - Visual breakdown of assignments per staff
- **Hourly Activity Trend** - See when requests peak throughout the day
- **7-Day Historical Trend** - Track volume over the past week
- **Balance Score** - Fairness metric showing how evenly requests are distributed

### 🎯 **Live Monitoring**
- **Activity Feed** - Real-time stream of all assignments and completions
- **Staff Leaderboard** - Top performers ranked by assignments handled
- **Round-Robin Status** - Shows who's next in line for assignment
- **Auto-refresh every 5 seconds** - No manual refresh needed!

### 🎨 **Premium UI**
- Modern dark mode with glassmorphism effects
- Smooth animations and transitions
- Mobile-responsive design
- Professional gradients and color schemes

## 🚀 Quick Start

### Option 1: Using the Launcher Script (Recommended)
```bash
cd "/home/deck/Documents/TRANSFER BOT"
./launch_dashboard.sh
```

### Option 2: Manual Launch
```bash
cd "/home/deck/Documents/TRANSFER BOT"
source venv/bin/activate
streamlit run dashboard.py
```

The dashboard will automatically open in your browser at:
- **Local**: http://localhost:8501
- **Network**: http://YOUR_IP:8501 (accessible from other devices on your network)

## 📱 Accessing Remotely

Your manager can access the dashboard from any device on the same network:

1. Find your computer's IP address:
   ```bash
   ip addr show | grep "inet " | grep -v 127.0.0.1
   ```

2. Share the URL: `http://YOUR_IP:8501`

3. They can bookmark it on their phone/tablet for instant access!

## 🔧 Configuration

The dashboard automatically reads from:
- `daily_stats.csv` - Activity log created by `distributor.py`
- `roster_state.json` - Current round-robin position
- `staff.txt` - List of staff members in rotation

**No configuration needed** - it just works! 🎉

## 📊 Data Refresh

- **Auto-refresh**: Every 5 seconds
- **Data cache**: 5-second TTL for optimal performance
- **Real-time updates**: See new assignments as they happen

## 🛠️ Technical Details

**Built with:**
- **Streamlit** - Modern Python dashboard framework
- **Plotly** - Interactive, professional charts
- **Pandas** - Data processing and analysis

**System Requirements:**
- Python 3.8+
- ~50MB RAM (very lightweight!)
- Any modern web browser

## 💡 Tips for Your Manager

1. **Bookmark the URL** on your phone's home screen for one-tap access
2. **Check the Balance Score** - anything below 60% might indicate an issue
3. **Monitor hourly trends** to identify peak times and plan staffing
4. **Export data** - The audit log can be copied/exported for reports
5. **Keep it running** - Leave the dashboard open on a spare monitor!

## 🎯 What's Being Tracked

### Per Request:
- Date and time received
- Email subject
- Staff member assigned
- Completion status

### Aggregated Metrics:
- Daily volume
- Weekly trends
- Per-staff workload
- Response time estimates
- Round-robin fairness

## 🔒 Security Note

The dashboard is **read-only** - it cannot modify assignments or settings. It purely displays data from the log files.

## 📞 Support

If you need to customize the dashboard:
- Modify `dashboard.py`
- Restart the launcher script
- Changes appear immediately!

---

**Made with ❤️ for SAMI Support Team**
