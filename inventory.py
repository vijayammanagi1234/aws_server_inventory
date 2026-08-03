import boto3
import pandas as pd

ec2 = boto3.client("ec2", region_name="us-east-1")

servers = []

response = ec2.describe_instances()

for reservation in response["Reservations"]:
    for instance in reservation["Instances"]:

        name = ""

        if "Tags" in instance:
            for tag in instance["Tags"]:
                if tag["Key"] == "Name":
                    name = tag["Value"]

        servers.append({

            "Name": name,
            "Instance ID": instance["InstanceId"],
            "State": instance["State"]["Name"],
            "Instance Type": instance["InstanceType"],
            "Private IP": instance.get("PrivateIpAddress",""),
            "Public IP": instance.get("PublicIpAddress",""),
            "Availability Zone": instance["Placement"]["AvailabilityZone"],
            "VPC": instance.get("VpcId",""),
            "Subnet": instance.get("SubnetId",""),
            "AMI": instance["ImageId"],
            "Launch Time": str(instance["LaunchTime"])

        })

df = pd.DataFrame(servers)

df.to_csv("EC2_Inventory.csv", index=False)

print(df)
