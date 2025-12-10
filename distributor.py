"""
Helpdesk Clinical Safety Bot v2.2
Risk-Aware Clinical Dispatcher with SLA Watchdog

Features:
- Fair round-robin distribution
- Semantic risk detection (deletions, urgent requests)
- 20-minute SLA enforcement
- Manager escalation on breach
- Robust error handling (never crashes)
"""

import os
import sys
import time
import json
import csv
import schedule
from datetime import datetime, timedelta

# Windows-specific imports (graceful fallback for Linux/Mac)
try:
    import win32com.client
    OUTLOOK_AVAILABLE = True
except ImportError:
    OUTLOOK_AVAILABLE = False
    print("⚠️ pywin32 not available - running in demo mode")

# ==================== CONFIGURATION ====================
CONFIG = {
    "mailbox": "Health:HelpdeskSupportTeam",
    "manager": "manager@example.com",
    "sla_minutes": 20,
    "check_interval_seconds": 60,
    "processed_folder": "Done"
}

FILES = {
    "staff": "staff.txt",
    "state": "roster_state.json",
    "log": "daily_stats.csv",
    "watchdog": "urgent_watchdog.json"
}

# ==================== SEMANTIC DICTIONARY ====================
# Risk Detection: (Action + Context) OR (Urgency + Action) OR (High Importance)

RISK_ACTIONS = [
    "delete", "deletion", "remove", "unlink", "purge", "erase", "destroy",
    "cancel", "void", "nullify", "terminate", 
    "merge", "merging", "merged", "split", "splitting",
    "combine", "duplicate", "dedupe", "dedup"
]

RISK_CONTEXT = [
    "patient", "scan", "accession", "study", "exam", "report",
    "imaging", "dicom", "mri", "ct", "ultrasound", "xray", "x-ray",
    "record", "data", "file", "prior", "comparison"
]

URGENCY_WORDS = [
    "stat", "asap", "urgent", "emergency", "critical", "immediate",
    "now", "rush", "priority", "life-threatening", "code"
]

# ==================== LOGGING ====================
def log(msg, level="INFO"):
    """Timestamped logging"""
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    symbol = {"INFO": "ℹ️", "WARN": "⚠️", "ERROR": "❌", "CRITICAL": "🚨", "SUCCESS": "✅"}.get(level, "📝")
    print(f"[{timestamp}] {symbol} {msg}")
    
    # Also append to log file
    try:
        with open("bot_activity.log", "a", encoding="utf-8") as f:
            f.write(f"[{timestamp}] [{level}] {msg}\n")
    except:
        pass

# ==================== FILE OPERATIONS ====================
def get_staff_list():
    """Load staff list from file"""
    try:
        if not os.path.exists(FILES["staff"]):
            return []
        with open(FILES["staff"], 'r') as f:
            return [line.strip().lower() for line in f if line.strip() and not line.startswith('#')]
    except Exception as e:
        log(f"Error loading staff list: {e}", "ERROR")
        return []

def get_roster_state():
    """Load roster state from JSON"""
    try:
        if os.path.exists(FILES["state"]):
            with open(FILES["state"], 'r') as f:
                return json.load(f)
    except:
        pass
    return {"current_index": 0, "total_processed": 0}

def save_roster_state(state):
    """Save roster state to JSON"""
    try:
        with open(FILES["state"], 'w') as f:
            json.dump(state, f, indent=4)
    except Exception as e:
        log(f"Error saving roster state: {e}", "ERROR")

def get_next_staff():
    """Get next staff member in rotation"""
    staff = get_staff_list()
    if not staff:
        return None
    
    state = get_roster_state()
    idx = state.get("current_index", 0)
    
    person = staff[idx % len(staff)]
    
    # Update state
    state["current_index"] = idx + 1
    state["total_processed"] = state.get("total_processed", 0) + 1
    save_roster_state(state)
    
    return person

def append_stats(subject, assigned_to, sender="unknown", risk_level="normal"):
    """Append entry to daily stats CSV"""
    try:
        file_exists = os.path.isfile(FILES["log"])
        with open(FILES["log"], 'a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            if not file_exists:
                writer.writerow(['Date', 'Time', 'Subject', 'Assigned To', 'Sender', 'Risk Level'])
            now = datetime.now()
            writer.writerow([
                now.strftime('%Y-%m-%d'),
                now.strftime('%H:%M:%S'),
                subject,
                assigned_to,
                sender,
                risk_level
            ])
    except Exception as e:
        log(f"Error writing stats: {e}", "ERROR")

# ==================== WATCHDOG OPERATIONS ====================
def load_watchdog():
    """Load urgent watchdog from JSON"""
    try:
        if os.path.exists(FILES["watchdog"]):
            with open(FILES["watchdog"], 'r') as f:
                return json.load(f)
    except:
        pass
    return {}

def save_watchdog(data):
    """Save urgent watchdog to JSON"""
    try:
        with open(FILES["watchdog"], 'w') as f:
            json.dump(data, f, indent=4, default=str)
    except Exception as e:
        log(f"Error saving watchdog: {e}", "ERROR")

def add_to_watchdog(msg_id, subject, assigned_to, sender, risk_type):
    """Add urgent ticket to watchdog"""
    watchdog = load_watchdog()
    watchdog[msg_id] = {
        "subject": subject[:100],
        "assigned_to": assigned_to,
        "sender": sender,
        "risk_type": risk_type,
        "timestamp": datetime.now().isoformat(),
        "escalation_count": 0
    }
    save_watchdog(watchdog)
    log(f"🚨 Added to watchdog: {subject[:50]}... -> {assigned_to}", "CRITICAL")

def remove_from_watchdog(msg_id):
    """Remove completed ticket from watchdog"""
    watchdog = load_watchdog()
    if msg_id in watchdog:
        del watchdog[msg_id]
        save_watchdog(watchdog)
        log(f"✅ Removed from watchdog: {msg_id}", "SUCCESS")

# ==================== RISK DETECTION ====================
def detect_risk(subject, body="", high_importance=False):
    """
    Semantic risk detection using (Action + Context) OR (Urgency + Action) logic.
    
    Returns: ("normal", "urgent", or "critical"), risk_reason
    """
    text = (subject + " " + body).lower()
    
    # Check for risk actions
    found_actions = [a for a in RISK_ACTIONS if a in text]
    found_context = [c for c in RISK_CONTEXT if c in text]
    found_urgency = [u for u in URGENCY_WORDS if u in text]
    
    # Rule 1: High Importance Flag (Outlook) = CRITICAL
    if high_importance:
        return "critical", "Outlook High Importance Flag"
    
    # Rule 2: (Action + Context) = CRITICAL (e.g., "delete patient scan")
    if found_actions and found_context:
        return "critical", f"Action+Context: {found_actions[0]}+{found_context[0]}"
    
    # Rule 3: (Urgency + Action) = CRITICAL (e.g., "STAT delete request")
    if found_urgency and found_actions:
        return "critical", f"Urgency+Action: {found_urgency[0]}+{found_actions[0]}"
    
    # Rule 4: Urgency words alone = URGENT
    if found_urgency:
        return "urgent", f"Urgency: {found_urgency[0]}"
    
    # Rule 5: Risk actions alone (without context) = WARN but not critical
    if found_actions:
        return "urgent", f"Action detected: {found_actions[0]}"
    
    return "normal", None

# ==================== SMART FILTER ====================
def is_internal_reply(sender_email, subject, staff_list):
    """
    Smart Filter: Only skip if:
    1. Sender IS in staff.txt AND
    2. Subject indicates a REPLY (RE:, Accepted:, etc.) OR contains bot tags
    """
    is_staff = sender_email.lower() in staff_list
    
    reply_prefixes = ('re:', 'accepted:', 'declined:', 'fw:', 'fwd:')
    is_reply = subject.lower().strip().startswith(reply_prefixes)
    is_bot_tagged = '[assigned:' in subject.lower() or '[completed:' in subject.lower()
    
    return is_staff and (is_reply or is_bot_tagged)

# ==================== SLA WATCHDOG CHECK ====================
def check_sla_breaches():
    """
    Check all urgent tickets for SLA breaches.
    If > 20 minutes: Re-assign, escalate to manager, log SLA_FAIL
    """
    watchdog = load_watchdog()
    if not watchdog:
        return
    
    now = datetime.now()
    sla_limit = timedelta(minutes=CONFIG["sla_minutes"])
    
    for msg_id, ticket in list(watchdog.items()):
        try:
            ticket_time = datetime.fromisoformat(ticket["timestamp"])
            elapsed = now - ticket_time
            
            if elapsed > sla_limit:
                # SLA BREACH!
                log(f"🚨 SLA BREACH: {ticket['subject'][:50]}... ({elapsed.seconds // 60}m elapsed)", "CRITICAL")
                
                # Re-assign to next staff member
                new_assignee = get_next_staff()
                if new_assignee and new_assignee != ticket["assigned_to"]:
                    log(f"🔄 Re-assigning from {ticket['assigned_to']} to {new_assignee}", "WARN")
                
                # Escalate to manager (would send email in real implementation)
                escalate_to_manager(ticket, elapsed)
                
                # Update watchdog with reset timer and escalation count
                watchdog[msg_id]["timestamp"] = now.isoformat()
                watchdog[msg_id]["escalation_count"] = ticket.get("escalation_count", 0) + 1
                watchdog[msg_id]["assigned_to"] = new_assignee or ticket["assigned_to"]
                
                # Log SLA failure
                append_stats(
                    f"[SLA_FAIL] {ticket['subject'][:50]}",
                    ticket["assigned_to"],
                    ticket["sender"],
                    "SLA_BREACH"
                )
                
        except Exception as e:
            log(f"Error checking SLA for {msg_id}: {e}", "ERROR")
    
    save_watchdog(watchdog)

def escalate_to_manager(ticket, elapsed):
    """Send escalation email to manager"""
    manager = CONFIG["manager"]
    log(f"📧 Escalating to manager ({manager}): {ticket['subject'][:30]}...", "CRITICAL")
    
    # In production, this would send an actual email
    # For now, we log the escalation
    try:
        with open("escalations.log", "a", encoding="utf-8") as f:
            f.write(f"[{datetime.now().isoformat()}] ESCALATION\n")
            f.write(f"  Manager: {manager}\n")
            f.write(f"  Subject: {ticket['subject']}\n")
            f.write(f"  Original Assignee: {ticket['assigned_to']}\n")
            f.write(f"  Risk Type: {ticket['risk_type']}\n")
            f.write(f"  Time Elapsed: {elapsed.seconds // 60} minutes\n")
            f.write(f"  Escalation Count: {ticket.get('escalation_count', 0) + 1}\n")
            f.write("-" * 50 + "\n")
    except:
        pass

# ==================== MAIN EMAIL PROCESSING ====================
def process_inbox():
    """Main email processing loop with risk detection"""
    if not OUTLOOK_AVAILABLE:
        log("Outlook not available - skipping inbox check", "WARN")
        return
    
    try:
        outlook = win32com.client.Dispatch("Outlook.Application").GetNamespace("MAPI")
        
        # Find shared mailbox
        mailbox = None
        for i in range(50):
            try:
                folder = outlook.Folders(i)
                if folder.Name.lower().strip() == CONFIG["mailbox"].lower().strip():
                    mailbox = folder
                    break
            except:
                pass
        
        if not mailbox:
            log(f"Cannot find mailbox: {CONFIG['mailbox']}", "ERROR")
            return
        
        inbox = mailbox.Folders["Inbox"]
        try:
            processed = inbox.Folders[CONFIG["processed_folder"]]
        except:
            log(f"Cannot find processed folder: {CONFIG['processed_folder']}", "ERROR")
            return
        
        # Get unread messages
        msgs = list(inbox.Items.Restrict("[UnRead] = True"))
        if not msgs:
            return  # No new messages
        
        staff_list = get_staff_list()
        
        for msg in msgs:
            try:
                # Extract email details
                try:
                    sender_email = msg.SenderEmailAddress.lower()
                except:
                    sender_email = "unknown"
                
                try:
                    subject = msg.Subject.strip()
                except:
                    subject = ""
                
                try:
                    body = msg.Body[:500] if msg.Body else ""  # First 500 chars
                except:
                    body = ""
                
                try:
                    high_importance = (msg.Importance == 2)  # 2 = High
                except:
                    high_importance = False
                
                try:
                    msg_id = msg.EntryID
                except:
                    msg_id = str(hash(subject + sender_email))
                
                # ===== SMART FILTER =====
                if is_internal_reply(sender_email, subject, staff_list):
                    log(f"⏩ Skipped internal reply from {sender_email}: {subject[:50]}...")
                    msg.Subject = f"[COMPLETED: {sender_email}] {msg.Subject}"
                    msg.Save()
                    append_stats(msg.Subject, "completed", sender_email, "normal")
                    msg.UnRead = False
                    msg.Move(processed)
                    
                    # If this was in watchdog, remove it
                    remove_from_watchdog(msg_id)
                    continue
                
                # ===== RISK DETECTION =====
                risk_level, risk_reason = detect_risk(subject, body, high_importance)
                
                if risk_level != "normal":
                    log(f"⚠️ Risk detected [{risk_level.upper()}]: {risk_reason}", "WARN")
                
                # ===== ROUND-ROBIN ASSIGNMENT =====
                assignee = get_next_staff()
                if not assignee:
                    log("No staff available for assignment!", "ERROR")
                    continue
                
                # Forward email
                fwd = msg.Forward()
                fwd.Recipients.Add(assignee)
                
                # Add risk warning if applicable
                if risk_level in ("urgent", "critical"):
                    risk_banner = (
                        "━" * 60 + "\n"
                        f"🚨 {risk_level.upper()} RISK TICKET 🚨\n"
                        f"Reason: {risk_reason}\n"
                        f"SLA: {CONFIG['sla_minutes']} MINUTES\n"
                        "━" * 60 + "\n\n"
                    )
                    fwd.Body = risk_banner + fwd.Body
                    
                    # Add to watchdog for SLA tracking
                    add_to_watchdog(msg_id, subject, assignee, sender_email, risk_reason)
                else:
                    fwd.Body = f"--- 🤖 AUTO-ASSIGNED TO {assignee} ---\n\n" + fwd.Body
                
                fwd.SentOnBehalfOfName = CONFIG["mailbox"]
                fwd.Send()
                
                log(f"[{risk_level.upper()}] Assigned to {assignee}: {subject[:50]}...")
                
                # Tag and archive original
                risk_tag = f"[{risk_level.upper()}]" if risk_level != "normal" else ""
                msg.Subject = f"[Assigned: {assignee}] {risk_tag} {msg.Subject}"
                msg.Save()
                
                append_stats(msg.Subject, assignee, sender_email, risk_level)
                msg.UnRead = False
                msg.Move(processed)
                
            except Exception as e:
                log(f"Error processing email: {e}", "ERROR")
                continue  # Don't crash - continue to next email
        
    except Exception as e:
        log(f"Outlook connection error: {e}", "ERROR")
        # Don't crash - will retry next cycle

def run_job():
    """Main job: Process inbox AND check SLA breaches"""
    try:
        process_inbox()
    except Exception as e:
        log(f"Error in process_inbox: {e}", "ERROR")
    
    try:
        check_sla_breaches()
    except Exception as e:
        log(f"Error in check_sla_breaches: {e}", "ERROR")

# ==================== MAIN ENTRY POINT ====================
if __name__ == "__main__":
    log("=" * 60)
    log("🏥 Helpdesk Clinical Safety Bot v2.2")
    log("=" * 60)
    log(f"Mailbox: {CONFIG['mailbox']}")
    log(f"Manager: {CONFIG['manager']}")
    log(f"SLA Limit: {CONFIG['sla_minutes']} minutes")
    log(f"Staff loaded: {len(get_staff_list())} members")
    log("=" * 60)
    
    # Initialize watchdog file if needed
    if not os.path.exists(FILES["watchdog"]):
        save_watchdog({})
        log("Initialized empty watchdog file")
    
    # Run immediately
    run_job()
    
    # Schedule to run every minute
    schedule.every(CONFIG["check_interval_seconds"]).seconds.do(run_job)
    
    log("🔄 Entering main loop (Ctrl+C to stop)")
    
    while True:
        try:
            schedule.run_pending()
            time.sleep(1)
        except KeyboardInterrupt:
            log("Bot stopped by user", "INFO")
            break
        except Exception as e:
            log(f"Unexpected error in main loop: {e}", "ERROR")
            time.sleep(5)  # Wait before retry