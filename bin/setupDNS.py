import os
import json
import argparse
import boto3
from time import sleep, time, ctime

client = boto3.client('route53')
elb_client = boto3.client('elb')


def _dns_change_template(source, record_type):
    return {
        'Action': 'UPSERT',
        'ResourceRecordSet': {
            'Name': source,
            'Type': record_type.upper()
        }
    }


def _alias_record(elb_zone, target):
    return {
        "AliasTarget": {
            "HostedZoneId": elb_zone,
            "DNSName": target,
            "EvaluateTargetHealth": False
        }
    }


def add_dns_record(source, target, record_type='cname', ttl=30, elb_zone=None, zone_id=None):
    if target is None:
        raise Exception("must provide target")

    if zone_id is None:
        print('using envvar HOSTED_ZONE_ID')
        zone_id = os.environ.get('HOSTED_ZONE_ID')
        if zone_id is None:
            raise Exception("No zone id was passed and HOSTED_HOST_ID environment variable not set")

    change_batch = _dns_change_template(source, record_type)
    if record_type == 'a':
        if elb_zone is None:
            raise Exception("Must specify zone ID for ELB")
        record_set = _alias_record(elb_zone, target)
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
            HostedZoneId=zone_id,
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


def wait_for_elb():
    elb = get_elb()
    while elb is None:
        elb = get_elb()
        if elb is None:
            print(f'{ctime(time())} ELB is not ready just yet, waiting..')
            sleep(20)
    return elb


def create_records(elb):
    print('Creating DNS records')
    elb_zone = get_elb('CanonicalHostedZoneNameID')
    add_dns_record('zigdata.org', elb, record_type='a', elb_zone=elb_zone)
    add_dns_record('www.zigdata.org', elb, record_type='a', elb_zone=elb_zone)


if __name__ == "__main__":
    # Instantiate the parser
    parser = argparse.ArgumentParser(description='Creates Route53 DNS records assuming 1 ELB in hosted zone')
    parser.add_argument('--zone', type=str,
                        help='AWS Route53 Zone ID, defaults to HOSTED_ZONE_ID environment variable')
    args = parser.parse_args()
    elb = wait_for_elb()
    create_records(elb)
