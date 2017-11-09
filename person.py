from enum import Enum
import random
import numpy


class person:
    
    def __init__(self, currentFloor, type, name, goalFloor):
        self.currentFloor = currentFloor
        self.name = name
        self.goalFloor = goalFloor
        self.guest = False
        self.employee = False
        self.vip = False
        if(type == "g"):
            self.guest = True
        elif(type == "e"):
            self.employee = True
        elif(type == "v"):
            self.vip = True


