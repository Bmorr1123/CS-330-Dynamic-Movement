"""
The main program of the first assignment of CS 330 at UAH.

This program implements the following dynamic AI behaviors:
    1 = Continue
    6 = Seek
    7 = Flee
    8 = Arrive

Then it outputs the trajectories of movers implementing this behaviors to a .txt file.

Author: Ben Morrison
Class: CS 330-01 (Fall '22)
Date: 9/11/2022
"""
from dynamic_movement import *

pi = 3.14

def program_1():

    program_name = "program_1"

    movers = []

    # Instantiating the Mover that implements the Continue
    mover = Mover(2601)
    mover.set_movement_behavior(Continue(mover))
    movers.append(mover)

    # Instantiating the Mover that implements the Flee
    mover = Mover(
        2602,
        position=Vector(-30, -50),
        velocity=Vector(2, 7),
        orientation=pi/4,
        max_speed=8,
        max_linear_acceleration=1.5
    )
    mover.set_movement_behavior(Flee(mover, movers[0]))
    movers.append(mover)

    # Instantiating the Mover that implements the Seek
    mover = Mover(
        2603,
        position=Vector(-50, 40),
        velocity=Vector(0, 8),
        orientation=3 * pi / 2,
        max_speed=8,
        max_linear_acceleration=2
    )
    mover.set_movement_behavior(Seek(mover, movers[0]))
    movers.append(mover)

    # Instantiating the Mover that implements the Arrive
    mover = Mover(
        2604,
        position=Vector(50, 75),
        velocity=Vector(-9, 4),
        orientation=pi,
        max_speed=10,
        max_linear_acceleration=2
    )
    mover.set_movement_behavior(Arrive(mover, movers[0], 4, 32, 1))
    movers.append(mover)

    # Instantiating the Simulation
    sim = Simulation(program_name, 0.5, movers)

    # Simulating 50 seconds
    sim.simulate(50)

    sim.write_output_files()

    return program_name

def program_2():

    program_name = "program_2"

    movers = []
    paths = []
    sim = Simulation(program_name, 0.5, movers, paths)

    mover = Mover(
        id=2701,
        position=Vector(20, 95),
        velocity=Vector(0, 0),
        max_speed=4,
        max_linear_acceleration=2
    )
    path = geometry.Path(
        (0, 90),
        (-20, 65),
        (20, 40),
        (-40, 15),
        (40, -10),
        (-60, -35),
        (60, -60),
        (0, -85)
    )
    paths.append(path)
    mover.set_movement_behavior(FollowPath(
        mover, path, 0.04
    ))
    movers.append(mover)

    # Simulate 125 seconds of dynamic movement
    sim.simulate(125)

    sim.write_output_files()

    return program_name

def main():
    return program_2()


if __name__ == '__main__':
    main()
