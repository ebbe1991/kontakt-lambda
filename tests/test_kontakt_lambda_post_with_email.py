import json
import os
from src import kontakt_handler, email_config_controller, kontakt_controller
from tests.helper import event, extract_headers, extract_status_code, lambda_response, DEFAULT_TENANT_ID


def test_create_kontakt_send_email(lambda_context, kontakt_table, email_config_table):
    os.environ['SEND_EMAIL'] = 'True'
    item = {
        'name': "Testuser Helene",
        'betreff': "Gefaellt mir!",
        "nachricht": "Mir gefaellt ihr Internetauftritt!\n Viele Grüße, Helene",
        "zeitpunkt": "2023-01-01T12:30:00",
        "email": "helene@fischer.de",
        "telefonnummer": "0123/123456",
        "gelesen": False
    }
    email_config_item = {
        'email-from': "noreply@mytenant1.com",
        'email-to': "info@mytenant1.com"
    }
    email_config_controller.create_email_config(
        DEFAULT_TENANT_ID, email_config_item)

    response = kontakt_handler.handle(
        event('/api/kontakt', 'POST', json.dumps(item)), lambda_context)

    assert extract_status_code(response) == 201
    headers = extract_headers(response)
    assert headers.get('email_sent') == 'True'
    assert len(kontakt_controller.get_kontakte(DEFAULT_TENANT_ID)) == 1


def test_create_kontakt_send_no_email(lambda_context, kontakt_table, email_config_table):
    os.environ['SEND_EMAIL'] = 'False'
    item = {
        'name': "Testuser Helene",
        'betreff': "Gefaellt mir!",
        "nachricht": "Mir gefaellt ihr Internetauftritt!\n Viele Grüße, Helene",
        "zeitpunkt": "2023-01-01T12:30:00",
        "email": "helene@fischer.de",
        "telefonnummer": "0123/123456",
        "gelesen": False
    }
    email_config_item = {
        'email-from': "noreply@mytenant1.com",
        'email-to': "info@mytenant1.com"
    }
    email_config_controller.create_email_config(
        DEFAULT_TENANT_ID, email_config_item)

    response = kontakt_handler.handle(
        event('/api/kontakt', 'POST', json.dumps(item)), lambda_context)

    assert extract_status_code(response) == 201
    headers = extract_headers(response)
    assert headers.get('email_sent') == 'False'
    assert len(kontakt_controller.get_kontakte(DEFAULT_TENANT_ID)) == 1


def test_create_kontakt_send_email_without_config_exception(lambda_context, kontakt_table, email_config_table):
    os.environ['SEND_EMAIL'] = 'True'
    item = {
        'name': "Testuser Helene",
        'betreff': "Gefaellt mir!",
        "nachricht": "Mir gefaellt ihr Internetauftritt!\n Viele Grüße, Helene",
        "zeitpunkt": "2023-01-01T12:30:00",
        "email": "helene@fischer.de",
        "telefonnummer": "0123/123456",
        "gelesen": False
    }

    response = kontakt_handler.handle(
        event('/api/kontakt', 'POST', json.dumps(item)), lambda_context)

    assert response == lambda_response(400, json.dumps(
        {'error_text': 'email config not present (tenant-id=mytenant1).'}))
    assert len(kontakt_controller.get_kontakte(DEFAULT_TENANT_ID)) == 0