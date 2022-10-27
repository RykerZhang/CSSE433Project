from pymongo import MongoClient

Mclient = MongoClient("mongodb://433-34.csse.rose-hulman.edu:27017")
db = Mclient['test']
testCol = db['test']
print(testCol.find({}))
testCol.delete_many({})