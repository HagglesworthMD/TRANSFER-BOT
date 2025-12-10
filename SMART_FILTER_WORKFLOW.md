# 🤖 Smart Filter Workflow Logic

## Overview

The Round-Robin Email Dispatcher now uses a **Smart Filter** to intelligently distinguish between:
- ✅ **Staff replies** to existing tickets (should be archived as completions)
- 📨 **Staff's own genuine tickets** (should be assigned like any other customer request)

---

## The Problem (Before)

**Old Logic:**
```
IF sender IS in staff.txt THEN mark as done/archive
```

**Why this was dangerous:**
- If a staff member emailed the helpdesk to log a genuine ticket (e.g., "My laptop is broken"), the bot would archive it immediately
- **No one would ever see it** - the ticket was lost
- This was a **Single Point of Failure**

---

## The Solution (Smart Filter)

**New Logic:**
```
IF sender IS in staff.txt AND (subject is a REPLY OR contains bot tags)
    THEN mark as complete/archive
ELSE
    TREAT AS NEW TICKET → Assign via Round-Robin
```

### Decision Matrix:

| Sender | Subject | Action |
|--------|---------|--------|
| Staff | Starts with `RE:` | ⏩ Archive as completion |
| Staff | Starts with `Accepted:` / `Declined:` | ⏩ Archive as completion |
| Staff | Contains `[Assigned:` | ⏩ Archive as completion |
| Staff | Contains `[COMPLETED:` | ⏩ Archive as completion |
| Staff | **NEW email (no prefix)** | 📨 **Assign as new ticket!** |
| External | Any | 📨 Assign as new ticket |

---

## Technical Implementation

### Reply Detection Patterns:
```python
reply_prefixes = ('re:', 'accepted:', 'declined:', 'fw:', 'fwd:')
is_reply = subject.lower().startswith(reply_prefixes)
is_bot_tagged = '[assigned:' in subject.lower() or '[completed:' in subject.lower()
```

### Smart Filter Check:
```python
is_internal_reply = is_staff_sender and (is_reply or is_bot_tagged)

if is_internal_reply:
    # Archive as completion
else:
    # Treat as new ticket - assign via round-robin
```

---

## Logging

The bot now logs specific events:

| Log Message | Meaning |
|-------------|---------|
| `⏩ Skipped internal reply from {email}: {subject}` | Staff reply archived |
| `📨 Staff member {email} submitted NEW ticket: {subject}` | Staff's own ticket being assigned |
| `[LIVE TEST] Assigned to {person}` | New ticket assigned to staff |

---

## Benefits

1. **No Lost Tickets**: Staff can now email the helpdesk to log their own issues
2. **Accurate Completion Tracking**: Only actual replies are counted as completions
3. **Clear Audit Trail**: Logs show exactly why each email was handled the way it was
4. **Backwards Compatible**: Existing workflow for external customers unchanged

---

## Example Scenarios

### Scenario 1: Staff Completes a Ticket ✅
```
From: john.drousas@sa.gov.au
Subject: RE: [Assigned: john.drousas@sa.gov.au] CT Scan Transfer
→ Smart Filter: is_reply=True, is_staff=True
→ Action: ARCHIVE AS COMPLETE
→ Log: "⏩ Skipped internal reply from john.drousas@sa.gov.au"
```

### Scenario 2: Staff Logs Their Own Ticket 📨
```
From: john.drousas@sa.gov.au
Subject: My computer won't turn on
→ Smart Filter: is_reply=False, is_bot_tagged=False
→ Action: ASSIGN TO NEXT PERSON (not John!)
→ Log: "📨 Staff member john.drousas@sa.gov.au submitted NEW ticket"
```

### Scenario 3: External Customer Request 📨
```
From: jones.radiology@hospital.com.au
Subject: CT Scan Transfer Request - Patient Smith
→ Smart Filter: is_staff=False
→ Action: ASSIGN TO NEXT PERSON
→ Log: "[LIVE TEST] Assigned to brian.shaw@sa.gov.au"
```

---

## Summary

The Smart Filter ensures:
- ✅ Staff replies → Marked complete
- ✅ Staff's own tickets → Assigned fairly
- ✅ Customer requests → Assigned normally
- ❌ No tickets lost
- ❌ No false completions

**This fix eliminates the Single Point of Failure.**
