from requests_oauthlib import OAuth1Session
import os

oAuth1Client = OAuth1Session(
    client_key=os.environ['API_OAUTH_CONSUMER_KEY'],
    client_secret=os.environ['API_OAUTH_CONSUMER_SECRET'],
    resource_owner_key=os.environ['API_OAUTH_TOKEN'],
    resource_owner_secret=os.environ['API_OAUTH_TOKEN_SECRET']
)

documentId = os.environ['SCHEMA_ID']
schemaId = os.environ['DOCUMENT_ID']

result = oAuth1Client.get('https://' + os.environ['API_HOST'] + '/users/v1/me')

print("Response", result.json())
