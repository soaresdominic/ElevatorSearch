class elevator:
    
    def __init__(self, capacity, serviceFloors, name, startFloor):
        self.name = name
        self.capacity = capacity
        self.currentFloor = startFloor
        self.occupants = []
        self.currentOccupancy = 0
        self.services = serviceFloors

