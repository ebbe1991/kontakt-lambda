import json
from datetime import datetime
from src import kontakt_handler
from src.kontakt_dto import KontaktDTO
from tests.helper import event, lambda_response, extract_id


def test_create_kontakt_ok(lambda_context, kontakt_table):
    item = {
        'name': "Testuser Helene",
        'betreff': "Gefaellt mir!",
        "nachricht": "Mir gefaellt ihr Internetauftritt!\n Viele Grüße, Helene",
        "zeitpunkt": "2023-01-01T12:30:00",
        "email": "helene@fischer.de",
        "telefonnummer": "0123/123456",
        "zusatzinfos": "Bitte um Rückruf",
        "gelesen": False
    }
    response = kontakt_handler.handle(
        event('/api/kontakt', 'POST', json.dumps(item)), lambda_context)

    id = extract_id(response)

    assert id is not None
    assert response == lambda_response(201, KontaktDTO(
        "Testuser Helene",
        "Gefaellt mir!",
        "Mir gefaellt ihr Internetauftritt!\n Viele Grüße, Helene",
        datetime.fromisoformat("2023-01-01T12:30:00"),
        "0123/123456",
        "Bitte um Rückruf",
        "helene@fischer.de",
        False,
        id).to_json(),  {'Content-Type': 'application/json', "email_sent": "False"})


def test_create_kontakt_invalid_dateformat_bad_request(lambda_context, kontakt_table):
    item = {
        'name': "Testuser Helene",
        'betreff': "Gefällt mir!",
        "nachricht": "Mir gefällt ihr Internetauftritt!\nViele Grüße, Helene",
        "zeitpunkt": "2023-01-01T12x12",
        "email": "helene@fischer.de",
        "telefonnummer": "0123/123456",
        "gelesen": False
    }
    response = kontakt_handler.handle(
        event('/api/kontakt', 'POST', json.dumps(item)), lambda_context)

    assert response == lambda_response(400, json.dumps(
        {'error_text': "Invalid isoformat string: '2023-01-01T12x12'"}))


def test_create_kontakt_missing_field_name_bad_request(lambda_context, kontakt_table):
    item = {
        'betreff': "Super!",
        "nachricht": "Mir gefällt ihr Internetauftritt!\nViele Grüße, Helene",
        "zeitpunkt": "2023-01-01T12:30:00",
        "email": "helene@fischer.de",
        "telefonnummer": "0123/123456",
        "gelesen": False
    }
    response = kontakt_handler.handle(
        event('/api/kontakt', 'POST', json.dumps(item)), lambda_context)

    assert response == lambda_response(
        400, json.dumps({'error_text': "'name' not present."}))


def test_create_kontakt_missing_field_betreff_bad_request(lambda_context, kontakt_table):
    item = {
        'name': "Testuser Helene",
        "nachricht": "Mir gefällt ihr Internetauftritt!\nViele Grüße, Helene",
        "zeitpunkt": "2023-01-01T12:30:00",
        "email": "helene@fischer.de",
        "telefonnummer": "0123/123456",
        "gelesen": False
    }
    response = kontakt_handler.handle(
        event('/api/kontakt', 'POST', json.dumps(item)), lambda_context)

    assert response == lambda_response(
        400, json.dumps({'error_text': "'betreff' not present."}))


def test_create_kontakt_missing_field_nachricht_bad_request(lambda_context, kontakt_table):
    item = {
        'name': "Testuser Helene",
        'betreff': "Gefällt mir!",
        "zeitpunkt": "2023-01-01T12:30:00",
        "email": "helene@fischer.de",
        "telefonnummer": "0123/123456",
        "gelesen": False,
        "typ": "Kontaktformular"
    }
    response = kontakt_handler.handle(
        event('/api/kontakt', 'POST', json.dumps(item)), lambda_context)

    assert response == lambda_response(400, json.dumps(
        {'error_text': "'nachricht' not present."}))


def test_create_kontakt_missing_field_email_bad_request(lambda_context, kontakt_table):
    item = {
        'name': 'Helene',
        'betreff': "Super!",
        "nachricht": "Mir gefällt ihr Internetauftritt!\nViele Grüße, Helene",
        "zeitpunkt": "2023-01-01T12:30:00",
        "telefonnummer": "0123/123456",
        "gelesen": False
    }
    response = kontakt_handler.handle(
        event('/api/kontakt', 'POST', json.dumps(item)), lambda_context)

    assert response == lambda_response(
        400, json.dumps({'error_text': "'email' not present."}))


def test_create_kontakt_invalid_email_bad_request(lambda_context, kontakt_table):
    item = {
        "name": "Helene",
        'betreff': "Super!",
        "nachricht": "Mir gefällt ihr Internetauftritt!\nViele Grüße, Helene",
        "zeitpunkt": "2023-01-01T12:30:00",
        "email": "fischer.de",
        "telefonnummer": "0123/123456",
        "gelesen": False
    }
    response = kontakt_handler.handle(
        event('/api/kontakt', 'POST', json.dumps(item)), lambda_context)

    assert response == lambda_response(
        400, json.dumps({'error_text': "invalid email address 'fischer.de'."}))

def test_create_kontakt_valid_email_with_hyphen(lambda_context, kontakt_table):
    item = {
        "name": "Helene",
        'betreff': "Super!",
        "nachricht": "Mir gefällt ihr Internetauftritt!\nViele Grüße, Helene",
        "zeitpunkt": "2023-01-01T12:30:00",
        "email": "helene-fischer@fischer.de",
        "telefonnummer": "0123/123456",
        "gelesen": False
    }
    response = kontakt_handler.handle(
        event('/api/kontakt', 'POST', json.dumps(item)), lambda_context)
    id = extract_id(response)

    assert id is not None


def test_create_kontakt_without_optional_parameters_ok(lambda_context, kontakt_table):
    item = {
        'name': "Testuser Helene",
        'betreff': "Gefällt mir!",
        "nachricht": "Mir gefällt ihr Internetauftritt!\nViele Grüße, Helene",
        "zeitpunkt": "2023-01-01T12:30:00",
        "email": "helene@fischer.de",
    }
    response = kontakt_handler.handle(
        event('/api/kontakt', 'POST', json.dumps(item)), lambda_context)
    id = extract_id(response)

    assert id is not None
    assert response == lambda_response(201, KontaktDTO(
        "Testuser Helene",
        "Gefällt mir!",
        "Mir gefällt ihr Internetauftritt!\nViele Grüße, Helene",
        datetime.fromisoformat("2023-01-01T12:30:00"),
        None,
        None,
        "helene@fischer.de",
        None,
        id).to_json(), {'Content-Type': 'application/json', "email_sent": "False"})


def test_create_kontakt_without_body_not_ok(lambda_context, kontakt_table):
    response = kontakt_handler.handle(
        event('/api/kontakt', 'POST'), lambda_context)

    assert response == lambda_response(400, json.dumps(
        {'error_text': 'body not present.'}))


def test_create_kontakt_without_tenant_id_not_ok(lambda_context, kontakt_table):
    headers = {
        'Content-Type': 'application/json'
    }
    item = {
        'name': "Testuser Helene",
        'betreff': "Gefällt mir!",
        "nachricht": "Mir gefällt ihr Internetauftritt!\nViele Grüße, Helene",
        "zeitpunkt": "2023-01-01T12:30:00",
        "email": "helene@fischer.de",
    }
    response = kontakt_handler.handle(
        event('/api/kontakt', 'POST', json.dumps(item), None, headers), lambda_context)

    assert response == lambda_response(400, json.dumps(
        {'error_text': 'tenant not present.'}))
