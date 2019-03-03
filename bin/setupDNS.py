import os
import json
import boto3
from time import sleep, time, ctime

client = boto3.client('route53')
elb_client = boto3.client('elb')

ZONE_ID = os.environ.get('ZIGDATA_HOSTED_ZONE')


def add_dns_record(source, target, record_type='cname', ttl=30, elb_zone=None):
    change_batch = {
        'Action': 'UPSERT',
        'ResourceRecordSet': {
            'Name': source,
            'Type': record_type.upper()
        }
    }

    if record_type == 'a':
        if elb_zone is None:
            raise Exception("Must specify zone ID for ELB")
        record_set = {
            "AliasTarget": {
                "HostedZoneId": elb_zone,
                "DNSName": target,
                "EvaluateTargetHealth": False
            }
        }
        change_batch['ResourceRecordSet'].update(record_set)
    elif record_type == 'cname':
        record_set = [{'Value': target}]
        change_batch['ResourceRecordSet']['ResourceRecords'] = record_set
        change_batch['ResourceRecordSet']['TTL'] = ttl

    else:
        raise Exception(f"Invalid record type: {record_type}")

    try:
        comment = f'add {source} -> {target}'
        print(comment)
        print(json.dumps(change_batch, indent=4))
        response = client.change_resource_record_sets(
            HostedZoneId=ZONE_ID,
            ChangeBatch={
                'Comment': comment,
                'Changes': [change_batch]
            })
    except Exception as e:
        print(e)


def get_elb(field='DNSName'):
    try:
        dns = elb_client.describe_load_balancers()['LoadBalancerDescriptions'][0][field]
    except:
        return None
    return dns


elb = get_elb()
while elb is None:
    elb = get_elb()
    if elb is None:
        print(f'{ctime(time())} ELB is not ready just yet, waiting..')
        sleep(20)

print('Creating DNS records')
subs = ['lab']
add_dns_record('zigdata.org', elb, record_type='a', elb_zone=get_elb('CanonicalHostedZoneNameID'))