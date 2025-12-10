# 🏗️ System Architecture & Logic

A lightweight, easy-to-follow guide to how the Helpdesk Transfer Bot works.

---

## 📊 System Flow Diagram

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                              INCOMING EMAIL                                  │
│                    (Shared Mailbox: Health:HelpdeskSupportTeam)                 │
└─────────────────────────────────────────────────────────────────────────────┘
                                      │
                                      ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                           📬 BOT CHECKS INBOX                                │
│                        (Every 1 minute via scheduler)                        │
└─────────────────────────────────────────────────────────────────────────────┘
                                      │
                                      ▼
                    ┌─────────────────────────────────┐
                    │     Is email UNREAD?            │
                    └─────────────────────────────────┘
                         │                    │
                        YES                   NO
                         │                    │
                         ▼                    ▼
                    Continue             Skip (already processed)
                         │
                         ▼
         ┌───────────────────────────────────────────┐
         │  SMART FILTER: Who sent this?             │
         │  Is sender in staff.txt?                  │
         └───────────────────────────────────────────┘
                  │                          │
             YES (Staff)               NO (External)
                  │                          │
                  ▼                          │
    ┌────────────────────────────┐           │
    │ Is it a REPLY?             │           │
    │ • Starts with "RE:"?       │           │
    │ • Contains "[Assigned:"?   │           │
    └────────────────────────────┘           │
           │              │                  │
          YES            NO                  │
           │              │                  │
           ▼              ▼                  ▼
    ┌──────────┐   ┌──────────────────────────────────┐
    │ COMPLETE │   │        ROUND-ROBIN ASSIGN        │
    │ (Archive)│   │   Staff ticket = new customer!   │
    └──────────┘   └──────────────────────────────────┘
           │                        │
           ▼                        ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                         📝 LOG TO daily_stats.csv                            │
│                     (Dashboard reads this for metrics)                       │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 🔄 Round-Robin Algorithm (Simple!)

### The Concept
Round-robin is just like dealing cards - each person gets one in turn, then repeat.

```
Email 1  →  Person A
Email 2  →  Person B
Email 3  →  Person C
Email 4  →  Person A  ← Back to start!
Email 5  →  Person B
...
```

### The Code (Simplified)

```python
# staff.txt contains:
# staff1@example.com     (index 0)
# manager@example.com   (index 1)
# staff2@example.com   (index 2)

def get_next_staff():
    # 1. Load the staff list
    staff = ["staff1@", "manager@", "staff2@"]
    
    # 2. Get the current position (stored in roster_state.json)
    current_index = load_from_json()  # e.g., 5
    
    # 3. Use MODULO to wrap around
    # 5 % 3 = 2, so person at index 2 = staff2
    next_person = staff[current_index % len(staff)]
    
    # 4. Increment and save for next time
    save_to_json(current_index + 1)
    
    return next_person
```

### The Magic: Modulo (%)

```
Index 0 % 3 = 0 → Brian
Index 1 % 3 = 1 → Jason
Index 2 % 3 = 2 → John
Index 3 % 3 = 0 → Brian  ← Wraps back!
Index 4 % 3 = 1 → Jason
Index 5 % 3 = 2 → John
...
```

**It never breaks** - no matter how high the index goes, modulo always gives 0, 1, or 2!

---

## 👤 User Permissions (Lightweight)

### No Complex Permissions Needed!

This system is **deliberately simple** - no databases, no user accounts, no passwords.

| File | Who Can Edit | Purpose |
|------|-------------|---------|
| `staff.txt` | Admin only | Controls who receives tickets |
| `roster_state.json` | Bot only | Tracks position in rotation |
| `daily_stats.csv` | Bot only | Activity log (append-only) |

### Adding/Removing Staff

**To add someone:**
```
# Just add their email to staff.txt
echo "new.person@example.com" >> staff.txt
```

**To remove someone:**
```
# Remove their line from staff.txt
# Bot will skip them on next run
```

**No restart needed!** The bot re-reads `staff.txt` on every check.

---

## 📁 File Permissions (Recommended)

```
staff.txt           → Read/Write: Admins only
roster_state.json   → Read/Write: Bot service account
daily_stats.csv     → Read/Write: Bot service account
                   → Read: Dashboard users
```

### Windows (Simple)
Just keep files in a folder only admins can access.

### Linux (If needed)
```bash
chmod 644 staff.txt          # Admin read/write, others read
chmod 644 roster_state.json  # Bot read/write
chmod 644 daily_stats.csv    # Bot write, dashboard read
```

---

## 🧠 Smart Filter Logic (Flowchart)

```
                    ┌─────────────────────┐
                    │   INCOMING EMAIL    │
                    └─────────────────────┘
                              │
                              ▼
                   ┌─────────────────────┐
                   │ Get sender email    │
                   └─────────────────────┘
                              │
                              ▼
              ┌───────────────────────────────┐
              │  Is sender in staff.txt?      │
              └───────────────────────────────┘
                     │              │
                    YES            NO
                     │              │
                     ▼              │
         ┌───────────────────────┐  │
         │ Check subject line:  │  │
         │ • Starts with "RE:"? │  │
         │ • Starts with "FW:"? │  │
         │ • Has "[Assigned:"?  │  │
         └───────────────────────┘  │
              │           │         │
             YES         NO         │
              │           │         │
              ▼           │         │
      ┌──────────────┐    │         │
      │   COMPLETE   │    │         │
      │   (Archive)  │    │         │
      └──────────────┘    │         │
                          │         │
                          ▼         ▼
                    ┌─────────────────────┐
                    │   ASSIGN TO NEXT    │
                    │   STAFF (Round-     │
                    │   Robin)            │
                    └─────────────────────┘
                              │
                              ▼
                    ┌─────────────────────┐
                    │  Forward email +    │
                    │  Tag subject line   │
                    │  [Assigned: x@...]  │
                    └─────────────────────┘
                              │
                              ▼
                    ┌─────────────────────┐
                    │  Move to "Done"     │
                    │  folder             │
                    └─────────────────────┘
```

---

## 📊 Data Flow (Simple)

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   OUTLOOK   │────▶│    BOT      │────▶│   CSV FILE  │
│   MAILBOX   │     │ distributor │     │ daily_stats │
└─────────────┘     │    .py      │     └─────────────┘
                    └─────────────┘            │
                                               │
                                               ▼
                                      ┌─────────────────┐
                                      │    DASHBOARD    │
                                      │  dashboard.py   │
                                      │  (reads CSV)    │
                                      └─────────────────┘
                                               │
                                               ▼
                                      ┌─────────────────┐
                                      │    BROWSER      │
                                      │  localhost:8501 │
                                      └─────────────────┘
```

---

## 🔧 Configuration Summary

| Setting | File | Example |
|---------|------|---------|
| Staff list | `staff.txt` | One email per line |
| Mailbox name | `distributor.py` | `"Health:HelpdeskSupportTeam"` |
| Processed folder | `distributor.py` | `"Done"` |
| Check interval | `distributor.py` | `1 minute` |
| Dashboard refresh | `dashboard.py` | `5 seconds` |

---

## ✅ Why This Design?

| Feature | Benefit |
|---------|---------|
| **No database** | Nothing to install, backup, or maintain |
| **CSV logging** | Human-readable, Excel-compatible |
| **Text file config** | Edit with Notepad, no special tools |
| **Modulo rotation** | Never breaks, always fair |
| **Smart Filter** | No lost tickets, accurate completions |
| **Separate dashboard** | Can run without bot (demo mode) |

---

## 🚨 Failure Modes (What Could Go Wrong)

| Problem | Cause | Solution |
|---------|-------|----------|
| Bot stops | Outlook closed | Keep Outlook running |
| No assignments | Empty staff.txt | Add at least one email |
| Dashboard empty | No CSV data | Run bot or simulator |
| Wrong mailbox | Typo in config | Check `LIVE_MAILBOX_NAME` |

---

## 🎯 TL;DR

1. **Email arrives** in shared mailbox
2. **Bot checks** every minute for unread
3. **Smart Filter** decides: complete or assign?
4. **Round-robin** picks next person (modulo magic)
5. **Forward + tag** email to them
6. **Log to CSV** for dashboard
7. **Dashboard reads** CSV every 5 seconds
8. **You see** beautiful real-time metrics!
