#!/bin/bash
# Health check script for api.roadtripsandhikes.org
# TESTING VERSION - restarts immediately on first failure

LOG_FILE="$HOME/api_health_check.log"

# Test the API endpoint with 10 second timeout
RESPONSE=$(curl -s -o /dev/null -w "%{http_code}" --max-time 10 "https://api.roadtripsandhikes.org/wrapper/bloggerApiGetLatestPost/")

if [ "$RESPONSE" = "200" ]; then
    # Success
    echo "$(date): API healthy (HTTP $RESPONSE)" >> "$LOG_FILE"
else
    # Failure - restart immediately (testing mode)
    echo "$(date): API unhealthy (HTTP $RESPONSE) - Restarting gunicorn-api" >> "$LOG_FILE"
    systemctl --user restart gunicorn-api
    sleep 5
    # Check if restart worked
    RECHECK=$(curl -s -o /dev/null -w "%{http_code}" --max-time 10 "https://api.roadtripsandhikes.org/wrapper/bloggerApiGetLatestPost/")
    echo "$(date): After restart - API status (HTTP $RECHECK)" >> "$LOG_FILE"
fi
