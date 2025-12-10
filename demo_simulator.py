#!/usr/bin/env python3
"""
DEMO SIMULATOR - Simulates the bot adding new entries
Run this alongside the dashboard to show live data updates!
"""
import csv
import random
import time
from datetime import datetime

STAFF = [
    "staff1@example.com",
    "manager@example.com", 
    "staff2@example.com",
    "staff3@example.com",
    "staff4@example.com",
    "staff5@example.com",
    "staff6@example.com",
    "staff7@example.com",
    "staff8@example.com",
    "staff9@example.com"
]

SENDERS = [
    "jones.radiology@hospital.com.au",
    "rah.emergency@example.com",
    "wch.imaging@example.com",
    "flinders.imaging@example.com",
    "mfm.unit@example.com"
]

REQUESTS = [
    "CT Scan Transfer Request",
    "MRI Transfer Request", 
    "Ultrasound Transfer",
    "X-Ray Transfer Request",
    "Cardiac Imaging Transfer"
]

# Urgent requests with clinical risk keywords (triggers CRITICAL detection)
URGENT_REQUESTS = [
    "STAT CT Brain - Suspected Stroke",
    "URGENT MRI Spine - Cord Compression Query",
    "STAT Cardiac CT - Chest Pain Query",
    "URGENT Fetal MRI - Immediate Review Required",
    "STAT CT Angio - Ruptured AAA Query"
]

PATIENTS = ["Smith J", "Brown M", "Wilson S", "Davis T", "Johnson R"]

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
    else:
        request = random.choice(REQUESTS)
        subject = f"[Assigned: {staff}] {request} - Patient: {patient}"
    
    with open('daily_stats.csv', 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow([
            now.strftime('%Y-%m-%d'),
            now.strftime('%H:%M:%S'),
            subject,
            staff,
            sender
        ])
    
    if is_urgent:
        print(f"🚨 CRITICAL REQUEST assigned to {staff.split('@')[0]}")
    else:
        print(f"✅ NEW REQUEST assigned to {staff.split('@')[0]}")
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
            'COMPLETED',
            staff
        ])
    
    print(f"✓ COMPLETED by {staff.split('@')[0]}")

if __name__ == "__main__":
    print("=" * 50)
    print("🤖 TRANSFER BOT SIMULATOR")
    print("=" * 50)
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
