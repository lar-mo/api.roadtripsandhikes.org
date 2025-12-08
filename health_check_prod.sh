#!/bin/bash
# Health check script for api.roadtripsandhikes.org
# PRODUCTION VERSION - restarts after 3 consecutive failures (3 minutes)

LOG_FILE="$HOME/api_health_check.log"
MAX_FAILURES=3
FAILURE_COUNT_FILE="/tmp/api_health_failures"

# Initialize failure count file if it doesn't exist
if [ ! -f "$FAILURE_COUNT_FILE" ]; then
    echo "0" > "$FAILURE_COUNT_FILE"
fi

# Read current failure count
FAILURES=$(cat "$FAILURE_COUNT_FILE")

# Test the API endpoint with 10 second timeout
RESPONSE=$(curl -s -o /dev/null -w "%{http_code}" --max-time 10 "https://api.roadtripsandhikes.org/wrapper/bloggerApiGetLatestPost/")

if [ "$RESPONSE" = "200" ]; then
    # Success - reset failure count
    if [ "$FAILURES" -gt "0" ]; then
        echo "$(date): API recovered (HTTP $RESPONSE) - Resetting failure counter" >> "$LOG_FILE"
    fi
    echo "0" > "$FAILURE_COUNT_FILE"
else
    # Failure - increment counter
    FAILURES=$((FAILURES + 1))
    echo "$FAILURES" > "$FAILURE_COUNT_FILE"
    echo "$(date): API unhealthy (HTTP $RESPONSE) - Failure $FAILURES/$MAX_FAILURES" >> "$LOG_FILE"
    
    # If we've hit max failures, restart
    if [ "$FAILURES" -ge "$MAX_FAILURES" ]; then
        echo "$(date): Restarting gunicorn-api after $FAILURES consecutive failures" >> "$LOG_FILE"
        systemctl --user restart gunicorn-api
        echo "0" > "$FAILURE_COUNT_FILE"
        
        # Wait and verify restart
        sleep 5
        RECHECK=$(curl -s -o /dev/null -w "%{http_code}" --max-time 10 "https://api.roadtripsandhikes.org/wrapper/bloggerApiGetLatestPost/")
        echo "$(date): After restart - API status (HTTP $RECHECK)" >> "$LOG_FILE"
    fi
fi
