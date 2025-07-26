import os

import boto3
import pytest
from moto import mock_aws

os.environ['KONTAKT_TABLE_NAME'] = 'KONTAKT_TABLE'
os.environ['EMAIL_CONFIG_TABLE_NAME'] = 'EMAIL_CONFIG_TABLE'
os.environ['AWS_DEFAULT_REGION'] = 'eu-central-1'


@pytest.fixture(name='lambda_context', scope="function")
def lambda_context():
    os.environ['SEND_EMAIL'] = '0'
    os.environ['TTL_FEATURE_ACTIVE'] = '0'
    return None


@pytest.fixture(scope='session')
def ses():
    with mock_aws():
        os.environ['AWS_SECURITY_TOKEN'] = 'test'
        ses = boto3.client('ses')
        ses.verify_email_identity(EmailAddress='noreply@mytenant1.com')
        yield ses


@pytest.fixture(scope='session')
def dynamodb():
    with mock_aws():
        yield boto3.resource('dynamodb')


@pytest.fixture(scope='function')
def kontakt_table(dynamodb):
    table_name = os.getenv('KONTAKT_TABLE_NAME')
    table = dynamodb.create_table(
        TableName=table_name,
        BillingMode='PAY_PER_REQUEST',
        KeySchema=[
            {
                'AttributeName': 'tenant-id',
                'KeyType': 'HASH'
            },
            {
                'AttributeName': 'id',
                'KeyType': 'RANGE'
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'tenant-id',
                'AttributeType': 'S'
            },
            {
                'AttributeName': 'id',
                'AttributeType': 'S'
            }
        ]
    )
    table.wait_until_exists()
    yield table
    table.delete()


@pytest.fixture(scope='function')
def email_config_table(dynamodb, ses):
    table_name = os.getenv('EMAIL_CONFIG_TABLE_NAME')
    table = dynamodb.create_table(
        TableName=table_name,
        BillingMode='PAY_PER_REQUEST',
        KeySchema=[
            {
                'AttributeName': 'tenant-id',
                'KeyType': 'HASH'
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'tenant-id',
                'AttributeType': 'S'
            }
        ]
    )
    table.wait_until_exists()
    yield table
    table.delete()
