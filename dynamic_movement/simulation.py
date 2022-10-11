import time
from output import OutputManager
from dynamic_movement import Mover

class Simulation:
    """
    An object used to simplify the simulation of the behaviors and used to handle the output of movement.
    """
    def __init__(self, sim_name, time_step, movers, paths=None):
        """
        The function that constructs a Simulation object.

        :param movers: A list of mover objects to tick and output in the simulation.
        :param time_step: The amount of time to simulate between each tick of the simulation.
        """
        self.sim_name = sim_name

        self.movers = movers
        self.time_step = time_step

        if not paths:
            paths = []
        self.paths = paths

        self._total_time = 0

        self.output_manager: OutputManager = OutputManager.get_output_manager(f"output_data/{sim_name}")

    def add_mover(self, mover: Mover):
        self.movers.append(mover)

    def add_path(self, path):
        self.paths.append(path)

    def generate_line(self, time, mover: Mover):
        """
        This function adds a line for a single mover at a single moment to the output string.

        :param time: The time of the simulation at this moment.
        :param mover: The mover to output the data on.
        """
        self.output_manager.write_trajectory(
            time,
            mover.id,
            mover.position.x,
            mover.position.y,
            mover.velocity.x,
            mover.velocity.y,
            mover.linear_acceleration.x,
            mover.linear_acceleration.y,
            mover.orientation,
            mover.movement_id,
            str(mover.collision_state).upper()
        )

    def simulate(self, seconds):
        """
        This function simulates the given amount of time one time step at a time.

        :param seconds: The amount of time to simulate.
        """
        start_time = time.time()
        sim_time = 0
        while sim_time <= seconds:

            for mover in self.movers:
                self.generate_line(self._total_time, mover)
                mover.tick(self.time_step)

            sim_time += self.time_step
            self._total_time += self.time_step

        print(f"Simulated {sim_time:.3f} seconds of the simulation in {time.time() - start_time:.4f} seconds realtime.")

    def write_output_files(self):
        if self.paths:
            self.output_manager.write_path(*self.paths)

        self.output_manager.write_output_files()
