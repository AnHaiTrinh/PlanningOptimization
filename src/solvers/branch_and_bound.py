from .solver import Solver
import numpy as np


class BranchAndBoundSolver(Solver):
    def solve(self) -> int:
        visited = np.array([False] * (2 * self.n + 1))
        num_passengers = 0
        min_distance = np.inf
        current_distance = 0
        min_cost = np.min(self.costs)

        def check(num_stops):
            return num_passengers <= self.k and (current_distance + min_cost * (2 * self.n - num_stops)) < min_distance

        def Try(last_visited, num_stops):
            nonlocal current_distance, min_distance, num_passengers
            if num_stops == 2 * self.n:
                if current_distance + self.costs[last_visited][0] < min_distance:
                    min_distance = current_distance + self.costs[last_visited][0]
                return
            if check(num_stops):
                for i in range(1, self.n + 1):
                    if not visited[i]:
                        visited[i] = True
                        num_passengers += 1
                        current_distance += self.costs[last_visited][i]
                        Try(i, num_stops + 1)
                        visited[i] = False
                        num_passengers -= 1
                        current_distance -= self.costs[last_visited][i]
                    elif visited[i] and (not visited[i + self.n]):
                        visited[i + self.n] = True
                        num_passengers -= 1
                        current_distance += self.costs[last_visited][i + self.n]
                        Try(i + self.n, num_stops + 1)
                        visited[i + self.n] = False
                        num_passengers += 1
                        current_distance -= self.costs[last_visited][i + self.n]

        Try(0, 0)
        return min_distance
