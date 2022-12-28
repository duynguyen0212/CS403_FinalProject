"""
Testing file used to test the map function for the rovers
"""
import random
from rover import Rover

rover = Rover


def readMap(map, filename):
    mapFile = open(filename, "r")
    columns = mapFile.readlines()
    for column in columns:
        column = column.strip()
        row = [i for i in column]
        map.append(row)



def random_location(map):
    # map = []
    # readMap(map, "map1.txt")
    found_empty_location = False
    while found_empty_location is False:
        rol = random.randint(0, map.__len__()-1)
        col = random.randint(0, map[0].__len__()-1)
        if map[rol][col] == " ":
            map[rol][col] = "O"
            found_empty_location = True

    return map


def print_map():
    map = []

    try:
        readMap(map, "map10.txt")
        new_map = random_location(map)
        for i in new_map:
            print("".join(i))

    except FileNotFoundError:
        print("No such file was found")




def main():
    print_map()


if __name__ == "__main__":
    main()
