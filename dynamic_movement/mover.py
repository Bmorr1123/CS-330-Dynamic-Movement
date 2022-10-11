from dynamic_movement import *

class Target:
    def __init__(self, position: Vector = Vector(0, 0)):
        self.position = position

class Mover(Target):
    """
    This class is an implementation of the Dynamic Mover to be used to test Dynamic Behaviors.

    Both rotational and linear accelerations can be used to control instances of this class.

    :author: Ben Morrison
    """
    def __init__(
            self,
            id,
            position: Vector = Vector(0, 0),
            orientation: float = 0,
            max_speed: float = 0,
            max_linear_acceleration: float = 0,
            max_angular_acceleration: float = 10000,
            velocity: Vector = Vector(0, 0)
    ):
        super().__init__(position)

        self.id = id
        self.movement_behavior: DynamicBehavior = None

        # Linear Physics Values
        self.velocity = velocity
        self.linear_acceleration = Vector(0, 0)

        self.max_speed = max_speed
        self.max_linear_acceleration = max_linear_acceleration

        # Angular Physics Values
        self.orientation = orientation
        self.rotation = 0
        self.angular_acceleration = 0

        self.max_angular_acceleration = max_angular_acceleration

        self.collision_state = False

    def set_movement_behavior(self, movement_behavior):
        self.movement_behavior = movement_behavior

    def get_movement_behavior_id(self):
        return self.movement_behavior.id

    def tick(self, delta):
        """
        This function is used to tick the movement behavior and the physics step of the Mover.
        :param delta: The amount of time during the step.
        """
        if not self.movement_behavior:
            raise ValueError("Movement Behavior not Assigned!")

        steering = self.movement_behavior.execute(delta)
        self.linear_acceleration = steering.linear
        self.angular_acceleration = steering.angular

        self.physics_tick(delta)

    def physics_tick(self, delta):
        """
        This function performs a step of physics for a certain amount of time.
        :param delta: The time step between ticks.
        """
        self.position += self.velocity * delta
        self.orientation += self.rotation * delta

        self.velocity += self.linear_acceleration * delta
        self.rotation += self.angular_acceleration * delta

        if self.max_speed != 0 and self.velocity.magnitude() > self.max_speed:
            self.velocity = self.velocity.normalize() * self.max_speed

    movement_id = property(get_movement_behavior_id)
