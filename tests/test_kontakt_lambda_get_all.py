import json
from src import kontakt_controller
from src import kontakt_handler
from tests.helper import event, extract_body, extract_status_code, lambda_response, DEFAULT_TENANT_ID


def test_get_kontakte_ok(lambda_context, kontakt_table):
    item1 = {
        'name': "Testuser Helene",
        'betreff': "Gefaellt mir!",
        "nachricht": "Mir gefaellt ihr Internetauftritt!\nViele Grüße, Helene",
        "zeitpunkt": "2023-01-01T12:30:00",
        "zusatzinfos": "Bitte dringend melden",
        "email": "helene@fischer.de"
    }
    item2 = {
        'name': "Testuser Uschi",
        'betreff': "Bitte melde Dich!",
        "nachricht": "...",
        "zeitpunkt": "2023-01-01T12:30:00",
        "email": "uschi@fischer.de"
    }
    kontakt_controller.create_kontakt(DEFAULT_TENANT_ID, item1)
    kontakt_controller.create_kontakt(DEFAULT_TENANT_ID, item2)

    response = kontakt_handler.handle(
        event('/api/kontakt', 'GET'), lambda_context)
    body = extract_body(response)

    assert extract_status_code(response) == 200
    assert len(body) == 2



def test_get_kontakte__one_element_ok(lambda_context, kontakt_table):
    item = {
        'name': "Testuser Helene",
        'betreff': "Gefaellt mir!",
        "nachricht": "Mir gefaellt ihr Internetauftritt!\nViele Grüße, Helene",
        "zeitpunkt": "2023-01-01T12:30:00",
        "email": "helene@fischer.de"
    }
    created_kontakt = kontakt_controller.create_kontakt(DEFAULT_TENANT_ID, item)

    response = kontakt_handler.handle(
        event('/api/kontakt', 'GET'), lambda_context)
    body = extract_body(response)

    assert extract_status_code(response) == 200
    assert len(body) == 1
    assert json.dumps(body[0]) == created_kontakt.to_json()


def test_get_kontakte_empty_ok(lambda_context, kontakt_table):
    response = kontakt_handler.handle(
        event('/api/kontakt', 'GET'), lambda_context)
    body = extract_body(response)

    assert extract_status_code(response) == 200
    assert len(body) == 0


def test_get_kontakte_without_tenant_id_not_ok(lambda_context, kontakt_table):
    headers = {
        'Content-Type': 'application/json'
    }
    response = kontakt_handler.handle(
        event('/api/kontakt', 'GET', None, None, headers), lambda_context)

    assert response == lambda_response(400, json.dumps(
        {'error_text': 'tenant not present.'}))
