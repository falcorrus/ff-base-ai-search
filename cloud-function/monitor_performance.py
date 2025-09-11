#!/usr/bin/env python3
"""
Script to monitor the performance of the Cloud Function.
"""

import os
import sys
import json
from datetime import datetime, timedelta
from google.cloud import monitoring_v3
from google.auth import default

# Configuration
PROJECT_ID = "ff-base"
FUNCTION_NAME = "sync-drive-to-gcs"
REGION = "us-central1"

def get_monitoring_client():
    """Initialize and return Google Cloud Monitoring client."""
    try:
        # Use default credentials
        credentials, project = default()
        
        # Initialize client
        client = monitoring_v3.MetricServiceClient(credentials=credentials)
        print("✅ Google Cloud Monitoring client initialized")
        return client
        
    except Exception as e:
        print(f"Error initializing Monitoring client: {e}")
        return None

def get_execution_count(client, project_id):
    """Get execution count for the function."""
    try:
        # Create query for execution count
        project_name = f"projects/{project_id}"
        
        # Define the time range (last 24 hours)
        end_time = datetime.utcnow()
        start_time = end_time - timedelta(hours=24)
        
        # Create the request
        request = monitoring_v3.ListTimeSeriesRequest(
            name=project_name,
            filter=f'metric.type="cloudfunctions.googleapis.com/function/execution_count" AND resource.labels.function_name="{FUNCTION_NAME}"',
            interval=monitoring_v3.TimeInterval(
                start_time={"seconds": int(start_time.timestamp())},
                end_time={"seconds": int(end_time.timestamp())}
            ),
            view=monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL
        )
        
        # Execute the request
        results = client.list_time_series(request=request)
        
        # Process results
        total_executions = 0
        for result in results:
            for point in result.points:
                total_executions += point.value.int64_value
        
        print(f"📈 Total executions in last 24 hours: {total_executions}")
        return total_executions
        
    except Exception as e:
        print(f"Error getting execution count: {e}")
        return 0

def get_execution_times(client, project_id):
    """Get execution times for the function."""
    try:
        # Create query for execution times
        project_name = f"projects/{project_id}"
        
        # Define the time range (last 24 hours)
        end_time = datetime.utcnow()
        start_time = end_time - timedelta(hours=24)
        
        # Create the request
        request = monitoring_v3.ListTimeSeriesRequest(
            name=project_name,
            filter=f'metric.type="cloudfunctions.googleapis.com/function/execution_times" AND resource.labels.function_name="{FUNCTION_NAME}"',
            interval=monitoring_v3.TimeInterval(
                start_time={"seconds": int(start_time.timestamp())},
                end_time={"seconds": int(end_time.timestamp())}
            ),
            view=monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL
        )
        
        # Execute the request
        results = client.list_time_series(request=request)
        
        # Process results
        execution_times = []
        for result in results:
            for point in result.points:
                execution_times.append(point.value.distribution_value.mean)
        
        if execution_times:
            avg_execution_time = sum(execution_times) / len(execution_times)
            min_execution_time = min(execution_times)
            max_execution_time = max(execution_times)
            
            print(f"⏱️  Average execution time: {avg_execution_time:.2f} seconds")
            print(f"⏱️  Minimum execution time: {min_execution_time:.2f} seconds")
            print(f"⏱️  Maximum execution time: {max_execution_time:.2f} seconds")
            
            return avg_execution_time, min_execution_time, max_execution_time
        else:
            print("⏱️  No execution times found")
            return 0, 0, 0
        
    except Exception as e:
        print(f"Error getting execution times: {e}")
        return 0, 0, 0

def get_error_count(client, project_id):
    """Get error count for the function."""
    try:
        # Create query for errors
        project_name = f"projects/{project_id}"
        
        # Define the time range (last 24 hours)
        end_time = datetime.utcnow()
        start_time = end_time - timedelta(hours=24)
        
        # Create the request
        request = monitoring_v3.ListTimeSeriesRequest(
            name=project_name,
            filter=f'metric.type="cloudfunctions.googleapis.com/function/execution_count" AND resource.labels.function_name="{FUNCTION_NAME}" AND metric.labels.status="error"',
            interval=monitoring_v3.TimeInterval(
                start_time={"seconds": int(start_time.timestamp())},
                end_time={"seconds": int(end_time.timestamp())}
            ),
            view=monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL
        )
        
        # Execute the request
        results = client.list_time_series(request=request)
        
        # Process results
        error_count = 0
        for result in results:
            for point in result.points:
                error_count += point.value.int64_value
        
        print(f"❌ Error count in last 24 hours: {error_count}")
        return error_count
        
    except Exception as e:
        print(f"Error getting error count: {e}")
        return 0

def monitor_performance():
    """Monitor the performance of the Cloud Function."""
    try:
        print("📊 Monitoring Cloud Function performance...")
        
        # Initialize client
        client = get_monitoring_client()
        if not client:
            return False
            
        # Get metrics
        executions = get_execution_count(client, PROJECT_ID)
        avg_time, min_time, max_time = get_execution_times(client, PROJECT_ID)
        errors = get_error_count(client, PROJECT_ID)
        
        # Calculate success rate
        if executions > 0:
            success_rate = ((executions - errors) / executions) * 100
            print(f"✅ Success rate: {success_rate:.2f}%")
        else:
            print("✅ Success rate: N/A (no executions)")
            success_rate = 0
        
        # Display summary
        print("\n📊 Performance Summary:")
        print(f"  Total executions: {executions}")
        print(f"  Errors: {errors}")
        print(f"  Success rate: {success_rate:.2f}%")
        print(f"  Average execution time: {avg_time:.2f} seconds")
        print(f"  Min execution time: {min_time:.2f} seconds")
        print(f"  Max execution time: {max_time:.2f} seconds")
        
        return True
        
    except Exception as e:
        print(f"Error monitoring performance: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("📊 Monitoring Cloud Function performance...")
    
    success = monitor_performance()
    
    if success:
        print("✅ Performance monitoring completed successfully")
        sys.exit(0)
    else:
        print("❌ Performance monitoring failed")
        sys.exit(1)