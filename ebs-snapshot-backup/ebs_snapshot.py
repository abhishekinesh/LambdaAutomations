import boto3

def lambda_handler(event, context):
    ec2 = boto3.client('ec2')
    
    volume_id = 'vol-0e40062b9a92abcc8'
    snapshot_name = 'Boto3-snapshot'
    
    # Create a new snapshot
    response = ec2.create_snapshot(
        Description='snapshot of iloyalrepo',
        VolumeId=volume_id,
        TagSpecifications=[
            {
                'ResourceType': 'snapshot',
                'Tags': [
                    {
                        'Key': 'Name',
                        'Value': snapshot_name
                    },
                ]
            },
        ],
    )
    print("New snapshot created:", response)
    
    # Retrieve existing snapshots for the volume
    snapshots = ec2.describe_snapshots(
        Filters=[
            {'Name': 'volume-id', 'Values': [volume_id]},
            {'Name': 'tag:Name', 'Values': [snapshot_name]}
        ]
    )['Snapshots']
    
    # Sort snapshots by StartTime in descending order (newest first)
    snapshots = sorted(snapshots, key=lambda x: x['StartTime'], reverse=True)
    
    # Delete all snapshots except the last two
    for snapshot in snapshots[2:]:
        snapshot_id = snapshot['SnapshotId']
        ec2.delete_snapshot(SnapshotId=snapshot_id)
        print(f"Deleted snapshot: {snapshot_id}")
