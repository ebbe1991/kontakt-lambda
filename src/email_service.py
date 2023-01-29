import boto3
import os
from kontakt_dto import KontaktDTO


def send_html_email(kontakt_dto: KontaktDTO):
    kontakt_email = kontakt_dto.email
    betreff = kontakt_dto.betreff
    from_email = os.getenv('EMAIL_FROM')
    to_email = os.getenv('EMAIL_TO')
    if from_email:
        ses_client = boto3.client("sesv2")
        CHARSET = "UTF-8"
        #todo
        HTML_EMAIL_CONTENT = """
            <html>
                <head></head>
                <h1 style='text-align:center'>This is the heading</h1>
                <p>Hello, world</p>
                </body>
            </html>
        """

        response = ses_client.send_email(
            FromEmailAddress=from_email,
            FromEmailAddressIdentityArn='string',#todo
            Destination={
                "ToAddresses": [
                    to_email,
                ],
            },
             ReplyToAddresses=[
                kontakt_email,
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
                },
            }
        )