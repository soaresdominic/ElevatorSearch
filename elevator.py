from enum import Enum
import random
import numpy


class elevator:
    
    def __init__(self, capacity, serviceFloors, name):
        self.name = name
        self.capacity = capacity
        self.currentFloor = 1
        self.occupants = []
        self.currentOccupancy = 0
        self.services = serviceFloors

