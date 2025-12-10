#!/usr/bin/env python3
"""
DEMO SIMULATOR - Simulates the bot adding new entries
Run this alongside the dashboard to show live data updates!
Reads staff list from staff.txt to match your actual team.
"""
import csv
import random
import time
import os
from datetime import datetime

def load_staff():
    """Load staff list from staff.txt"""
    staff_file = os.path.join(os.path.dirname(__file__), 'staff.txt')
    try:
        with open(staff_file, 'r') as f:
            return [line.strip().lower() for line in f if line.strip() and not line.startswith('#')]
    except FileNotFoundError:
        print("⚠️ staff.txt not found, using defaults")
        return [
            "brian.shaw@sa.gov.au",
            "jason.quinn2@sa.gov.au",
            "john.drousas@sa.gov.au",
            "betty.spaghetti@sa.gov.au",
            "chuck.norris@sa.gov.au"
        ]

# Load staff from file
STAFF = load_staff()

SENDERS = [
    "jones.radiology@rah.sa.gov.au",
    "imaging.requests@wch.sa.gov.au",
    "tqeh.imaging@sa.gov.au",
    "flinders.radiology@sa.gov.au",
    "mfm.requests@wch.sa.gov.au",
    "lyell.mcewin@nalhn.sa.gov.au",
    "modbury.imaging@nalhn.sa.gov.au"
]

REQUESTS = [
    "CT Scan Transfer Request",
    "MRI Transfer Request", 
    "Ultrasound Transfer",
    "X-Ray Transfer Request",
    "Cardiac Imaging Transfer",
    "PET Scan Transfer",
    "Mammogram Transfer Request"
]

# Urgent requests with DELETION/MERGE keywords (high-risk operations)
URGENT_REQUESTS = [
    "URGENT - Patient Record DELETION Request - Wrong Patient Imaged",
    "STAT - MERGE Patient Records - Duplicate MRN Found",
    "CRITICAL - DELETE Study Request - Privacy Breach",
    "URGENT - MERGE Required - Patient Identity Error",
    "STAT DELETE - Incorrect Patient Data Uploaded",
    "CRITICAL MERGE - Split Patient Records Need Combining",
    "URGENT DELETION - Confidential Study Sent to Wrong Site"
]

PATIENTS = ["Smith J", "Brown M", "Wilson S", "Davis T", "Johnson R", "Lee K", "Patel A", "Garcia M"]

email_count = 0  # Track emails for urgent scheduling
current_index = 0

def add_assignment():
    global current_index, email_count
    email_count += 1
    staff = STAFF[current_index % len(STAFF)]
    current_index += 1
    
    now = datetime.now()
    sender = random.choice(SENDERS)
    patient = random.choice(PATIENTS)
    
    # Every 5th email is URGENT/CRITICAL
    is_urgent = (email_count % 5 == 0)
    
    if is_urgent:
        request = random.choice(URGENT_REQUESTS)
        subject = f"🚨 [CRITICAL] [Assigned: {staff}] {request} - Patient: {patient}"
        risk_level = "critical"
    else:
        request = random.choice(REQUESTS)
        subject = f"[Assigned: {staff}] {request} - Patient: {patient}"
        risk_level = "normal"
    
    # Write to CSV with all columns including Risk Level
    with open('daily_stats.csv', 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow([
            now.strftime('%Y-%m-%d'),
            now.strftime('%H:%M:%S'),
            subject,
            staff,
            sender,
            risk_level
        ])
    
    # Display with friendly name
    friendly_name = staff.split('@')[0].replace('.', ' ').title()
    if is_urgent:
        print(f"🚨 CRITICAL REQUEST assigned to {friendly_name}")
    else:
        print(f"✅ NEW REQUEST assigned to {friendly_name}")
    return staff, is_urgent

def add_completion(staff):
    now = datetime.now()
    subject = f"[COMPLETED: {staff}] Request Completed"
    
    with open('daily_stats.csv', 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow([
            now.strftime('%Y-%m-%d'),
            now.strftime('%H:%M:%S'),
            subject,
            'completed',
            staff,
            'normal'
        ])
    
    friendly_name = staff.split('@')[0].replace('.', ' ').title()
    print(f"✓ COMPLETED by {friendly_name}")

if __name__ == "__main__":
    print("=" * 50)
    print("🤖 TRANSFER BOT SIMULATOR")
    print("=" * 50)
    print(f"Loaded {len(STAFF)} staff members from staff.txt")
    print("Staff: " + ", ".join([s.split('@')[0].replace('.', ' ').title() for s in STAFF[:5]]) + "...")
    print()
    print("This simulates the bot processing emails.")
    print("Watch the dashboard update in real-time!")
    print("Press Ctrl+C to stop.\n")
    
    pending_completions = []
    
    while True:
        try:
            # Add a new assignment
            staff, was_urgent = add_assignment()
            pending_completions.append((staff, time.time()))
            
            # Random chance to complete an old one
            if pending_completions and random.random() > 0.3:
                old_staff, _ = pending_completions.pop(0)
                time.sleep(1)
                add_completion(old_staff)
            
            # Fixed 10 second interval for demo
            print(f"   (Next in 10s...)\n")
            time.sleep(10)
            
        except KeyboardInterrupt:
            print("\n\n🛑 Simulator stopped.")
            break
