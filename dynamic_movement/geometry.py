from dynamic_movement import *


def closest_point(point1: Vector, point2: Vector, position: Vector):

    # Calculating Q-P
    line: Vector = point2 - point1
    # Calculating X-P
    relative_position = position - point1

    # Putting it together for (X-P).dot(Q-P) / (Q-P).dot(Q-P)
    percentage_along_line = (relative_position * line) / (line * line)
    # Clips the float to the range [0, 1]
    percentage_along_line = max(min(percentage_along_line, 1), 0)

    return point1 + line * percentage_along_line


class Path:
    def __init__(self, *points: [tuple]):
        self.points: [Vector] = [Vector(*point) for point in points]

        distances = [(self.points[i + 1] - self.points[i]).magnitude() for i in range(len(self.points) - 1)]
        path_length = sum(distances)
        self.relative_distances = [distance / path_length for distance in distances]

    def get_param(self, position: Vector) -> float:

        smallest_distance = 100_000_000  # Essentially Inf
        line_index = 0  # Eventually the index of the closest line
        closest_point_on_path = self.points[0]  # Eventually the exact closest point
        # Loops through every pair of points
        for i in range(len(self.points) - 1):
            # The pair of points the line consists of
            point1, point2 = self.points[i], self.points[i + 1]

            # Using the math supplied in the slides
            point_on_line = closest_point(point1, point2, position)

            # Calculating the distance between the point on the line and the character's position
            distance = (point_on_line - position).magnitude()

            # Checking if this point is the new closest
            if distance < smallest_distance:
                # Updating the variables to information of the closest line
                smallest_distance = distance
                line_index = i
                closest_point_on_path = point_on_line

        # print(f"[{closest_point_on_path.x: 5.2f}, {closest_point_on_path.y:5.2f}],")
        # print(f"Closest Line: {line_index:3}")

        # Calculating the percentage of the path that is before the closest line
        param = 0
        for i in range(line_index):
            param += self.relative_distances[i]

        # Finding the points of the closest line
        point1 = self.points[line_index]
        point2 = self.points[line_index + 1]

        # Adding the distance along the closest line
        param += (closest_point_on_path - point1).magnitude() / (point2 - point1).magnitude() * self.relative_distances[line_index]

        # Returning both the param and closest point for debugging purposes
        return param, closest_point_on_path

    def get_position(self, param: float) -> Vector:

        # Clipping param to range [0, 1]
        param = min(1.0, max(0.0, param))
        # print(f"Param: {param:04.2f}")

        i = 0   # Finding the index of the closest line based on the parameter
        while param > self.relative_distances[i] and i < len(self.relative_distances) - 1:
            param -= self.relative_distances[i]  # We subtract so we can calculate percentage
            i += 1

        # print(f"Lerp Line: {i:3}")

        # Percentage along line i
        percentage = param / self.relative_distances[i]

        # Clipping percentage to range [0, 1]
        percentage = min(1.0, max(0.0, percentage))
        # print(f"Lerp Percentage: {percentage*100:5.2f}%")

        # Grabbing the points on each end of the closest line
        first, second = self.points[i], self.points[i + 1]

        # Calculating the weighted average of the two points
        ret = first.lerp(second, percentage)

        # print(f"Target Position: {ret}")
        return ret


def main():
    path = Path((0, 0), (10, 10), (50, 0))

    diff = Vector(10, 5)

    print(f"Magnitude: {diff.magnitude() ** 2}")
    print(f"Dot Prod: {diff * diff}")

    print(param := path.get_param(Vector(7, 3)))
    print(path.get_position(param + .25))


if __name__ == '__main__':
    main()
