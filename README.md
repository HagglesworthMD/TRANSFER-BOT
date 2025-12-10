# 🚀 SAMI Transfer Bot

**Enterprise-grade email distribution system with real-time analytics dashboard**

Automatically distributes incoming SAMI transfer requests to staff in round-robin fashion, with comprehensive monitoring and reporting.

[![GitHub](https://img.shields.io/badge/GitHub-HagglesworthMD%2FTRANSFER--BOT-blue)](https://github.com/HagglesworthMD/TRANSFER-BOT)
[![Status](https://img.shields.io/badge/Status-Production%20Ready-success)]()
[![Python](https://img.shields.io/badge/Python-3.8%2B-blue)]()
[![License](https://img.shields.io/badge/License-MIT-green)]()

---

## ✨ Features

### 📧 **Email Distribution Bot**
- ✅ Automated round-robin assignment to staff
- ✅ Monitors shared Outlook mailbox
- ✅ Detects staff replies for completion tracking
- ✅ Comprehensive logging of all activities
- ✅ Sender tracking for analytics

### 📊 **Premium Analytics Dashboard**
- ✅ **Executive Summary** with health status (🟢🟡🔴)
- ✅ **Week-over-Week** performance comparison
- ✅ **Peak Hours Heatmap** for staffing optimization
- ✅ **Request Sources Analytics** (who's sending emails)
- ✅ **Individual Staff KPIs** with detailed metrics
- ✅ **Real-time charts** (hourly trends, workload distribution)
- ✅ **Export functionality** (CSV download)
- ✅ **Auto-refresh** every 5 seconds
- ✅ **Mobile-responsive** design

---

## 🎯 Quick Start

### **For Windows Users (Easiest):**

1. **Double-click:** `START_EVERYTHING.bat`
2. **Done!** Dashboard opens + bot starts

### **Manual Start:**

```bash
# Start the bot
python distributor.py

# Open dashboard (in browser)
http://localhost:8502
```

---

## 📋 Requirements

- **Python 3.8+**
- **Windows** (for Outlook integration)
- **Outlook** desktop application
- **Access** to shared SAMI mailbox

### **Python Dependencies:**
```
streamlit>=1.28.0
pandas>=2.0.0
plotly>=5.17.0
pywin32
```

**Install:**
```bash
pip install -r requirements.txt
```

---

## 🏗️ Project Structure

```
TRANSFER-BOT/
├── distributor.py              # Email distribution bot
├── dashboard.py                # Analytics dashboard
├── staff.txt                   # Staff roster (emails)
├── daily_stats.csv             # Activity log (auto-generated)
├── roster_state.json           # Current rotation state
│
├── START_EVERYTHING.bat        # One-click launcher (Windows)
├── START_BOT.bat              # Start bot only
├── OPEN_DASHBOARD.bat         # Open dashboard only
│
├── dashboard_service.sh        # Dashboard service manager (Linux)
├── launch_dashboard.sh         # Dashboard launcher (Linux)
│
├── HOW_TO_RUN.md              # Complete usage guide
├── PREMIUM_FEATURES_GUIDE.md  # Dashboard features documentation
├── MANAGER_CHEATSHEET.txt     # Quick reference
├── QUICKSTART.md              # Getting started guide
├── README.md                  # This file
└── requirements.txt           # Python dependencies
```

---

## 📖 Documentation

| File | Description |
|------|-------------|
| [HOW_TO_RUN.md](HOW_TO_RUN.md) | Complete setup and usage instructions |
| [PREMIUM_FEATURES_GUIDE.md](PREMIUM_FEATURES_GUIDE.md) | Dashboard features and capabilities |
| [MANAGER_CHEATSHEET.txt](MANAGER_CHEATSHEET.txt) | Quick reference for managers |
| [QUICKSTART.md](QUICKSTART.md) | 2-minute setup guide |

---

## 🎨 Dashboard Preview

**Executive Summary:**
- 🟢 System health status at a glance
- 📊 Today's activity with trend indicators
- ⚖️ Team balance score
- 💡 Smart insights and alerts

**Analytics Sections:**
- Week-over-week performance comparison
- Peak hours heatmap (day/hour visualization)
- Request sources tracking
- Individual staff performance KPIs
- Live activity feed
- Complete audit log

---

## ⚙️ Configuration

### **staff.txt**
List of staff email addresses (one per line):
```
brian.shaw@sa.gov.au
jason.quinn2@sa.gov.au
```

### **distributor.py**
Configure mailbox settings (lines 14-15):
```python
LIVE_MAILBOX_NAME = "Health:SAMISupportTeam"
LIVE_PROCESSED_FOLDER = "Done"
```

---

## 🚀 Deployment

### **Option 1: Quick Deploy (For Testing)**
```bash
# Terminal 1 - Start bot
python distributor.py

# Terminal 2 - Start dashboard (Linux)
./launch_dashboard.sh
```

### **Option 2: Production Deploy (24/7)**
```bash
# Start dashboard as service (Linux)
./dashboard_service.sh start

# Start bot in background (Windows)
START_EVERYTHING.bat
```

### **Dashboard Access:**
- Local: `http://localhost:8502`
- Network: `http://YOUR_IP:8502`

---

## 📊 What Gets Tracked

### **Per Request:**
- Date & time
- Email subject
- Staff assigned
- Sender email
- Completion status

### **Analytics:**
- Daily/weekly volume
- Hourly distribution
- Per-staff workload
- Response times
- Source patterns
- Fairness metrics

---

## 🎯 Business Value

**Cost Savings:**
- ✅ Optimal staffing reduces overtime
- ✅ Automated assignment saves admin time
- ✅ Data-driven resource allocation

**Quality Improvement:**
- ✅ Fair workload distribution
- ✅ Response time tracking
- ✅ Staff performance visibility

**Strategic Planning:**
- ✅ Historical trends for forecasting
- ✅ Peak hours for capacity planning
- ✅ Source analysis for relationships

---

## 🛠️ Troubleshooting

**Dashboard not loading?**
```bash
./dashboard_service.sh restart
```

**Bot not processing?**
- Ensure Outlook is open
- Check mailbox access
- Verify `staff.txt` has emails
- Check console for errors

**No data showing?**
- Bot must process at least one email
- Check `daily_stats.csv` exists
- Hard refresh browser (Ctrl+Shift+R)

---

## 📈 Future Enhancements

- [ ] Email notifications for alerts
- [ ] Automated reporting (daily summaries)
- [ ] SLA tracking and enforcement
- [ ] Integration with ticketing systems
- [ ] Machine learning for demand prediction

---

## 🤝 Contributing

This is an internal SAMI project. For improvements or bug fixes, please contact the development team.

---

## 📄 License

Proprietary - SA Health / SAMI Internal Use Only

---

## 👥 Credits

**Developed for:** SAMI Support Team  
**Department:** SA Medical Imaging  
**Organization:** SA Health

**Built with:**
- [Streamlit](https://streamlit.io/) - Dashboard framework
- [Plotly](https://plotly.com/) - Interactive visualizations  
- [Pandas](https://pandas.pydata.org/) - Data analysis
- [pywin32](https://github.com/mhammond/pywin32) - Outlook integration

---

## 📞 Support

For questions or support, contact the SAMI IT team.

---

**Made with ❤️ for SAMI Support Team**  
**Version 3.0 - Enterprise Edition**
