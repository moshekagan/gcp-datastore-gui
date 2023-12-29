from flask import Flask, jsonify, request, redirect
from google.cloud import datastore
import os
from flask_cors import CORS
from google.cloud.datastore import Key

app = Flask(__name__)
CORS(app)

# Environment variables
PORT = os.environ.get('PORT', '8002')
PROJECT_ID = os.environ.get('PROJECT_ID', 'local-dev')
DS_HOST = os.environ.get('DATASTORE_EMULATOR_HOST', 'localhost:8001')


def get_client():
    os.environ["DATASTORE_EMULATOR_HOST"] = "localhost:8001"
    os.environ["DATASTORE_EMULATOR_HOST_PATH"] = "localhost:8001/datastore"
    os.environ["DATASTORE_HOST"] = "http://localhost:8001"
    os.environ["DATASTORE_DATASET"] = "local-dev"
    os.environ["DATASTORE_PROJECT_ID"] = "local-dev"
    db = datastore.Client(project="local-dev")

    return db


@app.route('/')
def index():
    return redirect("/index", code=301)


@app.route('/namespaces', methods=['GET'])
def get_namespaces():
    client = get_client()
    query = client.query(kind="__namespace__")
    query.keys_only()

    keys = list(query.fetch())
    print("keys!!!")
    print(keys)
    # namespaces = [k.name if k.name else "default" for k in keys]

    return jsonify({"namespaces": ["default"]})


@app.route('/namespace/<namespace>', methods=['GET'])
def get_kinds(namespace):
    client = get_client()
    query = client.query(kind="__kind__")
    query.keys_only()

    keys = list(query.fetch())
    kinds = [k.key.id_or_name for k in keys]

    return jsonify({"kinds": kinds})

def _parse_entity(entity):
    res = {}
    for k, v in dict(entity).items():
        if type(v) is Key:
            res[k] = f"{str(v)}"
        else:
            res[k] = v

    return res


@app.route('/namespace/<namespace>/kind/<kind>', methods=['GET'])
def get_entities(namespace, kind):
    client = get_client()
    query = client.query(kind=kind)

    entities = list(query.fetch())
    response_entities = [_parse_entity(entity) for entity in entities]

    return jsonify({"entities": response_entities})



@app.route('/namespace/<namespace>/kind/<kind>/properties', methods=['GET'])
def get_properties(namespace, kind):
    # client = get_client()
    # query = client.query(kind="__property__")
    # query.keys_only()

    # keys = list(query.fetch())
    # properties = ["ID/Name"]
    # for k in keys:
    #     if k.parent.name == kind:
    #         name = k.name.split('.')[0]
    #         if properties[-1] != name:
    #             properties.append(name)
    # return jsonify({"properties": properties})

    client = get_client()
    query = client.query(kind=kind)

    entities = list(query.fetch())
    response_entities = [dict(entity) for entity in entities]

    print("ASDsa")
    print(list(response_entities[0].keys() if len(response_entities) > 0 else []))

    return jsonify({"properties": list(response_entities[0].keys() if len(response_entities) > 0 else [])})


@app.route('/namespace/<namespace>/kind/<kind>', methods=['DELETE'])
def delete_entities(namespace, kind):
    client = get_client()
    data = request.json

    keys = [datastore.Key(k.split('/')[1], int(k.split('/')[2]), project=PROJECT_ID) for k in data["keys"]]
    client.delete_multi(keys)

    return jsonify({"status": "success"})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(PORT))
