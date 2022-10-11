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
import math, random
from random import randint, shuffle

pi = 3.14

def generate_maze(extents, cell_size):
    cells_per_line = int((extents[1] - extents[0]) / cell_size)
    points = [(x + 5, y + 5) for y in range(*extents, cell_size) for x in range(*extents, cell_size) ]
    edges = []
    for i, point in enumerate(points):
        if i + 1 < len(points) and i % cells_per_line != cells_per_line - 1:
            edges.append((i, i + 1))
        j = i + cells_per_line
        if j < len(points):
            edges.append((i, j))

    start = randint(0, len(points) - 1)
    todo = [(start, start)]
    visited = []
    connected_edges = []
    while todo:
        previous, current = todo.pop(-1)
        if current not in visited:
            visited.append(current)

            check = [current + cells_per_line, current - cells_per_line]
            mod = current % cells_per_line
            if mod != cells_per_line - 1:
                check.append(current + 1)
            if mod != 0:
                check.append(current - 1)

            shuffle(check)
            for i in check:
                if 0 <= i < len(points) and i not in visited:
                    todo.append((current, i))

            if previous > current:
                previous, current = current, previous
            connected_edges.append((previous, current))

    return points, edges, connected_edges

def generate_walls(extents, cell_size, points, edges, connected_edges):
    cells_per_line = int((extents[1] - extents[0]) / cell_size)

    output_manager: OutputManager = OutputManager.get_output_manager()
    # Drawing Walls
    for edge in set(edges).difference(connected_edges):
        i, j = edge
        i, j = points[i], points[j]

        xd, yd = j[0] - i[0], j[1] - i[1]

        x1, y1 = i[0] + xd//2, i[1] + yd//2
        x2, y2 = x1, y1
        if xd == 0:
            x1 -= cell_size // 2
            x2 += cell_size // 2
        if yd == 0:
            y1 -= cell_size // 2
            y2 += cell_size // 2

        output_manager.write_line((x1, y1), (x2, y2))

def find_path(start_index, end_index, points, connected_edges):
    # 1_000_000_000 is Inf as far as we're concerned
    visited = []
    distances = [1_000_000_000 for point in points]
    previous = [-1 for point in points]

    distances[start_index] = 0
    current_index = start_index

    while current_index != end_index:

        visited.append(current_index)

        neighbors = []
        for edge in connected_edges:
            if edge[0] == current_index:
                neighbors.append(edge[1])
            elif edge[1] == current_index:
                neighbors.append(edge[0])

        current_distance = distances[current_index]
        for neighbor in neighbors:
            if neighbor not in visited:
                if current_distance + 1 < distances[neighbor]:
                    distances[neighbor] = current_distance + 1
                    previous[neighbor] = current_index

        closest_index, min_distance = 0, 1_000_000_000
        for i, distance in enumerate(distances):
            if distance < min_distance and i not in visited:
                closest_index = i
                min_distance = distances[closest_index]

        current_index = closest_index

    path = []
    while current_index != start_index:
        path.append(current_index)
        current_index = previous[current_index]
    path.append(current_index)

    return path

def program_0():

    program_name = "program_0"

    sim = Simulation(program_name, 0.5, [], [])

    # path_points = [mover.position]
    # angle = 1 / 4 * math.pi
    # variation = math.pi / 2
    # segment_length = 25
    # for i in range(10):
    #     path_points.append((path_points[-1] + Vector(math.cos(angle), math.sin(angle)) * segment_length))
    #     angle += variation * (random.random() - random.random())
    #
    # path = Path(*[point.as_int_tuple() for point in path_points])

    # path_points = [(-90, -90)]
    # angle, length = 0, 180
    # for i in range(15):
    #     x, y = path_points[-1]
    #     x, y = (x + math.cos(angle) * length, y + math.sin(angle) * length)
    #     angle += pi / 2
    #     length -= 10
    #     path_points.append((int(x), int(y)))

    extents = 250
    extents, cell_size = [-extents, extents], 10
    points, edges, connected_edges = generate_maze(extents, cell_size)
    generate_walls(extents, cell_size, points, edges, connected_edges)
    path_points = [points[i] for i in find_path(randint(0, len(points)), randint(0, len(points)), points, connected_edges)]

    mover = Mover(
        0,
        position=Vector(*path_points[0]),
        velocity=Vector(0, 0),
        max_speed=1,
        max_linear_acceleration=0.25
    )

    path = Path(*path_points)
    mover.set_movement_behavior(FollowPath(mover, path, 4 * mover.max_speed / path.path_length))
    sim.add_mover(mover)
    sim.add_path(path)

    sim.simulate(int(path.path_length / mover.max_speed))

    sim.write_output_files()

    return program_name

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
    return program_0()


if __name__ == '__main__':
    main()
