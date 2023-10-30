from ortools.linear_solver import pywraplp
from .solver import Solver
from ..utils.generation import generate_real_subset


class IpSolver(Solver):
    def solve(self) -> int:
        M = 2 * self.n + 1
        solver = pywraplp.Solver.CreateSolver('SCIP')

        x = [[solver.IntVar(0, 1, f'x({i}, {j})') for j in range(2 * self.n + 1)] for i in range(2 * self.n + 1)]
        y = [solver.IntVar(0, 2 * self.n, f'y({i})') for i in range(2 * self.n + 1)]
        z = [solver.IntVar(0, self.n, f'z({i})') for i in range(2 * self.n + 1)]

        # Each point is visited once
        for i in range(2 * self.n + 1):
            solver.Add(sum(x[i][j] for j in range(2 * self.n + 1)) == 1)
            solver.Add(sum(x[j][i] for j in range(2 * self.n + 1)) == 1)

        # No cycle constraint
        for subset in generate_real_subset(2 * self.n):
            solver.Add(sum(x[i][j] for i in subset for j in subset) <= len(subset) - 1)

        # Start at point 0
        solver.Add(y[0] == 0)

        # If we go from i to j then y[j] = y[i] + 1, except for j = 0, then y[j] + 2 * n  = y[i]
        for i in range(2 * self.n + 1):
            for j in range(2 * self.n + 1):
                if j == 0:
                    solver.Add(y[i] <= y[j] + 2 * self.n + M * (1 - x[i][j]))
                    solver.Add(y[j] + 2 * self.n <= y[i] + M * (1 - x[i][j]))
                else:
                    solver.Add(y[i] + 1 <= y[j] + M * (1 - x[i][j]))
                    solver.Add(y[j] <= y[i] + 1 + M * (1 - x[i][j]))

        # Visit point i before point i + n
        for i in range(1, self.n + 1):
            solver.Add(y[i] + 1 <= y[i + self.n])

        # Initially there are no passengers
        solver.Add(z[0] == 0)

        # If we go from i to j then z[j] = z[i] + 1 if 0 < j <= n, else z[j] = z[i] - 1
        for i in range(2 * self.n + 1):
            for j in range(1, self.n + 1):
                solver.Add(z[i] + 1 <= z[j] + M * (1 - x[i][j]))
                solver.Add(z[j] <= z[i] + 1 + M * (1 - x[i][j]))
            for j in range(self.n + 1, 2 * self.n + 1):
                solver.Add(z[i] - 1 <= z[j] + M * (1 - x[i][j]))
                solver.Add(z[j] <= z[i] - 1 + M * (1 - x[i][j]))

        # Maximum capacity constraint
        for i in range(1, 2 * self.n + 1):
            solver.Add(z[i] <= self.k)

        solver.Minimize(sum(self.costs[i][j] * x[i][j] for i in range(2 * self.n + 1) for j in range(2 * self.n + 1)))
        status = solver.Solve()
        if status == pywraplp.Solver.OPTIMAL:
            return int(solver.Objective().Value())
        else:
            raise Exception('No solution found')
