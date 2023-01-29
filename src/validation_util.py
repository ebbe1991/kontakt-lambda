from http_exception import ValidationException
import re


def check_required_field(field, fieldname: str):
    if field is None or len(field) <= 0:
        raise ValidationException(f"'{fieldname}' is missing.")


def check_email(email):
    regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
    if (re.search(regex, email)):
        pass
    else:
        raise ValidationException(f"invalid email '{email}'.")
