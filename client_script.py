import threading, time
import random
from bson.son import SON
import numpy as np
import math
import math_utils.math_utils
from pymongo import MongoClient



#generates random order parameters
def random_order(map_collection, client_collection, max_pass_amount):
    map_size = map_collection.count()
    rand_element = random.randint(0, map_size)
    source = map_collection.find()[rand_element]
    source_id = source['_id']
    source_coord = [source['Latitude'],source['Longitude']]
    rand_element = random.randint(0, map_size)
    destination = map_collection.find()[rand_element]
    destination_id = destination['_id']
    destination_coord = [destination['Latitude'],destination['Longitude']]
    clients_amount = client_collection.count()
    rand_element = random.randint(0, clients_amount)
    client_id = (client_collection.find()[rand_element])['_id']
    pass_amount = random.randint(1,max_pass_amount)
    return [source_coord, destination_coord, source_id, destination_id, client_id, pass_amount]

def is_start():
    t = random.randint(0, 100)
    if t>50:
        return True
    return False



#inserts order info in DB
def insert_order(db, order, price, distance):
    from db_utils.db_functions import insert_new_order
    inserted_order = insert_new_order(db, order, price, distance)

    return inserted_order.inserted_id

#finds the best car according to rank and distance
def find_car(db, order):
    coordx = str(order[0][0])
    coordy = str(order[0][1])

    from db_utils.db_functions import get_nearest_driver
    ans = get_nearest_driver(db, coordx, coordy)

    from math_utils.math_utils import get_best_driver
    driver = get_best_driver(np, ans)

    return [driver['obj']['_id'], driver['dis']]


# changes information about chosen car
def start_trip(db, driver_id):
    from db_utils.db_functions import update_driver_start_trip
    update_driver_start_trip(db, driver_id)




# inserts information about finished trip
def end_trip(db, driver_id, order_id, order):
    from db_utils.db_functions import update_driver_end_trip
    update_driver_end_trip(db, driver_id, order_id, order)

    from db_utils.db_functions import update_order_end_trip
    update_order_end_trip(db, order_id, driver_id)


def trip(db,collection,client_collection):
    order = random_order(collection, client_collection, 4)
    price, distance = math_utils.math_utils.calculate_trip_param(order)
    order_id = insert_order(db, order, price, distance)
    [driver_id, driver_dist] = find_car(db, order)
    
    from math_utils.math_utils import get_trip_length
    trip_length = get_trip_length(driver_dist, distance)

    start_trip(db, driver_id)
    print "trip started"
    print trip_length
    time.sleep(trip_length)
    end_trip(db, driver_id, order_id, order)
    print str(trip_length) + "_done"


def single_trip():
    client = MongoClient()
    db = client.taxidb
    collection = db.location
    client_collection = db.clients
    trip(db,collection,client_collection)


single_trip()




