# 📋 Changelog

All notable changes to the SAMI Transfer Bot project are documented in this file.

---

## [2.1.0] - 2025-12-10

### 🛡️ Critical Fix: Smart Filter Logic
**Problem Solved:** Staff emails were being blindly archived, causing lost tickets when staff logged their own issues.

#### Added
- **Smart Filter** - Intelligent email classification that distinguishes between:
  - Staff replies to existing tickets (archived)
  - Staff's own genuine tickets (assigned via round-robin)
- Reply detection patterns: `RE:`, `Accepted:`, `Declined:`, `FW:`, `FWD:`
- Bot tag detection: `[Assigned:`, `[COMPLETED:`
- New log message: `⏩ Skipped internal reply from {email}`
- New log message: `📨 Staff member {email} submitted NEW ticket`
- `SMART_FILTER_WORKFLOW.md` - Full documentation for manager presentation

#### Changed
- `distributor.py` - Complete refactor of email filtering logic
- Completion marker changed from `STAFF-REPLY` to `completed` (lowercase)

---

## [2.0.0] - 2025-12-10

### 🎨 Dashboard Overhaul

#### Added
- **Raw Data Viewer** - Live view of CSV data with filtering options
  - Filter by Type (All/Assignments/Completions)
  - Filter by Date
  - Filter by Staff member
  - Download filtered data as CSV
  - Green highlighting for completed entries
- **Demo Simulator** (`demo_simulator.py`) - Simulates bot activity for live demos
  - Adds fake entries every 3-8 seconds
  - Round-robin staff assignment
  - Random completions
- **Email John Button** - Humorous Easter egg for demos
  - Appears when workload imbalance detected
  - Opens email client with sarcastic pre-written message
- **Info Buttons** - Contextual help for each chart section
- **Theme Toggle** - Dark/Light mode support
- **Completion Rate Tracking** - Week-over-week performance metrics

#### Changed
- Chart colors now adapt to theme (dark text in light mode, white in dark mode)
- Axis labels use proper Plotly API (`title=dict(text=..., font=...)`)
- Total Processed reads from correct JSON key (`total_processed`)
- All staff emails normalized to lowercase for consistency

#### Fixed
- `ValueError: Invalid property 'titlefont'` - Updated to modern Plotly API
- Invisible chart text in light mode
- Completion rate showing 0% (case sensitivity issue)
- Round-robin index reading from wrong JSON key

---

## [1.5.0] - 2025-12-09

### 📊 Analytics Expansion

#### Added
- **Week-over-Week Performance** section with metrics
- **Peak Hours Heatmap** - Visual request volume by day/hour
- **Hourly Activity Trend** - Line chart showing daily patterns
- **7-Day Trend Analysis** - Historical bar chart
- **External Request Sources** - Top senders analysis
- **Staff Leaderboard** - Top performers for the day
- **Individual Staff Drill-down** - Expandable stats per person

#### Changed
- Time format now displays as `HH:00` for clarity
- Removed STAFF-REPLY from all staff visualizations

---

## [1.0.0] - 2025-12-08

### 🚀 Initial Release

#### Added
- **Round-Robin Email Dispatcher** (`distributor.py`)
  - Connects to Outlook shared mailbox
  - Fair distribution across team members
  - Automatic email forwarding with assignment tags
  - Completion tracking via staff replies
- **Live Dashboard** (`dashboard.py`)
  - Real-time metrics with auto-refresh
  - Workload distribution chart
  - Executive summary section
  - Activity feed
- **Configuration Files**
  - `staff.txt` - Team member list
  - `roster_state.json` - Round-robin state
  - `daily_stats.csv` - Activity log
- **Documentation**
  - `README.md` - Project overview
  - `WINDOWS_SETUP.md` - Installation guide
  - `HOW_TO_RUN.md` - Quick start instructions

---

## File Structure

```
TRANSFER BOT/
├── distributor.py          # Main bot script (Outlook integration)
├── dashboard.py            # Streamlit analytics dashboard
├── demo_simulator.py       # Demo mode simulator
├── staff.txt               # Team member list
├── roster_state.json       # Round-robin state
├── daily_stats.csv         # Activity log (auto-generated)
├── config.py               # Configuration settings
├── requirements.txt        # Python dependencies
├── CHANGELOG.md            # This file
├── README.md               # Project overview
├── SMART_FILTER_WORKFLOW.md # Smart filter documentation
├── WINDOWS_SETUP.md        # Windows installation guide
├── HOW_TO_RUN.md           # Quick start guide
├── START_BOT.bat           # Windows launcher (bot)
├── START_DEMO.bat          # Windows launcher (demo mode)
└── START_EVERYTHING.bat    # Launch all components
```

---

## Contributors

- **SAMI Support Team** - Requirements & Testing
- **Automated via AI Assistant** - Development & Documentation
