from email_config_dto import EmailConfigDTO, create
import dynamo_db_service
from lambda_utils.exception import ValidationException

def get_email_config(tenant_id: str) -> EmailConfigDTO:
    item = dynamo_db_service.get_email_config(tenant_id)
    if item:
        email_config = create(item)
        return email_config
    else:
        raise ValidationException(
            f"email config not present (tenant-id={tenant_id}).")


def create_email_config(tenant_id: str, dto: dict) -> EmailConfigDTO:
    email_config = create(dto)
    dynamo_db_service.put_email_config(tenant_id, email_config)
    return email_config
