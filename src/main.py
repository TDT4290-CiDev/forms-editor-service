from http import HTTPStatus
from flask import Flask, jsonify, request
from pymongo import MongoClient

from form_collection import FormCollection


app = Flask(__name__)

access_url = 'forms-editor-datastore:27017'

form_collection = FormCollection(MongoClient(access_url))


@app.route('/', methods=['GET'])
def get_all_forms():
    forms = form_collection.get_all_forms()
    return jsonify({'data': forms})


@app.route('/<fid>', methods=['GET'])
def get_one_form(fid):
    try:
        form = form_collection.get_one_form(fid)
        return jsonify({'data': form})
    except ValueError as e:
        return str(e), HTTPStatus.NOT_FOUND


@app.route('/', methods=['POST'])
def add_form():
    form = request.get_json()
    fid = form_collection.add_form(form)
    return fid, HTTPStatus.CREATED


@app.route('/<fid>', methods=['PUT'])
def update_one_form(fid):
    try:
        body = request.get_json()
        form_collection.update_one_form(fid, body)
        return '', HTTPStatus.NO_CONTENT
    except ValueError as e:
        return str(e), HTTPStatus.NOT_FOUND


@app.route('/<fid>', methods=['DELETE'])
def delete_one_form(fid):
    try:
        form_collection.delete_one_form(fid)
        return '', HTTPStatus.NO_CONTENT
    except ValueError as e:
        return str(e), HTTPStatus.NOT_FOUND


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)




