import boto3
import datetime

def get_ec2_client():
    """
    Create and return an EC2 client using boto3.
    """
    return boto3.client('ec2')

def list_ec2_instances(ec2):
    """
    List all EC2 instances with their current state.
    """
    response = ec2.describe_instances()
    for reservation in response['Reservations']:
        for instance in reservation['Instances']:
            print(f"Instance ID: {instance['InstanceId']} State: {instance['State']['Name']}")

def get_cpu_utilization(ec2_instance_id, start_time, end_time):
    """
    Get the average CPU utilization for a specific EC2 instance over a given time period.
    """
    cloudwatch = boto3.client('cloudwatch')
    response = cloudwatch.get_metric_statistics(
        Namespace='AWS/EC2',
        MetricName='CPUUtilization',
        Dimensions=[{'Name': 'InstanceId', 'Value': ec2_instance_id}],
        StartTime=start_time,
        EndTime=end_time,
        Period=3600,
        Statistics=['Average']
    )
    return response['Datapoints']

def main():
    ec2 = get_ec2_client()
    list_ec2_instances(ec2)

  
    instance_id = 'i-12231232dsfwq'  
    start = datetime.datetime.now() - datetime.timedelta(days=30)
    end = datetime.datetime.now()
    cpu_utilization = get_cpu_utilization(instance_id, start, end)
    print(cpu_utilization)

if __name__ == "__main__":
    main()
