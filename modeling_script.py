import client_script
from pymongo import MongoClient
import threading, time

def start_modeling(tripsamount, pause_duration, trip_increment, trip_max_number):


    #trip(db,collection,client_collection)
    #thread = threading.Thread(target=trip, args=(db,collection,client_collection))
    #thread.start()
    while True:
        if tripsamount < trip_max_number:
            if (client_script.is_start()):
                #print "trip started"
                #thread = threading.Thread(target=client_script.trip, args=(db, collection, client_collection))
                thread = threading.Thread(target=client_script.trip, args=())
                thread.start()
                time.sleep(pause_duration)
                tripsamount += trip_increment
            else:
                #print "trip not started"
                time.sleep(pause_duration)
        else:
            break




#timex = time.time()
tripsamount = 0
pause_duration = 0.1
trip_increment = 1
trip_max_number = 100
start_modeling(tripsamount, pause_duration, trip_increment, trip_max_number)
#print "\n"
#print time.time() - timex