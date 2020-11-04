import pymongo

def mongoConnection(Server_address,dbname,username,password):
    client = pymongo.MongoClient(Server_address)
    db = client[dbname]
    db.authenticate(username,password)
    return db
