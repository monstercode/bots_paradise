#!/usr/bin/env python
import os
from datetime import datetime
from flask import Flask, request
from pymongo import MongoClient
import logging
import sys
import uuid
import pathlib

logging.StreamHandler(sys.stdout)
logger = logging.getLogger("main")
logger.setLevel(logging.DEBUG)


app = Flask(__name__)
pathlib.Path("/src/uploads").mkdir(exist_ok=True)
app.config['UPLOAD_FOLDER'] = "/src/uploads"

client = MongoClient("mongo:27017")

@app.route('/')
def main():
    conter = client.main_database.bots_collection.count_documents({})
    return f"It Works! Current counter {conter}"


@app.route('/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE', 'HEAD'])
def bots_handler(path):
    try:
        if request.path == "/favicon.ico":
            return

        data = {
            "datetime": datetime.utcnow(),
            "uri": request.path,
            "method": request.method,
            "request_data": (request.data or request.form) if not request.files else f"<uploaded file(s)>: {len(request.files.keys())}",
            "query_string": dict(request.args),
            "origin": request.origin,
            "headers": dict(request.headers),
            "host": request.host,
            "ip": request.remote_addr,
            "user_agent": request.headers.get('User-Agent', ""),
        }
        if type(data["request_data"]) is bytes:
            data["request_data"] = data["request_data"].decode()
        
        try:
            if request.files:
                files_renaming_map = dict()
                for filename in request.files:
                    new_filename = str(uuid.uuid4())
                    files_renaming_map[new_filename] = filename
                    logger.error(request.files[filename])
                    request.files[filename].save(os.path.join(app.config['UPLOAD_FOLDER'], new_filename))

                data["request_data"] = f"<Files Uploaded>: {files_renaming_map}" 
        except Exception as e:
            logger.error(f"Failed saving file/s {e}")

        client.main_database.bots_collection.insert_one(data).inserted_id
    except Exception as e:
        logger.error(e)

    return ""


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=os.environ.get("FLASK_SERVER_PORT", 9090), debug=True)

