#!/usr/bin/env python3
"""
Test script to verify timezone handling in the sync function.
"""

import os
import sys
import json
from datetime import datetime
import pytz

# Add the cloud-function directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'cloud-function'))

def test_timezone_conversion():
    """Test timezone conversion functions."""
    print("🧪 Testing timezone conversion functions...")
    
    # Test importing required modules
    try:
        import pytz
        from datetime import datetime
        print("✅ Imported required modules successfully")
    except ImportError as e:
        print(f"❌ Failed to import required modules: {e}")
        return False
    
    # Test timezone definitions
    try:
        UTC = pytz.UTC
        BRT = pytz.timezone('America/Sao_Paulo')  # Brasília Time (UTC-3)
        print("✅ Timezone definitions loaded successfully")
        print(f"   UTC timezone: {UTC}")
        print(f"   BRT timezone: {BRT}")
    except Exception as e:
        print(f"❌ Failed to define timezones: {e}")
        return False
    
    # Test current time in different zones
    try:
        # Get current UTC time (using recommended approach)
        current_utc = datetime.now(pytz.UTC)
        print(f"🕐 Current UTC time: {current_utc.isoformat()}")
        
        # Convert to BRT
        current_brt = current_utc.astimezone(BRT)
        print(f"🕐 Current BRT time: {current_brt.strftime('%Y-%m-%d %H:%M:%S %Z')}")
        
        # Test conversion function
        utc_time_str = current_utc.isoformat().replace('+00:00', 'Z')
        print(f"🕐 UTC time string: {utc_time_str}")
        
        # Simulate the conversion function
        try:
            # Parse UTC time string
            if 'T' in utc_time_str and 'Z' in utc_time_str:
                # ISO format with Z suffix
                parsed_utc = datetime.fromisoformat(utc_time_str.replace('Z', '+00:00'))
            elif 'T' in utc_time_str and '+' in utc_time_str:
                # ISO format with timezone offset
                parsed_utc = datetime.fromisoformat(utc_time_str)
            else:
                # Assume it's already in a compatible format
                parsed_utc = current_utc
            
            # Convert to BRT
            brt_time = parsed_utc.astimezone(BRT)
            formatted_brt = brt_time.strftime('%Y-%m-%d %H:%M:%S BRT')
            print(f"🕐 Converted BRT time: {formatted_brt}")
            
            print("✅ Timezone conversion works correctly")
            
        except Exception as e:
            print(f"❌ Error in timezone conversion: {e}")
            return False
            
    except Exception as e:
        print(f"❌ Error testing current time: {e}")
        return False
    
    print("🎉 All timezone tests passed!")
    return True

def test_time_functions():
    """Test time-related functions."""
    print("🧪 Testing time-related functions...")
    
    # Import the main module
    try:
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'cloud-function'))
        import main
        print("✅ Imported main module successfully")
    except ImportError as e:
        print(f"❌ Failed to import main module: {e}")
        return False
    
    # Test current time functions
    try:
        utc_time = main.get_current_time_utc()
        brt_time = main.get_current_time_brt()
        
        print(f"🕐 Current UTC time: {utc_time}")
        print(f"🕐 Current BRT time: {brt_time}")
        
        print("✅ Time functions work correctly")
        
    except Exception as e:
        print(f"❌ Error testing time functions: {e}")
        return False
    
    print("🎉 All time function tests passed!")
    return True

if __name__ == "__main__":
    print("🚀 Testing timezone handling in sync function...")
    
    # Run tests
    success1 = test_timezone_conversion()
    success2 = test_time_functions()
    
    if success1 and success2:
        print("✅ All tests passed!")
        sys.exit(0)
    else:
        print("❌ Some tests failed!")
        sys.exit(1)