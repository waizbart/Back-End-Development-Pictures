from . import app
import os
import json
from flask import jsonify, request, make_response, abort, url_for  # noqa; F401

SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
json_url = os.path.join(SITE_ROOT, "data", "pictures.json")
data: list = json.load(open(json_url))

######################################################################
# RETURN HEALTH OF THE APP
######################################################################


@app.route("/health")
def health():
    return jsonify(dict(status="OK")), 200

######################################################################
# COUNT THE NUMBER OF PICTURES
######################################################################


@app.route("/count")
def count():
    """return length of data"""
    if data:
        return jsonify(length=len(data)), 200

    return {"message": "Internal server error"}, 500


######################################################################
# GET ALL PICTURES
######################################################################
@app.route("/picture", methods=["GET"])
def get_pictures():
    if data:
        return jsonify(data), 200

    return {"message": "Internal server error"}, 500

######################################################################
# GET A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["GET"])
def get_picture_by_id(id):
    if data:
        for picture in data: 
            if picture["id"] == id:
                return jsonify(picture), 200

    return {"message": "Not found"}, 404


######################################################################
# CREATE A PICTURE
######################################################################
@app.route("/picture", methods=["POST"])
def create_picture():
    for picture in data: 
        if picture["id"] == request.json["id"]:
            return {"Message": "picture with id {} already present".format(picture["id"])}, 302

    data.append(request.json)
    return request.json, 201

######################################################################
# UPDATE A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["PUT"])
def update_picture(id):
    for i in range(0, len(data)):
        if data[i]["id"] == id:
            data[i] = request.json
            return data[i], 200

    return {"Message": "Not found"}, 404

######################################################################
# DELETE A PICTURE
######################################################################
@app.route("/picture/<int:id>", methods=["DELETE"])
def delete_picture(id):
    for i in range(0, len(data)):
        if data[i]["id"] == id:
            data.pop(i)
            return {}, 204

    return {"Message": "Not found"}, 404
