# ============================================
# DEMO MODE CONFIGURATION
# ============================================
# Set to True for safe demonstration mode
# Set to False for live production mode
DEMO_MODE = True

# When DEMO_MODE is True:
# - Dashboard shows sample data
# - No real-time monitoring
# - Safe to demo without actual email processing
# - Auto-refresh is disabled

# When DEMO_MODE is False:
# - Dashboard connects to live data
# - Real-time updates every 5 seconds
# - Requires distributor.py to be running
