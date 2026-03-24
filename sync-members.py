import requests
from some_embedding_library import embed
from chromadb import Client
import schedule
import time

# Read member data from README.md
with open('README.md', 'r') as file:
    members_data = file.read()

# Convert member data to embeddings
embeddings = embed(members_data)

# Store embeddings in Chroma DB
chroma_client = Client(host='chromadb-yqg9j-u70373.vm.elestio.app', port=18374)
collection = chroma_client.create_collection('members')
collection.add(embeddings)

# Function to sync members data
def sync_members():
    with open('README.md', 'r') as file:
        new_members_data = file.read()
    new_embeddings = embed(new_members_data)
    collection.add(new_embeddings)

# Schedule sync every day at a specified time
schedule.every().day.at("01:00").do(sync_members)

while True:
    schedule.run_pending()
    time.sleep(1)