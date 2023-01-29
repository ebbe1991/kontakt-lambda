from kontakt_dto import KontaktDTO
from datetime import datetime


def test_compute_none():
    zeitpunkt = None
    kontakt = KontaktDTO(
        "Testuser Helene",
        "Gefällt mir!",
        "Mir gefällt ihr Internetauftritt!\nViele Grüße, Helene",
        zeitpunkt,
        "helene@fischer.de",
        "0123/123456",
        False,
        "Kontaktformular")
    assert kontakt.ttl is None


def test_compute_ttl():
    zeitpunkt = datetime.fromisoformat("2023-01-27T12:30:15")
    kontakt = KontaktDTO(
        "Testuser Helene",
        "Gefällt mir!",
        "Mir gefällt ihr Internetauftritt!\nViele Grüße, Helene",
        zeitpunkt,
        "helene@fischer.de",
        "0123/123456",
        False,
        "Kontaktformular")
    assert kontakt.ttl == 1683417600
