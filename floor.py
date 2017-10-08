from operator import itemgetter

from config import StaticValues


class FloorManager(object):

    def __init__(self, floors):
        self.floorsConfig = {}
        for f in floors:
            self.floorsConfig[f.value] = f

    def getUser(self, floorNumber, typeConfig=None):
        return self.floorsConfig[floorNumber].getUser(typeConfig)

    def isFloorEmpty(self, floorNumber, typeConfig=None):
        return self.floorsConfig[floorNumber].isFloorEmpty(typeConfig)

    def addUsers(self, floorNumber, users):
        return self.floorsConfig[floorNumber].addUsers(users)

    def getAllFloorsConfig(self):
        return self.floorsConfig

    def usersCount(self, floorNumber):
        return self.floorsConfig[floorNumber].usersCount()

    def totalUsersCount(self):
        usersCount = 0
        for fIndex, f in self.floorsConfig.items():
            usersCount += f.usersCount()

        return usersCount

    def getAllFloorsRequirement(self, liftsFloorConfig, currentlyOptimized):
        fRequirement = {}
        for fIndex, floor in self.floorsConfig.items():
            liftSpace = 0
            lFreeCounter = 0

            for l in liftsFloorConfig.get(fIndex, []):
                if l.capacity > l.usersCount():
                    liftSpace += l.capacity - l.usersCount()
                    lFreeCounter += 1

            floorUsersCount = floor.usersCount()
            
            if currentlyOptimized == StaticValues.timeOptimizer:
                fRequirement[fIndex] = floorUsersCount - lFreeCounter
            elif currentlyOptimized == StaticValues.powerOptimizer and floorUsersCount> liftSpace:
                fRequirement[fIndex] = floorUsersCount - liftSpace

        return fRequirement

    def visualize(self, liftManager):
        for f, v in sorted(self.floorsConfig.items(), reverse=True):
            v.visualize(liftManager)


class Floor(object):

    def __init__(self, value, users={}):
        self.value = value
        
        if not users:
            self.users = {StaticValues.goingUp: [], StaticValues.goingDown: []}
        else:
            self.users = users

    def usersCount(self, typeConfig=None):
        if not typeConfig:
            return len(self.users[StaticValues.goingUp]) + len(self.users[StaticValues.goingDown])
        else:
            return len(self.users[typeConfig])

    def addUsers(self, users):
        for u in users:
            self.users[u.travelType].append(u)

        self.users[StaticValues.goingUp] = sorted(
                                                self.users[StaticValues.goingUp],
                                                key=lambda x: [x.entryTime, x.distanceToTravel]
                                            )
        self.users[StaticValues.goingDown] = sorted(
                                                self.users[StaticValues.goingDown],
                                                key=lambda x: [x.entryTime, x.distanceToTravel]
                                            )
        return True

    def isFloorEmpty(self, typeConfig=None):
        if self.usersCount(typeConfig):
            return False

        return True

    def getUser(self, typeConfig=None):
        retVal = None

        if not typeConfig:
            upCount = self.usersCount(StaticValues.goingUp)
            downCount = self.usersCount(StaticValues.goingDown)
            if upCount and downCount:
                if abs(self.value - self.users[StaticValues.goingUp][0].destFloor) > \
                    abs(self.value - self.users[StaticValues.goingDown][0].destFloor):
                    retVal = self.users[StaticValues.goingDown].pop(0)
                else:
                    retVal = self.users[StaticValues.goingUp].pop(0)
            elif upCount:
                retVal = self.users[StaticValues.goingUp].pop(0)
            elif downCount:
                retVal = self.users[StaticValues.goingDown].pop(0)
        elif self.usersCount(typeConfig):
            retVal = self.users[typeConfig].pop(0)
        
        return retVal

    def visualize(self, liftManager, isPrint=True):
        liftsVisualize = liftManager.visualize(self, False)

        floorVisualize = [
             " " +  "_" * 11 + " ",
             ("|" +  " Floor: %s " + "|") % str(self.value).zfill(2), 
             ("|" +  "Waiting: %s" + "|") % str(self.usersCount()).zfill(2),
             "|" +  "_" * 11 + "|"
             ]

        aggregatedValue = [floorVisualize[i] + " | " + liftsVisualize[i] for i in range(4)]

        if isPrint:
            print "\n".join(aggregatedValue)
        else:
            return aggregatedValue
