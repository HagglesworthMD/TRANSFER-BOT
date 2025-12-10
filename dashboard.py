import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import json
import os

# ==================== DEMO MODE CONFIG ====================
try:
    from config import DEMO_MODE, DEMO_AUTO_REFRESH
except ImportError:
    DEMO_MODE = False  # Default to live mode if config doesn't exist
    DEMO_AUTO_REFRESH = True

# ==================== PAGE CONFIG ====================
st.set_page_config(
    page_title="SAMI Transfer Bot - Live Dashboard" if not DEMO_MODE else "SAMI Transfer Bot - DEMO MODE",
    page_icon="🚀" if not DEMO_MODE else "🎬",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Auto-refresh every 5 seconds (in live mode OR demo with auto-refresh enabled)
if not DEMO_MODE or DEMO_AUTO_REFRESH:
    import time
    if 'last_refresh' not in st.session_state:
        st.session_state.last_refresh = time.time()
    
    # Check if 5 seconds have passed
    if time.time() - st.session_state.last_refresh > 5:
        st.session_state.last_refresh = time.time()
        st.rerun()


# ==================== THEME TOGGLE ====================
if 'theme' not in st.session_state:
    st.session_state.theme = 'dark'  # Default to dark mode

# ==================== CUSTOM CSS ====================
# Theme colors
if st.session_state.theme == 'dark':
    bg_gradient = "linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%)"
    text_color = "#ffffff"
    card_bg = "rgba(255, 255, 255, 0.05)"
    border_color = "rgba(255, 255, 255, 0.1)"
    hover_bg = "rgba(255, 255, 255, 0.08)"
    chart_text_color = "white"
    chart_grid_color = "rgba(255,255,255,0.1)"
else:  # light mode
    bg_gradient = "linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%)"
    text_color = "#1a202c"
    card_bg = "rgba(255, 255, 255, 0.9)"
    border_color = "rgba(0, 0, 0, 0.1)"
    hover_bg = "rgba(0, 0, 0, 0.05)"
    chart_text_color = "#1a202c"
    chart_grid_color = "rgba(0,0,0,0.1)"

st.markdown(f"""
<style>
    /* Import Modern Font */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');
    
    /* Global Styles */
    * {{
        font-family: 'Inter', sans-serif;
    }}
    
    /* Main Background */
    .stApp {{
        background: {bg_gradient};
        color: {text_color};
    }}
    
    /* Header Styling */
    h1, h2, h3 {{
        color: {text_color} !important;
        font-weight: 700 !important;
        letter-spacing: -0.5px;
    }}
    
    /* Fix button visibility */
    .stButton > button {{
        background: {'rgba(102, 126, 234, 0.2)' if st.session_state.theme == 'dark' else 'rgba(102, 126, 234, 0.8)'} !important;
        color: {text_color} !important;
        border: 1px solid {'rgba(255, 255, 255, 0.2)' if st.session_state.theme == 'dark' else 'rgba(102, 126, 234, 0.3)'} !important;
        border-radius: 8px !important;
        padding: 0.5rem 1rem !important;
        font-weight: 600 !important;
        transition: all 0.3s ease !important;
    }}
    
    .stButton > button:hover {{
        background: {'rgba(102, 126, 234, 0.4)' if st.session_state.theme == 'dark' else 'rgba(102, 126, 234, 1.0)'} !important;
        border-color: {'rgba(255, 255, 255, 0.4)' if st.session_state.theme == 'dark' else 'rgba(102, 126, 234, 0.8)'} !important;
        transform: translateY(-2px);
    }}
    
    /* Download button fix */
    .stDownloadButton > button {{
        background: {'rgba(16, 185, 129, 0.2)' if st.session_state.theme == 'dark' else 'rgba(16, 185, 129, 0.8)'} !important;
        color: {text_color} !important;
        border: 1px solid {'rgba(16, 185, 129, 0.3)' if st.session_state.theme == 'dark' else 'rgba(16, 185, 129, 0.5)'} !important;
        border-radius: 8px !important;
        padding: 0.5rem 1rem !important;
        font-weight: 600 !important;
    }}
    
    .stDownloadButton > button:hover {{
        background: {'rgba(16, 185, 129, 0.4)' if st.session_state.theme == 'dark' else 'rgba(16, 185, 129, 1.0)'} !important;
    }}
    
    /* Metric Cards with Glassmorphism */
    [data-testid="stMetricValue"] {{
        font-size: 2.5rem !important;
        font-weight: 700 !important;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }}
    
    [data-testid="stMetricLabel"] {{
        font-size: 0.9rem !important;
        color: {'#a0aec0' if st.session_state.theme == 'dark' else '#4a5568'} !important;
        text-transform: uppercase;
        letter-spacing: 1px;
        font-weight: 600 !important;
    }}
    
    /* Glass Cards */
    .glass-card {{
        background: {card_bg};
        backdrop-filter: blur(10px);
        border-radius: 16px;
        border: 1px solid {border_color};
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
    }}
    
    /* Activity Feed */
    .activity-item {{
        background: {card_bg};
        border-left: 3px solid #667eea;
        padding: 0.8rem;
        margin: 0.5rem 0;
        border-radius: 8px;
        transition: all 0.3s ease;
    }}
    
    .activity-item:hover {{
        background: {hover_bg};
        transform: translateX(5px);
    }}
    
    /* Pulse Animation for Live Indicator */
    @keyframes pulse {{
        0%, 100% {{ opacity: 1; }}
        50% {{ opacity: 0.5; }}
    }}
    
    .live-indicator {{
        display: inline-block;
        width: 10px;
        height: 10px;
        background: #10b981;
        border-radius: 50%;
        margin-right: 8px;
        animation: pulse 2s infinite;
    }}
    
    /* DataFrame Styling */
    [data-testid="stDataFrame"] {{
        background: {card_bg};
        border-radius: 12px;
        padding: 1rem;
    }}
    
    /* Expander styling */
    .streamlit-expanderHeader {{
        background: {card_bg} !important;
        color: {text_color} !important;
        border-radius: 8px !important;
    }}
    
    /* Hide Streamlit Branding */
    #MainMenu {{visibility: hidden;}}
    footer {{visibility: hidden;}}
    
    /* Stat Number Glow */
    .stat-glow {{
        text-shadow: 0 0 20px rgba(102, 126, 234, 0.5);
    }}
</style>
""", unsafe_allow_html=True)

# ==================== DATA LOADING ====================
LOG_FILE = "daily_stats.csv"
STATE_FILE = "roster_state.json"
STAFF_FILE = "staff.txt"

@st.cache_data(ttl=5)  # Cache for 5 seconds for real-time feel
def load_data():
    """Load and process all data sources"""
    try:
        # Load CSV with flexible date parsing
        df = pd.read_csv(LOG_FILE)
        
        # Normalize date format - handle mixed formats
        def parse_date(date_str):
            """Parse date from multiple formats"""
            if pd.isna(date_str):
                return None
            
            date_str = str(date_str).strip()
            
            # Try YYYY-MM-DD format first
            try:
                return pd.to_datetime(date_str, format='%Y-%m-%d').strftime('%Y-%m-%d')
            except:
                pass
            
            # Try DD/MM/YYYY format
            try:
                return pd.to_datetime(date_str, format='%d/%m/%Y').strftime('%Y-%m-%d')
            except:
                pass
            
            # Fallback to pandas auto-parse with dayfirst
            try:
                return pd.to_datetime(date_str, dayfirst=True).strftime('%Y-%m-%d')
            except:
                return None
        
        df['Date'] = df['Date'].apply(parse_date)
        
        # Remove rows where date parsing failed
        df = df[df['Date'].notna()].copy()
        
        # Normalize email addresses to lowercase to prevent duplicates
        df['Assigned To'] = df['Assigned To'].str.lower()
        
        # Add datetime column for time-based analysis
        df['DateTime'] = pd.to_datetime(df['Date'] + ' ' + df['Time'], errors='coerce')
        
        # Load roster state
        with open(STATE_FILE, 'r') as f:
            roster_state = json.load(f)
        
        # Load staff list and normalize to lowercase
        with open(STAFF_FILE, 'r') as f:
            staff_list = [line.strip().lower() for line in f if line.strip()]
        
        return df, roster_state, staff_list
    except FileNotFoundError:
        return None, None, None

# ==================== HEADER ====================
col1, col2, col3, col4 = st.columns([3, 1, 0.4, 0.4])
with col1:
    st.markdown("<h1>🚀 SAMI Transfer Bot - Live Operations Center</h1>", unsafe_allow_html=True)
with col2:
    if DEMO_MODE:
        if DEMO_AUTO_REFRESH:
            # Demo with live updates - green pulsing indicator
            st.markdown(f"""
            <div style='text-align: right; padding-top: 1rem;'>
                <span class='live-indicator'></span>
                <span style='color: #10b981; font-weight: 600;'>DEMO LIVE</span>
                <br>
                <span style='color: #a0aec0; font-size: 0.8rem;'>Auto-refresh: ON</span>
            </div>
            """, unsafe_allow_html=True)
        else:
            # Demo without auto-refresh - yellow static indicator
            st.markdown(f"""
            <div style='text-align: right; padding-top: 1rem;'>
                <span style='display: inline-block; width: 10px; height: 10px; background: #fbbf24; border-radius: 50%; margin-right: 8px;'></span>
                <span style='color: #fbbf24; font-weight: 600;'>DEMO MODE</span>
                <br>
                <span style='color: #a0aec0; font-size: 0.8rem;'>Auto-refresh: OFF</span>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div style='text-align: right; padding-top: 1rem;'>
            <span class='live-indicator'></span>
            <span style='color: #10b981; font-weight: 600;'>LIVE</span>
            <br>
            <span style='color: #a0aec0; font-size: 0.8rem;'>{datetime.now().strftime('%d %b %Y, %H:%M:%S')}</span>
        </div>
        """, unsafe_allow_html=True)
with col3:
    st.markdown("<div style='padding-top: 1.5rem;'></div>", unsafe_allow_html=True)
    # Theme toggle button
    theme_icon = "🌙" if st.session_state.theme == 'dark' else "☀️"
    if st.button(theme_icon, help="Toggle Dark/Light Mode", use_container_width=True):
        st.session_state.theme = 'light' if st.session_state.theme == 'dark' else 'dark'
        st.rerun()
with col4:
    st.markdown("<div style='padding-top: 1.5rem;'></div>", unsafe_allow_html=True)
    if st.button("🔄", help="Refresh Now", use_container_width=True):
        st.rerun()

# ==================== LOAD DATA ====================
df, roster_state, staff_list = load_data()

# Handle missing data gracefully - don't stop, show what we have
if df is None:
    # Create empty dataframe with expected columns
    df = pd.DataFrame(columns=['Date', 'Time', 'Subject', 'Assigned To', 'Sender', 'Risk Level'])
    st.info("📭 **No data yet.** Start the bot or simulator to see live metrics.")

if roster_state is None:
    roster_state = {"current_index": 0, "total_processed": 0}

if staff_list is None:
    staff_list = []

# ==================== TODAY'S DATA ====================
today = datetime.now().strftime('%Y-%m-%d')
df_today = df[df['Date'] == today].copy() if len(df) > 0 else df.copy()

# ==================== CLINICAL CONTROL TOWER ====================
st.markdown("---")

# Load SLA Watchdog data
def load_watchdog():
    """Load urgent watchdog data"""
    try:
        watchdog_file = os.path.join(os.path.dirname(__file__), 'urgent_watchdog.json')
        if os.path.exists(watchdog_file):
            with open(watchdog_file, 'r') as f:
                return json.load(f)
    except:
        pass
    return {}

watchdog_data = load_watchdog()
sla_limit_minutes = 20

# Calculate SLA statuses
active_risks = []
breached_risks = []
now = datetime.now()

for msg_id, ticket in watchdog_data.items():
    try:
        ticket_time = datetime.fromisoformat(ticket['timestamp'])
        elapsed = now - ticket_time
        elapsed_minutes = elapsed.total_seconds() / 60
        remaining = sla_limit_minutes - elapsed_minutes
        
        ticket_info = {
            'id': msg_id[:8] + '...',
            'subject': ticket.get('subject', 'Unknown')[:40],
            'assignee': ticket.get('assigned_to', 'Unknown').split('@')[0],
            'risk_type': ticket.get('risk_type', 'Unknown'),
            'elapsed': int(elapsed_minutes),
            'remaining': max(0, int(remaining)),
            'escalations': ticket.get('escalation_count', 0)
        }
        
        if elapsed_minutes > sla_limit_minutes:
            breached_risks.append(ticket_info)
        else:
            active_risks.append(ticket_info)
    except:
        continue

# Determine overall status
if breached_risks:
    tower_status = "BREACH"
    banner_color = "#ef4444"  # Red
    banner_icon = "🚨"
    banner_text = f"SLA BREACH - {len(breached_risks)} ticket(s) exceeded {sla_limit_minutes}min limit!"
elif active_risks:
    tower_status = "ACTIVE"
    banner_color = "#f59e0b"  # Amber
    banner_icon = "⚠️"
    banner_text = f"Active Risks - {len(active_risks)} urgent ticket(s) being monitored"
else:
    tower_status = "NORMAL"
    banner_color = "#10b981"  # Green
    banner_icon = "✅"
    banner_text = "System Normal - No urgent tickets pending"

# Display Clinical Control Tower
col_tower_title, col_tower_info = st.columns([6, 1])
with col_tower_title:
    st.markdown("### 🏥 Clinical Control Tower")
    st.caption("*Real-time SLA monitoring for critical requests*")
with col_tower_info:
    with st.expander("ℹ️ Info"):
        st.caption("Monitors urgent tickets with 20-minute SLA. Red = Breach, Yellow = Active, Green = Normal.")

# Status Banner
st.markdown(f"""
<div style='
    background: linear-gradient(135deg, {banner_color}20 0%, {banner_color}10 100%);
    border-left: 4px solid {banner_color};
    border-radius: 8px;
    padding: 1rem 1.5rem;
    margin-bottom: 1rem;
'>
    <div style='display: flex; align-items: center; gap: 1rem;'>
        <span style='font-size: 2rem;'>{banner_icon}</span>
        <div>
            <div style='font-size: 1.2rem; font-weight: 700; color: {banner_color};'>{tower_status}</div>
            <div style='font-size: 0.9rem; color: {text_color};'>{banner_text}</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# Show urgent tickets table if any exist
if active_risks or breached_risks:
    col_metrics1, col_metrics2, col_metrics3, col_metrics4 = st.columns(4)
    
    with col_metrics1:
        st.metric("Active Risks", len(active_risks), delta=None)
    with col_metrics2:
        st.metric("SLA Breaches", len(breached_risks), delta_color="inverse" if breached_risks else "off")
    with col_metrics3:
        total_escalations = sum(t.get('escalations', 0) for t in breached_risks + active_risks)
        st.metric("Escalations", total_escalations)
    with col_metrics4:
        if 'Risk Level' in df_today.columns:
            critical_today = len(df_today[df_today['Risk Level'].isin(['critical', 'urgent'])])
        else:
            critical_today = 0
        st.metric("Critical Today", critical_today)
    
    # Tickets table
    if breached_risks:
        st.markdown("#### 🚨 SLA Breached Tickets")
        breach_df = pd.DataFrame(breached_risks)
        breach_df = breach_df.rename(columns={
            'assignee': 'Assigned To',
            'subject': 'Subject',
            'risk_type': 'Risk Type',
            'elapsed': 'Elapsed (min)',
            'escalations': 'Escalations'
        })
        
        # Highlight breached rows
        def highlight_breach(row):
            return ['background-color: rgba(239, 68, 68, 0.2)'] * len(row)
        
        st.dataframe(
            breach_df[['Subject', 'Assigned To', 'Risk Type', 'Elapsed (min)', 'Escalations']].style.apply(highlight_breach, axis=1),
            use_container_width=True,
            height=150
        )
    
    if active_risks:
        st.markdown("#### ⏱️ Active Urgent Tickets")
        active_df = pd.DataFrame(active_risks)
        active_df = active_df.rename(columns={
            'assignee': 'Assigned To',
            'subject': 'Subject',
            'risk_type': 'Risk Type',
            'remaining': 'Time Left (min)',
            'elapsed': 'Elapsed (min)'
        })
        
        # Highlight based on remaining time
        def highlight_urgency(row):
            remaining = row.get('Time Left (min)', 20)
            if remaining < 5:
                return ['background-color: rgba(239, 68, 68, 0.2)'] * len(row)
            elif remaining < 10:
                return ['background-color: rgba(245, 158, 11, 0.2)'] * len(row)
            return [''] * len(row)
        
        st.dataframe(
            active_df[['Subject', 'Assigned To', 'Risk Type', 'Time Left (min)']].style.apply(highlight_urgency, axis=1),
            use_container_width=True,
            height=200
        )

# ==================== EXECUTIVE SUMMARY & HEALTH STATUS ====================
st.markdown("---")

# Calculate health metrics
total_today = len(df_today)
active_staff = df_today[df_today['Assigned To'] != 'completed']['Assigned To'].nunique()
completed_today = len(df_today[df_today['Assigned To'] == 'completed'])

# Calculate balance score
if total_today > 0:
    assignment_data = df_today[df_today['Assigned To'] != 'completed']['Assigned To'].value_counts()
    if len(assignment_data) > 0:
        max_load = assignment_data.max()
        min_load = assignment_data.min()
        balance_score = 100 - ((max_load - min_load) / max_load * 100) if max_load > 0 else 100
    else:
        balance_score = 100
else:
    balance_score = 100

# Determine health status
if balance_score >= 80 and total_today >= 0:
    health_status = "🟢 Healthy"
    health_color = "#10b981"
    status_emoji = "✅"
elif balance_score >= 60:
    health_status = "🟡 Minor Issues"
    health_color = "#fbbf24"
    status_emoji = "⚠️"
else:
    health_status = "🔴 Needs Attention"
    health_color = "#ef4444"
    status_emoji = "❌"

# Get week-over-week comparison
yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
last_week_today = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')
df_yesterday = df[df['Date'] == yesterday]
df_last_week = df[df['Date'] == last_week_today]

wow_requests = total_today - len(df_last_week)
wow_trend = "↑" if wow_requests > 0 else "↓" if wow_requests < 0 else "→"

# Get top sender
top_sender = "N/A"
if 'Sender' in df_today.columns and len(df_today) > 0:
    sender_data = df_today[df_today['Sender'].notna() & (df_today['Sender'] != 'unknown')]['Sender'].value_counts()
    if len(sender_data) > 0:
        top_sender = sender_data.index[0].split('@')[0]
        top_sender_count = sender_data.iloc[0]
        top_sender = f"{top_sender} ({top_sender_count} requests)"

# Generate insight
if total_today > len(df_last_week) * 1.5:
    insight = f"📈 High volume alert: +{((total_today/len(df_last_week) - 1)*100):.0f}% vs last week" if len(df_last_week) > 0 else "📈 Activity increasing"
elif total_today < len(df_last_week) * 0.5 and len(df_last_week) > 0:
    insight = "📉 Unusually quiet - below normal volume"
elif balance_score < 70:
    insight = "⚖️ Workload imbalance detected - check distribution"
else:
    insight = "✨ All systems operating normally"

# Executive Summary Box
st.markdown(f"""
<div style='background: linear-gradient(135deg, {health_color}22 0%, {health_color}11 100%); 
            border-left: 4px solid {health_color}; 
            padding: 1.5rem; 
            border-radius: 8px; 
            margin-bottom: 1rem;'>
    <h2 style='margin: 0 0 1rem 0; color: #fff;'>📊 EXECUTIVE SUMMARY</h2>
    <div style='display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 1rem;'>
        <div>
            <p style='margin: 0; color: #a0aec0; font-size: 0.9rem;'>System Status</p>
            <p style='margin: 0.25rem 0 0 0; font-size: 1.3rem; font-weight: 700; color: {health_color};'>{health_status}</p>
        </div>
        <div>
            <p style='margin: 0; color: #a0aec0; font-size: 0.9rem;'>Today's Activity</p>
            <p style='margin: 0.25rem 0 0 0; font-size: 1.3rem; font-weight: 700; color: #fff;'>{total_today} requests {wow_trend}</p>
        </div>
        <div>
            <p style='margin: 0; color: #a0aec0; font-size: 0.9rem;'>Team Balance</p>
            <p style='margin: 0.25rem 0 0 0; font-size: 1.3rem; font-weight: 700; color: #fff;'>{balance_score:.0f}% {status_emoji}</p>
        </div>
        <div>
            <p style='margin: 0; color: #a0aec0; font-size: 0.9rem;'>Top Source</p>
            <p style='margin: 0.25rem 0 0 0; font-size: 1.3rem; font-weight: 700; color: #fff;'>{top_sender}</p>
        </div>
    </div>
    <div style='margin-top: 1rem; padding: 0.75rem; background: rgba(0,0,0,0.2); border-radius: 6px;'>
        <p style='margin: 0; color: #fff; font-size: 0.95rem;'><strong>💡 Insight:</strong> {insight}</p>
    </div>
</div>
""", unsafe_allow_html=True)

# DEBUG: Show what dates we have in the data
with st.expander("🔍 Debug Info (Click to expand)", expanded=False):
    st.write(f"**Current Date:** {today}")
    st.write(f"**Total records in CSV:** {len(df)}")
    st.write(f"**Records for today:** {len(df_today)}")
    st.write("**Unique dates in data:**")
    st.write(df['Date'].value_counts().sort_index(ascending=False))

# ==================== EXPORT FUNCTIONALITY ====================
col_export1, col_export2, col_export3 = st.columns([2, 1, 2])
with col_export2:
    csv_data = df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Export Full Data (CSV)",
        data=csv_data,
        file_name=f"helpdesk_transfer_bot_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
        mime="text/csv",
        use_container_width=True,
        help="Download complete dataset for external analysis"
    )

# ==================== SHAME JOHN BUTTON (Easter Egg) ====================
# Show button if workload is imbalanced and John exists in staff
if balance_score < 70 and 'staff2@example.com' in staff_list:
    john_assignments = len(df_today[df_today['Assigned To'] == 'staff2@example.com'])
    avg_assignments = total_today / len(staff_list) if len(staff_list) > 0 else 0
    
    if john_assignments < avg_assignments * 0.5:  # John is doing less than half the average
        st.markdown("---")
        col_shame1, col_shame2, col_shame3 = st.columns([1, 1, 1])
        with col_shame2:
            import urllib.parse
            
            chuck_count = len(df_today[df_today['Assigned To'] == 'staff4@example.com'])
            email_subject = "RE: Your Outstanding Workload Performance"
            email_body = f"""Hi John,

I hope this email finds you well and not napping at your desk!

I couldn't help but notice that while the rest of the team is crushing it with an average of {avg_assignments:.0f} requests today, you've managed to handle a whopping {john_assignments} requests.

That's {(john_assignments/avg_assignments*100):.0f}% of the team average! Impressive dedication to work-life balance!

Perhaps we could discuss:
  • Your secret productivity techniques (napping strategies?)
  • Whether you've discovered time travel (backwards only?)
  • If your keyboard is broken (just the work-related keys?)

Looking forward to your response... whenever you get around to it!

Best regards,
The Dashboard That Never Sleeps

P.S. Chuck Norris has done {chuck_count} requests today. Just saying.
"""
            # Properly encode the mailto URL
            mailto_link = f"mailto:staff2@example.com?subject={urllib.parse.quote(email_subject)}&body={urllib.parse.quote(email_body)}"
            
            if st.button("📧 Email John", use_container_width=True, type="primary"):
                st.markdown(f'<meta http-equiv="refresh" content="0;url={mailto_link}">', unsafe_allow_html=True)
                st.success("📧 Opening email client...")

st.markdown("---")

# ==================== KEY METRICS ROW ====================
st.markdown("### 📊 Real-Time Metrics")
col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    total_today = len(df_today)
    st.metric("📬 Requests Today", total_today, delta="+0" if total_today == 0 else f"+{len(df_today.tail(1))}")

with col2:
    active_staff = df_today[df_today['Assigned To'] != 'completed']['Assigned To'].nunique()
    st.metric("👥 Staff Active", active_staff, delta=f"{len(staff_list)} total")

with col3:
    completed = len(df_today[df_today['Assigned To'] == 'completed'])
    st.metric("✅ Completed", completed, delta=f"{(completed/total_today*100):.0f}%" if total_today > 0 else "0%")

with col4:
    avg_per_staff = total_today / len(staff_list) if len(staff_list) > 0 else 0
    st.metric("⚖️ Avg per Staff", f"{avg_per_staff:.1f}", delta="Balanced")

with col5:
    if not df_today.empty:
        last_action = df_today['DateTime'].max()
        mins_ago = int((datetime.now() - last_action).total_seconds() / 60)
        st.metric("🕐 Last Activity", f"{mins_ago}m ago" if mins_ago > 0 else "Just now")
    else:
        st.metric("🕐 Last Activity", "N/A")

st.markdown("---")

# ==================== MAIN CONTENT ====================
if not df_today.empty:
    # Row 1: Charts
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("### 📈 Workload Distribution")
        
        # Get assignment counts (excluding staff replies)
        assignment_data = df_today[df_today['Assigned To'] != 'completed']['Assigned To'].value_counts().reset_index()
        assignment_data.columns = ['Staff', 'Assignments']
        
        # Unique colors for each staff member (vibrant and distinct)
        staff_colors = {
            'staff1@example.com': '#667eea',        # Purple
            'manager@example.com': '#f093fb',      # Pink
            'staff2@example.com': '#ff6b6b',      # Red (slacker alert!)
            'staff3@example.com': '#feca57',   # Yellow
            'staff4@example.com': '#48dbfb',      # Cyan
            'staff5@example.com': '#ff9ff3', # Hot Pink
            'staff6@example.com': '#54a0ff',      # Blue
            'staff7@example.com': '#00d2d3',       # Teal
            'staff8@example.com': '#5f27cd',     # Deep Purple
            'staff9@example.com': '#ee5a6f'          # Coral
        }
        
        # Map colors to staff in the data
        colors = [staff_colors.get(email, '#888888') for email in assignment_data['Staff']]
        
        # Create horizontal bar chart with unique colors
        fig = go.Figure()
        fig.add_trace(go.Bar(
            y=assignment_data['Staff'],
            x=assignment_data['Assignments'],
            orientation='h',
            marker=dict(
                color=colors,
                line=dict(color='rgba(255, 255, 255, 0.2)', width=1)
            ),
            text=assignment_data['Assignments'],
            textposition='auto',
        ))
        
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color=chart_text_color),
            xaxis=dict(
                showgrid=True, 
                gridcolor=chart_grid_color,
                tickfont=dict(color=chart_text_color)
            ),
            yaxis=dict(
                showgrid=False,
                tickfont=dict(color=chart_text_color)
            ),
            margin=dict(l=0, r=0, t=0, b=0),
            height=300
        )
        
        # Debug theme (temporary)
        # st.write(f"Debug: Theme={st.session_state.theme}, TextColor={chart_text_color}")
        
        st.plotly_chart(fig, use_container_width=True, key="workload_distribution")
    
    with col2:
        st.markdown("### 🎯 System Status")
        
        # Calculate next in rotation
        next_idx = roster_state.get('current_index', 0) % len(staff_list) if staff_list else 0
        next_staff = staff_list[next_idx] if staff_list else "N/A"
        total_processed = roster_state.get('total_processed', len(df[df['Assigned To'] != 'completed']))
        
        st.markdown(f"""
        <div class='glass-card'>
            <h4 style='color: #667eea; margin-bottom: 1rem;'>🔄 Round-Robin State</h4>
            <p style='font-size: 0.9rem; color: #a0aec0;'>Next Assignment:</p>
            <p style='font-size: 1.2rem; font-weight: 600; color: #10b981;'>{next_staff.split('@')[0]}</p>
            <hr style='border-color: rgba(255,255,255,0.1);'>
            <p style='font-size: 0.9rem; color: #a0aec0;'>Total Processed:</p>
            <p style='font-size: 1.5rem; font-weight: 700; color: #667eea;'>{total_processed}</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Fairness Check
        if not assignment_data.empty:
            max_load = assignment_data['Assignments'].max()
            min_load = assignment_data['Assignments'].min()
            balance_score = 100 - ((max_load - min_load) / max_load * 100) if max_load > 0 else 100
            
            if balance_score > 80:
                badge_class = "badge-success"
                status_icon = "✅"
            elif balance_score > 60:
                badge_class = "badge-warning"
                status_icon = "⚠️"
            else:
                badge_class = "badge-warning"
                status_icon = "⚠️"
            
            st.markdown(f"""
            <div class='glass-card' style='margin-top: 1rem;'>
                <h4 style='color: #667eea;'>⚖️ Balance Score</h4>
                <p style='font-size: 2rem; font-weight: 700;'>{status_icon} {balance_score:.0f}%</p>
                <span class='status-badge {badge_class}'>
                    {['Unbalanced', 'Fair', 'Excellent'][int(balance_score/40)]}
                </span>
            </div>
            """, unsafe_allow_html=True)
    
    # Row 2: Activity Timeline
    # Hourly Activity section with info
    col_hourly_title, col_hourly_info = st.columns([6, 1])
    with col_hourly_title:
        st.markdown("### 🕒 Hourly Activity Trend")
    with col_hourly_info:
        with st.expander("ℹ️ Info"):
            st.caption("Shows when requests arrive throughout the day. Helps identify busy periods for staffing optimization.")
    
    # Group by hour
    df_today['Hour'] = df_today['DateTime'].dt.hour
    hourly_data = df_today.groupby('Hour').size().reset_index(name='Count')
    
    # Format hours as time (HH:00)
    hourly_data['Time'] = hourly_data['Hour'].apply(lambda x: f"{x:02d}:00")
    
    # Create area chart
    fig_timeline = go.Figure()
    fig_timeline.add_trace(go.Scatter(
        x=hourly_data['Time'],
        y=hourly_data['Count'],
        mode='lines+markers',
        fill='tozeroy',
        line=dict(color='#667eea', width=3),
        marker=dict(size=8, color='#764ba2'),
        fillcolor='rgba(102, 126, 234, 0.3)',
        hovertemplate='<b>%{x}</b><br>Requests: %{y}<extra></extra>'
    ))
    
    fig_timeline.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color=chart_text_color),
        xaxis=dict(
            showgrid=True,
            gridcolor=chart_grid_color,
            title=dict(text="Time of Day", font=dict(color=chart_text_color)),
            tickfont=dict(color=chart_text_color)
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor=chart_grid_color,
            title=dict(text="Requests", font=dict(color=chart_text_color)),
            tickfont=dict(color=chart_text_color)
        ),
        margin=dict(l=0, r=0, t=0, b=0),
        height=250
    )
    
    st.plotly_chart(fig_timeline, use_container_width=True, key="hourly_timeline")
    
    # ==================== WEEK-OVER-WEEK COMPARISON ====================
    col_wow_title, col_wow_info = st.columns([6, 1])
    with col_wow_title:
        st.markdown("### 📊 Week-over-Week Performance")
    with col_wow_info:
        with st.expander("ℹ️ Info"):
            st.caption("Compares this week's metrics vs last week. Shows if request volume and completion rates are improving or declining.")
    
    # Calculate this week vs last week
    this_week_start = (datetime.now() - timedelta(days=datetime.now().weekday())).strftime('%Y-%m-%d')
    last_week_start = (datetime.now() - timedelta(days=datetime.now().weekday() + 7)).strftime('%Y-%m-%d')
    last_week_end = (datetime.now() - timedelta(days=datetime.now().weekday() + 1)).strftime('%Y-%m-%d')
    
    # Get last 7 days for proper week comparison
    last_7_days = [(datetime.now() - timedelta(days=i)).strftime('%Y-%m-%d') for i in range(6, -1, -1)]
    prev_7_days = [(datetime.now() - timedelta(days=i+7)).strftime('%Y-%m-%d') for i in range(6, -1, -1)]
    
    this_week_df = df[df['Date'].isin(last_7_days)]
    last_week_df = df[df['Date'].isin(prev_7_days)]
    
    this_week_count = len(this_week_df)
    last_week_count = len(last_week_df)
    
    # Calculate changes
    volume_change = ((this_week_count - last_week_count) / last_week_count * 100) if last_week_count > 0 else 0
    
    col_wow1, col_wow2, col_wow3, col_wow4 = st.columns(4)
    
    with col_wow1:
        st.metric(
            "This Week Requests",
            this_week_count,
            delta=f"{volume_change:+.0f}% vs last week",
            delta_color="normal" if volume_change >= 0 else "inverse"
        )
    
    # Calculate completion metrics
    this_week_completed = len(this_week_df[this_week_df['Assigned To'] == 'completed'])
    this_week_requests = len(this_week_df[this_week_df['Assigned To'] != 'completed'])
    last_week_completed = len(last_week_df[last_week_df['Assigned To'] == 'completed'])
    last_week_requests = len(last_week_df[last_week_df['Assigned To'] != 'completed'])
    
    completion_rate_this = (this_week_completed / this_week_requests * 100) if this_week_requests > 0 else 0
    completion_rate_last = (last_week_completed / last_week_requests * 100) if last_week_requests > 0 else 0
    completion_change = completion_rate_this - completion_rate_last
    
    with col_wow2:
        st.metric(
            "Completion Rate",
            f"{completion_rate_this:.0f}%",
            delta=f"{completion_change:+.0f}% vs last week",
            delta_color="normal" if completion_change >= 0 else "inverse"
        )
    
    with col_wow3:
        avg_per_day_this = this_week_count / 7
        avg_per_day_last = last_week_count / 7 if last_week_count > 0 else 0
        st.metric(
            "Avg per Day",
            f"{avg_per_day_this:.1f}",
            delta=f"{avg_per_day_this - avg_per_day_last:+.1f} vs last week"
        )
    
    with col_wow4:
        # Determine trend
        if volume_change > 15:
            trend = "📈 Increasing"
        elif volume_change < -15:
            trend = "📉 Decreasing"
        else:
            trend = "➡️ Stable"
        st.metric("Trend", trend)
    
    # ==================== PEAK HOURS HEATMAP ====================
    col_heat_title, col_heat_info = st.columns([6, 1])
    with col_heat_title:
        st.markdown("### 🔥 Peak Hours Heatmap")
        st.caption("*Identify busiest times to optimize staffing*")
    with col_heat_info:
        with st.expander("ℹ️ Info"):
            st.caption("Visual heatmap showing request volume by day and time. Darker = busier. Use this to plan staffing levels.")
    
    # Prepare data for heatmap (last 7 days)
    df_heatmap = df[df['Date'].isin(last_7_days)].copy()
    
    if len(df_heatmap) > 0:
        df_heatmap['Hour'] = df_heatmap['DateTime'].dt.hour
        df_heatmap['DayOfWeek'] = df_heatmap['DateTime'].dt.day_name()
        
        # Create pivot table for heatmap
        heatmap_data = df_heatmap.groupby(['DayOfWeek', 'Hour']).size().reset_index(name='Count')
        
        # Pivot for heatmap
        heatmap_pivot = heatmap_data.pivot(index='Hour', columns='DayOfWeek', values='Count').fillna(0)
        
        # Reorder columns to weekday order
        day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        heatmap_pivot = heatmap_pivot.reindex(columns=[d for d in day_order if d in heatmap_pivot.columns])
        
        # Format y-axis as time (HH:00)
        time_labels = [f"{int(h):02d}:00" for h in heatmap_pivot.index]
        
        # Create heatmap
        fig_heatmap = go.Figure(data=go.Heatmap(
            z=heatmap_pivot.values,
            x=heatmap_pivot.columns,
            y=time_labels,
            colorscale='Viridis',
            text=heatmap_pivot.values,
            texttemplate='%{text}',
            textfont={"size": 10},
            colorbar=dict(title="Requests"),
            hovertemplate='<b>%{x}</b><br>Time: %{y}<br>Requests: %{text}<extra></extra>'
        ))
        
        fig_heatmap.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color=chart_text_color),
            xaxis=dict(
                title=dict(text="Day of Week", font=dict(color=chart_text_color)),
                side="bottom",
                tickfont=dict(color=chart_text_color)
            ),
            yaxis=dict(
                title=dict(text="Time of Day", font=dict(color=chart_text_color)),
                tickfont=dict(color=chart_text_color)
            ),
            margin=dict(l=0, r=0, t=0, b=0),
            height=400
        )
        
        st.plotly_chart(fig_heatmap, use_container_width=True, key="activity_heatmap")
        
        # Find peak hour
        if len(heatmap_data) > 0:
            peak_row = heatmap_data.loc[heatmap_data['Count'].idxmax()]
            peak_time = f"{int(peak_row['Hour']):02d}:00"
            st.info(f"🔥 **Peak Time:** {peak_row['DayOfWeek']} at {peak_time} ({int(peak_row['Count'])} requests)")
    else:
        st.info("Not enough data yet for heatmap analysis. Need at least 1 week of activity.")
    
    # Row 3: Recent Activity Feed
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("### 📜 Live Activity Feed")
        
        # Show last 10 activities
        recent = df_today.sort_values('DateTime', ascending=False).head(10)
        
        for _, row in recent.iterrows():
            time_str = row['DateTime'].strftime('%H:%M:%S')
            subject_short = row['Subject'][:60] + "..." if len(row['Subject']) > 60 else row['Subject']
            assigned = row['Assigned To']
            
            if assigned == 'completed':
                icon = "✅"
                color = "#10b981"
                label_text = "Completed"
            else:
                icon = "📨"
                color = "#3b82f6"
                label_text = assigned.split('@')[0]
            
            # Use columns for better layout (avoids HTML escaping issues)
            with st.container():
                col_feed1, col_feed2 = st.columns([4, 1])
                with col_feed1:
                    st.markdown(f"{icon} **:blue[{label_text}]**")
                    st.caption(subject_short)
                with col_feed2:
                    st.caption(time_str)
    
    with col2:
        st.markdown("### 🏆 Staff Leaderboard")
        
        leaderboard_data = df_today[df_today['Assigned To'] != 'completed']['Assigned To'].value_counts().head(5)
        
        medals = ["🥇", "🥈", "🥉", "4️⃣", "5️⃣"]
        for idx, (staff, count) in enumerate(leaderboard_data.items()):
            staff_name = staff.split('@')[0]
            
            with st.container():
                col_lb1, col_lb2 = st.columns([3, 1])
                with col_lb1:
                    st.markdown(f"{medals[idx]} **{staff_name}**")
                with col_lb2:
                    st.markdown(f"**:violet[{count}]**")
    
    # Row 4: Full Audit Log
    st.markdown("### 📋 Complete Audit Log")
    
    # Format dataframe for display
    display_df = df_today[['Time', 'Subject', 'Assigned To']].sort_values('Time', ascending=False).copy()
    display_df['Assigned To'] = display_df['Assigned To'].apply(lambda x: x.split('@')[0] if '@' in x else x)
    
    st.dataframe(
        display_df,
        use_container_width=True,
        height=300
    )
    
    # ==================== STAFF KPI SECTION ====================
    st.markdown("---")
    st.markdown("### 👥 Individual Staff Performance Dashboard")
    
    # Get all staff members (excluding COMPLETED)
    all_staff = set(staff_list)
    assigned_staff = set(df_today[df_today['Assigned To'] != 'completed']['Assigned To'].unique())
    all_staff.update(assigned_staff)
    
    # Explicitly remove COMPLETED if it somehow got included
    all_staff.discard('completed')
    all_staff.discard('staff-reply')
    
    # Calculate KPIs for each staff member
    for staff_email in sorted(all_staff):
        staff_name = staff_email.split('@')[0].title().replace('.', ' ')
        
        # Filter data for this staff member
        staff_data_today = df_today[df_today['Assigned To'] == staff_email]
        staff_data_all = df[df['Assigned To'] == staff_email]
        
        # Calculate metrics
        total_today = len(staff_data_today)
        total_all_time = len(staff_data_all)
        
        # Calculate completion-related metrics (approximation based on COMPLETED entries)
        # Note: Completions are tracked when staff replies, so we check for patterns
        completed_today = 0  # Would need COMPLETED tracking per person for accuracy
        
        # Calculate average assignment time (time between assignments)
        if len(staff_data_today) > 1:
            times = pd.to_datetime(staff_data_today['DateTime']).sort_values()
            time_diffs = times.diff().dropna()
            avg_gap = time_diffs.mean()
            avg_gap_mins = avg_gap.total_seconds() / 60 if not pd.isna(avg_gap) else 0
        else:
            avg_gap_mins = 0
        
        # 7-day trend
        last_7_days = [(datetime.now() - timedelta(days=i)).strftime('%Y-%m-%d') for i in range(6, -1, -1)]
        staff_7day = staff_data_all[staff_data_all['Date'].isin(last_7_days)]
        weekly_total = len(staff_7day)
        daily_avg = weekly_total / 7
        
        # Create expandable section for each staff member (collapsed by default)
        with st.expander(f"📊 **{staff_name}** - {total_today} requests today ({total_all_time} all-time)", expanded=False):
            
            # KPI Row
            kpi1, kpi2, kpi3, kpi4 = st.columns(4)
            
            with kpi1:
                st.metric(
                    "Today's Assignments", 
                    total_today,
                    delta=f"+{total_today - int(daily_avg)}" if total_today > daily_avg else f"{total_today - int(daily_avg)}" if total_today < daily_avg else "On pace"
                )
            
            with kpi2:
                st.metric(
                    "7-Day Total",
                    weekly_total,
                    delta=f"{daily_avg:.1f}/day avg"
                )
            
            with kpi3:
                st.metric(
                    "All-Time Total",
                    total_all_time,
                    delta="" if total_all_time == 0 else "Career"
                )
            
            with kpi4:
                # Calculate workload percentage (vs average)
                avg_per_staff_today = len(df_today[df_today['Assigned To'] != 'completed']) / len(staff_list) if len(staff_list) > 0 else 0
                workload_pct = (total_today / avg_per_staff_today * 100) if avg_per_staff_today > 0 else 100
                
                if workload_pct > 110:
                    delta_color = "inverse"
                    status = "Above avg"
                elif workload_pct < 90:
                    delta_color = "normal"
                    status = "Below avg"
                else:
                    delta_color = "off"
                    status = "Balanced"
                
                st.metric(
                    "Workload vs Avg",
                    f"{workload_pct:.0f}%",
                    delta=status
                )
            
            # Only show charts if there's data
            if total_today > 0 or weekly_total > 0:
                chart_col1, chart_col2 = st.columns(2)
                
                with chart_col1:
                    # Hourly distribution for this staff member
                    st.markdown("**📅 Today's Hourly Distribution**")
                    if total_today > 0:
                        staff_hourly = staff_data_today.copy()
                        staff_hourly['Hour'] = staff_hourly['DateTime'].dt.hour
                        hourly_counts = staff_hourly.groupby('Hour').size().reset_index(name='Count')
                        
                        fig_staff_hourly = go.Figure()
                        fig_staff_hourly.add_trace(go.Bar(
                            x=hourly_counts['Hour'],
                            y=hourly_counts['Count'],
                            marker=dict(
                                color=hourly_counts['Count'],
                                colorscale='Purples',
                                line=dict(color='rgba(255, 255, 255, 0.2)', width=1)
                            ),
                            text=hourly_counts['Count'],
                            textposition='auto',
                        ))
                        
                        fig_staff_hourly.update_layout(
                            plot_bgcolor='rgba(0,0,0,0)',
                            paper_bgcolor='rgba(0,0,0,0)',
                            font=dict(color=chart_text_color, size=10),
                            xaxis=dict(showgrid=False, title=dict(text="Hour", font=dict(color=chart_text_color))),
                            yaxis=dict(showgrid=True, gridcolor=chart_grid_color, title=dict(text="Requests", font=dict(color=chart_text_color))),
                            margin=dict(l=0, r=0, t=0, b=0),
                            height=200
                        )
                        
                        st.plotly_chart(fig_staff_hourly, use_container_width=True, key=f"staff_hourly_{staff_email}")
                    else:
                        st.info("No activity today")
                
                with chart_col2:
                    # 7-day trend for this staff member
                    st.markdown("**📈 7-Day Trend**")
                    if weekly_total > 0:
                        daily_counts = staff_7day.groupby('Date').size().reset_index(name='Count')
                        # Fill in missing days with 0
                        daily_counts_full = pd.DataFrame({'Date': last_7_days})
                        daily_counts_full = daily_counts_full.merge(daily_counts, on='Date', how='left').fillna(0)
                        
                        fig_staff_weekly = go.Figure()
                        fig_staff_weekly.add_trace(go.Scatter(
                            x=daily_counts_full['Date'],
                            y=daily_counts_full['Count'],
                            mode='lines+markers',
                            fill='tozeroy',
                            line=dict(color='#667eea', width=2),
                            marker=dict(size=6, color='#764ba2'),
                            fillcolor='rgba(102, 126, 234, 0.2)'
                        ))
                        
                        fig_staff_weekly.update_layout(
                            plot_bgcolor='rgba(0,0,0,0)',
                            paper_bgcolor='rgba(0,0,0,0)',
                            font=dict(color=chart_text_color, size=10),
                            xaxis=dict(showgrid=False, title=dict(text="Date", font=dict(color=chart_text_color))),
                            yaxis=dict(showgrid=True, gridcolor=chart_grid_color, title=dict(text="Requests", font=dict(color=chart_text_color))),
                            margin=dict(l=0, r=0, t=0, b=0),
                            height=200
                        )
                        
                        st.plotly_chart(fig_staff_weekly, use_container_width=True, key=f"staff_weekly_{staff_email}")
                    else:
                        st.info("No activity this week")
                
                # Recent assignments table
                if total_today > 0:
                    st.markdown("**📋 Recent Assignments**")
                    recent_assignments = staff_data_today[['Time', 'Subject']].sort_values('Time', ascending=False).head(5)
                    recent_assignments['Subject'] = recent_assignments['Subject'].apply(
                        lambda x: x[:80] + "..." if len(x) > 80 else x
                    )
                    st.dataframe(recent_assignments, use_container_width=True, height=150)
            else:
                st.info(f"💤 **{staff_name}** hasn't received any assignments yet today.")

else:
    st.info("📭 **No requests processed today yet.** System is monitoring and ready!")

# ==================== HISTORICAL TRENDS (7 DAYS) ====================
st.markdown("---")
st.markdown("### 📅 7-Day Trend Analysis")

# Get last 7 days
last_7_days = [(datetime.now() - timedelta(days=i)).strftime('%Y-%m-%d') for i in range(6, -1, -1)]
weekly_data = df[df['Date'].isin(last_7_days)].groupby('Date').size().reset_index(name='Count')

fig_weekly = go.Figure()
fig_weekly.add_trace(go.Bar(
    x=weekly_data['Date'],
    y=weekly_data['Count'],
    marker=dict(
        color=weekly_data['Count'],
        colorscale='Plasma',
        line=dict(color='rgba(255, 255, 255, 0.2)', width=1)
    ),
    text=weekly_data['Count'],
    textposition='auto',
))

fig_weekly.update_layout(
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='rgba(0,0,0,0)',
    font=dict(color=chart_text_color),
    xaxis=dict(
        showgrid=False, 
        title=dict(text="Date", font=dict(color=chart_text_color)),
        tickfont=dict(color=chart_text_color)
    ),
    yaxis=dict(
        showgrid=True, 
        gridcolor=chart_grid_color, 
        title=dict(text="Requests", font=dict(color=chart_text_color)),
        tickfont=dict(color=chart_text_color)
    ),
    margin=dict(l=0, r=0, t=0, b=0),
    height=250
)

st.plotly_chart(fig_weekly, use_container_width=True, key="weekly_trend")

# ==================== EXTERNAL REQUEST SOURCES ====================
st.markdown("---")
col_ext_title, col_ext_info = st.columns([6, 1])
with col_ext_title:
    st.markdown("### 📧 External Request Sources")
    st.markdown("*Who is sending us requests?*")
with col_ext_info:
    with st.expander("ℹ️ Info"):
        st.caption("Shows which external sources (hospitals, clinics, departments) send the most requests. Helps identify key partners and service demand.")

# Check if Sender column exists
if 'Sender' in df.columns:
    # Clean sender data (exclude staff replies from sender analysis)
    df_with_sender = df[(df['Sender'].notna()) & (df['Sender'] != 'unknown') & (df['Assigned To'] != 'completed')].copy()
    df_today_sender = df_today[(df_today['Sender'].notna()) & (df_today['Sender'] != 'unknown') & (df_today['Assigned To'] != 'completed')].copy()
    
    if len(df_with_sender) > 0:
        col_src1, col_src2 = st.columns(2)
        
        with col_src1:
            st.markdown("#### 📊 Top 10 Request Sources (All Time)")
            
            # Get top senders
            top_senders = df_with_sender['Sender'].value_counts().head(10)
            
            fig_senders = go.Figure()
            fig_senders.add_trace(go.Bar(
                y=top_senders.index,
                x=top_senders.values,
                orientation='h',
                marker=dict(
                    color=top_senders.values,
                    colorscale='Teal',
                    line=dict(color='rgba(255, 255, 255, 0.2)', width=1)
                ),
                text=top_senders.values,
                textposition='auto',
            ))
            
            fig_senders.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color=chart_text_color, size=10),
                xaxis=dict(
                    showgrid=True, 
                    gridcolor=chart_grid_color, 
                    title=dict(text="Total Requests", font=dict(color=chart_text_color)),
                    tickfont=dict(color=chart_text_color)
                ),
                yaxis=dict(
                    showgrid=False,
                    tickfont=dict(color=chart_text_color)
                ),
                margin=dict(l=0, r=0, t=0, b=0),
                height=350
            )
            
            st.plotly_chart(fig_senders, use_container_width=True, key="top_senders")
        
        with col_src2:
            st.markdown("#### � Sender Details")
            
            # Create sender summary
            sender_summary = df_with_sender.groupby('Sender').agg({
                'Date': 'count',
                'DateTime': ['min', 'max']
            }).reset_index()
            
            sender_summary.columns = ['Sender', 'Total Requests', 'First Request', 'Last Request']
            sender_summary = sender_summary.sort_values('Total Requests', ascending=False).head(10)
            
            # Format datetime columns
            sender_summary['First Request'] = pd.to_datetime(sender_summary['First Request']).dt.strftime('%Y-%m-%d')
            sender_summary['Last Request'] = pd.to_datetime(sender_summary['Last Request']).dt.strftime('%Y-%m-%d')
            
            st.dataframe(
                sender_summary,
                use_container_width=True,
                height=350
            )
    else:
        st.info("📭 No external sender data available yet. New requests will be tracked with sender information.")

# ==================== RAW DATA VIEWER ====================
st.markdown("---")
col_data_title, col_data_info = st.columns([6, 1])
with col_data_title:
    st.markdown("### 📂 Raw Data Viewer")
    st.markdown("*Live view of underlying CSV data*")
with col_data_info:
    with st.expander("ℹ️ Info"):
        st.caption("Shows the actual data being processed. All dashboard metrics are calculated from this data in real-time.")

with st.expander("🔍 **Click to View Raw Data**", expanded=False):
    # Data stats
    col_stat1, col_stat2, col_stat3, col_stat4 = st.columns(4)
    with col_stat1:
        st.metric("Total Records", len(df))
    with col_stat2:
        st.metric("Assignments", len(df[df['Assigned To'] != 'completed']))
    with col_stat3:
        st.metric("Completions", len(df[df['Assigned To'] == 'completed']))
    with col_stat4:
        st.metric("Unique Staff", df[df['Assigned To'] != 'completed']['Assigned To'].nunique())
    
    st.markdown("---")
    
    # Filtering options
    col_filter1, col_filter2, col_filter3 = st.columns(3)
    
    with col_filter1:
        show_type = st.selectbox(
            "Filter by Type",
            ["All", "Assignments Only", "Completions Only"],
            key="data_type_filter"
        )
    
    with col_filter2:
        date_options = ["All Dates"] + sorted(df['Date'].unique().tolist(), reverse=True)
        selected_date = st.selectbox(
            "Filter by Date",
            date_options,
            key="data_date_filter"
        )
    
    with col_filter3:
        staff_options = ["All Staff"] + sorted([s for s in df['Assigned To'].unique() if s != 'completed'])
        selected_staff = st.selectbox(
            "Filter by Staff",
            staff_options,
            key="data_staff_filter"
        )
    
    # Apply filters
    filtered_df = df.copy()
    
    if show_type == "Assignments Only":
        filtered_df = filtered_df[filtered_df['Assigned To'] != 'completed']
    elif show_type == "Completions Only":
        filtered_df = filtered_df[filtered_df['Assigned To'] == 'completed']
    
    if selected_date != "All Dates":
        filtered_df = filtered_df[filtered_df['Date'] == selected_date]
    
    if selected_staff != "All Staff":
        filtered_df = filtered_df[filtered_df['Assigned To'] == selected_staff]
    
    # Display count after filtering
    st.caption(f"Showing {len(filtered_df)} of {len(df)} records")
    
    # Display the data
    display_df = filtered_df[['Date', 'Time', 'Assigned To', 'Sender', 'Subject']].copy()
    display_df = display_df.sort_values(['Date', 'Time'], ascending=[False, False])
    
    # Truncate subject for display
    display_df['Subject'] = display_df['Subject'].apply(lambda x: x[:60] + "..." if len(str(x)) > 60 else x)
    
    # Colour code rows
    def highlight_completed(row):
        if row['Assigned To'] == 'completed':
            return ['background-color: rgba(16, 185, 129, 0.2)'] * len(row)
        return [''] * len(row)
    
    st.dataframe(
        display_df.style.apply(highlight_completed, axis=1),
        use_container_width=True,
        height=400
    )
    
    # CSV download
    st.download_button(
        label="📥 Download Filtered Data",
        data=filtered_df.to_csv(index=False).encode('utf-8'),
        file_name=f"transfer_data_filtered_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
        mime="text/csv",
        use_container_width=True
    )

# ==================== FOOTER ====================
st.markdown("---")
st.markdown(f"""
<div style='text-align: center; color: #718096; font-size: 0.85rem;'>
    <p>🤖 Automated Transfer Bot v2.0 | Last refresh: {datetime.now().strftime('%H:%M:%S')} | Auto-refreshes every 5 seconds</p>
</div>
""", unsafe_allow_html=True)