import os

class ParentOutputManagerNotInstantiated(BaseException):
    message = f"In order to use OutputManager.__init__ without passing an output_path parameter," \
              f" an OutputManager must be instantiated in advance."

    def __init__(self):
        super().__init__(ParentOutputManagerNotInstantiated.message)


class OutputManager:
    managers = []

    @classmethod
    def get_output_manager(cls, manager_path: str = None):
        if not manager_path:
            if not OutputManager.managers:
                raise ParentOutputManagerNotInstantiated()
            return OutputManager.managers[0]
        else:
            OutputManager.managers.append(OutputManager(manager_path))
            return OutputManager.managers[-1]

    def __init__(self, output_path: str = None):

        self.data = {}
        self.output_path = output_path

        self._path_count = 0

    def write_trajectory(
            self,
            time: float,
            mover_id: int,
            mover_position_x: float,
            mover_position_y: float,
            mover_velocity_x: float,
            mover_velocity_y: float,
            mover_linear_acceleration_x: float,
            mover_linear_acceleration_y: float,
            mover_orientation: float,
            mover_movement_id: float,
            mover_collision_state: str
    ):

        data = [
            time, mover_id, mover_position_x, mover_position_y, mover_velocity_x, mover_velocity_y,
            mover_linear_acceleration_x, mover_linear_acceleration_y, mover_orientation, mover_movement_id,
            mover_collision_state
        ]

        string_data = []
        for element in data:
            if isinstance(element, float):
                string_data.append(f"{element:10.3f}")
            else:
                string_data.append(f"{element:10}")

        if "trajectories" not in self.data:
            self.data["trajectories"] = ""

        self.data["trajectories"] += ", ".join(string_data) + "\n"

    def write_path(self, *paths):  # paths: [Path]
        if "paths" not in self.data:
            self.data["paths"] = ""

        for path in paths:
            self.data["paths"] += f"path, {self._path_count}"

            for i in range(len(path.points)):
                self.data["paths"] += f", {path.points[i].x}, {path.points[i].y}"

            self.data["paths"] += "\n"
            self._path_count += 1

    def write_line(self, point1, point2):
        if "paths" not in self.data:
            self.data["paths"] = ""

        self.data["paths"] += f"line, {point1[0]}, {point1[1]}, {point2[0]}, {point2[1]}\n"

    def write_temporary_point(self, time, x: float, y: float):
        if "points" not in self.data:
            self.data["points"] = ""

        self.data["points"] += f"{time}, {x:10.2f}, {y:10.2f}\n"

    def write_other(self, other: str, line):
        if other not in self.data:
            self.data[other] = ""
        self.data[other] += line + "\n"

    def write_output_files(self):
        try:
            os.mkdir(self.output_path)
            print(f"Created directory \"{self.output_path}\".")
        except FileExistsError:
            print(f"Directory \"{self.output_path}\" exists already.")
        # Outputting the trajectories to a file
        for key in self.data:
            file_path = f"{self.output_path}/{key}.txt"
            with open(file_path, "w+") as file:
                file.write(self.data[key])
            print(f"Wrote {key} to \"{file_path}\"")


if __name__ == '__main__':
    try:
        test = OutputManager.get_output_manager()
    except ParentOutputManagerNotInstantiated:
        print("Failed to instantiate a child output manager.")

    om = OutputManager.get_output_manager("test")

    try:
        test = OutputManager.get_output_manager()
    except ParentOutputManagerNotInstantiated:
        print("Failed to instantiate a child output manager.")
    else:
        print("Successfully instantiated a child output manager.")
