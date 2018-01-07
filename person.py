from enum import Enum
import random
import numpy


class person:
    
    def __init__(self, startFloor, type, name, goalFloor):
        self.startFloor = startFloor
        self.currentFloor = startFloor
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


