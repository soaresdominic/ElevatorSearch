class KnowledgeBase:
    
    def __init__(self, people, elevators):
        self.serviceMap = self.makeServiceMap(people, elevators)
        self.initFloors = self.getInitFloors(people)
        self.commonFloor = 5
        self.numPeople = len(people)

    def getInitFloors(self, people):
        initFloors = {}
        for person in people:
            initFloors[person.name] = person.startFloor
        return initFloors


    def makeServiceMap(self, people, elevators):
        serviceM = {}
        for person in people:  #for each person
            serviceM[person.name] = [[] for i in range(3)]  #start and end, start only, end only
            for elevator in elevators:  #for each elevator
                if((person.startFloor in elevator.services) and (person.goalFloor in elevator.services)):  #if the elevator services both
                    serviceM[person.name][0].append(elevator.name)  #append to start and end
                if(person.startFloor in elevator.services and not(person.goalFloor in elevator.services)):  #if elevator just services the start floor
                    serviceM[person.name][1].append(elevator.name)  #append to start
                if(not(person.startFloor in elevator.services) and (person.goalFloor in elevator.services)):  #if elevator just services the end floor
                    serviceM[person.name][2].append(elevator.name)  #append to start
        return serviceM


    def printMap(self):
        for key,value in self.serviceMap.items():
            print(key, value)



