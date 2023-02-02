import boto3
from kontakt_dto import KontaktDTO
from email_config_dto import EmailConfigDTO
from lambda_utils.ses_utils import is_email_send_ok
from lambda_utils.exception import HttpException


def send_html_email(tenant_id: str, kontakt: KontaktDTO, email_config: EmailConfigDTO):
    kontakt_email = kontakt.email
    betreff = kontakt.betreff

    CHARSET = "UTF-8"
    HTML_EMAIL_CONTENT = create_html_content(tenant_id, kontakt)
    ses_client = boto3.client("ses")

    response = ses_client.send_email(
        Destination={
            "ToAddresses": [
                email_config.email_to
            ],
        },
        ReplyToAddresses=[
            kontakt_email
        ],
        Message={
            "Body": {
                "Html": {
                    "Charset": CHARSET,
                    "Data": HTML_EMAIL_CONTENT,
                }
            },
            "Subject": {
                "Charset": CHARSET,
                "Data": f"Neue Nachricht! Betreff '{betreff}'",
            },
        },
        Source=email_config.email_from,
    )
    if is_email_send_ok is False:
        raise HttpException(f"Email send failed: {response}.", 500)


def create_html_content(tenant_id: str, kontakt: KontaktDTO):
    telefonnumer_html = ""
    if kontakt.telefonnummer:
        telefonnumer_html = f" oder per Telefon unter {kontakt.telefonnummer}"

    return f"""
           <html>
                <head></head>
                <body style="font-family: Segoe UI">
                    <h1>Neue Nachricht!</h1>
                    <p>Hallo! Du hast eine neue Nachricht für {tenant_id} erhalten!</p>
                    <p><i>{kontakt.name}</i> sendete am {kontakt.zeitpunkt} folgende Nachricht:</p>
                    <h2>{kontakt.betreff}</h2>
                    <p>{kontakt.nachricht}</p>
                    <p>
                        Bitte anworte <i>{kontakt.name}</i> per Email unter <a href="mailto:{kontakt.email}">{kontakt.email}</a>
                        {telefonnumer_html}.
                    </p>
                </body>
            </html>
        """
