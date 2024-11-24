import boto3

def lambda_handler(event, context):
    ec2 = boto3.client('ec2')
    
    try:
        # Fetch available volumes
        volumes = ec2.describe_volumes(Filters=[{'Name': 'status', 'Values': ['available']}])
        unused_volumes = [vol['VolumeId'] for vol in volumes['Volumes']]
        print("Unused volumes:", unused_volumes)
        
        deleted_volumes = []
        
        # Delete each unused volume
        for volume_id in unused_volumes:
            try:
                ec2.delete_volume(VolumeId=volume_id)
                deleted_volumes.append(volume_id)
            except Exception as e:
                print(f"Failed to delete volume {volume_id}: {str(e)}")
        
        return {
            "deleted_volumes": deleted_volumes
        }
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return {
            "error": str(e),
            "deleted_volumes": []
        }
