from .solver import Solver
import numpy as np


class BranchAndBoundSolver2(Solver):
    def solve(self) -> int:
        visited = np.array([False] * (2 * self.n + 1))
        num_passengers = 0
        min_distance = np.inf
        visited_last = 0
        current_distance = 0
        current_paths = [0] * (2 * self.n + 1)
        nonzero_values = self.costs[self.costs > 0]
        min_cost = np.min(nonzero_values) if len(nonzero_values) > 0 else None
        def check_can_visit(current_pos):
            if visited[current_pos]:
                return False
            if current_pos <= self.n:
                if num_passengers >= self.k:
                    return False
            else:
                if num_passengers <= 0 or not visited[current_pos - self.n]:
                    return False
            return True
        
        def check_can_bound(step):
            return current_distance + min_cost * (2 * self.n - step) < min_distance

        def backtrack(step):
            nonlocal current_distance, min_distance, num_passengers, visited_last
            temp_visited_last = visited_last
            if step == 2 * self.n:
                if current_distance + self.costs[visited_last][0] < min_distance:
                    min_distance = current_distance + self.costs[visited_last][0]
                return
            if check_can_bound(step):
                for i in range(1, 2 * self.n + 1):
                    if check_can_visit(i):
                        if i <= self.n:
                            num_passengers += 1
                        else:
                            num_passengers -= 1
                        current_distance += self.costs[current_paths[step-1]][i]
                        visited[i] = True
                        current_paths[step] = i
                        visited_last = i
                        backtrack(step + 1)
                        visited[i] = False
                        current_distance -= self.costs[current_paths[step-1]][i]
                        visited_last = temp_visited_last
                        if i <= self.n:
                            num_passengers -= 1
                        else:
                            num_passengers += 1

        backtrack(0)
        return int(min_distance)
