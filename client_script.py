import threading, time
import random
def my_threaded_func(arg, arg2):
    print "Running thread! Args:", (arg, arg2)
    time.sleep(10)
    print "Done!"

#thread = threading.Thread(target=my_threaded_func, args=("I'ma", "thread"))
#thread.start()
#print "Spun off thread"



#db.getCollection('places').stats()
#collection.stats()

#for obj in collection.find():
    #print obj['Latitude']

#obj = next(result, None)
#if obj:
  #username= obj['username']
  #print username



"""
from pymongo import MongoClient

#client = MongoClient('...', 27017)
client = MongoClient()
db = client.places
#db = client['...']
collection = db.places
#collection = db["..."]
#result = collection.find()

stats = collection.count()
print stats

print db.command("collstats", "places")
"""














def generate_order(collection):
    map_size = collection.count()
    print random.randint(0, map_size)
    #coordinates = collection.


from pymongo import MongoClient
client = MongoClient()
db = client.places
collection = db.places
generate_order(collection)