import math





def calculate_trip_param(order):
    distance = 1000*distance_on_unit_sphere(order[0][0],order[0][1],order[1][0],order[1][1])
    price = max(40, (25 + 5 * distance / 1000))
    return price, distance

def distance_on_unit_sphere(lat1, long1, lat2, long2):
    # approximate radius of earth in km
    R = 6373.0

    lat1 = math.radians(lat1)
    lon1 = math.radians(long1)
    lat2 = math.radians(lat2)
    lon2 = math.radians(long2)

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    distance = R * c
    return distance


def get_best_driver(np, ans):
    return ans['results'][np.argmin(map(lambda x: (x['dis']) / ((x['obj']['Rank']) ^ 2), ans['results']))]

def get_trip_length(driver_dist, distance):
    return (driver_dist / 1000 + distance) / 1000