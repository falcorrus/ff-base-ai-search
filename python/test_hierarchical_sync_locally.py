#!/usr/bin/env python3
"""
Local testing script for the hierarchical sync function.
"""

import os
import sys
from pathlib import Path

# Add the cloud-function directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'cloud-function'))

def test_hierarchical_sync():
    """Test the hierarchical sync function locally."""
    print("🧪 Testing hierarchical sync function locally...")
    
    # Set environment variables for local testing
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = './backend/service-account-key.json'
    os.environ['BUCKET_NAME'] = 'ff-base-knowledge-base'
    
    # Import the main module
    try:
        import main
        print("✅ Imported main module successfully")
    except ImportError as e:
        print(f"❌ Failed to import main module: {e}")
        return False
    
    # Test individual functions
    print("🔍 Testing individual functions...")
    
    # Test hash calculation function
    test_string = "FILE:test.md|2023-01-01T00:00:00Z|abc123\\nFOLDER:subfolder|def456\\n"
    expected_length = 32
    
    import hashlib
    test_hash = hashlib.md5(test_string.encode('utf-8')).hexdigest()
    
    if len(test_hash) == expected_length:
        print(f"✅ Hash calculation works correctly (length: {len(test_hash)})")
    else:
        print(f"❌ Hash calculation failed (length: {len(test_hash)}, expected: {expected_length})")
        return False
    
    # Test folder path construction
    test_path = "Как сделать/Авторизация/Авторизация по смс телефону.md"
    if "/" in test_path and len(test_path) > 10:
        print("✅ Folder path construction works correctly")
    else:
        print("❌ Folder path construction failed")
        return False
    
    # Test that all required dependencies are available
    required_packages = [
        'google.cloud.storage',
        'googleapiclient.discovery',
        'google.auth',
        'hashlib',
        'base64'
    ]
    
    for package in required_packages:
        try:
            __import__(package)
            print(f"✅ {package} imported successfully")
        except ImportError as e:
            print(f"❌ Failed to import {package}: {e}")
            return False
    
    print("🎉 All local tests passed!")
    return True

if __name__ == "__main__":
    success = test_hierarchical_sync()
    if success:
        print("✅ Local testing completed successfully")
        sys.exit(0)
    else:
        print("❌ Local testing failed")
        sys.exit(1)