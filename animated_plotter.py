# Updated to place the legend in a better position and put labels with the assignment's behavior ids.
# Updated to include the ability to plot paths and generate gifs.
#
# Require matplotlib
# To install run "pip install matplotlib==3.5.3" in command line / terminal
# Requires imageio
# To install imageio run "pip install imageio==2.21.3" in command line / terminal
# To run:
#  1. Place this file and the folders with your output to be plotted in the same folder
#  2. Open this file and change the variable folder to the name of the folder containing your trajectories.txt file.
#  3. Run in IDE, or run "animated_plotter.py'" in command line / terminal.

import time, csv, math, os
import matplotlib.pyplot as plt
import imageio.v2 as imageio

def distance(x1, y1, x2, y2):
    return ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** (1/2)

# Change this to data file name
def render(program_name, create_gif=True, extents=100):
    folder_name = f"output_data/{program_name}"
    frame_name = f"{folder_name}/trajectories.txt"
    paths_file = f"{folder_name}/paths.txt"
    points_file = f"{folder_name}/points.txt"

    PLOT_TITLE = f"{program_name} PVL NE1"
    do_orientation = False
    labels = {
        1: "Stop",
        6: "Seek",
        7: "Flee",
        8: "Arrive",
        11: "Follow Path"
    }
    point_colors = [
        "red",
        "orange",
        "yellow",
        "green",
        "blue",
        "magenta"
    ]
    line_thickness = 0.5
    constant = 3

    print("Loading data.")
    start_time = time.time()

    # ----------------------------------------------------------------------------------- Trajectory Data Processing ---
    # Mover class will hold data for each mover entity on the plot
    class Mover:
        def __init__(self, behavior):
            self.behavior = behavior  # steering behavior status code
            self.z = []  # position z (meters)
            self.x = []  # position x (meters)
            self.vXp = []  # values to plot velocity x (meters per second)
            self.vZp = []  # values to plot velocity z (meters per second)
            self.laXp = []  # values to plot linear acceleration x (meters per second per second)
            self.laZp = []  # values to plot linear acceleration z (meters per second per second)
            self.oXp = []  # values to plot orientation in x
            self.oZp = []  # values to plot orientation in z

    movers = {}  # create dictionary to store different movers
    time_entries = [0.0]
    try:
        with open(frame_name, 'r') as csvfile:
            csvreader = csv.reader(csvfile)

            for row in csvreader:
                if float(row[0]) != time_entries[-1]:
                    time_entries.append(float(row[0]))

                # If we find a new mover
                if row[1] not in movers:
                    movers[row[1]] = Mover(int(row[9]))  # add a new one to the dictionary

                # Grabbing the Mover object from the dict
                m = movers[row[1]]

                # Position Data
                m.x.append(float(row[2]))  # Position Y
                m.z.append(float(row[3]))  # Position Z

                # Velocity Data
                # (multiplied by constants to increase visibility)
                m.vXp.append((float(row[4]) * constant) + float(row[2]))  # Velocity X
                m.vZp.append((float(row[5]) * constant) + float(row[3]))  # Velocity Z

                # Acceleration Data
                m.laXp.append((float(row[6])) * constant + float(row[2]))  # Linear Acceleration X
                m.laZp.append((float(row[7])) * constant + float(row[3]))  # Linear Acceleration Z

                m.oXp.append((math.cos(float(row[8]))) + float(row[2]))  # Orientation X
                m.oZp.append((math.sin(float(row[8]))) + float(row[3]))  # Orientation Z
    except FileNotFoundError:
        print(f"Trajectories data file could not be found at \"{points_file}\"")

    # ----------------------------------------------------------------------------------------- Path Data Processing ---
    paths_data = []
    lines_data = []

    # The formatting of path files should be:
    #    path, id, point0x, point0y, point1x, point1y, ...
    # For example:
    #   "path, 0, 0, 90, -20, 65, 20, 40, -40, 15, 40, -10, -60, -35, 60, -60, 0, -85"
    #   This is the path for program 2

    try:
        with open(paths_file, "r") as csvfile:
            csvreader = csv.reader(csvfile)

            for row in csvreader:
                if row[0] == "path":
                    paths_data.append([])
                    for i in range(2, len(row), 2):
                        paths_data[int(row[1])].append([int(row[i]), int(row[i + 1])])

                if row[0] == "line":
                    lines_data.append([(int(row[1]), int(row[2])), (int(row[3]), int(row[4]))])

    except FileNotFoundError:
        print(f"Paths data file could not be found at \"{paths_file}\"")
    # ------------------------------------------------------------------------------ Temporary Point Data Processing ---
    points_data = {}
    try:
        with open(points_file, "r") as csv_file:
            csv_reader = csv.reader(csv_file)
            for row in csv_reader:
                point_time = float(row[0])

                if point_time not in points_data:
                    points_data[point_time] = []

                points_data[point_time].append([float(row[1]), float(row[2])])
    except FileNotFoundError:
        print(f"Points data file could not be found at \"{points_file}\"")

    print(f"Loaded data in {time.time() - start_time:.3f}s")

    # --------------------------------------------------------------------------------------------------- Plot Setup ---

    plt.xlabel('X')
    plt.ylabel('Z')
    plt.title(PLOT_TITLE)

    # create legend
    plt.plot(0, 0, color='red', label='position')
    plt.plot(0, 0, color='green', label='velocity')
    plt.plot(0, 0, color='blue', label='linear')
    if do_orientation:
        plt.plot(0, 0, color='yellow', label='orientation')

    plt.legend(loc='best')
    extents = (-extents, extents)
    plt.xlim(*extents)
    plt.ylim(*extents)

    xLineX = extents
    xLineY = [0, 0]
    yLineX = [0, 0]
    yLineY = extents
    plt.figure(figsize=(6, 6))

    # add dashed grey lines
    plt.plot(xLineX, xLineY, color='grey', linestyle='dashed', linewidth=1)
    plt.plot(yLineX, yLineY, color='grey', linestyle='dashed', linewidth=1)

    # ----------------------------------------------------------------------------------------------- Path Rendering ---
    for path_points in paths_data:
        lengths = []
        for i in range(len(path_points) - 1):
            x1, y1 = path_points[i][0], path_points[i][1]
            x2, y2 = path_points[i + 1][0], path_points[i + 1][1]
            plt.plot(
                [x1, x2], [y1, y2],
                color='grey', linestyle='dashed', linewidth=1
            )
            lengths.append(distance(x1, y1, x2, y2))

        total_length = sum(lengths)
        sum_of_lengths = 0
        for i, length in enumerate(lengths):
            sum_of_lengths += length / total_length
            point = path_points[i + 1]
            # plt.annotate(f"{sum_of_lengths:.2f}", color='grey', xy=(point[0] - 10, point[1] + 10))
            # plt.plot(*path_points[i], color='grey')
    # ----------------------------------------------------------------------------------------------- Line Rendering ---
    for line in lines_data:
        plt.plot([line[0][0], line[1][0]], [line[0][1], line[1][1]], xLineY, color='black', linewidth=1)

    for mov in movers:
        m = movers[mov]

        # Plot labels for steering behavior type
        label = ""
        if m.behavior in labels:
            label = labels[m.behavior]

        # This puts the steering behavior label on the graph
        plt.annotate(label, color='red', xy=(m.x[0] + 2, m.z[0] - 2))

        # add red dots to the start and end of each mover's trail
        plt.plot(m.x[0], m.z[0], color='red', marker='o', markerfacecolor='red', markersize=3)  # mark start position

    if create_gif and "frames" not in os.listdir():
        print("Generated a frames folder.")
        os.mkdir("frames")

    movers_list = list(movers.values())
    frame_names = []
    if create_gif:
        print(f"Generating {len(time_entries)} frames.")
    start_time = time.time()

    # ----------------------------------------------------------------------------------------- Trajectory Rendering ---
    for t in range(len(time_entries)):
        for u in range(len(movers_list)):
            mover = movers_list[u]

            x_pos, z_pos = mover.x[t], mover.z[t]

            # Velocity Line
            i = [x_pos, mover.vXp[t]]  # current x, current x + x velocity
            j = [z_pos, mover.vZp[t]]  # current z, current z + z velocity

            plt.plot(i, j, color='#5beb34', linewidth=line_thickness)  # green

            # Linear Acceleration
            i = [x_pos, mover.laXp[t]]  # current x, current x + x velocity
            j = [z_pos, mover.laZp[t]]  # current z, current z + z velocity

            plt.plot(i, j, color='blue', linewidth=line_thickness)

            # Orientation
            if do_orientation:
                i = [x_pos, mover.oXp[t]]  # current x, current x + x velocity
                j = [z_pos, mover.oZp[t]]  # current z, current z + z velocity

                plt.plot(i, j, color='yellow', linewidth=line_thickness)

            # Position
            if t + 1 < len(mover.x):
                i = [x_pos, mover.x[t + 1]]  # current x, next x
                j = [z_pos, mover.z[t + 1]]  # current z, next z

                plt.plot(i, j, color='red', linewidth=line_thickness)  # red

        if create_gif:
            remove_from_final = []
            if time_entries[t] in points_data:
                points = points_data[time_entries[t]]
                for i, point in enumerate(points):
                    remove_from_final += plt.plot(
                        point[0], point[1],
                        color=point_colors[i], marker='o', markerfacecolor='red', markersize=3
                    )

            frame_name = f"frames/frame_{t:03}.png"
            plt.savefig(frame_name, dpi=50)
            frame_names.append(frame_name)

            for thing in remove_from_final:
                thing.remove()

    print(f"Finished generating frames in {time.time() - start_time:.3f}s")

    for mov in movers:
        m = movers[mov]

        # Plot labels for steering behavior type
        label = ""
        if m.behavior in labels:
            label = labels[m.behavior]

        # This puts the steering behavior label on the graph
        plt.annotate(label, color='red', xy=(m.x[0] + 2, m.z[0] - 2))

        # add red dots to the start and end of each mover's trail
        plt.plot(m.x[0], m.z[0], color='red', marker='o', markerfacecolor='red', markersize=3)  # mark start position
        plt.plot(m.x[-1], m.z[-1], color='red', marker='o', markerfacecolor='red', markersize=4)  # mark end position

        # plot position
        # plt.plot(m.x, m.z, color='red', linewidth=1)

    if create_gif:
        print("Generating gif from frames.")
        start_time = time.time()
        # Build GIF
        if "frames" in os.listdir():
            if "image_files" not in os.listdir():
                print("Created image_files")
                os.mkdir("image_files")
            with imageio.get_writer('image_files/simulation.gif', mode='I') as writer:

                for i, frame_name in enumerate(frame_names):
                    print(f"{i/len(frame_names) * 100:0.2f}% complete.")

                    image = imageio.imread(frame_name)
                    writer.append_data(image)
                    os.remove(frame_name)

            print(f"Finished generating gif in {time.time() - start_time:.3f}s")

        else:
            print("Couldn't find frames directory.")
    else:
        plt.savefig("image_files/outputPlot.png", dpi=200)
    plt.show()


if __name__ == '__main__':
    render("program_2", False)
