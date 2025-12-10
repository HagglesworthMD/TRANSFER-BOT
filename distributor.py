import win32com.client
import os
import time
import json
import csv
import schedule
from datetime import datetime

# --- CONFIGURATION ---
# FALSE = LIVE MODE (Processes the real SAMI emails)
TEST_MODE = False

# LIVE SETTINGS (Matches your screenshot)
LIVE_MAILBOX_NAME = "Health:SAMISupportTeam" 
LIVE_PROCESSED_FOLDER = "Done"

FILES = {
    "staff": "staff.txt",
    "state": "roster_state.json",
    "log": "daily_stats.csv"
}

def log(msg):
    print(f"[{datetime.now().strftime('%H:%M:%S')}] {msg}")

def get_staff_list():
    if not os.path.exists(FILES["staff"]): return []
    with open(FILES["staff"], 'r') as f:
        return [l.strip().lower() for l in f if l.strip()]

def append_stats(subject, assigned_to, sender="unknown"):
    file_exists = os.path.isfile(FILES["log"])
    with open(FILES["log"], 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(['Date', 'Time', 'Subject', 'Assigned To', 'Sender'])
        now = datetime.now()
        writer.writerow([now.strftime('%Y-%m-%d'), now.strftime('%H:%M:%S'), subject, assigned_to, sender])

def get_next_staff():
    staff = get_staff_list()
    if not staff: return None
    
    idx = 0
    if os.path.exists(FILES["state"]):
        try:
            with open(FILES["state"], 'r') as f: idx = json.load(f).get('index', 0)
        except: pass
    
    person = staff[idx % len(staff)]
    with open(FILES["state"], 'w') as f: json.dump({'index': idx + 1}, f)
    return person

def run_job():
    try:
        outlook = win32com.client.Dispatch("Outlook.Application").GetNamespace("MAPI")
        
        # --- CONNECT TO THE SHARED MAILBOX ---
        mailbox = None
        for i in range(50):
            try:
                folder = outlook.Folders(i)
                if folder.Name.lower().strip() == LIVE_MAILBOX_NAME.lower().strip():
                    mailbox = folder
                    break
            except: pass
            
        if not mailbox:
            log(f"CRITICAL: Cannot find mailbox named '{LIVE_MAILBOX_NAME}' in your Outlook sidebar.")
            return

        inbox = mailbox.Folders["Inbox"]
        try:
            processed = inbox.Folders[LIVE_PROCESSED_FOLDER]
        except:
            log(f"Error: Could not find folder '{LIVE_PROCESSED_FOLDER}' inside {LIVE_MAILBOX_NAME} Inbox.")
            return

        # --- PROCESS UNREAD EMAILS ---
        msgs = list(inbox.Items.Restrict("[UnRead] = True"))
        if not msgs: return

        staff_list = get_staff_list()

        for msg in msgs:
            try:
                sender_email = msg.SenderEmailAddress.lower()
            except:
                sender_email = "unknown"
            
            try:
                subject = msg.Subject.strip()
            except:
                subject = ""
            
            # ==================== SMART FILTER ====================
            # Only treat as internal reply/completion if:
            # 1. Sender IS in staff.txt AND
            # 2. Subject indicates a REPLY (starts with RE:, Accepted:, Declined:)
            #    OR contains the bot's own tag [Assigned: (staff replying to assigned ticket)
            #
            # This prevents staff's OWN genuine tickets from being archived!
            # =========================================================
            
            is_staff_sender = sender_email in staff_list
            
            # Check if subject indicates this is a REPLY, not a new ticket
            reply_prefixes = ('re:', 'accepted:', 'declined:', 'fw:', 'fwd:')
            is_reply = subject.lower().startswith(reply_prefixes)
            is_bot_tagged = '[assigned:' in subject.lower() or '[completed:' in subject.lower()
            
            is_internal_reply = is_staff_sender and (is_reply or is_bot_tagged)
            
            if is_internal_reply:
                # This IS a staff reply to an existing ticket - mark as complete
                log(f"⏩ Skipped internal reply from {sender_email}: {subject[:50]}...")
                msg.Subject = f"[COMPLETED: {sender_email}] {msg.Subject}"
                msg.Save()
                append_stats(msg.Subject, "completed", sender_email)
                msg.UnRead = False
                msg.Move(processed)
                continue
            
            # If staff sends a NEW email (not a reply), treat as new ticket!
            if is_staff_sender and not is_internal_reply:
                log(f"📨 Staff member {sender_email} submitted NEW ticket: {subject[:50]}...")

            # 2. IF NOT STAFF, ASSIGN IT
            person = get_next_staff()
            if not person: 
                log("Error: No staff found in staff.txt")
                return

            fwd = msg.Forward()
            fwd.Recipients.Add(person)
            
            # --- THE TESTING NOTICE ---
            notice = (
                "****************************************************************\n"
                "⚠️ TESTING NOTICE: NEW AUTOMATION SYSTEM ⚠️\n"
                "This is a LIVE TEST of the Ticket Traffic Controller.\n"
                "This ticket has been auto-assigned to you to verify the workflow.\n"
                "Please process as normal or reply 'DONE' to close it.\n"
                "****************************************************************\n\n"
            )
            
            fwd.Body = notice + f"--- 🤖 AUTO-ASSIGNED TO {person} ---\n\n" + fwd.Body
            
            # SEND ON BEHALF OF THE SHARED MAILBOX
            fwd.SentOnBehalfOfName = LIVE_MAILBOX_NAME
            fwd.Send()
            log(f"[LIVE TEST] Assigned to {person}")

            # 3. RENAME AND FILE
            msg.Subject = f"[Assigned: {person}] {msg.Subject}"
            msg.Save()
            
            append_stats(msg.Subject, person, sender_email)
            msg.UnRead = False
            msg.Move(processed)

    except Exception as e:
        log(f"Error: {e}")

if __name__ == "__main__":
    log(f"System Online. Monitoring: {LIVE_MAILBOX_NAME}")
    log("Mode: LIVE TEST (Notices Active)")
    run_job()
    schedule.every(1).minutes.do(run_job)
    while True:
        schedule.run_pending()
        time.sleep(1)