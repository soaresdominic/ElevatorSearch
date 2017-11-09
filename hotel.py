from elevator import elevator
from person import person
from floor import floor
from KnowledgeBase import KnowledgeBase
import heapq
import copy


class hotel:
    def __init__(self,numFloors,numElevators,numPeople):
        #floors are a list of 2 lists that contains 0-n elevators, 0-n people, secure boolean
        #floors are contained in larger list
        self.floors = []
        for i in range(1, numFloors+1):
            if(i == 4 or i == 6 or i == 7):
                f = floor(i, True)
            else:
                f = floor(i, False)
            self.floors.append(f)
        
        e1 = elevator(5, [1,2,3,4,5,6], "e1", 1)
        e2 = elevator(8, [1,2,3,4,5,6], "e2", 1)
        e3 = elevator(3, [3,5,7,8,9,10], "e3", 10)
        e4 = elevator(5, [5,6,7,8,9,10], "e4", 10)
        elevators = []
        elevators.append(e1)
        elevators.append(e2)
        elevators.append(e3)
        elevators.append(e4)
        for e in elevators:
            self.floors[e.currentFloor-1].elevators.append(e)
            
        p1 = person(1, "v", "p1", 10)
        p2 = person(7, "e", "p2", 6)
        p3 = person(3, "e", "p3", 9)
        p4 = person(7, "e", "p4", 8)
        p5 = person(2, "e", "p5", 7)
        p6 = person(4, "e", "p6", 1)
        p7 = person(3, "e", "p7", 1)
        p8 = person(1, "e", "p8", 9)
        p9 = person(10, "e", "p9", 5)
        p10 = person(1, "e", "p10", 6)
        p11 = person(1, "e", "p11", 3)
        p12 = person(1, "e", "p12", 4)
        p13 = person(6, "e", "p13", 2)
        p14 = person(8, "v", "p14", 1)
        p15 = person(9, "g", "p15", 2)
        p16 = person(2, "e", "p16", 1)
        p17 = person(5, "e", "p17", 7)
        p18 = person(1, "g", "p18", 10)
        p19 = person(1, "e", "p19", 9)
        p20 = person(1, "g", "p20", 7)
        people = []
        people.append(p1)
        people.append(p2)
        people.append(p3)
        people.append(p4)
        people.append(p5)
        
        people.append(p6)
        people.append(p7)
        people.append(p8)
        people.append(p9)
        people.append(p10)
        
        people.append(p11)
        people.append(p12)
        people.append(p13)
        people.append(p14)
        people.append(p15)
        people.append(p16)
        
        people.append(p17)
        people.append(p18)
        people.append(p19)
        people.append(p20)
        
        for p in people:
            self.floors[p.currentFloor-1].occupants.append(p)

        self.KB = KnowledgeBase(people, elevators, numPeople)
        self.KB.printMap()
        #exit()


    def findMoves(self):
        moves = []

        #move elevator
        floorNum = 1
        for floor in self.floors:
            eNum = 0
            for e in floor.elevators:
                if(e.currentFloor > 1 and (e.currentFloor - 1 >= min(e.services))):  #move down
                    moveS = ("move " + e.name + " from floor " + str(floorNum) + " to " + str(floorNum - 1))
                    newState = copy.deepcopy(self)
                    el = newState.floors[floorNum-1].elevators.pop(eNum)  #delete elevator from floor
                    el.currentFloor -= 1
                    newState.floors[floorNum-2].elevators.append(el)  #append it to floor below
                    moves.append([newState, moveS])
                if(e.currentFloor < 10 and (e.currentFloor + 1 <= max(e.services))):  #move up
                    moveS = ("move " + e.name + " from floor " + str(floorNum) + " to " + str(floorNum + 1))
                    newState = copy.deepcopy(self)
                    el = newState.floors[floorNum-1].elevators.pop(eNum)  #delete elevator from floor
                    el.currentFloor += 1
                    newState.floors[floorNum].elevators.append(el)  #append it to floor above
                    moves.append([newState, moveS])
                eNum += 1
            floorNum += 1


        #load person
        floorNum = 1
        for floor in self.floors:  #for each floor
            if(len(floor.elevators) > 0 and len(floor.occupants) > 0):  #if theres an elevator on the floor and people waiting on the floor
                pNum = 0
                for person in floor.occupants:  #for each person on the floor
                    if(not(person.goalFloor == floor.number)):
                        if(len(self.KB.serviceMap[person.name][0]) > 0):  #if the person has an elevator to take it all the way
                            eNum = 0
                            for elevator in floor.elevators:  #for each elevator on the floor
                                if(elevator in self.KB.serviceMap[person.name][0] and floor.number in elevator.services):  #if the elevaor is in that list
                                    moveS = ("add person " + person.name + " to " + elevator.name)
                                    newState = copy.deepcopy(self)
                                    p = newState.floors[floor.number-1].occupants.pop(pNum)  #delete person waiting on the floor
                                    p.currentFloor = -1
                                    newState.floors[floor.number-1].elevators[eNum].occupants.append(p)
                                    newState.floors[floor.number-1].elevators[eNum].currentOccupancy += 1
                                    #print(newState.getHeur())
                                    moves.append([newState, moveS])
                                eNum += 1
                        else:  #they have to take at least two
                            goalF = 0
                            eNum = 0
                            for elevator in floor.elevators:  #for each elevator on the floor
                                if(elevator in self.KB.serviceMap[person.name][2] and floor.number in elevator.services):  #if the elevaor is in goal list
                                    moveS = ("add person " + person.name + " to " + elevator.name)
                                    newState = copy.deepcopy(self)
                                    p = newState.floors[floor.number-1].occupants.pop(pNum)  #delete person waiting on the floor
                                    p.currentFloor = -1
                                    newState.floors[floor.number-1].elevators[eNum].occupants.append(p)
                                    newState.floors[floor.number-1].elevators[eNum].currentOccupancy += 1
                                    #print(newState.getHeur())
                                    moves.append([newState, moveS])
                                    goalF = 1
                                eNum += 1
                            eNum = 0
                            if(goalF == 0):
                                for elevator in floor.elevators:  #for each elevator on the floor
                                    if(elevator in self.KB.serviceMap[person.name][1] and floor.number in elevator.services):  #if the elevaor is in start list
                                        moveS = ("add person " + person.name + " to " + elevator.name)
                                        newState = copy.deepcopy(self)
                                        p = newState.floors[floor.number-1].occupants.pop(pNum)  #delete person waiting on the floor
                                        p.currentFloor = -1
                                        newState.floors[floor.number-1].elevators[eNum].occupants.append(p)
                                        newState.floors[floor.number-1].elevators[eNum].currentOccupancy += 1
                                        #print(newState.getHeur())
                                        moves.append([newState, moveS])
                                    eNum += 1
                        pNum += 1




        #if an elevator has a person
            #if that person's goal floor is that floor, offload
            #else if that elevator is not in that persons goal elevators
                #drop him off here


        #offload person
        for floor in self.floors:  #for each floor
            if(len(floor.elevators) > 0):  #if theres an elevator on the floor
                eNum = 0
                for e in floor.elevators:  #for each elevator on the floor
                    if((floor.number in e.services) and e.currentOccupancy > 0):  #if it has people and services the floor
                        pNum = 0
                        for p in e.occupants:  #for each person in the elevator
                            if(p.goalFloor == e.currentFloor and floor.number in e.services):  #if persons goal floor is this floor, offload
                                hasEmployee = False
                                for p in floor.occupants:
                                    if(p.employee):
                                        hasEmployee = True

                                if(not floor.secured or hasEmployee or p.guest == False):
                                    moveS = ("add person " + p.name + " to floor " + str(floor.number))
                                    newState = copy.deepcopy(self)
                                    p = newState.floors[floor.number-1].elevators[eNum].occupants.pop(pNum) #delete person from elevator
                                    p.currentFloor = floor.number
                                    newState.floors[floor.number-1].occupants.append(p)
                                    newState.floors[floor.number-1].elevators[eNum].currentOccupancy -= 1
                                    moves.append([newState, moveS])


                            elif(e not in self.KB.serviceMap[p.name][2] and e not in self.KB.serviceMap[p.name][0] and floor.number in e.services):  #if this elevator is not in that persons goal elevators
                                hasEmployee = False
                                for p in floor.occupants:
                                    if(p.employee):
                                        hasEmployee = True

                                if(not floor.secured or hasEmployee or p.guest == False):
                                    moveS = ("add person " + p.name + " to floor " + str(floor.number))
                                    newState = copy.deepcopy(self)
                                    p = newState.floors[floor.number-1].elevators[eNum].occupants.pop(pNum) #delete person from elevator
                                    p.currentFloor = floor.number
                                    newState.floors[floor.number-1].occupants.append(p)
                                    newState.floors[floor.number-1].elevators[eNum].currentOccupancy -= 1
                                    moves.append([newState, moveS])

                            pNum += 1
                    eNum += 1
        return moves


    def checkForGoal(self):
        numPeople = 0
        for floor in self.floors:
            for person in floor.occupants:
                if(not(person.currentFloor == person.goalFloor)):
                    return False
                else:
                    numPeople += 1
        #print(numPeople, self.KB.numPeople)
        if(numPeople == self.KB.numPeople):
            return True



    def getHeur(self):
        value = 0
        global heurFlag

        if(heurFlag == 0):  #if at beginning - move people with 2 elevators to floor 5
            for floor in self.floors:  #for each floor
                for p in floor.occupants:  #for each person on the floor
                    if(p.vip == True):
                        if(len(self.KB.serviceMap[p.name][0]) == 0):  #they need 2 elevators and are a vip
                            if(floor.number == self.KB.initFloors[p.name]):  #if they are on their intial floor = bad
                                value += 10

                                elevatorFloorNums = []
                                for f in self.floors:  #for each floor
                                    for e in floor.elevators:  #for each elevator
                                        if(e.currentOccupancy < e.capacity and floor.number in e.services):  #if it can load the person
                                            elevatorFloorNums.append(abs(floor.number - f.number))
                                if(len(elevatorFloorNums) > 0):
                                    value += min(elevatorFloorNums)

                            elif(not floor.number == self.KB.initFloors[p.name] and not floor.number == self.KB.commonFloor):  #if they are on some random floor = really bad
                                value += 20
                            elif(floor.number == self.KB.commonFloor):  #if they are on the common floor = good
                                value -= 10
                    else:
                        value -= 100

                for e in floor.elevators:  #for each elevator on the floor
                    for per in e.occupants:  #for each person in the elevator
                        if(per.vip == True):
                            if(len(self.KB.serviceMap[per.name][0]) == 0):  #if they need 2 elevators
                                value += abs(floor.number - self.KB.commonFloor)
                            else:  #if they need 1
                                value += 0  #change if necessary
                        else:
                            value += 200

        ################################################

        if(heurFlag == 1):  #if everyone is on a floor that a goal elevator services
            for floor in self.floors:  #for each floor
                for p in floor.occupants:  #for each person on the floor
                    if(p.vip == True):
                        if(p.goalFloor == floor.number):  #if they are on their goal floor
                            value -= 1000  #goal floor

                        else:
                            if(floor.number == self.KB.initFloors[p.name]):  #if they are on their intial floor
                                value += 300  #still at their start
                            else:  #they are on a middle floor waiting to be picked up
                                value -= abs(self.KB.initFloors[p.name] - floor.number) * 5

                            #move elevators towards this person
                            elevatorFloorNums = []
                            for f in self.floors:  #for each floor
                                for e in floor.elevators:  #for each elevator
                                    if(e.currentOccupancy < e.capacity and floor.number in e.services):  #if it can load the person
                                        elevatorFloorNums.append(abs(floor.number - f.number))
                            if(len(elevatorFloorNums) > 0):
                                value += min(elevatorFloorNums)
                                #print(value) 
                    else:
                        value -= 1000


            for f in self.floors:  #for each floor
                for e in f.elevators:  #for each elevator
                    tmpHigh = []
                    for per in e.occupants:  #for each person in elevator
                        if(per.vip == True):
                            #make it better a person gets in a goal elevator, not much for nothing for non goal
                            if(e in self.KB.serviceMap[per.name][2] or e in self.KB.serviceMap[per.name][0]):  #if its a goal elevator
                                #print("goal elevator")
                                value -= 500  #make it much better that a person gets in an elevator if its a goal elevator but not better than getting off
                            else:
                                value -= 0
                            value += abs(e.currentFloor - per.goalFloor)
                        else:
                            value += 2000

        ##################################################
        ##################################################

        if(heurFlag == 2):  #if at beginning after taking vips - move people with 2 elevators to floor 5
            for floor in self.floors:  #for each floor
                for p in floor.occupants:  #for each person on the floor
                    if(p.vip == False):
                        if(len(self.KB.serviceMap[p.name][0]) == 0):  #they need 2 elevators
                            if(floor.number == self.KB.initFloors[p.name]):  #if they are on their intial floor = bad
                                value += 1000

                                elevatorFloorNums = []
                                for f in self.floors:  #for each floor
                                    for e in floor.elevators:  #for each elevator
                                        if(e.currentOccupancy < e.capacity and floor.number in e.services):  #if it can load the person
                                            elevatorFloorNums.append(abs(floor.number - f.number))
                                if(len(elevatorFloorNums) > 0):
                                    value += min(elevatorFloorNums)

                            elif(not floor.number == self.KB.initFloors[p.name] and not floor.number == self.KB.commonFloor):  #if they are on some random floor = really bad
                                value += 2000
                            elif(floor.number == self.KB.commonFloor):  #if they are on the common floor = good
                                value -= 1000

                for e in floor.elevators:  #for each elevator on the floor
                    for per in e.occupants:  #for each person in the elevator
                        if(per.vip == False):
                            if(len(self.KB.serviceMap[per.name][0]) == 0):  #if they need 2 elevators
                                value += abs(floor.number - self.KB.commonFloor)
                            else:  #if they need 1
                                value += 0  #change if necessary
                        else:
                            value += 1000

        ##################################################


        if(heurFlag == 3):  #if everyone is on a floor that a goal elevator services
            for floor in self.floors:  #for each floor
                for p in floor.occupants:  #for each person on the floor
                    if(p.vip == False):
                        if(p.goalFloor == floor.number):  #if they are on their goal floor
                            value -= 1000  #goal floor

                        else:
                            if(floor.number == self.KB.initFloors[p.name]):  #if they are on their intial floor
                                value += 300  #still at their start
                            else:  #they are on a middle floor waiting to be picked up
                                value -= abs(self.KB.initFloors[p.name] - floor.number) * 5
                                value += 0

                            #move elevators towards this person
                            elevatorFloorNums = []
                            for f in self.floors:  #for each floor
                                for e in floor.elevators:  #for each elevator
                                    if(e.currentOccupancy < e.capacity and floor.number in e.services):  #if it can load the person
                                        elevatorFloorNums.append(abs(floor.number - f.number))
                            if(len(elevatorFloorNums) > 0):
                                value += min(elevatorFloorNums)

            for f in self.floors:  #for each floor
                for e in f.elevators:  #for each elevator
                    tmpHigh = []
                    for per in e.occupants:  #for each person in elevator
                        if(per.vip == False):
                            #make it better a person gets in a goal elevator, not much for nothing for non goal
                            if(e in self.KB.serviceMap[per.name][2] or e in self.KB.serviceMap[per.name][0]):  #if its a goal elevator
                                #print("goal elevator")
                                value -= 500  #make it much better that a person gets in an elevator if its a goal elevator but not better than getting off
                            else:
                                value -= 0
                            value += abs(e.currentFloor - per.goalFloor)
                        else:
                            value += 1000

        return value


    def checkFlag(self):
        global heurFlag

        if(heurFlag == 0):
            for floor in self.floors:  #for each floor
                for person in floor.occupants:  #for each person
                    if(person.vip == True and len(self.KB.serviceMap[person.name][0]) == 0):  #if its a vip who has no elevator to go all the way
                        if(not floor.number == 5):  #if they are not on the 5th floor hub
                            return 0

                for e in floor.elevators:  #for each elevator
                    for per in e.occupants:
                        if(per.vip == True):  #if a vip is in an elevator
                            return 0
            return 1


        elif(heurFlag == 1):
            for floor in self.floors:  #for each floor
                for person in floor.occupants:  #for each person
                    if(person.vip == True):  #if its a vip
                        if(not floor.number == person.goalFloor):  #if they are not on their goal floor
                            return 1

                for e in floor.elevators:  #for each elevator
                    for per in e.occupants:
                        if(per.vip == True):  #if a vip is in an elevator
                            return 1
            return 2

        elif(heurFlag == 2):  #make sure all people not vips who need more than one elevator are on floor 5
            for floor in self.floors:  #for each floor
                for person in floor.occupants:  #for each person
                    if(person.vip == False and len(self.KB.serviceMap[person.name][0]) == 0):  #if its not vip who has no elevator to go all the way
                        if(not floor.number == 5):  #if they are not on the 5th floor hub
                            return 2

                for e in floor.elevators:  #for each elevator
                    for per in e.occupants:
                        if(per.vip == False and len(self.KB.serviceMap[per.name][0]) == 0):  #if a non vip is in an elevator who needs another el
                            return 2
            return 3

        else:
            return 3



def main():
    h = hotel(10,4,20)
    solution = AStar2(h)
    print(solution)



def AStar2(state):
    h = []
    global heurFlag
    heapq.heappush(h, (state.getHeur(), state, "", 0))
    val = set([])
    tmp = 10000000
    tmpf = 0
    while(len(h) > 0):
        curr_state = heapq.heappop(h)

        if(not heurFlag == tmpf):
            val = set([])
            tmp = 100000000
            #print curr_state[0]

        val.add(curr_state[0])
        if(min(val) < tmp):
            print(min(val))
            printState(curr_state[1])
            tmp = min(val)

        tmpf = heurFlag
        

        curr_st = curr_state[1]
        curr_moves = curr_state[2]
        curr_depth = curr_state[3]
        new_states = []
        new_states = curr_st.findMoves()  #returns a list of [[states, the move]]
        for st in new_states:
            state = st[0]
            move = st[1]
            if(state.checkForGoal()):  #check if its the solution
                #print(state.getHeur())
                printState(state)
                return curr_moves + move + "\n"
            elif(not state.checkFlag() == heurFlag):  #if the heurflag changes, delete rest of heap and change global flag
                h = []
                heurFlag = state.checkFlag()
                heapq.heappush(h, (state.getHeur() + curr_depth, state, curr_moves + move + "\n", curr_depth))
                #print("flag has changed!!!!!!!!!!!!!!!!!!!")
                #print(heurFlag)
                #print(len(h))
                #exit()
                break
            else:
                heapq.heappush(h, (state.getHeur() + curr_depth, state, curr_moves + move + "\n", curr_depth))
    return curr_moves






def printState(state):
    #print(state.getHeur())
    print "heurFlag = ", heurFlag
    for floor in state.floors:
        print floor.number
        print "elevators: "
        for e in floor.elevators:
            print "   ", e.name, "occupants: ",
            for p in e.occupants:
                print p.name,
            print ""
        print "occupants: ",
        for pe in floor.occupants:
            print pe.name,
        print("")
    print("\n\n\n")


heurFlag = 0
main()


