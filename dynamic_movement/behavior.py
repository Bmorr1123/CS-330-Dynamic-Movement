from dynamic_movement import Vector, Mover, Target, Path
from output import OutputManager
import abc

class SteeringOutput:
    """
    This class is a data type meant to store linear acceleration and rotational acceleration data.

    :author: Ben Morrison
    """
    def __init__(self, linear=Vector(0, 0), angular=0):
        self.linear: Vector = linear
        self.angular: float = angular

class DynamicBehavior(abc.ABC):
    """
    This class is an Abstract Class that provides a template for making implementations of dynamic behaviors.

    :author: Ben Morrison
    """
    def __init__(self, character, target, id):
        """

        :param character: The Mover that is being controlled.
        :param target: The Mover that is the target of the character. For some behaviors it will be None.
        :param id: The id of the behavior.
        """
        self.character: Mover = character
        self.target: Mover = target

        self.id = id

    @abc.abstractmethod
    def execute(self, delta) -> SteeringOutput:
        """
        This function must be overridden for the Behavior to be used.
        :param delta:
        :return: (linear_acceleration: float, angular_acceleration: float)
        """
        ...

class Continue(DynamicBehavior):
    """
    This is an implementation of the dynamic Continue behavior.

    Movers with this behavior just continue what they were doing.

    :author: Ben Morrison
    """
    def __init__(self, character):
        super().__init__(character, None, 1)

    def execute(self, delta) -> SteeringOutput:
        # This just returns what they were doing.
        return SteeringOutput(self.character.linear_acceleration, self.character.angular_acceleration)

class Seek(DynamicBehavior):
    """
    This is an implementation of the dynamic Seek behavior defined in AI for Games by Ian Millington.

    :author: Ben Morrison
    """
    def __init__(self, character, target):
        super().__init__(character, target, 6)

        self.max_acceleration = self.character.max_linear_acceleration

    def execute(self, delta) -> SteeringOutput:
        result = SteeringOutput()

        # Calculate the difference between the positions.
        result.linear = self.target.position - self.character.position

        # Clip the acceleration towards target to the max acceleration of the character
        result.linear = result.linear.normalize() * self.max_acceleration

        return result

class Flee(DynamicBehavior):
    """
    This is an implementation of the dynamic Flee behavior defined in AI for Games by Ian Millington.

    :author: Ben Morrison
    """
    def __init__(self, character, target):
        super().__init__(character, target, 7)

        self.max_acceleration = self.character.max_linear_acceleration

    def execute(self, delta) -> SteeringOutput:
        result = SteeringOutput()

        # Calculate the difference between the two positions, reversed to Seek to invert the direction.
        result.linear = self.character.position - self.target.position

        # Clip the acceleration to the maximum acceleration of the character
        result.linear = result.linear.normalize() * self.max_acceleration

        return result

class Arrive(DynamicBehavior):
    """
    This is an implementation of the dynamic Arrive behavior defined in AI for Games by Ian Millington.

    :author: Ben Morrison
    """
    def __init__(self, character, target, target_radius, slow_radius, time_to_target=0.1):
        super().__init__(character, target, 8)
        self.max_acceleration = self.character.max_linear_acceleration
        self.max_speed = self.character.max_speed
        self.target_radius = target_radius
        self.slow_radius = slow_radius
        self.time_to_target = time_to_target

    def execute(self, delta) -> SteeringOutput:
        result = SteeringOutput()

        # Calculate the difference between the positions
        direction = self.target.position - self.character.position

        # Find the distance between the positions
        distance = direction.magnitude()

        # Check if we have arrived
        if distance < self.target_radius:
            return result

        # Check if we should attempt to reach max_speed or a lower speed
        target_speed = self.max_speed
        if distance <= self.slow_radius:
            target_speed = self.max_speed * distance / self.slow_radius

        # Converting speed to velocity
        target_velocity = direction.normalize()
        target_velocity *= target_speed

        # Acceleration is matched to target arrival time
        result.linear = target_velocity - self.character.velocity  # Ideal acceleration
        result.linear /= self.time_to_target  # Matching acceleration to desired arrival time

        # Clipping
        if result.linear.magnitude() > self.max_acceleration:
            result.linear = result.linear.normalize() * self.max_acceleration

        return result

class FollowPath(Seek):
    def __init__(self, character, path, path_offset=0.1):
        super().__init__(character, Target())
        self.id = 11

        self.path: Path = path
        self.path_offset = path_offset
        self.current_param = 0

        self.time = 0
        self.output_manager: OutputManager = OutputManager.get_output_manager()

    def execute(self, delta) -> SteeringOutput:

        # Updating param based on current position
        self.current_param, closest_point_on_path = self.path.get_param(self.character.position)
        # I added closest_point_on_path so that I could draw it in my gifs

        # Closest point on path
        # closest_point_on_path = self.path.get_position(self.current_param)
        # self.output_manager.write_temporary_point(self.time, closest_point_on_path.x, closest_point_on_path.y)

        # Making us a little further along the path
        self.current_param += self.path_offset

        # Finding the target point
        self.target.position = self.path.get_position(self.current_param)
        # self.output_manager.write_temporary_point(self.time, self.target.position.x, self.target.position.y)

        # Distance between closest point and target point
        distance_to = (closest_point_on_path - self.target.position).magnitude()

        # Distance to target
        # distance_to = (self.target.position - self.character.position).magnitude()
        # print(f"Distance To Target: {distance_to}")
        self.time += delta
        return super().execute(delta)
