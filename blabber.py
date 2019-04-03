"""
Functions for API endpoints for blabber
"""
# System modules
from datetime import datetime, timedelta
import uuid
from bson.json_util import dumps

# 3rd party modules
from flask import make_response, abort, request, jsonify
from flask_pymongo import PyMongo
from pymongo import MongoClient
from server import mongo

def addBlab_1():
    """
    This function creates a new blab.
    """
    # Get input data - from user
    json_data = request.get_json(force=True)

    # Create empty blab
    new_blab = {}

    # Fill in info for blab
    new_blab['id'] = str(uuid.uuid1())
    new_blab['postTime'] = datetime.now()
    new_blab['author'] = json_data['author']
    new_blab['message'] = json_data['message']

    # Add blab to db
    mongo.db.blabs.insert_one(new_blab)

    return jsonify(new_blab)

def addBlab(id):
    """
    Remove a blab

    Parameters:
    ------------
    uid: str
        The unique id of the blab to remove
    """
    #blab = mongo.db.blabs.find_one({'_id': id})
    db_response = mongo.db.blabs.remove({'id': id})

    if db_response["n"] == 1:
        return "Blab successfully deleted."
    else:
        abort(
        404, "Blab with uid {uid} not found".format(uid=id)
    )

    return True

def doGet(createdSince=0):
    """
    This function response to an api request with the complete list of blabs.

    Return
    ---------------
    all_blabs: str
        json string with list of blabs
    """

    created_since = datetime.fromtimestamp(createdSince)

    created_since_blabs = mongo.db.blabs.find()

    return_blabs = []

    for blab in created_since_blabs:
        return_blabs.append(blab)

    return return_blabs
