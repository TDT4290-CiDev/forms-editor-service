from flask import Flask, jsonify, request
from form_collection import FormCollection


app = Flask(__name__)
form_collection = FormCollection()


@app.route('/', methods=['GET'])
def get_all_forms():
    forms = form_collection.get_all_forms()
    return jsonify({'all_forms': forms})


@app.route('/<id>', methods=['GET'])
def get_one_form(id):
    if id < 0:
        return jsonify({'message': 'invalid id'}), 401
    try:
        form = form_collection.get_form_by_id(id)

        return jsonify({'form': form})
    except ValueError:
        return jsonify({'message': 'form does not exist'}), 404


@app.route('/', methods=['POST'])
def add_form():
    try:
        form = request.get_json()
#       TODO: additional checks for required parameters in json object
        form_collection.add_form(form)
        return jsonify({'message': 'Successfully inserted document'}), 201

    except ValueError:
        return jsonify({'message': 'Credentials not provied'}), 401


@app.route('/<id>', methods=['PUT'])
def update_one_form(id):
    if id < 0:
        return jsonify({'message': 'invalid id'}), 401
    try:
        updates = request.get_json()
        form_collection.update_one_form(id, updates)
        return jsonify({'message': 'Successfully updated doc'}), 200

    except ValueError:
        return jsonify({'message': 'form does not exist'}), 404


@app.route('/<id>', methods=['DELETE'])
def delete_one_form(id):
    if id < 0:
        return jsonify({'message': 'invalid id'}), 401
    try:
        form_collection.delete_form_by_id(id)

        return jsonify({'message': 'form successfully deleted'}), 200
    except ValueError:
        return jsonify({'message': 'form does not exist'}), 404


if __name__ == '__main__':

    app.run(debug=True, host='0.0.0.0', port=8080)




