import json
from lambda_utils.validation import check_required_field, check_email


def create(item: dict):
    email_from = item.get('email-from')
    check_required_field(email_from, 'email-from')
    check_email(email_from)
    email_to = item.get('email-to')
    check_required_field(email_to, 'email-to')
    check_email(email_to)
    return EmailConfigDTO(email_from, email_to)


class EmailConfigDTO:

    def __init__(self,
                 email_from: str,
                 email_to: str):
        self.email_from = email_from
        self.email_to = email_to

    def to_json(self):
        return json.dumps(self.__dict__)
