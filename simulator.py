from enum import Enum
import random
import numpy

##################### VERSION 1.0, 2/11/2017 ###########################

PEOPLESERVED=0
TOTPEOPLE=0

class Lift:
    """This class represents the lift."""
    __FLOORTICKS=10 #number of ticks to wait between floors
    __DOORTICKS=5

    class Action(Enum):
        NONE = 0
        MOVE = 1
        DOOR = 2


    def __init__(self,location,capacity,minFloor,maxFloor,doorOpen,building):
        self.__location=location
        self.__capacity=capacity
        self.__minFloor=minFloor
        self.__maxFloor=maxFloor
        self.__building=building
        self.__doorOpen=doorOpen
        self.__destination=location

        self.__load=set() #people on the lift
        self.__waitingtime=0 #waiting time stores how many ticks will happen until something occurs
        self.__instruction=self.Action.NONE


    @property
    def people(self):
        return self.__load

    @property
    def location(self):
        if self.__waitingtime==0:
            return self.__location
        return -1

    @property
    def capacity(self):
        return self.__capacity

    @property
    def minFloor(self):
        return self.__minFloor

    @property
    def maxFloor(self):
        return self.__maxFloor

    @property
    def doorOpen(self):
        return self.__doorOpen

    @property
    def destination(self):
        return self.__destination

    @destination.setter
    def destination(self,floor):
        if self.__minFloor>floor or self.__maxFloor<floor:
            raise ValueError("floor outside legal range")
        if self.__doorOpen:
            raise Exception("door still open")
        self.__destination=floor
        self.__instruction=self.Action.MOVE
        if self.__waitingtime<=0: #TODO: handle case where we are between floors better
            self.__waitingtime=0+self.__FLOORTICKS

    def openDoor(self):
        if not self.__location==self.__destination:
            raise Exception("lift is moving")
        if not self.__doorOpen:
            self.__instruction=self.Action.DOOR
            if self.__waitingtime==0:
                self.__waitingtime=0+self.__DOORTICKS
        else:
            self.__instruction=self.NONE

    def closeDoor(self):
        if self.__location!=self.__destination:
            raise Exception("lift is moving")
        if self.__doorOpen:
            self.__instruction = self.Action.DOOR
            if self.__waitingtime==0:
                self.__waitingtime = 0+self.__DOORTICKS
        else:
            self.__instruction=self.NONE

    def tick(self):
        if self.__waitingtime>0:
            self.__waitingtime-=1
        print(self.__waitingtime)
        if self.__instruction==self.Action.NONE or self.__waitingtime>0:
            return

        if self.__instruction==self.Action.DOOR and self.__location==self.destination:
            self.__doorOpen=not self.__doorOpen
        elif self.__instruction==self.Action.MOVE:
            self.__location+=int((self.__destination-self.__location)/abs(self.__destination-self.__location))
            if self.__location==self.__destination:
                self.instruction=self.Action.NONE
                self.__waittime=0
            else:
                self.__waitingtime=0+self.__FLOORTICKS

#TODO: check that the person is on the right floor to be added
    def enterLift(self,person):
        if not self.__doorOpen:
            raise Exception("door is open")
        if len(self.__load)>=self.__capacity:
            raise Exception("lift full")
        self.__load.add(person)
        person.location=self

    def exitLift(self,person):
        if not self.__doorOpen:
            raise Exception("door is open")
        self.__load.remove(person)
        person.location = self.__building.floors[self.__location]


class Person:
    def __init__(self,currentLocation,goal,creationTime,hiddenGoal):
        self.__currentLocation=currentLocation
        self.__goal=goal
        self.__creationTime=creationTime
        self.__hiddenGoal=hiddenGoal

    def enterLift(self,lift):
        lift.enterLift(self)

    def exitLift(self):
        if type(self.__currentLocation)!=Lift:
            raise Exception("not in lift")
        self.location.exitLift(self)

    @property
    def location(self):
        return self.__currentLocation

    @property
    def targetLocation(self):
        if self.__hiddenGoal and not type(self.__currentLocation)==Lift:
            return -1
        return self.__goal

    @property
    def creationTime(self):
        return self.__creationTime


class Building:
    def __init__(self,floors,lifts,controller):
        self.__floors=floors
        self.__lifts=lifts
        for l in lifts:
            l.building=self
        self.__controller=controller
        self.__controller.building(self)
        self.__time=0

    def tick(self):
        for f in self.__floors:
            f.tick(self.__time)
        for l in self.__lifts:
            l.tick()
        self.__controller.tick(self.__time)
        self.__time+=1

    @property
    def floors(self):
        return self.__floors

    @property
    def lifts(self):
        return self.__lifts

    @property
    def time(self):
        return self.__time


class Floor:
    def __init__(self,number,generators,vanishers,maxPeople=20):
        self.__number=number
        self.__waitingPeople=set()
        self.__generators=generators
        self.__vanishers=vanishers
        self.__maxPeople=maxPeople
        for g in self.__generators: g.floor=self
        for v in self.__vanishers: v.floor=self

    def tick(self,time):
        toAdd=set()
        if len(self.__waitingPeople)<self.__maxPeople:
            for g in self.__generators:
                toAdd=g.tick(time)
                if toAdd!=None:
                    global TOTPEOPLE
                    TOTPEOPLE += 1
                    self.__waitingPeople.add(toAdd)
        for v in self.__vanishers:
            self.__waitingPeople=self.__waitingPeople - v.tick(time,self.__waitingPeople)

    @property
    def number(self):
        return self.__number

    @property
    def waitingPeople(self):
        return self.__waitingPeople

"""there is a beta distribution regarding the selected floor"""
class BetaFloorSelector:
    def __init__(self,minFloor,maxFloor,a=1,b=1):
        self.__minFloor=minFloor
        self.__maxFloor=maxFloor
        self.__a=a
        self.__b=b

    def pickFloor(self):
        if self.__maxFloor==self.__minFloor:
            return self.__maxFloor
        return int(round((numpy.random.beta(self.__a,self.__b)*(self.__maxFloor-self.__minFloor)+self.__minFloor),0))

"""beta generator for picking people"""
class BetaGenerator:
    def __init__(self,hiddenGoal,startTime,endTime,floorSelector,a=1,b=1):
        self.__hiddenGoal=hiddenGoal
        self.__startTime=startTime
        self.__endTime=endTime
        self.__floorSelector=floorSelector
        self.__a=a
        self.__b=b

    @property
    def floor(self):
        return self.__floor

    @floor.setter
    def floor(self,floor):
        self.__floor=floor

    def tick(self,time):
        if random.random()*3600*24<(numpy.random.beta(self.__a,self.__b)*(self.__endTime-self.__startTime)+self.__startTime):
            targetFloor=self.__floorSelector.pickFloor()
            return Person(self.__floor,targetFloor,time,self.__hiddenGoal)

class Vanisher:
    WAITINGTHRESHOLD=600

    @property
    def floor(self):
        return self.__floor

    @floor.setter
    def floor(self,floor):
        self.__floor=floor

    def tick(self,time,people):
        toRemove=set()
        for p in people:
            if time-p.creationTime>self.WAITINGTHRESHOLD:
                toRemove.add(p)
            if p.targetLocation==self.__floor:
                toRemove.append(p)
                global PEOPLESERVED
                PEOPLESERVED+=1
        return toRemove

class Controller:
    def building(self,building):
        pass
    def tick(self,time):
        pass
"""---------------------------------------------------------------------------------------------"""
HG=False #Don't hide goals from the controller


########## START PERSON GENERATION PROBABILITY DEFINITIONS ####################
morningGroundFloorSelector=BetaFloorSelector(1,10) 
morningGFGenerator=BetaGenerator(HG,7*3600,9*3600,morningGroundFloorSelector,5,5)
lunchGFGenerator=BetaGenerator(HG,12.5*3600,14*3600,morningGroundFloorSelector,5,5)
vanisher=Vanisher()

dayOtherFloorSelector=BetaFloorSelector(0,10)
dayOtherFloorGenerator=BetaGenerator(HG,8*3600,17*3600,dayOtherFloorSelector,2,2)

lunchOtherFloorSelector=BetaFloorSelector(0,0)
lunchOtherFloorGenerator=BetaGenerator(HG,12*3600,13.5*3600,lunchOtherFloorSelector)

eveningOtherFloorSelector=BetaFloorSelector(0,0)
eveningOtherFloorGenerator=BetaGenerator(HG,16.5*3600,18*3600,eveningOtherFloorSelector)
########## END PERSON GENERATION PROBABILITY DEFINITIONS ####################

########## START FLOOR DEFINITIONS ####################
floors=[]
groundFloor=Floor(0,[morningGFGenerator,lunchGFGenerator,dayOtherFloorGenerator],[vanisher])
floors.append(groundFloor)
for i in range(1,11):
    f=Floor(i,[dayOtherFloorGenerator,lunchOtherFloorGenerator,eveningOtherFloorGenerator],[vanisher])
    floors.append(f)

########## END FLOOR DEFINITIONS ####################
########## START LIFT DEFINITIONS ####################
l1=Lift(0,10,0,10,False,None) #this lift goes across all floors
l2=Lift(0,20,0,5,False,None)  #services the first 6 floors, more capacity
l3=Lift(0,5,3,10,False,None)  #services floor 4 - 10, less capacity
########## END LIFT DEFINITIONS ####################

########## REPLACE WITH OWN CONTROLLER####################
controller=Controller()

########## BUILDING DEFINITION ####################

building=Building(floors,[l1,l2,l3],controller)

########## RUN OVER A SINGLE 24 HOUR PERIOD####################
for i in range(0,3600*24):
    building.tick()
