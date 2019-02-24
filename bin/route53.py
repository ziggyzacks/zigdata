import boto3

client = boto3.client('route53')
elb_client = boto3.client('elb')

ZONE_ID = "Z1AN2A39DS5PBL"


def add_cname_record(source, target):
    try:
        comment = f'add {source} -> {target}'
        print(comment)
        response = client.change_resource_record_sets(
            HostedZoneId=ZONE_ID,
            ChangeBatch={
                'Comment': comment,
                'Changes': [
                    {
                        'Action': 'UPSERT',
                        'ResourceRecordSet': {
                            'Name': source,
                            'Type': 'CNAME',
                            'TTL': 300,
                            'ResourceRecords': [{'Value': target}]
                        }
                    }]
            })
    except Exception as e:
        print(e)


def get_elb_dns():
    dns = elb_client.describe_load_balancers()['LoadBalancerDescriptions'][0]['DNSName']
    return dns

elb = get_elb_dns()
subs = ['elb', 'app', 'lab', 'dev']
for sub in subs:
    add_cname_record(f'{sub}.zigdata.org', elb)
