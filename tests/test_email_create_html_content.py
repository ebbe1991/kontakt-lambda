from kontakt_dto import KontaktDTO
from datetime import datetime
import email_service

def test_create_content_with_telefonnummer():
    kontakt = KontaktDTO(
        "Testuser Helene",
        "Gefaellt mir!",
        "Mir gefaellt ihr Internetauftritt!",
        datetime.fromisoformat("2023-01-01T12:30:00"),
        "0123/123456",
        None,
        "helene@fischer.de",
        False,
        id)
    content = email_service.create_html_content('example.com', kontakt)
    assert content == """
           <html>
                <head></head>
                <body style="font-family: Segoe UI">
                    <h1>Neue Nachricht!</h1>
                    <p>Hallo! Du hast eine neue Nachricht für example.com erhalten!</p>
                    <p><i>Testuser Helene</i> sendete am 2023-01-01 12:30:00 folgende Nachricht:</p>
                    <b>Gefaellt mir!</b>
                    <pre style="border:1px solid black;">Mir gefaellt ihr Internetauftritt!</pre>
                    <p>
                        Bitte anworte <i>Testuser Helene</i> per Email unter <a href="mailto:helene@fischer.de">helene@fischer.de</a>
                         oder per Telefon unter 0123/123456.
                    </p>
                </body>
            </html>
        """
    

def test_create_content_with_telefonnummer_and_zusatzinfos():
    kontakt = KontaktDTO(
        "Testuser Helene",
        "Gefaellt mir!",
        "Mir gefaellt ihr Internetauftritt!",
        datetime.fromisoformat("2023-01-01T12:30:00"),
        "0123/123456",
        "Bevorzugt wird eine telefonische Rückmeldung.",
        "helene@fischer.de",
        False,
        id)
    content = email_service.create_html_content('example.com', kontakt)
    assert content == """
           <html>
                <head></head>
                <body style="font-family: Segoe UI">
                    <h1>Neue Nachricht!</h1>
                    <p>Hallo! Du hast eine neue Nachricht für example.com erhalten!</p>
                    <p><i>Testuser Helene</i> sendete am 2023-01-01 12:30:00 folgende Nachricht:</p>
                    <b>Gefaellt mir!</b>
                    <pre style="border:1px solid black;">Mir gefaellt ihr Internetauftritt!</pre>
                    <p>
                        Bitte anworte <i>Testuser Helene</i> per Email unter <a href="mailto:helene@fischer.de">helene@fischer.de</a>
                         oder per Telefon unter 0123/123456.<br>Bevorzugt wird eine telefonische Rückmeldung.
                    </p>
                </body>
            </html>
        """

def test_create_content_without_telefonnummer():
    kontakt = KontaktDTO(
        "Testuser Helene",
        "Gefaellt mir!",
        "Mir gefaellt ihr Internetauftritt!",
        datetime.fromisoformat("2023-01-01T12:30:00"),
        None,
        None,
        "helene@fischer.de",
        False,
        id)
    content = email_service.create_html_content('example.com', kontakt)
    assert content == """
           <html>
                <head></head>
                <body style="font-family: Segoe UI">
                    <h1>Neue Nachricht!</h1>
                    <p>Hallo! Du hast eine neue Nachricht für example.com erhalten!</p>
                    <p><i>Testuser Helene</i> sendete am 2023-01-01 12:30:00 folgende Nachricht:</p>
                    <b>Gefaellt mir!</b>
                    <pre style="border:1px solid black;">Mir gefaellt ihr Internetauftritt!</pre>
                    <p>
                        Bitte anworte <i>Testuser Helene</i> per Email unter <a href="mailto:helene@fischer.de">helene@fischer.de</a>
                        .
                    </p>
                </body>
            </html>
        """
