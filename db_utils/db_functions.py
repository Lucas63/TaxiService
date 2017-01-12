from pymongo import MongoClient
global client
client = MongoClient()
global db
db = client.taxidb
global collection
collection = db.location
global client_collection
client_collection = db.clients




def update_driver_start_trip(db, driver_id):
    db.driver.update_one({
        '_id': driver_id
    }, {
        '$set': {
            'is_free': 0
        }
    }, upsert=False)


# TODO: merge functions
def update_driver_end_trip(db, driver_id, order_id, order):
    db.driver.update_one({
        '_id': driver_id
    }, {
        '$push': {
            'Orders': "ObjectId(" + '"' + str(order_id) + '"' + ")"
        }
    }, upsert=False)
    db.driver.update_one({
        '_id': driver_id
    }, {
        '$set': {
            'is_free': 1,
            'Latitude': order[1][0],
            'Longitude': order[1][1],
            'location.coordinates': order[1]
        }
    }, upsert=False)


def update_order_end_trip(db, order_id, driver_id):
    db.order.update_one({
        '_id': order_id
    }, {
        '$set': {
            'Status': "done",
            'Driver': driver_id
        }
    }, upsert=False)



def insert_new_order(db, order, price, distance):
    inserted_order = db.order.insert_one(
        {
            'Start': order[2],
            'Finish': order[3],
            'Client': order[4],
            'Price': price,
            'Distance': distance,
            'Status': "processing",
            'Pass_amount': order[5]
        })
    return inserted_order


def get_nearest_driver(db, coordx, coordy,driversamount,max_distance):
    return db.eval("get_drivers(" + coordy + ", " + coordx + ", " + max_distance + ", " + driversamount + ")")






#initial functions

def insert_passanger(name, telephone, email, db):
    result = db.clients.insert_one(
        {
            "Name": name,
            "Telephone": telephone,
            "Email": email
        }
    )
    return result

def insert_driver(name, Latitude, Longitude, smoker, number, car_type, mode, capacity, rank, is_free, db):
    result = db.driver.insert_one(
        {
            "Name": name,
            "Latitude": Latitude,
            "Longitude": Longitude,
            "Smoker": smoker,
            "Number": number,
            "Type": car_type,
            "Mode": mode,
            "Capacity": capacity,
            "Rank": rank,
            "is_free": is_free,
            "Orders": [],
            "location": {
                "type": "Point",
                "coordinates": [Longitude, Latitude]
            }
        }
    )
    return result

def insert_place(Latitude, Longitude, district, db):
    result = db.location.insert_one(
        {
            "Latitude": Latitude,
            "Longitude": Longitude,
            "District": district,
            "location": {
                "type": "Point",
                "coordinates": [Longitude, Latitude]
            }
        }
    )
    return result
