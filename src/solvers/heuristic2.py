from .solver import Solver
import time
import numpy as np

class Heuristic(Solver):
    MAX = 24

    def __init__(self, n, k, costs, optimal):
        self.m, self.p, self.min_c, self.l = 0, 0, float('inf'), 0
        self.c = np.zeros((self.MAX, self.MAX), dtype=int)
        self.visited = np.zeros(self.MAX, dtype=int)
        self.res = float('inf')
        self.cnt = 0
        self.k = k
        self.n = n
        self.costs = costs
        self.optimal = optimal

    def isValidEdge(self, v, prev, k):
        if self.c[prev][v] == 0 or self.visited[v]:
            return False
        tmp = self.cnt + self.c[prev][v] + (self.l - k) * self.min_c
        return tmp < self.res

    def explorePaths(self, k, prev):
        if k == (2 * self.n + 1):
            if self.c[prev][0] != 0:
                self.res = min(self.res, self.cnt + self.c[prev][0])
            return
        for v in range(1, 2 * self.n + 1):
            if v <= self.n:
                if self.p + 1 <= self.m:
                    if self.isValidEdge(v, prev, k):
                        self.p += 1
                        self.cnt += self.c[prev][v]
                        self.visited[v] = 1
                        self.explorePaths(k + 1, v)
                        self.p -= 1
                        self.cnt -= self.c[prev][v]
                        self.visited[v] = 0
            else:
                if self.visited[v - self.n]:
                    if self.isValidEdge(v, prev, k):
                        self.p -= 1
                        self.cnt += self.c[prev][v]
                        self.visited[v] = 1
                        self.explorePaths(k + 1, v)
                        self.p += 1
                        self.cnt -= self.c[prev][v]
                        self.visited[v] = 0

    def solve(self, n=0, m=0):
        m = self.k
        n = self.n
        self.n, self.m = n, m
        self.l = 2 * self.n + 1
        self.c[: self.costs.shape[0], : self.costs.shape[1]] = self.costs

        for i in range(2 * self.n + 1):
            for j in range(2 * self.n + 1):
                if self.c[i][j] > 0:
                    self.min_c = min(self.min_c, self.c[i][j])

        self.visited[0] = 1
        self.explorePaths(1, 0)
        return self.res

    # Heuristic version
    def heuristic_solve(self, n=0, m=0):
        # Implement your heuristic here
        return self.solve(n, m)
