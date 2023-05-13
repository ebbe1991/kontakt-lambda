import json
from src import kontakt_controller
from src import kontakt_handler
from tests.helper import event, lambda_response, DEFAULT_TENANT_ID


def test_get_kontakt_not_found(lambda_context, kontakt_table):
    pathParameters = {
        "id": "unknown_id"
    }
    response = kontakt_handler.handle(event(
        '/api/kontakt/{id}', 'GET', None, pathParameters), lambda_context)

    assert response == lambda_response(404)


def test_get_kontakt_ok(lambda_context, kontakt_table):
    item = {
        'name': "Testuser Helene",
        'betreff': "Gefaellt mir!",
        "nachricht": "Mir gefaellt ihr Internetauftritt!\nViele Grüße, Helene",
        "zeitpunkt": "2023-01-01T12:30:00",
        "email": "helene@fischer.de"
    }
    createdKontakt = kontakt_controller.create_kontakt(
        DEFAULT_TENANT_ID, item)

    pathParameters = {
        "id": createdKontakt.id
    }
    response = kontakt_handler.handle(event(
        '/api/kontakt/{id}', 'GET', None, pathParameters), lambda_context)

    assert response == lambda_response(200, createdKontakt.to_json())

def test_get_kontakt_with_zusatzinfos_ok(lambda_context, kontakt_table):
    item = {
        'name': "Testuser Helene",
        'betreff': "Gefaellt mir!",
        "nachricht": "Mir gefaellt ihr Internetauftritt!\nViele Grüße, Helene",
        "zeitpunkt": "2023-01-01T12:30:00",
        "zusatzinfos": "Melde dich!",
        "email": "helene@fischer.de"
    }
    createdKontakt = kontakt_controller.create_kontakt(
        DEFAULT_TENANT_ID, item)

    pathParameters = {
        "id": createdKontakt.id
    }
    response = kontakt_handler.handle(event(
        '/api/kontakt/{id}', 'GET', None, pathParameters), lambda_context)

    assert response == lambda_response(200, createdKontakt.to_json())

def test_get_kontakt_without_tenant_id_not_ok(lambda_context, kontakt_table):
    headers = {
        'Content-Type': 'application/json'
    }
    item = {
        'name': "Testuser Helene",
        'betreff': "Gefaellt mir!",
        "nachricht": "Mir gefaellt ihr Internetauftritt!\nViele Grüße, Helene",
        "zeitpunkt": "2023-01-01T12:30:00",
        "email": "helene@fischer.de"
    }
    createdKontakt = kontakt_controller.create_kontakt(
        DEFAULT_TENANT_ID, item)

    pathParameters = {
        "id": createdKontakt.id
    }
    response = kontakt_handler.handle(event(
        '/api/kontakt/{id}', 'GET', None, pathParameters, headers), lambda_context)

    assert response == lambda_response(400, json.dumps(
        {'error_text': 'tenant not present.'}))
