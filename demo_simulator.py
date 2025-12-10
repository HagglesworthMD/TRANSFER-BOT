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
    "brian.shaw@sa.gov.au",
    "jason.quinn2@sa.gov.au", 
    "john.drousas@sa.gov.au",
    "betty.spaghetti@sa.gov.au",
    "chuck.norris@sa.gov.au",
    "diana.wonderwoman@sa.gov.au",
    "tony.baloney@sa.gov.au",
    "frank.beans@sa.gov.au",
    "stella.artois@sa.gov.au",
    "max.power@sa.gov.au"
]

SENDERS = [
    "jones.radiology@hospital.com.au",
    "rah.emergency@sa.gov.au",
    "wch.imaging@sa.gov.au",
    "flinders.imaging@sa.gov.au",
    "mfm.unit@sa.gov.au"
]

REQUESTS = [
    "CT Scan Transfer Request",
    "MRI Transfer Request", 
    "Ultrasound Transfer",
    "X-Ray Transfer Request",
    "Cardiac Imaging Transfer"
]

PATIENTS = ["Smith J", "Brown M", "Wilson S", "Davis T", "Johnson R"]

current_index = 0

def add_assignment():
    global current_index
    staff = STAFF[current_index % len(STAFF)]
    current_index += 1
    
    now = datetime.now()
    sender = random.choice(SENDERS)
    request = random.choice(REQUESTS)
    patient = random.choice(PATIENTS)
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
    
    print(f"✅ NEW REQUEST assigned to {staff.split('@')[0]}")
    return staff

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
            staff = add_assignment()
            pending_completions.append((staff, time.time()))
            
            # Random chance to complete an old one
            if pending_completions and random.random() > 0.3:
                old_staff, _ = pending_completions.pop(0)
                time.sleep(1)
                add_completion(old_staff)
            
            # Wait 3-8 seconds before next
            wait_time = random.randint(3, 8)
            print(f"   (Next in {wait_time}s...)\n")
            time.sleep(wait_time)
            
        except KeyboardInterrupt:
            print("\n\n🛑 Simulator stopped.")
            break
