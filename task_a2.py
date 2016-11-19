import simpy
import random
import math

def generateEvent(outcomes):
    res = random.random()
    cur_p = 0
    for outcome in outcomes:
        cur_p += outcomes[outcome]
        if cur_p >= res:
            return outcome

class DiningRoom(object):
    def __init__(self, hotFoodWorkers=1, coldFoodWorkers=1, beverageWorkers=1, cashWorkers=1):
        self.env = simpy.Environment()
        self.hotFood = simpy.Resource(self.env, capacity=hotFoodWorkers)
        self.coldFood = simpy.Resource(self.env, capacity=coldFoodWorkers)
        self.beverage = simpy.Resource(self.env, capacity=beverageWorkers)
        self.cash = simpy.Resource(self.env, capacity=cashWorkers)

class Stat(object):
    def __init__(self, diningRoom, initTime, student_id):
        self.diningRoom = diningRoom
        self.id = student_id
        self.action = diningRoom.env.process(self.run(initTime))

class Student(object):
    def __init__(self, diningRoom, initTime, student_id):
        self.diningRoom = diningRoom
        self.id = student_id
        self.action = diningRoom.env.process(self.run(initTime))

    def run(self, initTime):
        yield self.diningRoom.env.timeout(initTime)
        #choose way
        way = generateEvent({'hot_food': 0.8, 'cold_food': 0.15, 'beverage': 0.05})
        print("{} : {} Start process: {}".format(self.diningRoom.env.now, self.id, way))
        #time for cash
        cashTime = 0
        if way == 'hot_food':
            with self.diningRoom.hotFood.request() as req:
                print("{} : {} task hot_food wait".format(self.diningRoom.env.now, self.id))
                yield req
                hotFoodDelay = random.uniform(25, 60)
                print("{} : {} task hot_food service {}".format(self.diningRoom.env.now, self.id, hotFoodDelay))
                yield self.diningRoom.env.timeout(hotFoodDelay)
                print("{} : {} task hot_food complete".format(self.diningRoom.env.now, self.id))    
                cashTime += random.uniform(20, 40)
        
        if way == 'cold_food':
            with self.diningRoom.coldFood.request() as req:
                print("{} : {} task cold_food wait".format(self.diningRoom.env.now, self.id))
                yield req
                coldFoodDelay = random.uniform(60, 180)
                print("{} : {} task cold_food service {}".format(self.diningRoom.env.now, self.id, coldFoodDelay))
                yield self.diningRoom.env.timeout(coldFoodDelay)
                print("{} : {} task cold_food complete".format(self.diningRoom.env.now, self.id))    
                cashTime += random.uniform(5, 15)
        
        with self.diningRoom.beverage.request() as req:
            print("{} : {} task beverage wait".format(self.diningRoom.env.now, self.id))
            yield req
            beverageDelay = random.uniform(5, 20)
            print("{} : {} task beverage service {}".format(self.diningRoom.env.now, self.id, beverageDelay))
            yield self.diningRoom.env.timeout(beverageDelay)
            print("{} : {} task beverage complete".format(self.diningRoom.env.now, self.id))    
            cashTime += random.uniform(5, 10)

        with self.diningRoom.cash.request() as req:
            print("{} : {} task cash wait".format(self.diningRoom.env.now, self.id))
            yield req
            print("{} : {} task cash service {}".format(self.diningRoom.env.now, self.id, cashTime))
            yield self.diningRoom.env.timeout(cashTime)
            print("{} : {} task cash complete".format(self.diningRoom.env.now, self.id))      
   
def generateGroup(diningRoom, time, student_id):
    count = generateEvent({1: 0.5, 2 : 0.3, 3 : 0.1, 4 : 0.1})
    for i in range(count):
        Student(diningRoom, time, student_id)
        student_id += 1
    return student_id

def generateExp(e):
    return - e * math.log(random.random())

if __name__ == '__main__':
    init_time = 0
    end_time = 2 * 60 * 60
    cur_time = init_time
    expectedValueGroups = 30
    diningRoom = DiningRoom()
    cur_student_id = 0
    while cur_time <= end_time:
        cur_time += generateExp(expectedValueGroups)
        if cur_time > end_time:
            break
        cur_student_id = generateGroup(diningRoom, cur_time, cur_student_id)
    diningRoom.env.run()