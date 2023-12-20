import boto3
import csv
import datetime

def get_ec2_instances():
    ec2_client = boto3.client('ec2')
    instances = ec2_client.describe_instances()
    instance_info = []
    for reservation in instances['Reservations']:
        for instance in reservation['Instances']:
            instance_id = instance['InstanceId']
            instance_name = ''
            for tag in instance['Tags']:
                if tag['Key'] == 'Name':
                    instance_name = tag['Value']
            instance_info.append({'InstanceId': instance_id, 'InstanceName': instance_name})
    return instance_info

def get_cloudwatch_metrics(instance_id, period_days):
    cloudwatch = boto3.client('cloudwatch')
    end_time = datetime.datetime.now()
    start_time = end_time - datetime.timedelta(days=period_days)
    response = cloudwatch.get_metric_statistics(
        Namespace='AWS/EC2',
        MetricName='CPUUtilization',
        Dimensions=[{'Name': 'InstanceId', 'Value': instance_id}],
        StartTime=start_time,
        EndTime=end_time,
        Period=3600,
        Statistics=['Average']
    )
    avg_cpu_utilization = sum(data_point['Average'] for data_point in response['Datapoints']) / len(response['Datapoints']) if response['Datapoints'] else 0
    return avg_cpu_utilization

def generate_csv_report(instance_info):
    with open('ec2_report.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Instance ID', 'Instance Name', 'CPU Utilization (60 days)', 'CPU Utilization (30 days)', 'CPU Utilization (7 days)'])

        for instance in instance_info:
            instance_id = instance['InstanceId']
            cpu_util_60_days = get_cloudwatch_metrics(instance_id, 60)
            cpu_util_30_days = get_cloudwatch_metrics(instance_id, 30)
            cpu_util_7_days = get_cloudwatch_metrics(instance_id, 7)
            writer.writerow([instance_id, instance['InstanceName'], cpu_util_60_days, cpu_util_30_days, cpu_util_7_days])

if __name__ == "__main__":
    ec2_instances = get_ec2_instances()
    generate_csv_report(ec2_instances)
