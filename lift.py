from collections import defaultdict
from operator import itemgetter

from config import StaticValues


class LiftManager(object):

    def __init__(self, lifts, optimizerConfig=StaticValues.optimizerConfig):
        self.lifts = lifts

        self.liftsFloorConfig = {}
        self.maxOptimizerConfig = optimizerConfig
        self.curOptimizerConfig = dict((k, 0) for k, v in self.maxOptimizerConfig.iteritems())
        self.currentOptimized = max(self.maxOptimizerConfig.iteritems(), key=itemgetter(1))[0]

    def createLiftsFloorConfig(self):
        self.liftsFloorConfig = {}

        for l in self.lifts:
            if l.currentFloor not in self.liftsFloorConfig:
                self.liftsFloorConfig[l.currentFloor] = []
            self.liftsFloorConfig[l.currentFloor].append(l)

    def _switchCurrentOptimized(self):
        self.currentOptimized = StaticValues.timeOptimizer if self.currentOptimized == \
                                     StaticValues.powerOptimizer else StaticValues.powerOptimizer

    def optimizationCheck(self):
        if self.curOptimizerConfig[self.currentOptimized] == self.maxOptimizerConfig[self.currentOptimized]:
            self.curOptimizerConfig[self.currentOptimized] = 0
            self._switchCurrentOptimized()

            if self.maxOptimizerConfig[self.currentOptimized] == 0:
                self._switchCurrentOptimized()

    def runLifts(self, floorManager):
        logs, usersDeboardedCount, powerConsumed = [], 0, 0
        self.optimizationCheck()

        logs.append(StaticValues.optimization % {"parameter": self.currentOptimized})

        if self.currentOptimized == StaticValues.timeOptimizer:
            for lift in sorted(self.lifts, key=lambda x: x.usersCount()):
                liftLogs, liftUserDeboarded, liftPowerConsumed = lift.run(floorManager, True)
                logs += liftLogs
                usersDeboardedCount += liftUserDeboarded
                powerConsumed += liftPowerConsumed
        elif self.currentOptimized == StaticValues.powerOptimizer:
            sortedLifts = sorted(self.lifts, key=lambda x: [x.currentFloor, x.usersCount()], reverse=True)
            floor = sortedLifts[0].currentFloor
            requirements = floorManager.usersCount(floor)
            for lift in sortedLifts:
                if floor != lift.currentFloor:
                    floor = lift.currentFloor
                    requirements = floorManager.usersCount(floor)

                if requirements <= 0:
                    liftLogs, liftUserDeboarded, liftPowerConsumed = lift.run(floorManager, False)
                    logs += liftLogs
                    usersDeboardedCount += liftUserDeboarded
                    powerConsumed += liftPowerConsumed
                else:
                    liftLogs, liftUserDeboarded, liftPowerConsumed = lift.run(floorManager, True)
                    logs += liftLogs
                    usersDeboardedCount += liftUserDeboarded
                    powerConsumed += liftPowerConsumed

                requirements -= lift.capacity - lift.usersCount()
        
        deployLogs, deploymentPowerConsumed = self.deployIdleLifts(floorManager)

        logs += deployLogs
        powerConsumed += deploymentPowerConsumed

        self.curOptimizerConfig[self.currentOptimized] += 1

        return logs, usersDeboardedCount, powerConsumed

    def totalUsersCount(self):
        usersCount = 0
        for l in self.lifts:
            usersCount += l.usersCount()

        return usersCount

    def _createLiftDeploymentSequence(self, idleLifts, floorManager):
        liftsDeployment = defaultdict(list)
        floorRequirement = floorManager.getAllFloorsRequirement(self.liftsFloorConfig, self.currentOptimized)

        l = idleLifts.pop(0)
        while l:
            strikeUpper, strikeLower = False, False
            i = 1
            while not strikeUpper or not strikeLower:

                if not strikeUpper:
                    upFloor = l.currentFloor + i
                    if upFloor < StaticValues.floors:
                        if upFloor in floorRequirement:
                            liftsDeployment[upFloor].append(l)
                    else:
                        strikeUpper = True

                if not strikeLower:
                    downFloor = l.currentFloor - i
                    if downFloor >= 0:
                        if downFloor in floorRequirement:
                            liftsDeployment[downFloor].append(l)
                    else:
                        strikeLower = True

                i += 1

            if idleLifts:
                l = idleLifts.pop(0)
            else:
                l = None

        return liftsDeployment, floorRequirement

    def _getIdleLifts(self):
        idleLifts = []
        for l in sorted(self.lifts, key=lambda x: x.currentFloor):
            if l.currentStatus == StaticValues.liftIdle:
                idleLifts.append(l)

        return idleLifts

    def deployIdleLifts(self, floorManager):
        logs, powerConsumed = [], 0
        idleLifts = self._getIdleLifts()

        if not idleLifts:
            return logs, powerConsumed

        self.createLiftsFloorConfig()

        deployableConfig, floorRequirement  = self._createLiftDeploymentSequence(idleLifts, floorManager)

        deployedLifts = []
        requirementDepricate = StaticValues.liftCapacity if self.currentOptimized == StaticValues.powerOptimizer \
                                else 1

        for k in deployableConfig:
            deployableConfig[k] = sorted(deployableConfig[k], key=lambda x: abs(k - x.currentFloor))

        for floor, liftsArray in sorted(deployableConfig.items(),
                                key=lambda x: [
                                                abs(x[0] - x[1][0].currentFloor),
                                                -floorManager.usersCount(x[0])
                                                ]):
            requirement = floorRequirement[floor]
            
            for l in liftsArray:
                if l.index in deployedLifts:
                    continue

                if requirement <= 0:
                    break

                if l.currentFloor > floor:
                    l.currentFloor -= 1
                    powerConsumed += 1
                    logs.append(StaticValues.liftMoving % {
                                        "liftIndex": l.index,
                                        "srcFloor": l.currentFloor + 1,
                                        "destFloor": l.currentFloor
                                        })
                else:
                    l.currentFloor += 1
                    powerConsumed += 1
                    logs.append(StaticValues.liftMoving % {
                                        "liftIndex": l.index,
                                        "srcFloor": l.currentFloor - 1,
                                        "destFloor": l.currentFloor
                                        })
                
                deployedLifts.append(l.index)
                requirement -= requirementDepricate

        return logs, powerConsumed

    def visualize(self, floor, isPrint=True):
        aggregatedArray = ["" for _ in range(4)]
        spaceArray = [" " * 4 for _ in range(4)]
        
        for l in self.lifts:
            liftArray = l.visualize(floor, False)

            aggregatedArray = [aggregatedArray[i] + liftArray[i] for i in range(4)]
            aggregatedArray = [aggregatedArray[i] + spaceArray[i] for i in range(4)]

        if isPrint:
            print "\n".join(aggregatedArray)
        else:
            return aggregatedArray


class Lift(object):

    def __init__(self, index, currentFloor=StaticValues.liftStartingFloor, capacity=StaticValues.liftCapacity):
        self.index = index
        self.currentUsers = []
        self.currentStatus = StaticValues.liftIdle
        self.currentFloor = currentFloor
        self.capacity = capacity
        self.directionToMove = None

    def deboard(self):
        if self.currentUsers:
            return self.currentUsers.pop(0)
        else:
            return None

    def board(self, user):
        self.currentUsers.append(user)
        self.currentUsers = sorted(self.currentUsers, key=itemgetter("destFloor"))

    def usersCount(self):
        return len(self.currentUsers)

    def nextDestination(self):
        if self.usersCount() > 0:
            return self.currentUsers[0].destFloor
        return None

    def visualize(self, floor, isPrint=True):
        if floor.value == self.currentFloor:
            val = [
                     " " +  "_" * 10 + " ",
                     ("|" +  " Lift: %s "  + "|") % str(self.index).zfill(2),
                     ("|" +  " Load: %s " + "|") % str(self.usersCount()).zfill(2),
                     "|" +  "_" * 10 + "|"
                     ]
        else:
            val = [
                 " " * 12 for _ in range(4)
                 ]

        if isPrint:
            print "\n".join(val)
        else:
            return val

    def moveOrDeboard(self, logs, usersDeboardedCount, powerConsumed):
        if self.currentFloor > self.nextDestination():
            self.currentFloor -= 1
            self.currentStatus = StaticValues.liftMoving
            powerConsumed += 1
            logs.append(StaticValues.liftMoving % {
                "liftIndex": self.index,
                "srcFloor": self.currentFloor + 1,
                "destFloor": self.currentFloor
                })
        elif self.currentFloor < self.nextDestination():
            self.currentFloor += 1
            self.currentStatus = StaticValues.liftMoving
            powerConsumed += 1
            logs.append(StaticValues.liftMoving % {
                "liftIndex": self.index,
                "srcFloor": self.currentFloor - 1,
                "destFloor": self.currentFloor
                })
        else:
            user = self.deboard()
            usersDeboardedCount += 1
            self.currentStatus = StaticValues.liftDeboarding

            logs.append(StaticValues.userDeboarding % {
                        "userIndex": user.index,
                        "userSrc": user.srcFloor,
                        "userDest": user.destFloor,
                        "liftIndex": self.index
            })

            if self.usersCount():
                self.directionToMove = StaticValues.goingUp if self.currentFloor < self.nextDestination() else \
                                        StaticValues.goingDown

        return logs, usersDeboardedCount, powerConsumed

    def run(self, floorManager, isBoardingAllowed=True):
        logs, usersDeboardedCount, powerConsumed = [], 0, 0

        if isBoardingAllowed and self.usersCount() < self.capacity and \
                 not floorManager.isFloorEmpty(self.currentFloor, self.directionToMove):
            user = floorManager.getUser(self.currentFloor, self.directionToMove)
            
            self.board(user)
            
            logs.append(StaticValues.userBoarding % {
                        "userIndex": user.index,
                        "userSrc": user.srcFloor,
                        "userDest": user.destFloor,
                        "liftIndex": self.index
            })
            
            if not self.directionToMove:
                self.directionToMove = user.travelType
            self.currentStatus = StaticValues.liftBoarding
        elif self.usersCount() > 0:
            logs, usersDeboardedCount, powerConsumed = self.moveOrDeboard(logs, usersDeboardedCount, powerConsumed)
        elif self.usersCount() == 0:
            self.directionToMove = None
            self.currentStatus = StaticValues.liftIdle

        return logs, usersDeboardedCount, powerConsumed

