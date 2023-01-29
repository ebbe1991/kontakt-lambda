import json
from src import kontakt_controller

from src import kontakt_handler
from tests.helper import event, lambda_response, DEFAULT_TENANT_ID


def test_delete_kontakt_ok(lambda_context, dynamodb_table):
    item = {
        'name': "Testuser Helene",
        'betreff': "Gefaellt mir!",
        "nachricht": "Mir gefaellt ihr Internetauftritt!\nViele Grüße, Helene",
        "zeitpunkt": "2023-01-01T12:30:00",
        "email": "helene@fischer.de"
    }
    createdKontakt = kontakt_controller.create_kontakt(
        DEFAULT_TENANT_ID, item)

    kontakte = kontakt_controller.get_kontakte(DEFAULT_TENANT_ID)
    assert len(kontakte) == 1

    pathParameters = {
        "id": createdKontakt.id
    }
    response = kontakt_handler.handle(event(
        '/api/kontakt/{id}', 'DELETE', None, pathParameters), lambda_context)

    assert response == lambda_response(204)
    kontakte = kontakt_controller.get_kontakte(DEFAULT_TENANT_ID)
    assert len(kontakte) == 0


def test_delete_kontakt_not_ok(lambda_context, dynamodb_table):
    pathParameters = {
        "id": "abc123"
    }
    response = kontakt_handler.handle(event(
        '/api/kontakt/{id}', 'DELETE', None, pathParameters), lambda_context)

    assert response == lambda_response(404)


def test_delete_kontakt_without_tenant_id_not_ok(lambda_context, dynamodb_table):
    pathParameters = {
        "id": "abc123"
    }
    headers = {
        'Content-Type': 'application/json'
    }
    response = kontakt_handler.handle(event(
        '/api/kontakt/{id}', 'DELETE', None, pathParameters, headers), lambda_context)

    assert response == lambda_response(400, json.dumps(
        {'error_text': 'tenant not present.'}))
