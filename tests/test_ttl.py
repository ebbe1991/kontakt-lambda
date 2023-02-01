import json
import os
from src import dynamo_db_service
from src import kontakt_handler
from tests.helper import event, extract_id, DEFAULT_TENANT_ID


def test_ttl_in_dynamobo_active(lambda_context, kontakt_table):
    os.environ['TTL_FEATURE_ACTIVE'] = '1'
    item = {
        'name': "Testuser Helene",
        'betreff': "Gefällt mir!",
        "nachricht": "Mir gefällt ihr Internetauftritt!\nViele Grüße, Helene",
        "zeitpunkt": "2023-01-01T12:30:00",
        "email": "helene@fischer.de",
        "telefonnummer": "1234/1234"
    }
    response = kontakt_handler.handle(
        event('/api/kontakt', 'POST', json.dumps(item)), lambda_context)
    id = extract_id(response)
    item = dynamo_db_service.get_kontakt(DEFAULT_TENANT_ID, id)

    assert item['ttl'] == 1681216200


def test_ttl_in_dynamobo_inactive(lambda_context, kontakt_table):
    os.environ['TTL_FEATURE_ACTIVE'] = '0'
    item = {
        'name': "Testuser Helene",
        'betreff': "Gefällt mir!",
        "nachricht": "Mir gefällt ihr Internetauftritt!\nViele Grüße, Helene",
        "zeitpunkt": "2023-01-01T12:30:00",
        "email": "helene@fischer.de",
        "telefonnummer": "1234/1234"
    }
    response = kontakt_handler.handle(
        event('/api/kontakt', 'POST', json.dumps(item)), lambda_context)
    id = extract_id(response)
    item = dynamo_db_service.get_kontakt(DEFAULT_TENANT_ID, id)

    assert item['ttl'] is None
