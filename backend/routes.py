from . import app
import os
import json
from flask import jsonify, request, make_response, abort, url_for  # noqa; F401

SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
json_url = os.path.join(SITE_ROOT, "data", "pictures.json")
data: list = json.load(open(json_url))

# UTILITIES
def data_id_refresh():
    for i, q in enumerate(data):
        q["id"] = i+1

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
    try:
        if data:
            return ({ "length" : len(data) }, 200 )
    except Exception:
        return ( {"message": "Internal server error"}, 500 )


######################################################################
# GET ALL PICTURES
######################################################################
@app.route("/picture", methods=["GET"])
def get_pictures():
    try:
        return ( jsonify(data), 200 )
    except Exception:
        return ({ "message" : f"Server error: {Exception}"}, 500 )

######################################################################
# GET A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["GET"])
def get_picture_by_id(id):
    try:
        for q in data:
            if q["id"] == id:
                return ( jsonify(q), 200 )
        return ({ "message" : "Picture not found"}, 404 )
    except Exception:
        return ({ "message" : f"Server error: {Exception}"}, 500 )


######################################################################
# CREATE A PICTURE
######################################################################
@app.route("/picture", methods=["POST"])
def create_picture():
    try:
        posts_data = request.json
        for picture in data:
           if picture["id"] == posts_data["id"]:
                return ({"Message" : f"picture with id {picture['id']} already present"}, 302 )
        
        #posts_data["id"] = len(data)+1
        data.append(posts_data)
        return ({ "message" : "Picture added", "id" : posts_data["id"] }, 201 )        
    except Exception:
        return ({ "message" : f"Server error: {Exception}"}, 500 )

######################################################################
# UPDATE A PICTURE
######################################################################
@app.route("/picture/<int:id>", methods=["PUT"])
def update_picture(id):
    try:
        data_id_refresh()
        for i, picture in enumerate(data):
            if picture["id"] == id:
                requests_data = request.get_json()
                requests_keys = requests_data.keys()
                for key in requests_keys:
                    if key in data[i]:
                        data[i][key] = requests_data[key]
                
        return ( request.json, 200 )
    except Exception:
         return ({ "message" : f"Server error: {str(Exception)}"}, 500 )

######################################################################
# DELETE A PICTURE
######################################################################
@app.route("/picture/<int:id>", methods=["DELETE"])
def delete_picture(id):
    try:
        data_id_refresh()
        for i, picture in enumerate(data):
            if picture["id"] == id:
               data.pop(i)
               data_id_refresh()
               return ({"message" : "Picture deleted", "data_length" : len(data)}, 204 )
        return ({"message" : "Picture not in database"}, 404 )
               
    except Exception:
         return ({ "message" : f"Server error: {Exception}", "id" : id, "data_length" : len(data)}, 500 )
