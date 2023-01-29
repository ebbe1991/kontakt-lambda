import boto3
import os
import email_config_controller
from kontakt_dto import KontaktDTO
from email_config_dto import EmailConfigDTO
from http_exception import ValidationException


def send_html_email(tenant_id: str, kontakt: KontaktDTO):
    kontakt_email = kontakt.email
    betreff = kontakt.betreff

    send_email = os.getenv('SEND_EMAIL') == 1
    if send_email:
        email_config: EmailConfigDTO = email_config_controller.get_email_config(
            tenant_id)
        if email_config is None or email_config.email_from is None or email_config.email_to is None:
            raise ValidationException(
                f"Email-Config not present (tenant-id={tenant_id}).")

        CHARSET = "UTF-8"
        HTML_EMAIL_CONTENT = create_html_content(tenant_id, kontakt)
        ses_client = boto3.client("sesv2")
        response = ses_client.send_email(
            FromEmailAddress=email_config.email_from,
            FromEmailAddressIdentityArn='string',  # todo
            Destination={
                "ToAddresses": [
                    email_config.email_to
                ],
            },
            ReplyToAddresses=[
                kontakt_email
            ],
            Content={
                'Simple': {
                    'Subject': {
                        'Data': f"Neue Nachricht! Betreff '{betreff}'",
                        'Charset': CHARSET
                    },
                    'Body': {
                        'Html': {
                            'Data': HTML_EMAIL_CONTENT,
                            'Charset': CHARSET
                        }
                    }
                }
            }
        )


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
