from aws_lambda_powertools.event_handler import APIGatewayHttpResolver
import kontakt_controller
from kontakt_controller import KontaktDTO
from lambda_utils.event_utils import extract_body, extract_id, extract_tenant
from lambda_utils.response_utils import response, empty_response
from lambda_utils.exception import ValidationException
from lambda_utils.env_utils import getenv_as_boolean
import email_service
import json
app = APIGatewayHttpResolver()


def handle(event: dict, context: dict):
    return app.resolve(event, context)


@app.post('/api/kontakt')
def post():
    event = app.current_event
    tenant_id = extract_tenant(event)
    body = extract_body(event)
    kontakt = kontakt_controller.create_kontakt(tenant_id, body)

    headers = None
    if getenv_as_boolean('SEND_EMAIL', False):
        email_sent = email_service.send_html_email(tenant_id, kontakt)
        headers = {"email_sent": [str(email_sent)]}

    return response(201, kontakt.to_json(), headers)


@app.put('/api/kontakt/{id}')
def put():
    event = app.current_event
    tenant_id = extract_tenant(event)
    id = extract_id(event)
    body = extract_body(event)
    kontakt = kontakt_controller.update_kontakt(tenant_id, id, body)
    return response(200, kontakt.to_json())


@app.get('/api/kontakt/{id}')
def get():
    event = app.current_event
    tenant_id = extract_tenant(event)
    id = extract_id(event)
    kontakt = kontakt_controller.get_kontakt(tenant_id, id)
    if kontakt:
        return response(200, kontakt.to_json())
    else:
        return empty_response(404)


@app.get('/api/kontakt')
def getAll():
    event = app.current_event
    tenant_id = extract_tenant(event)
    kontakte = kontakt_controller.get_kontakte(tenant_id)
    return response(200, json.dumps(kontakte, default=KontaktDTO.to_json))


@app.delete('/api/kontakt/{id}')
def delete():
    event = app.current_event
    tenant_id = extract_tenant(event)
    id = extract_id(event)
    deleted = kontakt_controller.delete_kontakt(tenant_id, id)
    if deleted:
        return empty_response(204)
    else:
        return empty_response(404)


@app.exception_handler(ValidationException)
def handle_http_exception(exception: ValidationException):
    return response(exception.http_status, exception.to_json())
