import uuid
import json
import os
from datetime import datetime, timezone, date, timedelta
from http_exception import ValidationException
from validation_util import check_email, check_required_field


def create(item: dict):
    name = item.get('name')
    check_required_field(name, 'name')
    betreff = item.get('betreff')
    check_required_field(betreff, 'betreff')
    nachricht = item.get('nachricht')
    check_required_field(nachricht, 'nachricht')
    zeitpunkt = item.get('zeitpunkt')
    telefonnummer = item.get('telefonnummer')
    email = item.get('email')
    check_required_field(email, 'email')
    check_email(email)
    gelesen = item.get('gelesen')
    typ = item.get('typ')
    return KontaktDTO(
        name,
        betreff,
        nachricht,
        None if zeitpunkt is None else fromisoformat(zeitpunkt),
        telefonnummer,
        email,
        gelesen,
        typ,
        item.get('id')
    )


def fromisoformat(d: str):
    try:
        return datetime.fromisoformat(d)
    except ValueError as ex:
        raise ValidationException(ex.args[0])


class KontaktDTO:

    def __init__(self, name: str,
                 betreff: str,
                 nachricht: str,
                 zeitpunkt: datetime,
                 telefonnummer: str,
                 email: str,
                 gelesen: bool,
                 typ: str,
                 id: str = None):
        if id:
            self.id = id
        else:
            self.id = str(uuid.uuid4())
        self.name = name
        self.betreff = betreff
        self.nachricht = nachricht
        self.zeitpunkt = zeitpunkt
        self.telefonnummer = telefonnummer
        self.email = email
        self.gelesen = gelesen
        self.typ = typ
        self.ttl = compute_ttl(zeitpunkt)

    def to_json(self):
        return json.dumps(self.__dict__, cls=KontaktDTOEncoder)


def compute_ttl(zeitpunkt: date) -> int:
    ttl_feature_active = int(os.getenv('TTL_FEATURE_ACTIVE', 1)) == 1
    if ttl_feature_active == 1 and zeitpunkt:
        local_date = zeitpunkt + timedelta(days=100)
        utc_date = datetime(year=local_date.year,
                            month=local_date.month,
                            day=local_date.day,
                            tzinfo=timezone.utc)
        return int(utc_date.timestamp())
    else:
        return None


class KontaktDTOEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        else:
            return super().default(obj)
