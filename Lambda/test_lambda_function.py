# -*- coding: utf-8 -*-
"""Test module of lambda_function module."""
import boto3
import json
import tempfile

from mock import Mock
from moto import mock_ec2
from nose.tools import eq_, ok_
from unittest import TestCase

from src import lambda_function as l


class LambdaFunctionTestCase(TestCase):
    """Test class of lambda_function module."""
    def setUp(self):
        """Set up before test methods."""
        self.event = json.load(open('test_event.json', 'r'))
        self.context = None

        self.result = Mock()

    def tearDown(self):
        """Tear down after test methods."""
        pass

    @mock_ec2
    def test_lambda_handler(self):
        """Test test_lambda_handler(self)."""
        ec2_client = boto3.client('ec2', region_name='ap-northeast-1')
        ec2_client.run_instances(ImageId='ami-1234abcd',
                                 MinCount=1,
                                 MaxCount=1)
        eq_(None, l.lambda_handler(self.event, self.context))

        l.describe_regions = Mock()
        l.describe_regions.side_effect = Exception("test")
        eq_(None, l.lambda_handler(self.event, self.context))

        l.describe_regions.side_effect = l.ClientError(
            {
                'Error': {
                    'Code': 404,
                    'Message': 'NotFound',
                },
            },
            'NotoFound',
        )
        eq_(None, l.lambda_handler(self.event, self.context))

    @mock_ec2
    def test_describe_regions(self):
        """Test describe_regions()."""
        ok_(l.describe_regions())

    @mock_ec2
    def test_fetch_ec2_instances(self):
        """Test fetch_ec2_instances(ec2_client)."""
        ec2_client = boto3.client('ec2', region_name='ap-northeast-1')
        for i in range(1001):
            ec2_client.run_instances(ImageId='test', MinCount=1, MaxCount=1)
        ok_(l.fetch_ec2_instances(ec2_client))

    def test_filter_ec2_instances(self):
        """Test filter_ec2_instances(instances)."""
        instances = [{
            'Tags': [{
                'Key': l.TAG_KEY,
                'Value': l.TAG_VALUE
            }, {
                'Key': 'Name',
                'Value': 'test'
            }],
            'InstanceId':
            'i-000'
        }, {
            'Tags': [{
                'Key': l.TAG_KEY,
                'Value': l.TAG_VALUE + 'hoge'
            }, {
                'Key': 'Name',
                'Value': 'test-instance'
            }],
            'InstanceId':
            'test-id'
        }]
        expected = {'test-id': 'test-instance'}
        eq_(expected, l.filter_ec2_instances(instances))

    def test_create_message(self):
        """Test create_message(region, target_instances)."""
        region = ['ap-northeast-1']
        target_instances = {'i-0123456789': 'test_instance', 'i-0000': ''}
        ok_(l.create_message(region, target_instances))
