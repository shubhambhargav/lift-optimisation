How to start the Application
==

* Go to the folder where the app is extracted.
* Run the following code from command line:
    ```python runner.py```

_For help_:

```python runner.py --help```

Output Description:
--
When the app starts, you will be shown with the initial configuration of the system.

To move to the next instance of time i.e. t + 1, just press enter. You will see that the configuration is reloaded with the updated changes.

In addition you will see the following information:

* Current Time : Number of instances of time passed since the app started.
* Total User Time : Aggregated user time till now including waiting time, travel time etc.
* Total Power Consumption : Aggregated power consumption of all the lifts till now.
* Logs : Activity logs showing the activities that happened in the previous instance of time.

Additional parameters:
-- 
--timeOptimizer (Default: 1. Number of times user-time optimisation should kick in out of total optimizations)

--powerOptimizer (Default: 1. Number of times power optimisation should kick in out of total optimizations)

--hasFutureInput (Default: false. If given true, program asks for addition of users if required before every iteration)

**Sample code with parameters**

```python runner.py --timeOptimizer 3 --powerOptimizer 4 --hasFutureInput true```

The above code signifies that out of 7 (i.e. 4+3) runs, in 4 runs, power optimization will be done and in 3 runs, time optimization will be done.

_Disclaimer_: If the above parameters are not provided, the default values of **timeOptimizer=1** and **powerOptimizer=1** kicks in.

Users' Configuration Changes:
--
Default configuration is set in `config.py` under `StaticValues` class as a variable called `usersConfigBasic`.

The format of the stored value is as following:

```
{
    <sourceFloorNumber1> : {
                            <destinationFloorNumber1> : <userCount1>,
                            <destinationFloorNumber2> : <userCount2>,
                            <destinationFloorNumber3> : <userCount3>
                            },
    <sourceFloorNumber2> : {
                            <destinationFloorNumber3> : <userCount4>,
                            <destinationFloorNumber4> : <userCount5>,
                            <destinationFloorNumber5> : <userCount6>
                            },
    ...
}
```

**This configuration is visible when the app starts. By changing the configuration at the given location, you will be able to see the changes once the app restarts.**