#!/bin/bash
# Script to set up Cloud Monitoring for the sync function

# Set project ID (replace with your actual project ID)
PROJECT_ID="ff-base"

# Set region (replace with your preferred region)
REGION="us-central1"

echo "📈 Setting up Cloud Monitoring for sync function..."

# Create uptime check for the function
gcloud monitoring uptime-check-configs create sync-drive-to-gcs-uptime \\
  --project=$PROJECT_ID \\
  --display-name="FF-BASE Sync Function Uptime Check" \\
  --http-check-url="https://$REGION-$PROJECT_ID.cloudfunctions.net/sync-drive-to-gcs" \\
  --http-check-path="/" \\
  --http-check-port=443 \\
  --http-check-use-ssl=true \\
  --http-check-validate-ssl=true \\
  --selected-regions="usa-iowa,usa-virginia,europe-west" \\
  --period=300s \\
  --timeout=10s

echo "✅ Uptime check created!"

# Create alert policy for function errors
gcloud alpha monitoring policies create \\
  --project=$PROJECT_ID \\
  --display-name="FF-BASE Sync Function Errors" \\
  --documentation="Alert when sync function encounters errors" \\
  --conditions='[{
    "conditionThreshold": {
      "filter": "metric.type=\\"cloudfunctions.googleapis.com/function/execution_count\\" AND resource.type=\\"cloud_function\\" AND metric.label.\\"status\\"=\\"error\\"",
      "comparison": "COMPARISON_GT",
      "thresholdValue": 0,
      "duration": "60s",
      "aggregations": [{
        "alignmentPeriod": "60s",
        "perSeriesAligner": "ALIGN_RATE"
      }]
    }
  }]'

echo "✅ Alert policy for errors created!"

# Create alert policy for function timeout
gcloud alpha monitoring policies create \\
  --project=$PROJECT_ID \\
  --display-name="FF-BASE Sync Function Timeout" \\
  --documentation="Alert when sync function times out" \\
  --conditions='[{
    "conditionThreshold": {
      "filter": "metric.type=\\"cloudfunctions.googleapis.com/function/execution_times\\" AND resource.type=\\"cloud_function\\" AND metric.label.\\"status\\"=\\"timeout\\"",
      "comparison": "COMPARISON_GT",
      "thresholdValue": 0,
      "duration": "60s",
      "aggregations": [{
        "alignmentPeriod": "60s",
        "perSeriesAligner": "ALIGN_PERCENTILE_99"
      }]
    }
  }]'

echo "✅ Alert policy for timeouts created!"

# Create dashboard for monitoring function metrics
gcloud monitoring dashboards create \\
  --project=$PROJECT_ID \\
  --display-name="FF-BASE Sync Function Dashboard" \\
  --config='{
    "displayName": "FF-BASE Sync Function Dashboard",
    "gridLayout": {
      "widgets": [
        {
          "title": "Execution Count",
          "xyChart": {
            "dataSets": [
              {
                "timeSeriesQuery": {
                  "timeSeriesFilter": {
                    "filter": "metric.type=\\"cloudfunctions.googleapis.com/function/execution_count\\" AND resource.type=\\"cloud_function\\""
                  }
                }
              }
            ],
            "chartOptions": {
              "mode": "COLOR"
            }
          }
        },
        {
          "title": "Execution Times",
          "xyChart": {
            "dataSets": [
              {
                "timeSeriesQuery": {
                  "timeSeriesFilter": {
                    "filter": "metric.type=\\"cloudfunctions.googleapis.com/function/execution_times\\" AND resource.type=\\"cloud_function\\""
                  }
                }
              }
            ],
            "chartOptions": {
              "mode": "COLOR"
            }
          }
        },
        {
          "title": "Errors",
          "xyChart": {
            "dataSets": [
              {
                "timeSeriesQuery": {
                  "timeSeriesFilter": {
                    "filter": "metric.type=\\"cloudfunctions.googleapis.com/function/execution_count\\" AND resource.type=\\"cloud_function\\" AND metric.label.\\"status\\"=\\"error\\""
                  }
                }
              }
            ],
            "chartOptions": {
              "mode": "COLOR"
            }
          }
        },
        {
          "title": "Active Instances",
          "xyChart": {
            "dataSets": [
              {
                "timeSeriesQuery": {
                  "timeSeriesFilter": {
                    "filter": "metric.type=\\"cloudfunctions.googleapis.com/function/active_instances\\" AND resource.type=\\"cloud_function\\""
                  }
                }
              }
            ],
            "chartOptions": {
              "mode": "COLOR"
            }
          }
        }
      ]
    }
  }'

echo "✅ Monitoring dashboard created!"

echo "📈 Cloud Monitoring setup completed!"