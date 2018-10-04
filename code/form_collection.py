from flask import Flask, jsonify, request
from pymongo import MongoClient


access_url = '192.168.99.100:32768'

class FormCollection:

    client = None
    db = None
    form_collection = None

    def __init__(self):
        self.client = MongoClient(access_url)
        self.db = self.client.cidev_db
        self.form_collection = self.db.form_collection

    def get_one_form(self, name, author):
        form = self.form_collection.find_one({'name': name, 'author': author})
        
        if not form:
            return 'No results'

        del form['_id']
    	
        return form
    
    def get_all_forms(self):
        forms = self.form_collection.find({})
        
        result = []
        for form in forms:
        	result.append(form)

        return result
    	
    def add_form(self, form):

        self.form_collection.insert_one(form)
        return True

    def update_one_form(self, name='Hei', author='Blei', updates={'key1': 'arg1', 'key2': 'arg2'}):
        updates = {'$set': updates}
        form = self.form_collection.update_one({'name': name, 'author': author}, updates, True) 

    def delete_one_form(self, name, author):
        self.form_collection.delete_one({'name': name, 'author': author})
        return True

    def delete_all_forms(self):
        self.form_collection.delete_many({})
        return True    
