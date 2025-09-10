#!/usr/bin/env python3
"""
Script to set up Google Drive change notifications (Webhook)
"""

import os
import sys
from pathlib import Path
from googleapiclient.discovery import build
from google.oauth2 import service_account
from dotenv import load_dotenv
import hashlib
import hmac
import base64
from datetime import datetime, timedelta

def load_environment():
    """Load environment variables from .env file."""
    env_file = Path("backend/.env")
    if env_file.exists():
        load_dotenv(env_file)
        print("Environment variables loaded")

def get_drive_service():
    """Initialize and return Google Drive service."""
    try:
        # Load service account credentials
        service_account_path = "./backend/service-account-key.json"
        if not os.path.exists(service_account_path):
            print("Service account key not found")
            return None
            
        # Define scopes
        scopes = [
            "https://www.googleapis.com/auth/drive.readonly",
            "https://www.googleapis.com/auth/drive.metadata.readonly"
        ]
        
        # Create credentials
        credentials = service_account.Credentials.from_service_account_file(
            service_account_path, scopes=scopes)
        
        # Build the service
        service = build('drive', 'v3', credentials=credentials)
        print("✅ Google Drive service initialized")
        return service
        
    except Exception as e:
        print(f"Error initializing Google Drive service: {e}")
        return None

def find_ff_base_folder(service):
    """Find the FF-BASE folder in Google Drive."""
    try:
        # Search for the folder by name
        query = "name='FF-BASE' and mimeType='application/vnd.google-apps.folder'"
        results = service.files().list(
            q=query,
            fields="files(id, name)"
        ).execute()
        
        items = results.get('files', [])
        if not items:
            print("FF-BASE folder not found in Google Drive")
            return None
            
        folder = items[0]
        print(f"Found FF-BASE folder: {folder['name']} (ID: {folder['id']})")
        return folder['id']
        
    except Exception as e:
        print(f"Error finding FF-BASE folder: {e}")
        return None

def setup_watch(service, folder_id):
    """Set up watch for changes in the folder."""
    try:
        # Generate unique channel ID
        channel_id = hashlib.md5(f"ff-base-sync-{datetime.now().isoformat()}".encode()).hexdigest()
        
        # Set up watch request
        watch_body = {
            "id": channel_id,
            "type": "web_hook",
            "address": "https://your-domain.com/webhook",  # This needs to be replaced with your actual endpoint
            "expiration": (datetime.now() + timedelta(days=1)).timestamp() * 1000  # 1 day expiration
        }
        
        # Set up watch on the folder
        response = service.files().watch(
            fileId=folder_id,
            body=watch_body
        ).execute()
        
        print(f"✅ Watch setup completed")
        print(f"Channel ID: {response.get('id')}")
        print(f"Resource ID: {response.get('resourceId')}")
        
        return response
        
    except Exception as e:
        print(f"Error setting up watch: {e}")
        return None

def setup_drive_notifications():
    """Set up Google Drive change notifications."""
    try:
        # Load environment variables
        load_environment()
        
        # Initialize services
        drive_service = get_drive_service()
        if not drive_service:
            return False
            
        # Find FF-BASE folder
        folder_id = find_ff_base_folder(drive_service)
        if not folder_id:
            return False
            
        # Set up watch for changes
        watch_response = setup_watch(drive_service, folder_id)
        if watch_response:
            print("✅ Google Drive notifications setup completed successfully")
            print("Note: You need to set up a webhook endpoint to receive notifications")
            return True
        else:
            print("❌ Failed to set up Google Drive notifications")
            return False
        
    except Exception as e:
        print(f"Error setting up Drive notifications: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Main function."""
    print("🔄 Setting up Google Drive change notifications...")
    
    success = setup_drive_notifications()
    if success:
        print("\n✅ Google Drive notifications setup completed")
        print("\nNext steps:")
        print("1. Set up a webhook endpoint to receive notifications")
        print("2. Deploy the endpoint to a public URL")
        print("3. Update the webhook address in this script")
        print("4. Configure the endpoint to trigger sync when notifications are received")
    else:
        print("❌ Failed to set up Google Drive notifications")
        sys.exit(1)

if __name__ == "__main__":
    main()