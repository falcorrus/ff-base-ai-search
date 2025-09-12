#!/usr/bin/env python3
"""
Time utility functions for the Cloud Function.
"""

import pytz
from datetime import datetime

# Time zones
UTC = pytz.UTC

def utc_to_brt(utc_time_str):
    """Convert UTC time string to UTC for display in logs."""
    # Just return the UTC time string as is
    return utc_time_str

def get_current_time_brt():
    """Get current time in UTC format for display."""
    try:
        current_utc = datetime.now(UTC)
        return current_utc.strftime('%Y-%m-%d %H:%M:%S UTC')
    except Exception as e:
        print(f"Error getting current time in UTC: {e}")
        return "Unknown UTC time"

def get_current_time_utc():
    """Get current time in UTC format for internal operations."""
    try:
        current_utc = datetime.now(UTC).isoformat()
        return current_utc
    except Exception as e:
        print(f"Error getting current time in UTC: {e}")
        return "1970-01-01T00:00:00Z"