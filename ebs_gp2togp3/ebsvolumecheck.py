import boto3

def extract_vid(volume_arn):
    arn_parts = volume_arn.split(':')
    volume_id = arn_parts[-1].split('/')[-1]
    return volume_id

def lambda_handler(event, context):
    
    volume_arn = event['resources'][0]    
    volume_id = extract_vid(volume_arn)
    print(volume_id)

    ebs = boto3.client('ec2')

    response = ebs.modify_volume(
    VolumeId=volume_id,
    VolumeType='gp3',
    )