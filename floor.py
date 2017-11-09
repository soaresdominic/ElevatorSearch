from enum import Enum
import random
import numpy


class floor:
    
    def __init__(self, number, secure):
        self.number = number
        self.elevators = []
        self.occupants = []
        self.secured = secure

