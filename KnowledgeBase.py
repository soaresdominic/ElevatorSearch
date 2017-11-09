



class KnowledgeBase:
    
    def __init__(self, people, elevators, numPeople):
        self.serviceMap = self.makeServiceMap(people, elevators)
        self.numPeople = numPeople
        self.initFloors = self.getInitFloors(people)
        self.commonFloor = 5

        #self.people = self.makePeopleList(people)  #dictionary of people name, status as employee, guest, vip

    """
    def makePeopleList(self, people):
        pd = {}
        for person in people:
            if(pd[person[2]] == None):
                pd[person[2]] = person[1]
        return pd
    """

    def getInitFloors(self, people):
        initFloors = {}
        for person in people:
            initFloors[person.name] = person.currentFloor
        return initFloors


    def makeServiceMap(self, people, elevators):
        serviceM = {}
        for person in people:  #for each person
            serviceM[person.name] = [[] for i in range(3)]  #start and end, start only, end only
            for elevator in elevators:  #for each elevator
                if((person.currentFloor in elevator.services) and (person.goalFloor in elevator.services)):  #if the elevator services both
                    serviceM[person.name][0].append(elevator)  #append to start and end
                elif(person.currentFloor in elevator.services):  #if elevator services the start floor
                    for el in elevators:  #for each elevator
                        #if it services the goal floor and a floor in common, add them to the respective lists
                        if(person.goalFloor in el.services):
                            if(bool(set(el.services) and set(elevator.services))):  #if they have a common floor number
                                serviceM[person.name][1].append(elevator)  #append the first elevator to the start list
                                serviceM[person.name][2].append(el)  #append the second elevator to the goal list
        return serviceM



    def printMap(self):
        for key,value in self.serviceMap.items():
            print(key, value)



