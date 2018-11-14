from bson.objectid import ObjectId
from bson.errors import InvalidId



def catch_invalid_id(form_operator):
    def catch_wrapper(*args):
        try:
            return form_operator(*args)
        except InvalidId:
            raise ValueError('{} is not a valid ID. '.format(args[1]))
    return catch_wrapper


class FormCollection:

    def __init__(self, client):
        self.client = client
        self.db = self.client.cidev_db
        self.form_collection = self.db.form_collection

    @catch_invalid_id
    def get_one_form(self, fid):
        form = self.form_collection.find_one(ObjectId(fid))
        if not form:
            raise ValueError('Form with id {} does not exist'.format(fid))
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

    @catch_invalid_id
    def update_one_form(self, fid, updates):
        updates = {'$set': updates}
        update_res = self.form_collection.update_one({'_id': ObjectId(fid)}, updates)
        if update_res.matched_count == 0:
            raise ValueError('Form with id {} does not exist'.format(fid))

    @catch_invalid_id
    def delete_one_form(self, fid):
        del_res = self.form_collection.delete_one({'_id': ObjectId(fid)})
        if del_res.deleted_count == 0:
            raise ValueError('Form with id {} does not exist'.format(fid))

    def delete_all_forms(self):
        self.form_collection.delete_many({})
        return True



