# This script creates new EBS volumes in the given region encrypted by the given KMS key. A snapshot is
# created from each volume, and encrypted copies are created with the given KMS key. New EBS volumes
# are then restored from the snapshot copies.
#
# For more info - Changing the Encryption State of Your Data (Encrypt a Snapshot Under a New CMK):
# https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/EBSEncryption.html#EBSEncryption_considerations
#
# 2018 Devin S.

#!/usr/bin/env python3

import boto3
import argparse

encrypted_vols = []
encrypted_snaps = []
new_snaps = []

parser = argparse.ArgumentParser()
parser.add_argument("-r", "--region", dest = "region", help = "The region of volumes that should be re-encrypted")
parser.add_argument("-k", "--key-id", dest = "key", help = "The KMS key ID of the key used to encrypt the new volumes")
args = parser.parse_args()
if not args.region:
    if args.key:
        parser.error("A region is required")
    else:
        parser.error("A region and KMS key ID are required")
elif not args.key:
    parser.error("A KMS key ID is required")

ec2 = boto3.client('ec2', region_name = args.region)

# Get encrypted volumes
vols = ec2.describe_volumes()

if len(vols['Volumes']) > 0:
    for vol in vols['Volumes']:
        if vol['Encrypted'] == True:
            encrypted_vols.append(vol['VolumeId'])
        else:
            continue
else:
    print("There are no encrypted volumes in this region, please try a different region.")

# Create snapshots of encrypted volumes
for vol in encrypted_vols:
    encrypted_snaps.append(ec2.create_snapshot(
        VolumeId = vol
    ))

# Create snapshot copies with new KMS key
for snap in encrypted_snaps:
    new_snaps.append(ec2.copy_snapshot(
        Description = ("Snapshot copy encrypted with KMS key ID " + args.key + " from snapshot " + snap['SnapshotId']),
        Encrypted = True,
        KmsKeyId = args.key,
        SourceRegion = args.region,
        SourceSnapshotId = snap['SnapshotId']
    ))

print("\nEncrypted volumes:")
for vol in encrypted_vols:
    print(vol)
print("\nSnapshots created from encrypted volumes:")
for snap in encrypted_snaps:
    print(snap['SnapshotId'])
print("\nSnapshot copies encrypted with KMS key " + args.key + ":")
for snap in new_snaps:
    print(snap['SnapshotId'])
