import os
import exh

transition_name = 'submit_result' # For this example we will use a fixed transition name
schemaId = os.environ['SCHEMA_ID']
documentId = os.environ['DOCUMENT_ID']

print('Fetching the document...')
document = exh.get_document(schemaId, documentId)

print('Downloading the raw data...')
rawDataFileToken = document['data']['rawDataFileToken']
exh.download_file(rawDataFileToken, './data/raw_data_file.csv')

print('Processing the data...')
# Do some processing on the file
# In a real scenario the processing might produce a new file as a side effect and, of course, a "result"
# For this example we just copy the raw data file
with open('./data/raw_data_file.csv', 'r') as f:
    with open('./data/processed_data_file.csv', 'w') as g:
        g.write(f.read())

# And we pick a random number as the "result"
result = 42

print('Uploading the processed data...')
processed_data_file_token = exh.upload_file('./data/processed_data_file.csv', 'processed_data_file.csv')

print('Find the transition to trigger...')
schema = exh.get_schema(schemaId)
transition = exh.find_transition_in_schema(schema, 'submit_result')

print('Transitioning the document with the processed file and result...')
exh.transition_document(schemaId, documentId, transition['id'], {
    'processedDataFileToken': processed_data_file_token,
    'result': result
})


