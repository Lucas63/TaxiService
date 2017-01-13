import threading, time
import random
from bson.son import SON
import numpy as np
import math
import math_utils.math_utils
from pymongo import MongoClient
from config import minute_length
#import modeling_script
import db_utils.db_functions

#DONE: abs(source-dest)>eps
#generates random order parameters
def random_order(map_collection, client_collection, max_pass_amount):
    map_size = map_collection.count()
    rand_element = random.randint(0, map_size)
    source = map_collection.find()[rand_element]
    source_id = source['_id']
    source_coord = [source['Latitude'],source['Longitude']]
    while True:
        rand_element = random.randint(0, map_size)
        destination = map_collection.find()[rand_element]
        destination_id = destination['_id']
        destination_coord = [destination['Latitude'], destination['Longitude']]
        from math_utils.math_utils import distance_on_unit_sphere
        distance = 1000 * distance_on_unit_sphere(source_coord[0], source_coord[1], destination_coord[0],destination_coord[1])
        distance = int(distance)
        if distance > 2500:
            break
    clients_amount = client_collection.count()
    rand_element = random.randint(0, clients_amount)
    client_id = (client_collection.find()[rand_element])['_id']
    pass_amount = random.randint(1,max_pass_amount)
    return [source_coord, destination_coord, source_id, destination_id, client_id, pass_amount]

def is_start():
    t = random.randint(0, 100)
    #print t
    if t>30:
        return True
    return False



#inserts order info in DB
def insert_order(db, order, price, distance):
    from db_utils.db_functions import insert_new_order
    inserted_order = insert_new_order(db, order, price, distance)

    return inserted_order.inserted_id

#DONE: specify selected drivers amount
#finds the best car according to rank and distance
def find_car(db, order):
    coordx = str(order[0][0])
    coordy = str(order[0][1])
    driversamount = "25"
    max_distance = "3500"
    from db_utils.db_functions import get_nearest_driver

    while True:
        ans = get_nearest_driver(db, coordx, coordy,driversamount,max_distance)
        #print (len(ans['results']))
        if len(ans['results']) > 0:
            break
        time.sleep(1)


    from math_utils.math_utils import get_best_driver
    driver = get_best_driver(np, ans)

    return [driver['obj']['_id'], driver['dis']]


# changes information about chosen car
def start_trip(db, driver_id):
    from db_utils.db_functions import update_driver_start_trip
    update_driver_start_trip(db, driver_id)

# changes information about chosen car
def move_to_passanger(db, driver_id):
    from db_utils.db_functions import update_driver_move_to_client
    update_driver_move_to_client(db, driver_id)


# inserts information about finished trip
def end_trip(db, driver_id, order_id, order):
    from db_utils.db_functions import update_driver_end_trip
    update_driver_end_trip(db, driver_id, order_id, order)

    from db_utils.db_functions import update_order_end_trip
    update_order_end_trip(db, order_id, driver_id)

#DONE: trip status moving to client
def trip():
    """
    order = random_order(collection, client_collection, 4)
    price, distance = math_utils.math_utils.calculate_trip_param(order)
    order_id = insert_order(db, order, price, distance)

    #TODO: distance from mongo function
    [driver_id, driver_dist] = find_car(db, order)
    
    from math_utils.math_utils import get_trip_length
    trip_length = get_trip_length(driver_dist, distance)

    start_trip(db, driver_id)
    #print "trip started"
    print trip_length

    time.sleep(trip_length*minute_length)
    end_trip(db, driver_id, order_id, order)
    print str(trip_length) + "_done"
    """
    order = random_order(db_utils.db_functions.collection, db_utils.db_functions.client_collection, 4)
    price, distance = math_utils.math_utils.calculate_trip_param(order)
    order_id = insert_order(db_utils.db_functions.db, order, price, distance)

    # TODO: distance from mongo function
    [driver_id, driver_dist] = find_car(db_utils.db_functions.db, order)

    from math_utils.math_utils import get_trip_to_pass
    trip_length = get_trip_to_pass(driver_dist)
    move_to_passanger(db_utils.db_functions.db, driver_id)
    print trip_length
    time.sleep(trip_length * minute_length)


    from math_utils.math_utils import get_trip_with_pass
    trip_length = get_trip_with_pass(distance)
    start_trip(db_utils.db_functions.db, driver_id)
    print trip_length
    time.sleep(trip_length * minute_length)


    end_trip(db_utils.db_functions.db, driver_id, order_id, order)
    print str(trip_length) + "_done"

def single_trip():
    client = MongoClient()
    db = client.taxidb
    collection = db.location
    client_collection = db.clients
    trip()



#single_trip()



