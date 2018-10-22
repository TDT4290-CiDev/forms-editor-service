from flask import Flask, jsonify, request
from pymongo import MongoClient
from form_collection import FormCollection


app = Flask(__name__)

form_collection = FormCollection()


@app.route('/', methods=['GET'])
def get_all_forms():
    
    forms = form_collection.get_all_forms()
    
    for form in forms:
        del form['_id']

    return jsonify({'all_forms' : forms})

@app.route('/{id:}', methods=['GET'])
def get_one_form(id):
    query = request.get_json()
    name = query['name']
    author = query['author']
    form = form_collection.get_one_form(name, author)

    return jsonify({'result' : form})

@app.route('/', methods=['POST'])
def add_form():

    form = request.get_json()
    form_collection.add_form(form)

    return jsonify({'message': 'successfully inserted document'})


@app.route('/{id}', methods=['PUT'])
def update_one_form(id):

    form = request.get_json()
    name = form['name']
    author = form['author']

    form_collection.update_one_form()

    return jsonify({'message': 'successfully updated document'})



@app.route('/{}', methods=['DELETE'])
def delete_one_form():

    form = request.get_json()
    name = form['name']
    author = form['author']

    form_collection.delete_one_form(name, author)    

    return jsonify({'message': 'successfully deleted document'})
"""
#dangerous to have "delete all" as an option

@app.route('/delete_all_forms', methods=['POST'])
def delete_all_forms():
    form_collection.delete_all_forms()
    return jsonify({'message': 'successfully deleted all forms'})
"""

# Only for testing purposes - should use WSGI server in production
if __name__ == '__main__':

    app.run(debug=True, host='0.0.0.0', port=8080)
   