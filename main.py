from window import *

# Press Maj+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

# Press the green button in the gutter to run the script.


def read_data(filename):
    with open(filename) as file:
        string = file.readline().strip()
        if string == "":
            s_1 = []
        else:
            s_1 = list(map(int, string.split()))
        string = file.readline().strip()
        if string == "":
            s_2 = []
        else:
            s_2 = list(map(int, string.split()))
        n = len(s_1) + len(s_2)
        edges = []
        for _ in range(n):
            line = list(map(convert, file.readline().strip().split()))
            edges.append(line)
        return TwoPlayerGame(s_1, s_2, edges)


def convert(s):
    if s == 'x':
        return float('-inf')
    return int(s)


if __name__ == '__main__':
    game = read_data("tests/test3.txt")
    for i in range(3, 4):
        res_old = game.fw_mp(i, "old_updated")
        res_new = game.fw_mp(i, "new")
        if res_old != res_new:
            print("\nRes:\n\n", res_old, res_new, i)

    print("Done !")
