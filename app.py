import os
from flask import Flask, request, jsonify
from pymongo import MongoClient, ReadPreference
from pymongo.write_concern import WriteConcern

app = Flask(__name__)

MONGO_URI = os.environ.get("MONGO_URI", "mongodb+srv://<db_username>:<db_password>@cluster0.dgykqba.mongodb.net/?appName=Cluster0")
client = MongoClient(MONGO_URI)
db = client["ev_db"]


@app.route("/insert-fast", methods=["POST"])
def insert_fast():
    data = request.get_json(force=True)
    collection = db.get_collection("vehicles", write_concern=WriteConcern(w=1))
    result = collection.insert_one(data)
    return jsonify({"inserted_id": str(result.inserted_id)})


@app.route("/insert-safe", methods=["POST"])
def insert_safe():
    data = request.get_json(force=True)
    collection = db.get_collection("vehicles", write_concern=WriteConcern(w="majority"))
    result = collection.insert_one(data)
    return jsonify({"inserted_id": str(result.inserted_id)})


@app.route("/count-tesla-primary", methods=["GET"])
def count_tesla_primary():
    collection = db.get_collection("vehicles", read_preference=ReadPreference.PRIMARY)
    count = collection.count_documents({"Make": "TESLA"})
    return jsonify({"count": count})


@app.route("/count-bmw-secondary", methods=["GET"])
def count_bmw_secondary():
    collection = db.get_collection("vehicles", read_preference=ReadPreference.SECONDARY_PREFERRED)
    count = collection.count_documents({"Make": "BMW"})
    return jsonify({"count": count})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
