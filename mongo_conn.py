from pymongo import MongoClient

def get_conn(username, password,db_name):
    client = MongoClient("mongodb+srv://{}:{}@cluster0.jqc5t.mongodb.net/{}?retryWrites=true&w=majority".format(username,password,db_name))
    db = client.tasks
    return db