#!/bin/bash
# Script to manage all monitoring aspects

# Set project ID (replace with your actual project ID)
PROJECT_ID="ff-base"

# Set region (replace with your preferred region)
REGION="us-central1"

echo "📊 Managing all monitoring aspects..."

# Function to show menu
show_menu() {
    echo "📋 Monitoring Management Menu:"
    echo "1. View Cloud Function logs"
    echo "2. View filtered Cloud Function logs"
    echo "3. View Cloud Scheduler logs"
    echo "4. View Cloud Function performance metrics"
    echo "5. View scheduled job status"
    echo "6. Run performance monitoring"
    echo "7. Setup monitoring schedule"
    echo "8. Pause scheduled jobs"
    echo "9. Resume scheduled jobs"
    echo "10. Exit"
    echo
    read -p "Enter your choice [1-10]: " choice
}

# Function to view Cloud Function logs
view_function_logs() {
    echo "📋 Viewing Cloud Function logs..."
    ./view_logs.sh
}

# Function to view filtered Cloud Function logs
view_filtered_logs() {
    echo "📋 Viewing filtered Cloud Function logs..."
    ./view_filtered_logs.sh
}

# Function to view Cloud Scheduler logs
view_scheduler_logs() {
    echo "📋 Viewing Cloud Scheduler logs..."
    ./view_scheduler_logs.sh
}

# Function to view performance metrics
view_performance_metrics() {
    echo "📊 Viewing Cloud Function performance metrics..."
    ./view_performance_metrics.sh
}

# Function to view job status
view_job_status() {
    echo "📅 Viewing scheduled job status..."
    ./view_job_status.sh
}

# Function to run performance monitoring
run_performance_monitoring() {
    echo "📈 Running performance monitoring..."
    ./run_monitoring.sh
}

# Function to setup monitoring schedule
setup_monitoring_schedule() {
    echo "📅 Setting up monitoring schedule..."
    ./setup_monitoring_schedule.sh
}

# Function to pause scheduled jobs
pause_scheduled_jobs() {
    echo "⏸️ Pausing scheduled jobs..."
    gcloud scheduler jobs pause sync-drive-to-gcs-daily \
      --project=$PROJECT_ID \
      --location=$REGION
      
    gcloud scheduler jobs pause monitor-drive-to-gcs-performance \
      --project=$PROJECT_ID \
      --location=$REGION
      
    gcloud scheduler jobs pause daily-report-drive-to-gcs \
      --project=$PROJECT_ID \
      --location=$REGION
      
    echo "✅ Scheduled jobs paused!"
}

# Function to resume scheduled jobs
resume_scheduled_jobs() {
    echo "▶️ Resuming scheduled jobs..."
    gcloud scheduler jobs resume sync-drive-to-gcs-daily \
      --project=$PROJECT_ID \
      --location=$REGION
      
    gcloud scheduler jobs resume monitor-drive-to-gcs-performance \
      --project=$PROJECT_ID \
      --location=$REGION
      
    gcloud scheduler jobs resume daily-report-drive-to-gcs \
      --project=$PROJECT_ID \
      --location=$REGION
      
    echo "✅ Scheduled jobs resumed!"
}

# Main loop
while true; do
    show_menu
    
    case $choice in
        1) view_function_logs ;;
        2) view_filtered_logs ;;
        3) view_scheduler_logs ;;
        4) view_performance_metrics ;;
        5) view_job_status ;;
        6) run_performance_monitoring ;;
        7) setup_monitoring_schedule ;;
        8) pause_scheduled_jobs ;;
        9) resume_scheduled_jobs ;;
        10) echo "👋 Exiting..."; exit 0 ;;
        *) echo "❌ Invalid choice. Please enter a number between 1-10." ;;
    esac
    
    echo
    read -p "Press Enter to continue..."
    clear
done