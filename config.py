# ============================================
# DEMO MODE CONFIGURATION
# ============================================
# Set to True for safe demonstration mode
# Set to False for live production mode
DEMO_MODE = True

# Enable auto-refresh during demo (for live simulator demo)
# Set to True to show live updates from demo_simulator.py
DEMO_AUTO_REFRESH = False

# When DEMO_MODE is True:
# - Dashboard shows DEMO MODE indicator (yellow)
# - Safe to demo without actual email processing
# - If DEMO_AUTO_REFRESH is True: Dashboard refreshes every 5s
# - If DEMO_AUTO_REFRESH is False: No auto-refresh (static)

# When DEMO_MODE is False:
# - Dashboard connects to live data
# - Real-time updates every 5 seconds
# - Requires distributor.py to be running
