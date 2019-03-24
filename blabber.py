"""
Functions for API endpoints for blabber
"""

# System modules
from datetime import datetime
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
    "postTime": get_timestamp(),
    "author": {
        "email" : "fake_email@vt.edu",
        "name" : "Blabber User",
        },
    "message" : "First Blab"
        },

        str(uuid.uuid1()): {
        "postTime": get_timestamp(),
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

    blab['postTime'] = get_timestamp()
    uid = str(uuid.uuid1())

    json_data = request.get_json(force=True)
    blab['author'] = json_data['author']
    blab['message'] = json_data['message']

    BLABS[uid] = blab

    convert_blab = {'id': BLABS[uid]}
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
        convert_blab = {'id': BLABS[id]}
        return_blabs = return_schema(convert_blab)
        del BLABS[id]
        return return_blabs[0]
    else:
        abort(
            404, "Blab with uid {uid} not found".format(uid=id)
        )

def doGet():
    """
    This function response to an api request with the complete list of blabs.

    Return
    ---------------
    all_blabs: str
        json string with list of blabs
    """
    return_blabs = return_schema(BLABS)

    return return_blabs
