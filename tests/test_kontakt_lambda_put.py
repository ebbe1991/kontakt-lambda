import json
from datetime import datetime
from src import kontakt_controller

from src import kontakt_handler
from src.kontakt_dto import KontaktDTO
from tests.helper import event, lambda_response, DEFAULT_TENANT_ID


def test_update_kontakt_ok(lambda_context, dynamodb_table):
    item = {
        'name': "Testuser Helene",
        'betreff': "Gefällt mir!",
        "nachricht": "Mir gefällt ihr Internetauftritt!\nViele Grüße, Helene",
        "zeitpunkt": "2023-01-01T12:30:00",
        "email": "helene@fischer.de",
    }
    createdKontakt = kontakt_controller.create_kontakt(
        DEFAULT_TENANT_ID, item
    )

    pathParameters = {
        "id": createdKontakt.id
    }
    itemUpdate = {
        'name': "Testuser Helene",
        'betreff': "Gefällt mir!",
        "nachricht": "Mir gefällt ihr Internetauftritt!\nViele Grüße, Helene",
        "zeitpunkt": "2023-01-01T12:30:00",
        "email": "helene@fischer.de",
        "gelesen": True
    }
    response = kontakt_handler.handle(event(
        '/api/kontakt/{id}', 'PUT', json.dumps(itemUpdate), pathParameters), lambda_context)

    assert response == lambda_response(200, KontaktDTO(
        "Testuser Helene",
        "Gefällt mir!",
        "Mir gefällt ihr Internetauftritt!\nViele Grüße, Helene",
        datetime.fromisoformat("2023-01-01T12:30:00"),
        None,
        "helene@fischer.de",
        True,
        None,
        createdKontakt.id).to_json())


def test_update_kontakt_required_field_to_null_not_ok(lambda_context, dynamodb_table):
    item = {
        'name': "Testuser Helene",
        'betreff': "Gefällt mir!",
        "nachricht": "Mir gefällt ihr Internetauftritt!\nViele Grüße, Helene",
        "zeitpunkt": "2023-01-01T12:30:00",
        "email": "helene@fischer.de",
    }
    createdKontakt = kontakt_controller.create_kontakt(
        DEFAULT_TENANT_ID, item
    )

    pathParameters = {
        "id": createdKontakt.id
    }
    itemUpdate = {
        'name': None,
        'betreff': "Gefällt mir!",
        "nachricht": "Mir gefällt ihr Internetauftritt!\nViele Grüße, Helene",
        "zeitpunkt": "2023-01-01T12:30:00",
        "email": "helene@fischer.de",
    }
    response = kontakt_handler.handle(event(
        '/api/kontakt/{id}', 'PUT', json.dumps(itemUpdate), pathParameters), lambda_context)

    assert response == lambda_response(
        400, json.dumps({'error_text': "'name' is missing."}))


def test_update_kontakt_with_unknown_id_not_ok(lambda_context, dynamodb_table):
    pathParameters = {
        "id": 'unknown'
    }
    itemUpdate = {
        'name': "Testuser Helene",
        'betreff': "Gefällt mir!",
        "nachricht": "Mir gefällt ihr Internetauftritt!\nViele Grüße, Helene",
        "zeitpunkt": "2023-01-01T12:30:00",
        "email": "helene@fischer.de",
    }
    response = kontakt_handler.handle(event(
        '/api/kontakt/{id}', 'PUT', json.dumps(itemUpdate), pathParameters), lambda_context)

    assert response == lambda_response(
        400, json.dumps({'error_text': "unknown id 'unknown' (tenant='mytenant1') to update."}))


def test_update_kontakt_set_null_value(lambda_context, dynamodb_table):
    item = {
        'name': "Testuser Helene",
        'betreff': "Gefällt mir!",
        "nachricht": "Mir gefällt ihr Internetauftritt!\nViele Grüße, Helene",
        "zeitpunkt": "2023-01-01T12:30:00",
        "email": "helene@fischer.de",
        "telefonnummer": "1234/1234"
    }
    createdKontakt = kontakt_controller.create_kontakt(
        DEFAULT_TENANT_ID, item)

    pathParameters = {
        "id": createdKontakt.id
    }

    itemUpdate = {
        'name': "Testuser Helene",
        'betreff': "Gefällt mir!",
        "nachricht": "Mir gefällt ihr Internetauftritt!\nViele Grüße, Helene",
        "zeitpunkt": "2023-01-01T12:30:00",
        "email": "helene@fischer.de"
    }
    response = kontakt_handler.handle(event(
        '/api/kontakt/{id}', 'PUT', json.dumps(itemUpdate), pathParameters), lambda_context)

    assert response == lambda_response(200, KontaktDTO(
        "Testuser Helene",
        "Gefällt mir!",
        "Mir gefällt ihr Internetauftritt!\nViele Grüße, Helene",
        datetime.fromisoformat("2023-01-01T12:30:00"),
        None,
        "helene@fischer.de",
        None,
        None,
        createdKontakt.id).to_json())


def test_update_kontakt_without_body_not_ok(lambda_context, dynamodb_table):
    item = {
        'name': "Testuser Helene",
        'betreff': "Gefällt mir!",
        "nachricht": "Mir gefällt ihr Internetauftritt!\nViele Grüße, Helene",
        "zeitpunkt": "2023-01-01T12:30:00",
        "email": "helene@fischer.de",
        "telefonnummer": "1234/1234"
    }
    createdKontakt = kontakt_controller.create_kontakt(
        DEFAULT_TENANT_ID, item)

    pathParameters = {
        "id": createdKontakt.id
    }

    response = kontakt_handler.handle(
        event('/api/kontakt/{id}', 'PUT', None, pathParameters), lambda_context)

    assert response == lambda_response(400, json.dumps(
        {'error_text': 'body not present.'}))


def test_update_kontakt_without_id_not_ok(lambda_context, dynamodb_table):
    item = {
        'name': "Testuser Helene",
        'betreff': "Gefällt mir!",
        "nachricht": "Mir gefällt ihr Internetauftritt!\nViele Grüße, Helene",
        "zeitpunkt": "2023-01-01T12:30:00",
        "email": "helene@fischer.de",
        "telefonnummer": "1234/1234"
    }
    kontakt_controller.create_kontakt(
        DEFAULT_TENANT_ID, item)

    pathParameters = {
        "id": ''
    }

    response = kontakt_handler.handle(
        event('/api/kontakt/{id}', 'PUT', json.dumps(item), pathParameters), lambda_context)

    assert response == lambda_response(400, json.dumps(
        {'error_text': 'id not present.'}))


def test_update_kontakt_without_tenant_id_not_ok(lambda_context, dynamodb_table):
    headers = {
        'Content-Type': 'application/json'
    }
    item = {
        'name': "Testuser Helene",
        'betreff': "Gefällt mir!",
        "nachricht": "Mir gefällt ihr Internetauftritt!\nViele Grüße, Helene",
        "zeitpunkt": "2023-01-01T12:30:00",
        "email": "helene@fischer.de",
        "telefonnummer": "1234/1234"
    }
    createdKontakt = kontakt_controller.create_kontakt(
        DEFAULT_TENANT_ID, item)

    pathParameters = {
        "id": createdKontakt.id
    }
    itemUpdate = {
        'name': "Testuser Helene",
        'betreff': "Gefällt mir!",
        "nachricht": "Mir gefällt ihr Internetauftritt!\nViele Grüße, Helene",
        "zeitpunkt": "2023-01-01T12:30:00",
        "email": "helene@fischer.de",
        "telefonnummer": "1234/1234",
        "gelesen": True
    }
    response = kontakt_handler.handle(event(
        '/api/kontakt/{id}', 'PUT', json.dumps(itemUpdate), pathParameters, headers), lambda_context)

    assert response == lambda_response(400, json.dumps(
        {'error_text': 'tenant not present.'}))
