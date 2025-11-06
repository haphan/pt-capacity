#!/bin/bash

# Replace with your values
PROJECT_ID="your-gcp-project-id"
REGION="us-central1"
# This is often the project number, sometimes referred to as model_user_id
MODEL_USER_ID="your-project-number"
METRIC_TYPE="aiplatform.googleapis.com/publisher/online_serving/token_count"
RESOURCE_TYPE="aiplatform.googleapis.com/PublisherModel"

# Get the current time and 5 minutes ago in RFC3339 UTC format
END_TIME=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
START_TIME=$(date -u -d "5 minutes ago" +"%Y-%m-%dT%H:%M:%SZ")

# Construct the filter
FILTER="metric.type=\"${METRIC_TYPE}\" AND resource.type=\"${RESOURCE_TYPE}\" AND resource.labels.location=\"${REGION}\" AND resource.labels.model_user_id=\"${MODEL_USER_ID}\""

# Call the API
ACCESS_TOKEN=$(gcloud auth print-access-token)

curl -H "Authorization: Bearer ${ACCESS_TOKEN}" \
     -H "Content-Type: application/json" \
     "https://monitoring.googleapis.com/v3/projects/${PROJECT_ID}/timeSeries?filter=$(python -c "import urllib.parse; print(urllib.parse.quote('${FILTER}'))")&interval.startTime=${START_TIME}&interval.endTime=${END_TIME}&aggregation.alignmentPeriod=60s&aggregation.perSeriesAligner=ALIGN_RATE&aggregation.crossSeriesReducer=REDUCE_SUM&aggregation.groupByFields=metric.labels.request_type"