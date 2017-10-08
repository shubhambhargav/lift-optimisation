
class StaticValues:

    lifts = 10
    liftCapacity = 10
    floors = 10
    liftStartingFloor = 0

    goingUp = "goingUp" # for user/lift
    goingDown = "goingDown" # for user/lift

    # Lift Status
    liftMoving = "moving"
    liftBoarding = "boarding"
    liftDeboarding = "deboarding"
    liftIdle = "idle"

    # OptimizerConfig Parameters
    timeOptimizer = "timeOptimizer"
    powerOptimizer = "powerOptimizer"

    optimizerConfig = {
        timeOptimizer: 1,
        powerOptimizer: 1
    }

    # Log Formats
    optimization = "[Optimization] Paramter optimized: %(parameter)s"
    userBoarding = "[Boarding] User %(userIndex)s boarded lift %(liftIndex)s at floor %(userSrc)s for destination floor %(userDest)s"
    userDeboarding = "[Deboarding] User %(userIndex)s deboarded lift %(liftIndex)s at floor %(userDest)s from source floor %(userSrc)s"
    liftMoving = "[LiftMoving] Lift %(liftIndex)s moved from floor %(srcFloor)s to floor %(destFloor)s"

    # User Config Basic
    usersConfigBasic = {
                        1: {
                            2: 10,
                            3: 4,
                            9: 12
                        },
                        5: {
                            3: 5,
                            8: 12
                        },
                        7: {
                            0: 15,
                            2: 16
                        },
                        9: {
                            4: 24,
                            1: 12
                        }
                    }