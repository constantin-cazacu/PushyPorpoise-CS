from pathlib import Path
from pymongo import MongoClient
from pymongo.encryption_options import AutoEncryptionOpts
from pymongo.errors import EncryptionError
from bson import json_util

# Create data for database
data = {"_id": ['ca9ae8e3-21d0-4399-b030-f0ae3bb59165',
                '5b16f413-dc42-4895-844c-f0a427d60688',
                '00211a65-4461-4d71-bfd4-44d0fbff9f52',
                '3fd78a04-064f-48b9-a83f-112b2cd119bb',
                '7036220c-30d8-4d22-90af-6ef013d49303',
                '5b5f70d7-fcfe-48a9-a927-8fb6fb716a96',
                'e4ace6ff-2cc1-4f6e-99ae-53342a5bf845',
                '52e3ec95-0b03-4e51-b882-91d37ce6d767',
                '88ddfaa1-da87-404a-919e-2baac2e7a92e',
                'a9d7bd5b-37bf-4566-9092-217f23d0d20'],
        "agent_name": ['Sterling Archer',
                       'Demolition Dan',
                       'Ann the Arsinest',
                       'Moscow Mincer',
                       'Sergei Skripal',
                       'Desmund Bones',
                       'Paul Plauge',
                       'Ivana Humpalot',
                       'Simon Sly',
                       'Finn Storm'],
        "real_name": ['Augustus Snyder',
                      'Marek Searle',
                      'Aneesa Knapp',
                      'Samah Davies',
                      'Tasnim Vinson',
                      'Noel Smart',
                      'Joey Mckay',
                      'Chloe-Ann Ahmad',
                      'Mitchel Matthams',
                      'Gianni Norris'],
        "ssn": ['303305726',
                '303211762',
                '247929955',
                '011169763',
                '036443047',
                '468988472',
                '541109143',
                '252486957',
                '430396073',
                '237553988'],
        "last_known_location": ['28 deg. N 16 deg. W',
                                '53 deg. N 50 deg. E',
                                '29 deg. N 84 deg. W',
                                '9 deg. N 84 deg. W',
                                '20 deg. N 105 deg. W',
                                '54 deg. N 73 deg. E',
                                '45 deg. S 72 deg. W ',
                                '37 deg. N 25 deg. W',
                                '39 deg. S 176 deg. E',
                                '2 deg. S 104 deg. E']}

# Load the master key from 'key_bytes.bin':
key_bin = Path("key_bytes.bin").read_bytes()

# Load the 'person' schema from "json_schema.json":
collection_schema = json_util.loads(Path("json_schema.json").read_text())

# Configure a single, local KMS provider, with the saved key:
kms_providers = {"local": {"key": key_bin}}

# Create a configuration for PyMongo, specifying the local master key,
# the collection used for storing key data, and the json schema specifying
# field encryption:
csfle_opts = AutoEncryptionOpts(
    kms_providers,
    "cs_lab7.__keystore",
    schema_map={"cs_lab7.agents": collection_schema},
)

username = 'CostelLab7'
password = 'LaboratoryWorkCS'

# Add a new document to the "agents" collection, and then read it back out
# to demonstrate that the ssn field is automatically decrypted by PyMongo:
with MongoClient(
        "mongodb+srv://" + username + ":" + password + "@cluster0.wzmuw.mongodb.net/cluster0?retryWrites=true&w=majority",
        auto_encryption_opts=csfle_opts) as client:
    client.cs_lab7.agents.delete_many({})

    for index in range(len(data['agent_name'])):
        client.cs_lab7.agents.insert_one({
            "_id": data['_id'][index],
            "agent_name": data['agent_name'][index],
            "real_name": data['real_name'][index],
            "ssn": data['ssn'][index],
            "last_known_location": data['last_known_location'][index],
        })
