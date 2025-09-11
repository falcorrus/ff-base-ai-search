#!/usr/bin/env python3
"""
Time utility functions for the Cloud Function.
"""

import pytz
from datetime import datetime

# Time zones
UTC = pytz.UTC
BRT = pytz.timezone('America/Sao_Paulo')  # Brasília Time (UTC-3)

def utc_to_brt(utc_time_str):
    """Convert UTC time string to BRT for display in logs."""
    try:
        # Handle different time string formats
        if 'T' in utc_time_str and 'Z' in utc_time_str:
            # ISO format with Z suffix
            utc_dt = datetime.fromisoformat(utc_time_str.replace('Z', '+00:00'))
        elif 'T' in utc_time_str and '+' in utc_time_str:
            # ISO format with timezone offset
            utc_dt = datetime.fromisoformat(utc_time_str)
        else:
            # Assume it's already in a compatible format
            return utc_time_str
        
        # Convert to BRT
        brt_dt = utc_dt.astimezone(BRT)
        
        # Format for display
        return brt_dt.strftime('%Y-%m-%d %H:%M:%S BRT')
    except Exception as e:
        print(f"Error converting time {utc_time_str} to BRT: {e}")
        return utc_time_str

def get_current_time_brt():
    """Get current time in BRT format for display."""
    try:
        current_utc = datetime.now(UTC)
        current_brt = current_utc.astimezone(BRT)
        return current_brt.strftime('%Y-%m-%d %H:%M:%S BRT')
    except Exception as e:
        print(f"Error getting current time in BRT: {e}")
        return "Unknown BRT time"

def get_current_time_utc():
    """Get current time in UTC format for internal operations."""
    try:
        current_utc = datetime.now(UTC).isoformat() + 'Z'
        return current_utc
    except Exception as e:
        print(f"Error getting current time in UTC: {e}")
        return "1970-01-01T00:00:00Z"