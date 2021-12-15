from pathlib import Path
from pymongo import MongoClient
from pymongo.encryption_options import AutoEncryptionOpts
from pymongo.errors import EncryptionError
from bson import json_util


def is_correct_log_in(username, password):
    if username == 'CostelLab7' and password == 'LaboratoryWorkCS':
        return True

    return False


def read_data(username_x, password_x):
    if username_x == 'CostelLab7' and password_x == 'LaboratoryWorkCS':
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

        with MongoClient(
                "mongodb+srv://" + username + ":" + password + "@cluster0.wzmuw.mongodb.net/cluster0?retryWrites=true&w=majority",
                auto_encryption_opts=csfle_opts) as client:

            post_count = client.cs_lab7.agents.count_documents({})

            # Decrypted results
            list_of_agents = []
            results = client.cs_lab7.agents.find({})
            for result in results:
                list_of_agents.append(result)

        return post_count, list_of_agents
