import random
from pymongo import MongoClient



def generate_names(names_file, surnames_file, amount):
    ans = []
    names = []
    with open(names_file) as f:
        iterf = iter(f)
        for line in iterf:
            data = line.split('\r')
            for i in xrange(len(data)):
                names.append(data[i])
    surnames = []
    with open(surnames_file) as f:
        iterf = iter(f)
        for line in iterf:
            data = line.split('\r')
            for i in xrange(len(data)):
                surnames.append(data[i])
    first_size = len(names)
    last_size = len(surnames)
    for i in xrange(amount):
        first_num = random.randint(0, first_size - 1)
        last_num = random.randint(0, last_size - 1)
        selected_name = names[first_num]
        selected_surname = surnames[last_num]
        ans.append(selected_name + " " + selected_surname)
    return ans


def insert_drivers(names, numbers, db, map_size):
    ans =[]
    from db_utils.db_functions import insert_driver
    for i in xrange(len(names)):
        rand_element = random.randint(0, map_size)
        collection = db.location
        source = collection.find()[rand_element]
        #source_coord = [source['Latitude'], source['Longitude']]

        Latitude = source['Latitude']
        Longitude = source['Longitude']
        name = names[i]
        smoker = random.randint(0, 1)
        car_type = random.randint(0, 5)
        mode = random.randint(0, 3)
        capacity = random.randint(4, 5)
        rank = 5
        is_free = 1
        number = numbers[i]
        ans.append(insert_driver(name, Latitude, Longitude, smoker, number, car_type, mode, capacity, rank, is_free, db))
        #line = name + Latitude + Longitude + smoker + number + car_type + mode + capacity + rank + is_free + orders
    return ans



def insert_passangers(names, telephones, db):
    from db_utils.db_functions import insert_passanger
    ans = []
    for i in xrange(len(names)):
        email = names[i].replace(" ", "")+"@gmail.com"
        ans.append(insert_passanger(names[i], (int)("38099"+str(telephones[i])), email, db))
    return ans

def read_places(places_file):
    lat = []
    long = []
    district = []
    with open(places_file) as f:
        iterf = iter(f)
        for line in iterf:
            data = line.split(',')
            lat.append((float)(data[0]))
            long.append((float)(data[1]))
            district.append(data[2])
    return lat, long, district

def insert_places(lat, long, district, db):
    from db_utils.db_functions import insert_place
    ans = []
    for i in xrange(len(lat)):
        ans.append(insert_place(lat[i], long[i], district[i], db))
    return ans



def initial(places_file, names_file, surnames_file, drivers_amount, passangers_amount):
    import time
    start_time = time.time()

    from pymongo import MongoClient
    client = MongoClient()
    db = client.taxidb
    lat, long, district = read_places(places_file)
    names = generate_names(names_file, surnames_file, drivers_amount + passangers_amount)
    car_numbers = random.sample(xrange(1000000, 9999999), drivers_amount)
    driver_names = names[0:drivers_amount]
    pass_names = names[drivers_amount:drivers_amount + passangers_amount]
    pass_telephones = random.sample(xrange(1000000, 9999999), passangers_amount)

    print "initial "
    print time.time() - start_time
    start_time = time.time()

    places_ids = insert_places(lat, long, district, db)

    print "places "
    print time.time() - start_time
    start_time = time.time()

    passangers_ids = insert_passangers(pass_names, pass_telephones, db)

    print "passangers "
    print time.time() - start_time
    start_time = time.time()

    map_size = len(places_ids)
    drivers_ids = insert_drivers(driver_names, car_numbers, db, map_size)

    print "map "
    print time.time() - start_time

    return places_ids, passangers_ids, drivers_ids



places_file = "Places.csv"
names_file = "First.csv"
surnames_file = "Last.csv"
drivers_amount = 10000
passangers_amount = 500000

places_ids, passangers_ids, drivers_ids = initial(places_file, names_file, surnames_file, drivers_amount, passangers_amount)

















"""
drivers_amount = 10000
passangers_amount = 500000


names = generate_names('First.csv', 'Last.csv', drivers_amount + passangers_amount)
car_numbers = random.sample(xrange(1000000,9999999), drivers_amount)
driver_names = names[0:drivers_amount-1]
pass_names = names[passangers_amount:drivers_amount + passangers_amount-1]
pass_telephones = random.sample(xrange(1000000,9999999), passangers_amount)
#####
from pymongo import MongoClient
client = MongoClient()
db = client.places
collection = db.places
map_size = collection.count()
#####
"""

















