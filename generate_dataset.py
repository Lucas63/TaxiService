import random
import time

def generate_rank():
    t = random.randint(0, 100)
    #print t
    if t>50:
        return 5
    if t > 25:
        return 4
    if t > 10:
        return 3
    if t > 5:
        return 2
    return 1



drivers = []
with open('drivers.csv') as f:
    iterf = iter(f)
    for line in iterf:
        data = line.split(',')
        drivers.append([data[0].replace(' ','_'),data[1],data[2],data[3],data[4],data[5],data[6],data[7],data[8],data[9]])
passangers = []
with open('people.csv') as f:
    iterf = iter(f)
    for line in iterf:
        data = line.split(',')
        passangers.append([data[0].replace(' ','_'),data[1],data[2]])
locations = []
with open("Places.csv") as f:
    iterf = iter(f)
    for line in iterf:
        data = line.split(',')
        locations.append([(float)(data[0]),(float)(data[1]),data[2].replace('\n','')])

start_time = time.time()
f = output = open('output_small.csv', "a")

for i in xrange(100000):
    src = random.randint(0, len(locations)-1)
    while True:
        dest = random.randint(0, len(locations)-1)
        from math_utils.math_utils import distance_on_unit_sphere
        distance = 1000*distance_on_unit_sphere(locations[src][0],locations[src][1],locations[dest][0],locations[dest][1])
        distance = int(distance)
        if distance > 2500:
            #print distance
            break
        #print "bad_dist" + str(i) +'\n'
        #print distance
    driver = random.randint(0, len(drivers)-1)
    passang = random.randint(0, len(passangers)-1)
    rank = generate_rank()
    string = "pass_name:"+ passangers[passang][0]+",pass_phone:"+str(passangers[passang][1])+",srclat:" + str(locations[src][0])+",srclong:" + str(locations[src][1])+",destlat:" + str(locations[dest][0])+",destlong:" + str(locations[dest][1])+",srcdistrict:" + str(locations[src][2])+",destdistrict:" + str(locations[dest][2])+",driverid:" + str(drivers[driver][4])+",distance:" + str(distance)+",rank:" + str(rank)+'\n'
    print string
    f.write(string)
f.close()
print time.time() - start_time





















