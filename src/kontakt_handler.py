from aws_lambda_powertools.event_handler import APIGatewayHttpResolver
import kontakt_controller
from kontakt_controller import KontaktDTO
from handler_util import extractBody, extractId, extractTenant, response, emptyResponse
from http_exception import ValidationException
import email_service 
import json
app = APIGatewayHttpResolver()


def handle(event: dict, context: dict):
    return app.resolve(event, context)


@app.post('/api/kontakt')
def post():
    event = app.current_event
    tenant_id = extractTenant(event)
    body = extractBody(event)
    kontakt = kontakt_controller.create_kontakt(tenant_id, body)
    email_service.send_html_email(tenant_id, kontakt)
    return response(201, kontakt.to_json())


@app.put('/api/kontakt/{id}')
def put():
    event = app.current_event
    tenant_id = extractTenant(event)
    id = extractId(event)
    body = extractBody(event)
    kontakt = kontakt_controller.update_kontakt(tenant_id, id, body)
    return response(200, kontakt.to_json())


@app.get('/api/kontakt/{id}')
def get():
    event = app.current_event
    tenant_id = extractTenant(event)
    id = extractId(event)
    kontakt = kontakt_controller.get_kontakt(tenant_id, id)
    if kontakt:
        return response(200, kontakt.to_json())
    else:
        return emptyResponse(404)


@app.get('/api/kontakt')
def getAll():
    event = app.current_event
    tenant_id = extractTenant(event)
    kontakte = kontakt_controller.get_kontakte(tenant_id)
    return response(200, json.dumps(kontakte, default=KontaktDTO.to_json))


@app.delete('/api/kontakt/{id}')
def delete():
    event = app.current_event
    tenant_id = extractTenant(event)
    id = extractId(event)
    deleted = kontakt_controller.delete_kontakt(tenant_id, id)
    if deleted:
        return emptyResponse(204)
    else:
        return emptyResponse(404)


@app.exception_handler(ValidationException)
def handle_http_exception(exception: ValidationException):
    return response(exception.http_status, exception.to_json())
