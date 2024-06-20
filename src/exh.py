from requests_oauthlib import OAuth1Session
from dotenv import load_dotenv
import os

load_dotenv()

base_url = 'https://' + os.environ['API_HOST']

client = OAuth1Session(
    client_key=os.environ['API_OAUTH_CONSUMER_KEY'],
    client_secret=os.environ['API_OAUTH_CONSUMER_SECRET'],
    resource_owner_key=os.environ['API_OAUTH_TOKEN'],
    resource_owner_secret=os.environ['API_OAUTH_TOKEN_SECRET']
)

def get_schema(schema_id):
    response = client.get(base_url + '/data/v1/?id=' + schema_id).json()
    return response['data'][0]


def get_document(schema_name_or_id, document_id):
    response = client.get(base_url + '/data/v1/' + schema_name_or_id + '/documents/?id=' + document_id).json()
    return response['data'][0]


def transition_document(schema_id, document_id, transition_id, data):
    json = {
        'id': transition_id,
        'data': data,
    }
    client.post(base_url + '/data/v1/' + schema_id + '/documents/' + document_id + '/transition/', json=json).json()


def upload_file(file_path, file_name):
    files = {'file': (file_name, open(file_path, 'rb'))}
    response = client.post(base_url + '/files/v1/', files={'file': (file_name, open(file_path, 'rb')) }).json()
    return response['tokens'][0]['token']


def download_file(token, output_path):
    response = client.get(base_url + '/files/v1/' + token + '/file')
    
    with open(output_path, 'wb') as f:
        f.write(response.content)


def find_transition_in_schema(schema, transition_name):
    for transition in schema['transitions']:
        if transition['name'] == transition_name:
            return transition
    return None
