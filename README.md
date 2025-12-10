# 🤖 SAMI Transfer Bot

**Automated Round-Robin Email Dispatcher with Real-Time Analytics Dashboard**

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-Dashboard-FF4B4B.svg)](https://streamlit.io)
[![License](https://img.shields.io/badge/License-Internal-green.svg)]()

---

## 🎯 What It Does

The SAMI Transfer Bot automatically distributes incoming emails from a shared Outlook mailbox to team members using a **fair round-robin algorithm**, then provides real-time analytics via a beautiful dashboard.

### Key Features

| Feature | Description |
|---------|-------------|
| ⚖️ **Fair Distribution** | Round-robin ensures equal workload across all team members |
| 📧 **Outlook Integration** | Monitors shared mailbox, forwards & tags emails automatically |
| 📊 **Live Dashboard** | Real-time metrics, charts, and team analytics |
| 🛡️ **Smart Filter** | Distinguishes staff replies from new tickets (no lost tickets!) |
| 🌓 **Dark/Light Mode** | Theme toggle for presenter preference |
| 📥 **Data Export** | Download filtered data as CSV |

---

## 📸 Dashboard Preview

The dashboard provides:
- 📈 **Workload Distribution** - See who's handling what
- 🕒 **Hourly Activity Trend** - Peak hours visualization
- 🔥 **Heatmap** - Request volume by day/hour
- 📊 **Week-over-Week Performance** - Completion rates & trends
- 📂 **Raw Data Viewer** - Live view of underlying CSV data
- 👤 **Individual Staff Stats** - Drill-down per team member

---

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Microsoft Outlook (for bot functionality)
- Chrome/Edge/Firefox (for dashboard)

### Installation

```bash
# Clone the repository
git clone https://github.com/HagglesworthMD/TRANSFER-BOT.git
cd TRANSFER-BOT

# Create virtual environment
python -m venv venv

# Activate (Windows)
venv\Scripts\activate
# Activate (Linux/Mac)
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Running the Dashboard

```bash
streamlit run dashboard.py
```
Opens at `http://localhost:8501`

### Running the Bot (Windows Only)

```bash
python distributor.py
```
Requires Outlook to be running with access to the shared mailbox.

### Demo Mode (No Outlook Required)

```bash
# Terminal 1: Start dashboard
streamlit run dashboard.py

# Terminal 2: Start simulator
python demo_simulator.py
```
Watch the dashboard update in real-time as the simulator adds entries!

---

## 📁 Project Structure

```
TRANSFER BOT/
├── 🤖 Core
│   ├── distributor.py      # Main bot (Outlook integration)
│   ├── dashboard.py        # Streamlit analytics dashboard
│   └── demo_simulator.py   # Demo mode simulator
│
├── 📊 Data
│   ├── staff.txt           # Team member list
│   ├── roster_state.json   # Round-robin state
│   └── daily_stats.csv     # Activity log
│
├── 📚 Documentation
│   ├── README.md           # This file
│   ├── CHANGELOG.md        # Version history
│   ├── SYSTEM_ARCHITECTURE.md  # 🆕 Flow diagrams & logic explained
│   ├── SMART_FILTER_WORKFLOW.md  # Filter logic docs
│   ├── WINDOWS_SETUP.md    # Windows installation
│   └── HOW_TO_RUN.md       # Quick start guide
│
└── 🪟 Windows Launchers
    ├── START_BOT.bat       # Launch bot
    ├── START_DEMO.bat      # Launch demo mode
    └── START_EVERYTHING.bat # Launch all
```

---

## ⚙️ Configuration

### staff.txt
Add one email per line:
```
brian.shaw@sa.gov.au
jason.quinn2@sa.gov.au
john.drousas@sa.gov.au
```

### distributor.py
```python
LIVE_MAILBOX_NAME = "Health:SAMISupportTeam"  # Shared mailbox name
LIVE_PROCESSED_FOLDER = "Done"                 # Folder for processed emails
```

---

## 🛡️ Smart Filter Logic

The bot uses intelligent filtering to avoid losing tickets:

| Sender | Subject Pattern | Action |
|--------|-----------------|--------|
| Staff | `RE: ...` | ✅ Archive as completion |
| Staff | Contains `[Assigned:` | ✅ Archive as completion |
| Staff | **New email** | 📨 Assign via round-robin |
| External | Any | 📨 Assign via round-robin |

**Why?** Staff can email the helpdesk to log their own issues without them being accidentally archived.

See [SMART_FILTER_WORKFLOW.md](SMART_FILTER_WORKFLOW.md) for full details.

---

## 📊 Dashboard Sections

### Executive Summary
- System status
- Today's activity count
- Active team members
- Top request source
- AI-generated insights

### Workload Distribution
- Horizontal bar chart
- Unique colors per staff member
- Live updates

### Week-over-Week Performance
- Request volume comparison
- Completion rate
- Average per day
- Trend indicator

### Peak Hours Heatmap
- Request volume by day/hour
- Helps optimize staffing

### Raw Data Viewer
- Live CSV data display
- Filtering by type/date/staff
- CSV export

---

## 🔄 How Round-Robin Works

```
Email 1 → brian.shaw
Email 2 → jason.quinn2
Email 3 → john.drousas
Email 4 → brian.shaw  (cycle repeats)
...
```

State is persisted in `roster_state.json`:
```json
{
    "current_index": 47,
    "total_processed": 356
}
```

---

## 📝 Changelog

See [CHANGELOG.md](CHANGELOG.md) for version history.

**Latest: v2.1.0** - Smart Filter implementation, Dashboard overhaul

---

## 🤝 Contributing

This is an internal tool for SA Health SAMI Support Team.

---

## 📄 License

Internal use only. © 2025 SA Health
