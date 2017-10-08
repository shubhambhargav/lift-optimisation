# Assumptions/Restrictions
# 1. First come first serve
# 2. Lift's single direction movement for a given iteration

import os
from collections import defaultdict
from argparse import ArgumentParser

from user import User
from config import StaticValues
from utils import Utitilies


if __name__ == '__main__':
    parser = ArgumentParser(description="Lift power/time optimization.")
    parser.add_argument('--timeOptimizer', dest="timeOptimizer", type=int,
                            help="Number of iterations for user-time optimization.")
    parser.add_argument('--powerOptimizer', dest="powerOptimizer", type=int,
                            help="Number of iterations for power-consumption optimization.")
    parser.add_argument('--hasFutureInput', dest="hasFutureInput", type=bool,
                            help="If given true, program asks for addition of users if required before every iteration.")
    args = parser.parse_args()

    if args.timeOptimizer:
        StaticValues.optimizerConfig[StaticValues.timeOptimizer] = args.timeOptimizer
    if args.powerOptimizer:
        StaticValues.optimizerConfig[StaticValues.powerOptimizer] = args.powerOptimizer

    floorManager = Utitilies.getFloorManager()
    liftManager = Utitilies.getLiftManager()

    Utitilies.createUserConfig(floorManager)

    currentTime, totalUserTime, powerConsumed = 0, 0, 0
    floorManager.visualize(liftManager)

    while True:

        if args.hasFutureInput:
            print "Type 'y' and then press Enter to input users\n"

            nextStep = raw_input("Input: ")

            users = defaultdict(list)
            
            while nextStep == "y":
                sourceFloor = int(raw_input("Source floor: "))
                destionationFloor = int(raw_input("Destination floor: "))
                
                userIndex = floorManager.totalUsersCount() + 1
                users[sourceFloor].append(User(userIndex, sourceFloor, destionationFloor, currentTime))

                nextStep = raw_input("Another user? (Type 'y' for Yes and then press Enter) ")

            for floor, userList in users.iteritems():
                if userList:
                    floorManager.addUsers(floor, userList)
        else:
            raw_input()

        os.system('clear')

        currentTime += 1
        logs, usersDeboardedCount, iterationPowerConsumed = liftManager.runLifts(floorManager)

        totalUserTime += floorManager.totalUsersCount() + liftManager.totalUsersCount() + usersDeboardedCount
        powerConsumed += iterationPowerConsumed

        floorManager.visualize(liftManager)

        print "\nCurrent Time: %d second(s)\nTotal User Time: %d second(s)\nTotal Power Consumed: %d unit(s)" % (
                                                                                    currentTime,
                                                                                    totalUserTime,
                                                                                    powerConsumed
                                                                                    )

        print "\n::Logs Start::"
        print "\n".join(logs)
        print "::Logs End::"

        print "\nPress Ctrl+C or Cmd+C to stop the program at any point.\n"

