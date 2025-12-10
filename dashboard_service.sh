#!/bin/bash

# SAMI Dashboard - Background Service Manager
# Allows the dashboard to run in the background

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PID_FILE="$SCRIPT_DIR/dashboard.pid"
LOG_FILE="$SCRIPT_DIR/dashboard.log"

case "$1" in
    start)
        if [ -f "$PID_FILE" ]; then
            PID=$(cat "$PID_FILE")
            if ps -p $PID > /dev/null 2>&1; then
                echo "❌ Dashboard is already running (PID: $PID)"
                echo "   Access it at: http://localhost:8502"
                exit 1
            fi
        fi
        
        echo "🚀 Starting SAMI Dashboard in background..."
        cd "$SCRIPT_DIR"
        source venv/bin/activate
        nohup streamlit run dashboard.py --server.port 8502 --server.address 0.0.0.0 --server.headless true > "$LOG_FILE" 2>&1 &
        echo $! > "$PID_FILE"
        sleep 3
        
        if ps -p $(cat "$PID_FILE") > /dev/null 2>&1; then
            echo "✅ Dashboard started successfully!"
            echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
            echo "   Local:   http://localhost:8502"
            echo "   Network: http://$(hostname -I | awk '{print $1}'):8502"
            echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
            echo "   Use './dashboard_service.sh status' to check"
            echo "   Use './dashboard_service.sh stop' to stop"
            echo "   Logs: $LOG_FILE"
        else
            echo "❌ Failed to start dashboard. Check $LOG_FILE for errors."
            rm -f "$PID_FILE"
            exit 1
        fi
        ;;
        
    stop)
        if [ ! -f "$PID_FILE" ]; then
            echo "❌ Dashboard is not running (no PID file found)"
            exit 1
        fi
        
        PID=$(cat "$PID_FILE")
        if ps -p $PID > /dev/null 2>&1; then
            echo "🛑 Stopping dashboard (PID: $PID)..."
            kill $PID
            rm -f "$PID_FILE"
            sleep 2
            
            if ps -p $PID > /dev/null 2>&1; then
                echo "⚠️  Process still running, force killing..."
                kill -9 $PID
            fi
            
            echo "✅ Dashboard stopped"
        else
            echo "❌ Dashboard is not running (stale PID file)"
            rm -f "$PID_FILE"
        fi
        ;;
        
    restart)
        $0 stop
        sleep 2
        $0 start
        ;;
        
    status)
        if [ ! -f "$PID_FILE" ]; then
            echo "⚫ Dashboard is NOT running"
            exit 1
        fi
        
        PID=$(cat "$PID_FILE")
        if ps -p $PID > /dev/null 2>&1; then
            echo "🟢 Dashboard is RUNNING (PID: $PID)"
            echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
            echo "   Local:   http://localhost:8502"
            echo "   Network: http://$(hostname -I | awk '{print $1}'):8502"
            echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
            
            # Show last few log entries
            if [ -f "$LOG_FILE" ]; then
                echo ""
                echo "Recent activity:"
                tail -5 "$LOG_FILE" | grep -v "^$"
            fi
        else
            echo "⚫ Dashboard is NOT running (stale PID file)"
            rm -f "$PID_FILE"
            exit 1
        fi
        ;;
        
    logs)
        if [ -f "$LOG_FILE" ]; then
            tail -f "$LOG_FILE"
        else
            echo "❌ No log file found at $LOG_FILE"
            exit 1
        fi
        ;;
        
    *)
        echo "SAMI Dashboard Service Manager"
        echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
        echo "Usage: $0 {start|stop|restart|status|logs}"
        echo ""
        echo "Commands:"
        echo "  start   - Start the dashboard in background"
        echo "  stop    - Stop the dashboard"
        echo "  restart - Restart the dashboard"
        echo "  status  - Check if dashboard is running"
        echo "  logs    - View live dashboard logs"
        echo ""
        echo "Example: ./dashboard_service.sh start"
        exit 1
        ;;
esac

exit 0
