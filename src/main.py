from flask import Flask, jsonify, request
from form_collection import FormCollection
from http import HTTPStatus


app = Flask(__name__)

form_collection = FormCollection()


@app.route('/', methods=['GET'])
def get_all_forms():
    forms = form_collection.get_all_forms()
    return jsonify({'all_forms': forms})


@app.route('/<fid>', methods=['GET'])
def get_one_form(fid):
    form = form_collection.get_one_form(fid)
    return jsonify({'form': form})


@app.route('/', methods=['POST'])
def add_form():
    form = request.get_json()
    fid = form_collection.add_form(form)
    return fid, HTTPStatus.CREATED 


@app.route('/<fid>', methods=['PUT'])
def update_one_form(fid):
    body = request.get_json()
    form_collection.update_one_form(fid, body)
    return 'Successfully updated document'


@app.route('/<fid>', methods=['DELETE'])
def delete_one_form(fid):
    successfully_deleted = form_collection.delete_one_form(id)
    if successfully_deleted:
        return '', HTTPStatus.NO_CONTENT
    else:
        return 'Form with id %d does not exist', HTTPStatus.NOT_FOUND


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)




