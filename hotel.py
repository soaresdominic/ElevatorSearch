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
                f = floor(i, True)
                #f = floor(i, False)
            self.floors.append(f)
        
        e1 = elevator(5, [1,2,3,4,5,6], "e1")
        e2 = elevator(8, [1,2,3,4,5,6], "e2")
        e3 = elevator(3, [3,7,8,9,10], "e3")
        e4 = elevator(5, [6,7,8,9,10], "e4")
        elevators = []
        elevators.append(e1)
        elevators.append(e2)
        elevators.append(e3)
        elevators.append(e4)
        for e in elevators:
            self.floors[e.currentFloor-1].elevators.append(e)
            
        p1 = person(1, "g", "p1", 10)
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
        p14 = person(8, "g", "p14", 1)
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
        #KB.printMap()
        #exit()


    def findMoves(self):
        moves = []

        #move elevator
        floorNum = 1
        for floor in self.floors:
            eNum = 0
            for e in floor.elevators:
                if(e.currentFloor > 1):  #move down
                    moveS = ("move " + e.name + " from floor " + str(floorNum) + " to " + str(floorNum - 1))
                    newState = copy.deepcopy(self)
                    el = newState.floors[floorNum-1].elevators.pop(eNum)  #delete elevator from floor
                    el.currentFloor -= 1
                    newState.floors[floorNum-2].elevators.append(el)  #append it to floor below
                    moves.append([newState, moveS])
                if(e.currentFloor < 10):  #move up
                    moveS = ("move " + e.name + " from floor " + str(floorNum) + " to " + str(floorNum + 1))
                    newState = copy.deepcopy(self)
                    el = newState.floors[floorNum-1].elevators.pop(eNum)  #delete elevator from floor
                    #print(newState.floors[floorNum-1].number, newState.floors[floorNum-1].elevators)
                    el.currentFloor += 1
                    newState.floors[floorNum].elevators.append(el)  #append it to floor above
                    #print(newState.floors[floorNum].number, newState.floors[floorNum].elevators)
                    #exit()
                    moves.append([newState, moveS])
                eNum += 1
            floorNum += 1





        #load person
        floorNum = 1
        for floor in self.floors:  #for each floor
            if(len(floor.elevators) > 0 and len(floor.occupants) > 0):  #if theres an elevator on the floor and people waiting on the floor
                pNum = 0
                for person in floor.occupants:  #for each person on the floor
                    if(len(self.KB.serviceMap[person.name][0]) > 0):  #if the person has an elevator to take it all the way
                        eNum = 0
                        for elevator in floor.elevators:  #for each elevator on the floor
                            if(elevator in self.KB.serviceMap[person.name][0]):  #if the elevaor is in that list
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
                        eNum = 0
                        for elevator in floor.elevators:  #for each elevator on the floor
                            if(elevator in self.KB.serviceMap[person.name][2]):  #if the elevaor is in goal list
                                moveS = ("add person " + person.name + " to " + elevator.name)
                                newState = copy.deepcopy(self)
                                p = newState.floors[floor.number-1].occupants.pop(pNum)  #delete person waiting on the floor
                                p.currentFloor = -1
                                newState.floors[floor.number-1].elevators[eNum].occupants.append(p)
                                newState.floors[floor.number-1].elevators[eNum].currentOccupancy += 1
                                #print(newState.getHeur())
                                moves.append([newState, moveS])
                                continue
                            eNum += 1
                        eNum = 0
                        for elevator in floor.elevators:  #for each elevator on the floor
                            if(elevator in self.KB.serviceMap[person.name][1]):  #if the elevaor is in start list
                                moveS = ("add person " + person.name + " to " + elevator.name)
                                newState = copy.deepcopy(self)
                                p = newState.floors[floor.number-1].occupants.pop(pNum)  #delete person waiting on the floor
                                p.currentFloor = -1
                                newState.floors[floor.number-1].elevators[eNum].occupants.append(p)
                                newState.floors[floor.number-1].elevators[eNum].currentOccupancy += 1
                                #print(newState.getHeur())
                                moves.append([newState, moveS])
                                continue
                            eNum += 1
                    pNum += 1


        """
        #load person
        floorNum = 1
        for floor in self.floors:
            if(len(floor.elevators) > 0 and len(floor.occupants) > 0):  #if theres an elevator and people waiting on the floor
                eNum = 0
                for e in floor.elevators:  #for each elevator
                    if(e.currentOccupancy < e.capacity and (floorNum in e.services)):
                        pNum = 0
                        for p in floor.occupants:  #for each person
                            #print(p.goalFloor, e.services)
                            if(p.goalFloor != floorNum):  #keep person there if thats where they wanna go
                                #print(p.goalFloor, e.services)
                                #print("load")
                                moveS = ("add person " + p.name + " to " + e.name)
                                newState = copy.deepcopy(self)
                                p = newState.floors[floorNum-1].occupants.pop(pNum)  #delete person waiting on the floor
                                newState.floors[floorNum-1].elevators[eNum].occupants.append(p)
                                newState.floors[floorNum-1].elevators[eNum].currentOccupancy += 1
                                #print(newState.getHeur())
                                moves.append([newState, moveS])
                            #else:
                                #print("dont load because he's cool", p.name, p.currentFloor, p.goalFloor)
                            pNum += 1
                    eNum += 1
            floorNum += 1
        """


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
                            if(p.goalFloor == e.currentFloor):  #if persons goal floor is this floor, offload
                                #print(p.goalFloor, floor.number)
                                #print("offload")
                                moveS = ("add person " + p.name + " to floor " + str(floor.number))
                                newState = copy.deepcopy(self)
                                p = newState.floors[floor.number-1].elevators[eNum].occupants.pop(pNum) #delete person from elevator
                                p.currentFloor = floor.number
                                newState.floors[floor.number-1].occupants.append(p)
                                newState.floors[floor.number-1].elevators[eNum].currentOccupancy -= 1
                                moves.append([newState, moveS])

                            elif(e not in self.KB.serviceMap[p.name][2] and e not in self.KB.serviceMap[p.name][0]):  #if this elevator is not in that persons goal elevators
                                #print(p.goalFloor, floor.number)
                                #print("offload")
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
        print(numPeople, self.KB.numPeople)
        if(numPeople == self.KB.numPeople):
            return True




        """
        floorNum = 1
        for floor in self.floors:


            if(floorNum == 1):
                if(len(floor.occupants) == 2):
                    people = []
                    for person in floor.occupants:
                        people.append(person.name)
                    if(not(people.__contains__("p6") and people.__contains__("p7"))):
                        return False
                else:
                    return False

            if(floorNum == 5):
                if(len(floor.occupants) == 1):
                    people = []
                    for person in floor.occupants:
                        people.append(person.name)
                    if(not(people.__contains__("p9"))):
                        return False
                else:
                    return False

            if(floorNum == 6):
                if(len(floor.occupants) == 2):
                    people = []
                    for person in floor.occupants:
                        people.append(person.name)
                    if(not(people.__contains__("p2") and people.__contains__("p10"))):
                        return False
                else:
                    return False

            if(floorNum == 7):
                if(len(floor.occupants) == 1):
                    people = []
                    for person in floor.occupants:
                        people.append(person.name)
                    if(not(people.__contains__("p5"))):
                        return False
                else:
                    return False

            if(floorNum == 8):
                if(len(floor.occupants) == 1):
                    people = []
                    for person in floor.occupants:
                        people.append(person.name)
                    if(not(people.__contains__("p4"))):
                        return False
                else:
                    return False


            if(floorNum == 9):
                if(len(floor.occupants) == 2):
                    people = []
                    for person in floor.occupants:
                        people.append(person.name)
                    if(not(people.__contains__("p3") and people.__contains__("p8"))):
                        return False
                else:
                    return False


            if(floorNum == 9):
                if(len(floor.occupants) == 1):
                    people = []
                    for person in floor.occupants:
                        people.append(person.name)
                    if(not(people.__contains__("p1"))):
                        return False
                else:
                    return False

            floorNum+=1
        return True








    
    def checkForGoal(self):
        floorNum = 1
        for floor in self.floors:
            if(floorNum == 1):
                if(len(floor.occupants) == 4):
                    if(floor.occupants.__contains__("p6") and floor.occupants.__contains__("p7") and floor.occupants.__contains__("p14") and floor.occupants.__contains__("p16")):
                        continue
                    else:
                        return False
                else:
                    return False

            if(floorNum == 2):
                if(len(floor.occupants) == 2):
                    if(floor.occupants.__contains__("p13") and floor.occupants.__contains__("p15")):
                        continue
                    else:
                        return False
                else:
                    return False

            if(floorNum == 3):
                if(len(floor.occupants) == 1):
                    if(floor.occupants.__contains__("p11")):
                        continue
                    else:
                        return False
                else:
                    return False

            if(floorNum == 4):
                if(len(floor.occupants) == 1):
                    if(floor.occupants.__contains__("p12")):
                        continue
                    else:
                        return False
                else:
                    return False

            if(floorNum == 5):
                if(len(floor.occupants) == 1):
                    if(floor.occupants.__contains__("p9")):
                        continue
                    else:
                        return False
                else:
                    return False


            if(floorNum == 6):
                if(len(floor.occupants) == 2):
                    if(floor.occupants.__contains__("p2") and floor.occupants.__contains__("p10")):
                        continue
                    else:
                        return False
                else:
                    return False


            if(floorNum == 7):
                if(len(floor.occupants) == 3):
                    if(floor.occupants.__contains__("p5") and floor.occupants.__contains__("p17") and floor.occupants.__contains__("p20")):
                        continue
                    else:
                        return False
                else:
                    return False


            if(floorNum == 8):
                if(len(floor.occupants) == 1):
                    if(floor.occupants.__contains__("p4")):
                        continue
                    else:
                        return False
                else:
                    return False


            if(floorNum == 9):
                if(len(floor.occupants) == 3):
                    if(floor.occupants.__contains__("p3") and floor.occupants.__contains__("p8") and floor.occupants.__contains__("p19")):
                        continue
                    else:
                        return False
                else:
                    return False

            if(floorNum == 10):
                if(len(floor.occupants) == 2):
                    if(floor.occupants.__contains__("p1") and floor.occupants.__contains__("p18")):
                        continue
                    else:
                        return False
                else:
                    return False

            floorNum+=1
        return True
    """


    #for each person
    #if they are on a floor that is not where they wanna go, +5
    #if they are in an elevator 0
    #if they are on the floor they wanna go -5
    #EACH MOVE NEEDS TO CHANGE THE HEURISTIC
    def getHeur(self):
        value = 0
        pAtGoal = 0
        for floor in self.floors:  #for each floor
            for p in floor.occupants:  #for each person
                if(p.goalFloor == floor.number):  #make offloading good
                    pAtGoal += 1
                    value -= 500
                else:
                    value += abs(p.currentFloor - p.goalFloor)
                    elevatorFloorNums = []
                    for f in self.floors:  #for each floor
                        for e in floor.elevators:  #for each elevator
                            if(e.currentOccupancy < e.capacity and floor.number in e.services):  #if it can load the person
                                elevatorFloorNums.append(abs(floor.number - f.number))
                    if(len(elevatorFloorNums) > 0):
                        value += min(elevatorFloorNums)
                        #print(value) 


        for f in self.floors:  #for each floor
            for e in f.elevators:
                for per in e.occupants:
                    #make it better a person gets in a goal elevator, not much for nothing for non goal
                    if(e in self.KB.serviceMap[per.name][2] or e in self.KB.serviceMap[per.name][0]):
                        value -= 100  #make it much better that a person gets in an elevator if its a goal elevator
                    else:
                        value -= 0
                    value += abs(e.currentFloor - per.goalFloor) * 3

                
        return value




    """
    def getHeur(self):
        value = 0

        floorNum = 1
        for floor in self.floors:  #for each floor
            for p in floor.occupants:  #for each person waiting on the floor
                if(p.goalFloor == floorNum):  #make offloading good
                    value -= 4
                else:
                    value += abs(p.goalFloor - floorNum) * 2

                
                #how close is nearest elevator
                if(p.goalFloor != floorNum):
                    floorNum2 = 1
                    elevatorFloorNums = []
                    for f in self.floors:
                        for e in floor.elevators:
                            if(e.currentOccupancy < e.capacity):  #if it can add people
                                elevatorFloorNums.append(abs(floorNum - floorNum2))
                        floorNum2 += 1
                    if(len(elevatorFloorNums) > 0):
                        value += min(elevatorFloorNums)
                

            for e in floor.elevators:
                for per in e.occupants:
                    value += abs(per.goalFloor - floorNum)
                    value -= 2  #make onloading good

            floorNum += 1
        return value
    """







def main():
    h = hotel(10,4,20)
    solution = AStar2(h)
    print(solution)



def AStar2(state):
    h = []
    heapq.heappush(h, (state.getHeur(), state, "", 0))
    val = set([])
    tmp = 100
    while(len(h) > 0):
        curr_state = heapq.heappop(h)

        #printState(curr_state[1])
        
        val.add(curr_state[0])
        if(min(val) < tmp):
            print(min(val))
            printState(curr_state[1])
            tmp = min(val)
        

        curr_st = curr_state[1]
        curr_moves = curr_state[2]
        curr_depth = curr_state[3]
        new_states = []
        new_states = curr_st.findMoves()  #returns a list of [[states, the move]]
        for st in new_states:
            state = st[0]
            move = st[1]
            #print(move)
            #print(state.getHeur())
            #if(state.floors != curr_st.floors):
            if(True):
                if(state.checkForGoal()):
                    print(state.getHeur())
                    printState(state)
                    return curr_moves + move + "\n"
                #print(state.getHeur() + curr_depth)

                """
                for floor in state.floors:
                    for e in floor.elevators:
                        print(e.occupants)
                """

                heapq.heappush(h, (state.getHeur() + curr_depth, state, curr_moves + move + "\n", curr_depth))
    return curr_moves




def printState(state):
    #print(state.getHeur())
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

main()


