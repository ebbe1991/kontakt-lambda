from aws_lambda_powertools.event_handler import APIGatewayHttpResolver
import kontakt_controller
import email_config_controller
from kontakt_controller import KontaktDTO
from lambda_utils.event_utils import extract_body, extract_tenant
from lambda_utils.response_utils import response, empty_response, to_json_array
from lambda_utils.exception import ValidationException
from lambda_utils.env_utils import getenv_as_boolean
import os
import email_service
app = APIGatewayHttpResolver()


def handle(event: dict, context: dict):
    return app.resolve(event, context)


@app.post('/api/kontakt')
def post():
    event = app.current_event
    tenant_id = extract_tenant(event)
    body = extract_body(event)
    send_email = getenv_as_boolean('SEND_EMAIL', False)

    email_config = email_config_controller.get_email_config(
        tenant_id) if send_email else None
    kontakt = kontakt_controller.create_kontakt(tenant_id, body)

    if send_email:
        email_service.send_html_email(tenant_id, kontakt, email_config)

    return response(201, kontakt.to_json(), {"email_sent": [str(send_email)]})


@app.put('/api/kontakt/<id>')
def put(id):
    event = app.current_event
    tenant_id = extract_tenant(event)
    body = extract_body(event)
    kontakt = kontakt_controller.update_kontakt(tenant_id, id, body)
    return response(200, kontakt.to_json())


@app.get('/api/kontakt/<id>')
def get(id):
    event = app.current_event
    tenant_id = extract_tenant(event)
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
    body = to_json_array(list(map(KontaktDTO.to_json, kontakte)))
    return response(200, body)


@app.delete('/api/kontakt/<id>')
def delete(id):
    event = app.current_event
    tenant_id = extract_tenant(event)
    deleted = kontakt_controller.delete_kontakt(tenant_id, id)
    if deleted:
        return empty_response(204)
    else:
        return empty_response(404)


@app.exception_handler(ValidationException)
def handle_http_exception(exception: ValidationException):
    return response(exception.http_status, exception.to_json())
