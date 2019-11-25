# -*- coding: utf-8 -*-
"""stop ec2 instances."""
from botocore.exceptions import ClientError

import boto3
import json
import logging
import os

LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.DEBUG)

AWS_REGION = 'ap-northeast-1'

TAG_KEY = 'Auto-stop'
TAG_VALUE = 'No'


def lambda_handler(event, context):
    """Handle lambda events and return a mixed value.
    This function is required. Don't remove this.
    """
    try:
        LOGGER.info({'event': event, 'context': context})

        all_regions = describe_regions()
        for region in all_regions:
            LOGGER.info(region)
            ec2_client = boto3.client('ec2', region_name=region)
            ec2_instances = fetch_ec2_instances(ec2_client)
            target_instances = filter_ec2_instances(ec2_instances)

            if len(target_instances) > 0:
                ec2_client.stop_instances(
                    InstanceIds=list(target_instances.keys()))
                LOGGER.info(create_message(region, target_instances))

    except ClientError as e:
        LOGGER.error('ClientError happened. Process False!')
        LOGGER.error('Boto3 Error.')
        LOGGER.error(e)

    except Exception as e:
        LOGGER.error('Error happened. Process False!')
        LOGGER.error(e)

    return


def describe_regions():
    """Describe regions for EC2."""
    ec2 = boto3.client('ec2')
    return list(
        map(lambda x: x['RegionName'],
            ec2.describe_regions()['Regions']))


def fetch_ec2_instances(ec2_client):
    """Fetch EC2 instances in all regions."""
    ec2_instances = []

    resp = ec2_client.describe_instances()
    if len(resp['Reservations']) > 0:
        ec2_instances.extend(
            sum([
                reservation['Instances']
                for reservation in resp['Reservations']
            ], []))
    while 'NextToken' in resp:
        resp = ec2_client.describe_instances(NextToken=resp['NextToken'])
        ec2_instances.extend(
            sum([
                reservation['Instances']
                for reservation in resp['Reservations']
            ], []))

    return ec2_instances


def filter_ec2_instances(instances):
    """Filter instances by tag:Auto-stop = No"""
    instances_data = {}
    for instance in instances:
        auto_stop = True
        Name = ''
        if 'Tags' in instance:
            for tag in instance['Tags']:
                if tag['Key'] == TAG_KEY and tag['Value'] == TAG_VALUE:
                    auto_stop = False

                if tag['Key'] == 'Name':
                    Name = tag['Value']

        if auto_stop is True:
            instances_data[instance['InstanceId']] = Name

    LOGGER.info(instances_data)
    return instances_data


def create_message(region, target_instances):
    """Create message."""
    message = 'Region: %s\n' % (region)
    for instance_id, instance_name in target_instances.items():
        message += '- %s(%s)\n' % (instance_name, instance_id)

    message += '---------------------------------------\n'

    return message
