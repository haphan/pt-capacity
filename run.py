from google.cloud import monitoring_v3
from google.protobuf.timestamp_pb2 import Timestamp
import time

# Replace with your values
project_id = "your-gcp-project-id"
region = "us-central1"
# This is often the project number
model_user_id = "your-project-number"
metric_type = "aiplatform.googleapis.com/publisher/online_serving/token_count"
resource_type = "aiplatform.googleapis.com/PublisherModel"

client = monitoring_v3.MetricServiceClient()
project_name = f"projects/{project_id}"

# Time interval: last 5 minutes
end_time = time.time()
start_time = end_time - 300  # 5 minutes ago

interval = monitoring_v3.TimeInterval(
    start_time=Timestamp(seconds=int(start_time)),
    end_time=Timestamp(seconds=int(end_time)),
)

# Filter
filter_string = (
    f'metric.type="{metric_type}" AND '
    f'resource.type="{resource_type}" AND '
    f'resource.labels.location="{region}" AND '
    f'resource.labels.model_user_id="{model_user_id}"'
)

# Aggregation
aggregation = monitoring_v3.Aggregation(
    alignment_period={"seconds": 60},  # 1 minute
    per_series_aligner=monitoring_v3.Aggregation.Aligner.ALIGN_RATE,
    cross_series_reducer=monitoring_v3.Aggregation.Reducer.REDUCE_SUM,
    group_by_fields=["metric.labels.request_type"],
)

try:
    results = client.list_time_series(
        request={
            "name": project_name,
            "filter": filter_string,
            "interval": interval,
            "aggregation": aggregation,
        }
    )

    for result in results:
        request_type = result.metric.labels.get("request_type", "unknown")
        print(f"Request Type: {request_type}")
        # print(f"Metric: {result.metric.type}")
        # print(f"Resource: {result.resource.type}")
        for point in result.points:
            print(
                f"  Time: {point.interval.end_time.ToDatetime()} "
                f"Value: {point.value.double_value} tokens/sec"
            )
        print("-" * 20)

except Exception as e:
    print(f"Error fetching metrics: {e}")