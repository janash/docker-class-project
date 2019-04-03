from flask import render_template, Blueprint
from datetime import datetime
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
import connexion

import os
import json

options = {'swagger_ui': True}

class JSONEncoder(json.JSONEncoder):
    ''' extend json-encoder class'''

    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        if isinstance(o, datetime):
            return str(o)
        return json.JSONEncoder.default(self, o)

# Create the application instance
connex = connexion.FlaskApp(__name__, specification_dir='./', options=options)
app = connex.app
app.config['MONGO_URI'] = os.environ.get('DB')
mongo = PyMongo(app)
app.json_encoder = JSONEncoder

# Create a URL route in our application for "/"
@app.route('/')
def home():
    """
    This function just responds to the browser ULR
    localhost:5000/

    :return:        the rendered template 'home.html'
    """
    return render_template('home.html')

# If we're running in stand alone mode, run the application
if __name__ == '__main__':
    blab = {}
    blab['postTime'] = datetime.now()
    blab['author'] = 'Author 1'
    blab['message'] = 'This is my message'

    # Add blab to db
    #blabs.insert_one(blab)
    # Read the swagger.yml file to configure the endpoints
    connex.add_api('swagger.json', resolver=connexion.resolver.RestyResolver('api'))

    app.run(host='0.0.0.0', port=5000, debug=True)
