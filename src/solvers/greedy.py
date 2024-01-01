from src.solvers.solver import Solver


class GreedySolver(Solver):
    def solve(self) -> int:
        visited = set()
        current = 0
        visited.add(current)
        num_passengers = 0
        distance = 0
        while len(visited) < 2 * self.n + 1:
            possible_next_points = []
            for i in range(1, self.n + 1):
                if i in visited and i + self.n not in visited:
                    possible_next_points.append(i + self.n)
            if num_passengers < self.k:
                for i in range(1, self.n + 1):
                    if i not in visited:
                        possible_next_points.append(i)

            next_point = min(possible_next_points, key=lambda x: self.costs[current][x])
            distance += self.costs[current][next_point]
            visited.add(next_point)
            num_passengers += (1 if next_point <= self.n else -1)
            current = next_point

        distance += self.costs[current][0]
        return distance
