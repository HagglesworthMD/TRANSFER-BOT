# 📋 Changelog

All notable changes to the SAMI Transfer Bot project.

---

## [2.2.0] - 2025-12-11 🏥 Clinical Safety Release

### 🚨 NEW: Risk-Aware Urgent Filter

**The Problem:** Critical requests (deletions, STAT cases) were being treated the same as routine transfers.

**The Solution:** Semantic risk detection with SLA enforcement.

#### Urgent Filter Workflow:
```
INCOMING EMAIL
      │
      ▼
┌─────────────────────────┐
│  SEMANTIC RISK CHECK    │
│  • Contains "delete"?   │
│  • Contains "patient"?  │
│  • Marked URGENT?       │
└─────────────────────────┘
      │
      ├── CRITICAL ──▶ 🚨 20-min SLA timer starts
      │                   └── If breached: Re-assign + Escalate to Manager
      │
      ├── URGENT ────▶ ⚠️ Flagged in dashboard
      │
      └── NORMAL ────▶ ✅ Standard round-robin
```

#### Risk Detection Rules:
| Condition | Risk Level |
|-----------|------------|
| Action + Context (e.g., "delete patient scan") | 🚨 CRITICAL |
| Urgency + Action (e.g., "STAT delete") | 🚨 CRITICAL |
| Outlook High Importance Flag | 🚨 CRITICAL |
| Urgency word alone (e.g., "ASAP") | ⚠️ URGENT |
| Normal request | ✅ NORMAL |

#### New Dashboard: Clinical Control Tower
- **Green Banner:** System Normal - no urgent tickets
- **Yellow Banner:** Active risks being monitored
- **Red Banner:** SLA BREACH - ticket exceeded 20 minutes!

---

## [2.1.0] - 2025-12-10 🛡️ Smart Filter

### Fixed: Single Point of Failure
**Problem:** Staff emails were blindly archived, losing tickets when staff logged their own issues.

**Solution:** Smart Filter only archives if:
- Sender IS in staff.txt AND
- Subject starts with "RE:", "Accepted:", "Declined:" OR contains "[Assigned:"

Staff sending NEW emails are now treated as customers!

---

## [2.0.0] - 2025-12-10 📊 Dashboard Overhaul

### Added
- Raw Data Viewer with filtering
- Demo Simulator for live demonstrations
- Email John Button (Easter egg)
- Info buttons for each chart
- Dark/Light mode toggle
- Completion rate tracking
- 3 weeks of historical data

### Fixed
- Chart visibility in light mode
- Theme-aware colors
- Completion rate showing 0%

---

## [1.0.0] - 2025-12-08 🚀 Initial Release

### Core Features
- Round-robin email distribution
- Outlook shared mailbox integration
- Real-time Streamlit dashboard
- Staff workload balancing
- Daily stats CSV logging

---

## How Metrics Are Calculated

### Response Time Tracking:
```
1. EMAIL ARRIVES
   └── Bot logs: [Assigned: staff@] + TIMESTAMP
   
2. STAFF REPLIES (CC's shared inbox)
   └── Bot logs: [COMPLETED: staff@] + TIMESTAMP
   
3. DASHBOARD CALCULATES
   └── Response Time = COMPLETED timestamp - ASSIGNED timestamp
   └── Completion Rate = COMPLETED count / ASSIGNED count × 100
```

### The CSV Contains:
```csv
Date,Time,Subject,Assigned To,Sender,Risk Level
2025-12-11,08:30:00,[Assigned: chuck.norris@...],chuck.norris@sa.gov.au,sender@...,normal
2025-12-11,09:15:00,[COMPLETED: chuck.norris@...],completed,chuck.norris@sa.gov.au,normal
```

---

## File Structure
```
TRANSFER BOT/
├── distributor.py      # V2.2 Clinical Safety Bot
├── dashboard.py        # Live dashboard with Control Tower
├── demo_simulator.py   # Demo mode (no Outlook needed)
├── daily_stats.csv     # All activity logs
├── urgent_watchdog.json # SLA tracking
├── staff.txt           # Team members
└── roster_state.json   # Round-robin state
```
