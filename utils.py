from config import StaticValues

from user import User
from floor import Floor, FloorManager
from lift import Lift, LiftManager


class Utitilies:

    @staticmethod
    def createUserConfig(floorManager, usersConfigBasic=StaticValues.usersConfigBasic):
        userCount = 0
        for src, config in usersConfigBasic.items():
            for dest, n in config.items():
                floorManager.addUsers(src, [User(userCount + i, src, dest) for i in range(n)])

                userCount += (n-1)

    @staticmethod
    def getFloorManager(floorsCount=StaticValues.floors):
        return FloorManager([Floor(i) for i in range(floorsCount)])

    @staticmethod
    def getLiftManager(liftsCount=StaticValues.lifts):
        return LiftManager([Lift(i) for i in range(liftsCount)])