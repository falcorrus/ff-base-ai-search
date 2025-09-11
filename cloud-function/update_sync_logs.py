#!/usr/bin/env python3
"""
Script to update sync logs file with the latest sync results.
Keeps only the last 3 sync entries, removing older ones.
"""

import os
import json
from datetime import datetime
import pytz
from pathlib import Path

# Configuration
LOG_FILE_PATH = "/Users/eugene/MyProjects/ff-base-ai-search/sync_logs.md"
MAX_ENTRIES = 3

# Time zones
BRT = pytz.timezone('America/Sao_Paulo')  # Brasília Time (UTC-3)

def get_current_time_brt():
    """Get current time in BRT format."""
    try:
        current_utc = datetime.utcnow()
        current_brt = current_utc.replace(tzinfo=pytz.UTC).astimezone(BRT)
        return current_brt.strftime('%Y-%m-%d %H:%M:%S BRT')
    except Exception as e:
        return "Unknown BRT time"

def update_sync_logs(success, duration, synced_count, skipped_count, failed_count, error_message=None):
    """Update sync logs file with the latest sync results."""
    try:
        # Create log entry
        current_time = get_current_time_brt()
        
        if success:
            log_entry = f"""
## ✅ Sync Completed Successfully - {current_time}

- **Duration**: {duration}
- **Files synced**: {synced_count}
- **Files unchanged**: {skipped_count}
- **Files failed**: {failed_count}

"""
        else:
            log_entry = f"""
## ❌ Sync Failed - {current_time}

- **Duration**: {duration}
- **Files synced**: {synced_count}
- **Files unchanged**: {skipped_count}
- **Files failed**: {failed_count}
- **Error**: {error_message}

"""
        
        # Read existing log file
        if os.path.exists(LOG_FILE_PATH):
            with open(LOG_FILE_PATH, 'r', encoding='utf-8') as f:
                content = f.read()
        else:
            # Create new log file with header
            content = """# Sync Logs

This file contains logs of the last 3 synchronization operations.
Older entries are automatically removed to keep the file size manageable.

---
"""
        
        # Split content into header and entries
        if "---" in content:
            header_part, entries_part = content.split("---", 1)
            header = header_part + "---\n"
            
            # Split entries
            entries = entries_part.strip().split("\n\n")
            
            # Remove empty entries
            entries = [entry for entry in entries if entry.strip()]
        else:
            header = content
            entries = []
        
        # Add new entry at the beginning
        entries.insert(0, log_entry.strip())
        
        # Keep only the last MAX_ENTRIES entries
        entries = entries[:MAX_ENTRIES]
        
        # Join entries
        updated_content = header + "\n\n".join(entries) + "\n\n"
        
        # Write updated content back to file
        with open(LOG_FILE_PATH, 'w', encoding='utf-8') as f:
            f.write(updated_content)
        
        print(f"✅ Sync logs updated with {len(entries)} entries")
        return True
        
    except Exception as e:
        print(f"Error updating sync logs: {e}")
        return False

def main():
    """Main function for testing."""
    print("🧪 Testing sync logs update...")
    
    # Test successful sync
    success = update_sync_logs(
        success=True,
        duration="0:02:30.864728",
        synced_count=6,
        skipped_count=341,
        failed_count=0
    )
    
    if success:
        print("✅ Sync logs updated successfully")
    else:
        print("❌ Failed to update sync logs")

if __name__ == "__main__":
    main()