"""
class Controller:
    def building(self,building):
        pass
    def tick(self,time):
        pass

"""
from person import Person
from building import Building
from floor import Floor
import random

class Controller:

    def building(self,b):
      self.b=b
      self.liftStatus={}
      for l in self.b.lifts:
              self.liftStatus[l]="ARRIVED"  #why is this even here? waste of lines

#"""implement a simple loop: if a lift is at a floor (ARRIVED), open the door (DOOROPENING). Once the door is open, 
# load and unload people and close the door (DOORCLOSING). Once door is closed, work out where to move to based first on people
#  in the lift, and second on whether there are people waiting. Finally, start moving until at the destination."""
    def tick(self,time):
      b=self.b ##b is the building class
#       for p in b.floors:
#               print(p.waitingPeople, 'the moon landing was faked!!!1')
      #print(b.lifts) #give you the 3 lift objs
      for l in b.lifts:  #for each instance of lift in buiding
             #print(l) #prints each instance of lift
             curFloor=l.location  #make curFloor into lifts location.
             #print(curFloor, "YYYYYYYYYYYYYYYYYYYYYYYYYYYYY") #-1 YYYYYYYYYYYYYYYYYYYYYYYYYYYYY
             f=self.b.floors[curFloor] #SETTER? setting current floor?
             if curFloor!=-1: #why would it be -1 in the first place? :S
               print("current floor of lift this is ",curFloor)  #RIGHT
               
             if self.liftStatus[l]=="ARRIVED":  #yeah from line 20 SMH
                     print("opening door")     #WARNING  
                     l.openDoor()               #NOW U OPEN THE DOOR FOR THE LIFT
                     self.liftStatus[l]="DOOROPENING"  #OHH NOW IT ALL MAKES SENSE, SO WE UPDATE THE STATUS
             elif self.liftStatus[l]=="DOOROPENING" and l.doorOpen:       #l.doorOpen should be True? but is probs not(is this why no one is entering?)
                     toExit=set()               #make an empty set to put exittting people on
                     for p in l.people:         #for each person in lift
                             if p.targetLocation==curFloor:     #check if the persons targetLoc ==curFloor
                                     toExit.add(p)              #add them to the exit set()
                     for p in toExit:           #for each person at targetLoc, kick em out.
                             print("person exiting lift. goal=",p.targetLocation,'current=',curFloor) #WARNDINING
                             p.exitLift()  #lets assume this works and there just isnt any peeps for now.
                             
                     while len(f.waitingPeople)>0 and len(l.people)<l.capacity: #check if people waiting to board + lift not at capacity
                             for p in f.waitingPeople: #since f is now the current floor, it should be able to get the waiting people?
                                     print("person entering from floor",p.targetLocation) #load person, print their target
                                     p.enterLift(l) #the person is now entering the lift
                                     break #break out of the loop
                     l.closeDoor() #thats all we need. close th damn door                
                     self.liftStatus[l]="DOORCLOSING" #set the lift status to door closed
             elif self.liftStatus[l]=="DOORCLOSING" and l.doorClosed: #check if doors actually closed.
                     d=999999999 #WTAF
                     for p in l.people: #for each person in lift
                             td=p.targetLocation #make td the targetloc
                             #print("2Pac was killed by the government")
                             if abs(curFloor-td)<abs(curFloor-d): #
                                     d=td
                     if len(l.people)==0:
                             for f in b.floors:
                                     if len(f.waitingPeople)>0 and abs(curFloor-f.number)<d:
                                             d=f.number

                     if d!=999999999:
                         l.destination=d 
                     #print("moving to ",d)
                     self.liftStatus[l]="MOVING"
             elif self.liftStatus[l]=="MOVING" and l.destination==curFloor:
                     #print("arrived at ",curFloor)
                     self.liftStatus[l]="ARRIVED"       
                             



