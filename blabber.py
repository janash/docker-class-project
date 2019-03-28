"""
Functions for API endpoints for blabber
"""

# System modules
from datetime import datetime, timedelta
import uuid

# 3rd party modules
from flask import make_response, abort, request, jsonify

def get_timestamp():
    return datetime.now().strftime(("%Y-%m-%d %H:%M:%S"))

def return_schema(blab):
    responses = []

    for uid in blab.keys():
        response = {}
        response["id"] = uid
        response["postTime"] = blab[uid]["postTime"]
        response["author"] = blab[uid]["author"]
        response["message"] = blab[uid]["message"]
        responses.append(response)
    return responses

BLABS = {
    str(uuid.uuid1()): {
    "postTime": datetime.now(),
    "author": {
        "email" : "fake_email@vt.edu",
        "name" : "Blabber User",
        },
    "message" : "First Blab"
        },

        str(uuid.uuid1()): {
        "postTime": datetime.now(),
        "author": {
            "email" : "fake_email@vt.edu",
            "name" : "Another User",
            },
        "message" : "Second Blab"
            },
    }

def addBlab_1():
    """
    This function creates a new blab in the BLAB structure.
    """
    blab = {}

    blab['postTime'] = datetime.now()
    uid = str(uuid.uuid1())

    json_data = request.get_json(force=True)
    blab['author'] = json_data['author']
    blab['message'] = json_data['message']

    BLABS[uid] = blab

    convert_blab = {uid: BLABS[uid]}
    return_blab = return_schema(convert_blab)

    return return_blab[0]

def addBlab(id):
    """
    Remove a blab

    Parameters:
    ------------
    uid: str
        The unique id of the blab to remove
    """

    if id in BLABS:
        convert_blab = {uid: BLABS[id]}
        return_blabs = return_schema(convert_blab)
        del BLABS[id]
        return return_blabs[0]
    else:
        abort(
            404, "Blab with uid {uid} not found".format(uid=id)
        )

def doGet(createdSince):
    """
    This function response to an api request with the complete list of blabs.

    Return
    ---------------
    all_blabs: str
        json string with list of blabs
    """
    created_since = datetime.fromtimestamp(createdSince)

    new_blabs = {}

    for id, blab in BLABS.items():
        if blab["postTime"] > created_since:
            new_blabs[id] = blab

    return_blabs = return_schema(new_blabs)

    return return_blabs
