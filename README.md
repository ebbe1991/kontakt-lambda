# Kontakt-Lambda

## Routen

### Kontakt

- POST api/kontakt
- GET api/kontakt/<id>
- GET api/kontakt
- PUT api/kontakt/<id>
- DELETE api/kontakt/<id>


## Umgebungsvariablen
| Name                    | Beschreibung                                          |
|-------------------------|-------------------------------------------------------|
| KONTAKT_TABLE_NAME      | Name der Kontakt DynamoDB-Table                       |
| EMAIL_CONFIG_TABLE_NAME | Name der Email-Config DynamoDB-Table                  |
| TTL_FEATURE_ACTIVE      | Flag, ob TTL für die Kontakt DynamoDB-Table aktiv ist |