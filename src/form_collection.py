from pymongo import MongoClient
from bson.objectid import ObjectId
from bson.errors import InvalidId

def is_valid_object_id(obj_id):
    try:
        wid = ObjectId(obj_id)
        return True
    except InvalidId:
        return False


access_url = 'forms-editor-datastore:27017'


class FormCollection:

    def __init__(self):
        self.client = MongoClient(access_url)
        self.db = self.client.cidev_db
        self.form_collection = self.db.form_collection

    def get_one_form(self, fid):
        if not is_valid_object_id(fid):
            raise ValueError
        form = self.form_collection.find_one(ObjectId(fid))
        if not form:
            raise ValueError
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
        if not is_valid_object_id(fid):
            raise ValueError
        updates = {'$set': updates}
        update_res = self.form_collection.update_one({'_id': ObjectId(fid)}, updates)
        if update_res.matched_count == 0:
            raise ValueError

    def delete_one_form(self, fid):
        if not is_valid_object_id(fid):
            raise ValueError
        del_res = self.form_collection.delete_one({'_id': ObjectId(fid)})
        if del_res.deleted_count == 0:
            raise ValueError

    def delete_all_forms(self):
        self.form_collection.delete_many({})
        return True


form = FormCollection()

