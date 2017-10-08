from config import StaticValues


class User(object):

    def __init__(self, index, srcFloor, destFloor, entryTime=0):
        self.index = index
        self.srcFloor = srcFloor
        self.destFloor = destFloor
        self.travelType = StaticValues.goingUp if self.destFloor > self.srcFloor else \
                            StaticValues.goingDown
        self.distanceToTravel = abs(destFloor - srcFloor)
        self.entryTime = entryTime

    def __getitem__(self, key):
        return getattr(self, key, None)