# ReencryptVolumes

This script creates new EBS volumes in the given region encrypted by the given KMS key. A snapshot is created from each volume, and encrypted copies are created with the given KMS key. New EBS volumes are then restored from the snapshot copies.

For more info - Changing the Encryption State of Your Data (Encrypt a Snapshot Under a New CMK):
https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/EBSEncryption.html#EBSEncryption_considerations
