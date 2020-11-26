import copy


class TwoPlayerGame:  # Only for one dimensional 2 player game

    def __init__(self, s_1, s_2, edges):
        self.size = len(s_1) + len(s_2)
        self.S = []
        self.tab_label = s_1 + s_2
        self.tab_label.sort()
        for i in self.tab_label:
            if i in s_1:
                self.S.append(1)
            else:
                self.S.append(2)
        self.edges = edges  # Weighted adjacency matrix (- infinity if no edge)

    def label(self, index):
        return self.tab_label[index]

    def sub_game(self, vertex):
        new_s_1 = [s for s in vertex if self.S[s] == 1]
        new_s_2 = [s for s in vertex if self.S[s] == 2]
        new_edges = [[self.edges[u][v] for v in vertex] for u in vertex]
        return TwoPlayerGame(new_s_1, new_s_2, new_edges)

    def attractor(self, target, player):  # target is a dict
        set_res = target
        set_res_old = []
        while set_res_old != set_res:
            set_res_old = copy.copy(set_res)
            for s in range(self.size):
                if s not in set_res:  # s not in res yet
                    if self.S[s] == player:  # s belongs to player 1
                        for t in range(self.size):
                            if self.edges[s][t] != float('-inf') and t in set_res:
                                set_res.append(s)
                                break
                    else:  # s belongs to the other player
                        good_candidate = True
                        for t in range(self.size):
                            if self.edges[s][t] != float('-inf') and t not in set_res:
                                good_candidate = False
                                break
                        if good_candidate:
                            set_res.append(s)
        return set_res

    def good_windows_old(self, l_max, semi_update=True):
        c = [[0 for _i in range(l_max+1)] for _s in range(self.size)]
        for i in range(1, l_max+1):
            for s in range(self.size):
                choices = [self.edges[s][t] + c[t][i-1]
                           for t in range(self.size) if self.edges[s][t] != float('-inf')]
                if self.S[s] == 1:  # s belongs to player 1
                    c[s][i] = max(choices)
                else:  # s belongs to player 2
                    if semi_update:
                        choices = [max(self.edges[s][t], self.edges[s][t] + c[t][i - 1])
                                   for t in range(self.size) if self.edges[s][t] != float('-inf')]
                    c[s][i] = min(choices)
        if semi_update:
            print("c_old_semi_update :", c)  # TO CHANGE
            res = [s for s in range(self.size) if c[s][l_max] >= 0]
        else:
            res = []
            for s in range(self.size):
                for i in range(1, l_max+1):
                    if c[s][i] >= 0:
                        res.append(s)
                        break
        return res

    def good_windows_new(self, l_max):
        c = [[0 for _i in range(l_max+1)] for _s in range(self.size)]
        for i in range(1, l_max+1):
            for s in range(self.size):
                choices = [max(self.edges[s][t], self.edges[s][t] + c[t][i-1])
                           for t in range(self.size) if self.edges[s][t] != float('-inf')]
                if self.S[s] == 1:  # s belongs to player 1
                    c[s][i] = max(choices)
                else:  # s belongs to player 2
                    c[s][i] = min(choices)
        print("c_new :", c)
        return [s for s in range(self.size) if c[s][l_max] >= 0]

    def dfw_mp(self, l_max, version="new"):
        if version == "new":
            w_gw = self.good_windows_new(l_max)
        else:
            w_gw = self.good_windows_old(l_max)
        if len(w_gw) == len(self.S) or w_gw == []:
            w_d = w_gw
        else:
            w_not_gw = [s for s in range(self.size) if s not in w_gw]
            w_not_safe = self.attractor(w_not_gw, 2)
            w_safe = [s for s in w_gw if s not in w_not_safe]
            s_g = self.sub_game(w_safe)
            w_d = s_g.dfw_mp(l_max, version)
            w_d = list(map(s_g.label, w_d))
        return w_d

    def fw_mp(self, l_max, version="new"):
        w = []
        actual_game = self
        while True:
            w_d = actual_game.dfw_mp(l_max, version)
            w_attractor = actual_game.attractor(w_d, 1)
            w = [s for s in range(actual_game.size) if s in w or s in w_attractor]
            not_w = [s for s in range(actual_game.size) if s not in w]
            actual_game = actual_game.sub_game(not_w)
            if len(w) == self.size or w_attractor == []:
                break
        return w
