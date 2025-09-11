#!/usr/bin/env python3
"""
Main Cloud Function to sync notes from Google Drive to Google Cloud Storage.
Entry point for both HTTP and background triggers.
Uses highly optimized incremental sync with timeout handling.
"""

# Import the optimized sync function
from optimized_sync import sync_drive_to_gcs_optimized, sync_drive_to_gcs_http, sync_drive_to_gcs

# Export functions for Cloud Functions
sync_drive_to_gcs_http = sync_drive_to_gcs_http
sync_drive_to_gcs = sync_drive_to_gcs

def main():
    """Main function for local testing."""
    print("🔄 Testing optimized sync function locally...")
    print(f"🕒 Local test started at (BRT): {get_current_time_brt()}")
    
    success = sync_drive_to_gcs_optimized()
    
    if success:
        print("✅ Optimized sync completed successfully")
        print(f"🕒 Local test completed at (BRT): {get_current_time_brt()}")
    else:
        print("❌ Optimized sync failed")
        print(f"🕒 Local test failed at (BRT): {get_current_time_brt()}")

if __name__ == "__main__":
    main()