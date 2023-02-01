from kontakt_dto import KontaktDTO, create
from lambda_utils.exception import UnknownIdException
import dynamo_db_service


def create_kontakt(tenant_id: str, dto: dict) -> KontaktDTO:
    kontakt = create(dto)
    dynamo_db_service.put_kontakt(tenant_id, kontakt)
    return kontakt


def update_kontakt(tenant_id: str, id: str, dto: dict) -> KontaktDTO:
    dto.update({'id': id})
    kontakt = create(dto)
    to_update = get_kontakt(tenant_id, id)
    if to_update:
        dynamo_db_service.put_kontakt(tenant_id, kontakt)
        return kontakt
    else:
        raise UnknownIdException(id, tenant_id)


def get_kontakt(tenant_id: str, id: str) -> KontaktDTO:
    item = dynamo_db_service.get_kontakt(tenant_id, id)
    if item:
        kontakt = create(item)
        return kontakt
    else:
        return None


def get_kontakte(tenant_id: str) -> list[KontaktDTO]:
    kontakte = []
    items = dynamo_db_service.get_kontakte(tenant_id)
    for item in items:
        kontakt = create(item)
        kontakte.append(kontakt)
    return kontakte


def delete_kontakt(tenant_id: str, id: str) -> bool:
    kontakt = get_kontakt(tenant_id, id)
    if kontakt:
        dynamo_db_service.delete_kontakt(tenant_id, id)
        return True
    else:
        return False
