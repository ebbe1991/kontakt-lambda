import uuid
import json
from datetime import datetime
from lambda_utils.exception import ValidationException
from lambda_utils.date_utils import compute_ttl_for_datetime
from lambda_utils.validation import check_email, check_required_field
from lambda_utils.env_utils import getenv_as_boolean


def create(item: dict):
    name = item.get('name')
    check_required_field(name, 'name')
    betreff = item.get('betreff')
    check_required_field(betreff, 'betreff')
    nachricht = item.get('nachricht')
    check_required_field(nachricht, 'nachricht')
    zeitpunkt = item.get('zeitpunkt')
    telefonnummer = item.get('telefonnummer')
    zusatzinfos = item.get('zusatzinfos')
    email = item.get('email')
    check_required_field(email, 'email')
    check_email(email)
    gelesen = item.get('gelesen')
    return KontaktDTO(
        name,
        betreff,
        nachricht,
        None if zeitpunkt is None else fromisoformat(zeitpunkt),
        telefonnummer,
        zusatzinfos,
        email,
        gelesen,
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
                 zusatzinfos: str,
                 email: str,
                 gelesen: bool,
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
        self.zusatzinfos = zusatzinfos
        self.email = email
        self.gelesen = gelesen
        self.ttl = compute_ttl_for_datetime(zeitpunkt) if getenv_as_boolean(
            'TTL_FEATURE_ACTIVE', True) else None

    def to_json(self):
        return json.dumps(self.__dict__, cls=KontaktDTOEncoder)


class KontaktDTOEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        else:
            return super().default(obj)
