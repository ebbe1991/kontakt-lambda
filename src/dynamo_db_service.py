import os
import boto3
from kontakt_dto import KontaktDTO
from boto3.dynamodb.conditions import Key


def get_kontakte_table():
    dynamodb = boto3.resource('dynamodb')
    table_name = os.getenv('KONTAKT_TABLE_NAME')
    return dynamodb.Table(table_name)


def put_kontakt(tenant_id: str, kontakt: KontaktDTO):
    table = get_kontakte_table()
    table.put_item(
        Item={
            'tenant-id': tenant_id,
            'id': kontakt.id,
            'name': kontakt.name,
            'betreff': kontakt.betreff,
            'nachricht': kontakt.nachricht,
            'zeitpunkt': kontakt.zeitpunkt.isoformat() if kontakt.zeitpunkt is not None else None,
            'telefonnummer': kontakt.telefonnummer,
            'email': kontakt.email,
            'gelesen': kontakt.gelesen,
            'typ': kontakt.typ,
            'ttl': kontakt.ttl
        }
    )


def get_kontakt(tenant_id: str, id: str):
    table = get_kontakte_table()
    result = table.get_item(
        Key={
            "tenant-id": tenant_id,
            "id": id
        }
    )
    return result.get('Item')


def get_kontakte(tenant_id: str) -> list:
    table = get_kontakte_table()
    response = table.query(
        KeyConditionExpression=Key('tenant-id').eq(tenant_id)
    )
    data = response['Items']

    while 'LastEvaluatedKey' in response:
        response = table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
        data.extend(response['Items'])
    return data


def delete_kontakt(tenant_id: str, id: str):
    table = get_kontakte_table()
    table.delete_item(
        Key={
            "tenant-id": tenant_id,
            "id": id
        }
    )
