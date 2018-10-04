from flask import Flask, jsonify, request
from pymongo import MongoClient


access_url = '192.168.99.100:32768'

class PersonCollection:
