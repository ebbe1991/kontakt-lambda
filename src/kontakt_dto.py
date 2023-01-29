import uuid
import json
from datetime import datetime, timezone
import os
import re
from datetime import date, timedelta
from http_exception import ValidationException


def create(item: dict):
    name = item.get('name')
    checkRequiredField(name, 'name')
    betreff = item.get('betreff')
    checkRequiredField(betreff, 'betreff')
    nachricht = item.get('nachricht')
    checkRequiredField(nachricht, 'nachricht')
    zeitpunkt = item.get('zeitpunkt')
    telefonnummer = item.get('telefonnummer')
    email = item.get('email')
    checkRequiredField(email, 'email')
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


def checkRequiredField(field, fieldname: str):
    if field is None or len(field) <= 0:
        raise ValidationException(f"'{fieldname}' is missing.")


def check_email(email):
    regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
    if (re.search(regex, email)):
        pass
    else:
        raise ValidationException(f"invalid email '{email}'.")


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
