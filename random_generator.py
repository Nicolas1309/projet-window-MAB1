from random import random, randint
from window import *


def random_generator(n, threshold, w):
    separator = randint(0, n-1)
    s_1 = [i for i in range(separator)]
    s_2 = [i for i in range(separator, n)]
    tab = [[float('-inf') for _j in range(n)] for _i in range(n)]
    for i in range(n):
        j = randint(0, n-1)
        tab[i][j] = randint(-w, w)
    for i in range(n):
        for j in range(n):
            if random() < threshold:
                tab[i][j] = randint(-w, w)
    return TwoPlayerGame(s_1, s_2, tab)


if __name__ == "__main__":
    n = 1
    threshold = 0.4
    w = 3
    max_iter = 100
    found_counterexample = False
    for _ in range(max_iter):
        game = random_generator(n, threshold, w)
        for i in range(1, 15):
            res_old = game.fw_mp(i, "old")
            res_new = game.fw_mp(i, "new")
            if res_old != res_new:
                print("Counterexample: \n\n")
                print(game.S)
                for line in range(n):
                    print(game.edges[line])
                print("\n\n")
                found_counterexample = True
                print("\nRes:\n\n", res_old, res_new, i)
                break
            else:
                pass  # print("No difference !")
        if found_counterexample:
            break
