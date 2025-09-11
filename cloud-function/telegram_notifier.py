#!/usr/bin/env python3
"""
Script to send notifications to Telegram.
"""

import os
import requests
import json
from datetime import datetime
import pytz

# Configuration
TELEGRAM_BOT_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')
TELEGRAM_CHAT_ID = os.environ.get('TELEGRAM_CHAT_ID')
BRT = pytz.timezone('America/Sao_Paulo')  # Brasília Time (UTC-3)

def get_current_time_brt():
    """Get current time in BRT format for display."""
    try:
        current_utc = datetime.utcnow()
        current_brt = current_utc.replace(tzinfo=pytz.UTC).astimezone(BRT)
        return current_brt.strftime('%Y-%m-%d %H:%M:%S BRT')
    except Exception as e:
        return "Unknown BRT time"

def send_telegram_message(message):
    """Send message to Telegram chat."""
    try:
        if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
            print("Telegram bot token or chat ID not found in environment variables")
            return False
            
        # Format message with timestamp
        timestamp = get_current_time_brt()
        formatted_message = f"[{timestamp}] {message}"
        
        # Send message to Telegram
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        payload = {
            'chat_id': TELEGRAM_CHAT_ID,
            'text': formatted_message,
            'parse_mode': 'Markdown'
        }
        
        response = requests.post(url, json=payload)
        if response.status_code == 200:
            print("✅ Notification sent to Telegram")
            return True
        else:
            print(f"❌ Failed to send notification to Telegram: {response.status_code} - {response.text}")
            return False
            
    except Exception as e:
        print(f"Error sending Telegram message: {e}")
        return False

def send_sync_notification(success, duration, synced_count, skipped_count, failed_count):
    """Send sync completion notification to Telegram."""
    try:
        if success:
            message = f"""
✅ *Sync Completed Successfully*

⏱️ Duration: {duration}
📄 Files synced: {synced_count}
⏭️ Files unchanged: {skipped_count}
❌ Files failed: {failed_count}

🕒 Completed at (BRT): {get_current_time_brt()}
"""
        else:
            message = f"""
❌ *Sync Failed*

⏱️ Duration: {duration}
📄 Files synced: {synced_count}
⏭️ Files unchanged: {skipped_count}
❌ Files failed: {failed_count}

🕒 Failed at (BRT): {get_current_time_brt()}
"""
        
        return send_telegram_message(message)
        
    except Exception as e:
        print(f"Error sending sync notification: {e}")
        return False

def send_error_notification(error_message):
    """Send error notification to Telegram."""
    try:
        message = f"""
🚨 *Sync Error*

❌ {error_message}

🕒 Error occurred at (BRT): {get_current_time_brt()}
"""
        
        return send_telegram_message(message)
        
    except Exception as e:
        print(f"Error sending error notification: {e}")
        return False

if __name__ == "__main__":
    # Test sending a notification
    send_telegram_message("🔔 Test notification from FF-BASE sync system")