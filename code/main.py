from flask import Flask, jsonify, request
from pymongo import MongoClient


app = Flask(__name__)


#Running mongoDB on local host. Requires mongoDB to be installed and run locally. Must be generalized/dockerized

client = MongoClient('mongodb://datastore:27017/dockerdemo')

"""
app.config['MONGO_DBNAME'] = 'form'
app.config['MONGO_URI'] = 'mongodb://localhost:27017/form'

mongo = PyMongo(app)
"""

db = client.cidevdb

form_collection = db.form


@app.route('/')
def hello_docker():
	form_collection.insert_one({'name': 'TreeCuttingForm'})
	return 'Hello friends! I have just inserted a form'

@app.route('/get_forms', methods=['GET'])
def get_all_forms():
    form = form_collection 

    output = []

    for q in form.find():
        output.append({'name': q['name']})

    return jsonify({'result' : output})

@app.route('/form/<name>', methods=['GET'])
def get_one_form(name):
    form = form_collection

    q = form.find_one({'name' : name})

    if q:
        output = q
    else:
        output = 'No results found'

    return jsonify({'result' : output})

@app.route('/form', methods=['POST'])
def add_form():
    form = form_collection 

    name = request.json['name']

    form_id = form.insert_one({'name' : name})
    new_form = form.find_one({'_id' : form_id})

    output = {'name' : new_form['name']}

    return jsonify({'result' : output})


# Only for testing purposes - should use WSGI server in production
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)