from pymongo import MongoClient
from bson.objectid import ObjectId


access_url = 'forms-editor-datastore:27017'


class FormCollection:

    def __init__(self):
        self.client = MongoClient(access_url)
        self.db = self.client.cidev_db
        self.form_collection = self.db.form_collection

    def get_one_form(self, fid):
        form = self.form_collection.find_one(ObjectId(fid))
        if not form:
            return 'No results'
        form['_id'] = str(form['_id'])
        return form

    def get_all_forms(self):
        with self.form_collection.find({}) as forms:
            result = []
            for form in forms:
                form['_id'] = str(form['_id'])
                result.append(form)
        return result

    def add_form(self, form):
        fid = self.form_collection.insert_one(form).inserted_id
        return str(fid)

    def update_one_form(self, fid, updates):
        updates = {'$set': updates}
        self.form_collection.update_one({'_id': ObjectId(fid)}, updates)

    def delete_one_form(self, fid):
        self.form_collection.delete_one({'_id': ObjectId(fid)})
        return True

    def delete_all_forms(self):
        self.form_collection.delete_many({})
        return True


form = FormCollection()

