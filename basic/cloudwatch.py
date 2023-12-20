import boto3
import datetime

def get_cloudwatch_client():
    """
    Create and return a CloudWatch client using boto3.
    """
    return boto3.client('cloudwatch')

def get_metric_statistics(client, instance_id, metric_name, start_time, end_time):
    """
    Get statistics for a specific metric from CloudWatch.
    """
    response = client.get_metric_statistics(
        Namespace='AWS/EC2',
        MetricName=metric_name,
        Dimensions=[{'Name': 'InstanceId', 'Value': instance_id}],
        StartTime=start_time,
        EndTime=end_time,
        Period=3600,
        Statistics=['Average']
    )
    return response['Datapoints']

def collect_instance_metrics(instance_id, start_time, end_time):
    """
    Collect various metrics for a specific EC2 instance.
    """
    cloudwatch = get_cloudwatch_client()

    metrics = {
        'CPUUtilization': get_metric_statistics(cloudwatch, instance_id, 'CPUUtilization', start_time, end_time),
        'NetworkIn': get_metric_statistics(cloudwatch, instance_id, 'NetworkIn', start_time, end_time),
        'NetworkOut': get_metric_statistics(cloudwatch, instance_id, 'NetworkOut', start_time, end_time),
        'DiskReadOps': get_metric_statistics(cloudwatch, instance_id, 'DiskReadOps', start_time, end_time),
        'DiskWriteOps': get_metric_statistics(cloudwatch, instance_id, 'DiskWriteOps', start_time, end_time),
        'DiskReadBytes': get_metric_statistics(cloudwatch, instance_id, 'DiskReadBytes', start_time, end_time),
        'DiskWriteBytes': get_metric_statistics(cloudwatch, instance_id, 'DiskWriteBytes', start_time, end_time)
    }

    return metrics

def main():
 
    instance_id = 'i-2349asdfasd'  
    start = datetime.datetime.now() - datetime.timedelta(days=30)
    end = datetime.datetime.now()

    instance_metrics = collect_instance_metrics(instance_id, start, end)
    for metric, data in instance_metrics.items():
        print(f"{metric}: {data}")

if __name__ == "__main__":
    main()
