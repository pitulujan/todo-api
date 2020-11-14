from pymongo import MongoClient


def get_conn(username, password, db_name):
    client = MongoClient(
        "mongodb+srv://{}:{}@cluster0.jqc5t.mongodb.net/{}?retryWrites=true&w=majority".format(
            os.environ["MONGO_USER"], os.environ["MONGO_PASS"], os.environ["MONGO_DB"]
        )
    )
    db = client.tasks
    return db
