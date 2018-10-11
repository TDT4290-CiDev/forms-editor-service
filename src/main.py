from flask import Flask, jsonify, request
from flask_pymongo import PyMongo


app = Flask(__name__)


#Running mongoDB on local host. Requires mongoDB to be installed and run locally. Must be generalized/dockerized
app.config['MONGO_DBNAME'] = 'form'
app.config['MONGO_URI'] = 'mongodb://localhost:27017/form'

mongo = PyMongo(app)



@app.route('/')
def hello_docker():
    return 'Hello Docker friends!'

@app.route('/form', methods=['GET'])
def get_all_forms():
    form = mongo.db.form 

    output = []

    for q in form.find():
        output.append({'name': q['name']})

    return jsonify({'result' : output})

@app.route('/form/<name>', methods=['GET'])
def get_one_form(name):
    form = mongo.db.form

    q = form.find_one({'name' : name})

    if q:
        output = q
    else:
        output = 'No results found'

    return jsonify({'result' : output})

@app.route('/form', methods=['POST'])
def add_form():
    form = mongo.db.form 

    name = request.json['name']

    form_id = form.insert({'name' : name})
    new_form = form.find_one({'_id' : form_id})

    output = {'name' : new_form['name']}

    return jsonify({'result' : output})


# Only for testing purposes - should use WSGI server in production
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)