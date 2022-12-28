"""
Name: Ngoc Duy Nguyen
Subject: CS403 Final Project

How to build, run the project: just as the instruction in CS403 Final project
in CMD run python rover.py
than in the other ones run python main.py parsing-tests\test.txt Rover1
"""
import multiprocessing
import pathlib
import random
import time
import traceback

import parser

# The maximum amount of time that the rover can run in seconds
MAX_RUNTIME = 36000

# Rover direction
direction = ["North", "East", "South", "West"]
direction_index = 0
forward = direction[direction_index]

# Rovers that exist
ROVER_1 = "Rover1"
ROVER_2 = "Rover2"
ROVERS = [ROVER_1, ROVER_2, ]
cmd_rover1 = False
cmd_rover2 = False
# Command file is stored within the rover directory. Here we're building one file
# for each of the rovers defined above
ROVER_COMMAND_FILES = {rover_name: pathlib.Path(pathlib.Path(__file__).parent.resolve(), f"{rover_name}.txt") for
                       rover_name in ROVERS}
for _, file in ROVER_COMMAND_FILES.items():
    with file.open("w") as f:
        pass

# Constant used to store the rover command for parsing
ROVER_COMMAND = {rover_name: None for rover_name in ROVERS}


def get_command(rover_name):
    """Checks, and gets a command from a rovers command file.

    It returns True when something was found, and False
    when nothing was found. It also truncates the contents
    of the file if it found something so that it doesn't
    run the same command again (unless it was re-run from
    the controller/main program).
    """
    fcontent = None
    with ROVER_COMMAND_FILES[rover_name].open() as f:
        fcontent = f.read()
    if fcontent is not None and fcontent:
        ROVER_COMMAND[rover_name] = fcontent
        with ROVER_COMMAND_FILES[rover_name].open("w+") as f:
            pass
        return True
    if rover_name == ROVER_1:
        global cmd_rover1
        cmd_rover1 = True
    else:
        global cmd_rover2
        cmd_rover2 = True
    return False


class Rover(object):
    def __init__(self, name, row, col, map, forward):
        self.name = name
        self.row = row
        self.col = col
        self.map = map
        self.forward = forward

    def print(self, msg):
        print(f"{self.name}: {msg}")

    def parse_and_execute_cmd(self, command):
        print(f"Running command: {command}")
        result, error = parser.run('<stdin>', command)
        if error:
            print(error.as_string())
        else:
            print(result)
        pass

    def wait_for_command(self):
        start = time.time()
        while (time.time() - start) < MAX_RUNTIME:
            # Sleep 1 second before trying to check for
            # content again
            self.print("Waiting for command...")
            time.sleep(1)
            if get_command(self.name):
                self.print("Found a command...")
                try:
                    self.parse_and_execute_cmd(ROVER_COMMAND[self.name])
                except Exception as e:
                    self.print(f"Failed to run command: {ROVER_COMMAND[self.name]}")
                    self.print(traceback.format_exc())
                finally:
                    self.print("Finished running command.\n\n")

    """
    Random location method
    Put the rover on random location on the map
    """

    def random_location(self):
        print("Putting the rover on random location on the map: " + "(" + str(self.row) + "," + str(self.col) + ")")
        self.map[self.row][self.col] = "R"

    """
    Drilling method
    The rover will drill a hole in a wall in front of it
    If there's no wall the rover will prompt the message not able to drill
    """

    def drill(self):
        print(self.name + " is drilling...")

        if not self.can_move_forward():
            if self.forward == "North":
                if self.map[self.row - 1][self.col] == "X":
                    self.map[self.row - 1][self.col] = "D"
            elif self.forward == "East":
                if self.map[self.row][self.col + 1] == "X":
                    self.map[self.row][self.col + 1] = "D"
            elif self.forward == "South":
                if self.map[self.row + 1][self.col] == "X":
                    self.map[self.row + 1][self.col] = "D"
            else:
                if self.map[self.row][self.col - 1] == "X":
                    self.map[self.row][self.col - 1] = "D"
        else:
            print("Cannot drill because drilling spot is not a wall")

    """
    Rover's information will be display when this method is called
    """

    def info(self):
        print("Here's some info of " + self.name)
        print("Facing direction: " + str(self.forward))
        print("Current location: " + str(self.row) + ", " + str(self.col))
        print("Current map state:")
        for i in self.map:
            print("".join(i))

    """
    This method used to change map
    If the file map cannot found error message will be shown
    @param map_name
    """

    def change_map(self, map_name):
        name = str(map_name).lstrip('IDENTIFIER:') + '.txt'

        print("Switch to " + name)
        self.map = []
        try:
            readMap(self.map, name)
            print("Here is new map:")
            for i in self.map:
                print("".join(i))

        except FileNotFoundError:
            print(name + " was not found")

    """
    Switch the rover facing direction to the right
    """

    def turn_right(self):
        print("Turning right...")
        index = (direction_index + 1) % 4
        self.forward = direction[index]

    """
    Switch the rover facing direction to the left
    """

    def turn_left(self):
        print("Turing left...")
        index = (direction_index + 3) % 4
        self.forward = direction[index]

    """
    Make the rover move forward by replacing current location 'R' to ' '
    and put 'R' to new location
    """

    def move_forward(self):
        if self.can_move_forward():
            print("Moving forward...")
            self.map[self.row][self.col] = " "
            if self.forward == "North":
                self.row -= 1
            elif self.forward == "East":
                self.col += 1
            elif self.forward == "South":
                self.row += 1
            else:
                self.col -= 1
            self.map[self.row][self.col] = "R"
        else:
            print("Cannot move forward because of wall and hole")

    """
    Check if the rover can move forward based on its facing direction
    """

    def can_move_forward(self):
        flag = True
        if self.forward == "North":
            if self.map[self.row - 1][self.col] == "X" or self.map[self.row - 1][self.col] == "D":
                flag = False
        elif self.forward == "East":
            if self.map[self.row][self.col + 1] == "X" or self.map[self.row - 1][self.col] == "D":
                flag = False
        elif self.forward == "South":
            if self.map[self.row + 1][self.col] == "X" or self.map[self.row - 1][self.col] == "D":
                flag = False
        else:
            if self.map[self.row][self.col - 1] == "X" or self.map[self.row - 1][self.col] == "D":
                flag = False
        return flag


"""
Read map function
@param map
@param filename
"""


def readMap(map, filename):
    mapFile = open(filename, "r")
    columns = mapFile.readlines()
    for column in columns:
        column = column.strip()
        row = [i for i in column]
        map.append(row)
    return map


"""
This method used to generate random method for the rover
Using while loop to find empty spot and assign it as location for the rover
"""


def random_location():
    map = []
    readMap(map, "map1.txt")
    r = 0
    c = 0
    found_empty_location = False
    while found_empty_location is False:
        row = random.randint(0, map.__len__() - 1)
        col = random.randint(0, map[0].__len__() - 1)
        if map[row][col] == " ":
            map[row][col] = "R"
            found_empty_location = True
        r = row
        c = col

    return [r, c]


# Initialize the rovers out-side def method so it can be access in parser.py
result = random_location()
row = result[0]
col = result[1]
new_map = readMap([], "map1.txt")
rover1 = Rover(ROVER_1, row, col, new_map, forward)
rover2 = Rover(ROVER_2, row, col, new_map, forward)


def main():
    my_rovers = [rover1, rover2]
    # Run the rovers in parallel
    procs = []
    for rover in my_rovers:
        p = multiprocessing.Process(target=rover.wait_for_command, args=())
        p.start()
        procs.append(p)

    # Wait for the rovers to stop running (after MAX_RUNTIME)
    for p in procs:
        p.join()


if __name__ == "__main__":
    main()
