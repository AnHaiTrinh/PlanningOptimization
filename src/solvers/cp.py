from ortools.sat.python import cp_model
from .solver import Solver


class CpSolver(Solver):
    def solve(self) -> int:
        M = 2 * self.n + 1
        model = cp_model.CpModel()

        x = [[model.NewIntVar(0, 1, f'x({i}, {j})') for j in range(2 * self.n + 1)] for i in range(2 * self.n + 1)]
        y = [model.NewIntVar(0, 2 * self.n, f'y({i})') for i in range(2 * self.n + 1)]
        z = [model.NewIntVar(0, self.k, f'z({i})') for i in range(2 * self.n + 1)]

        # Each point is visited once
        for i in range(2 * self.n + 1):
            model.Add(sum(x[i][j] for j in range(2 * self.n + 1)) == 1)
            model.Add(sum(x[j][i] for j in range(2 * self.n + 1)) == 1)

        # Start at point 0
        model.Add(y[0] == 0)

        # If we go from i to j then y[j] = y[i] + 1, except for j = 0, then y[j] + 2 * n  = y[i]
        for i in range(2 * self.n + 1):
            for j in range(2 * self.n + 1):
                if j == 0:
                    model.Add(y[i] - 2 * self.n <= y[j] + M * (1 - x[i][j]))
                    model.Add(y[j] <= y[i] - 2 * self.n + M * (1 - x[i][j]))
                else:
                    model.Add(y[i] + 1 <= y[j] + M * (1 - x[i][j]))
                    model.Add(y[j] <= y[i] + 1 + M * (1 - x[i][j]))

        # Visit point i before point i + n
        for i in range(1, self.n + 1):
            model.Add(y[i] + 1 <= y[i + self.n])

        # Initially there are no passengers
        model.Add(z[0] == 0)

        # If we go from i to j then z[j] = z[i] + 1 if 0 < j <= n, else z[j] = z[i] - 1
        for i in range(2 * self.n + 1):
            for j in range(1, self.n + 1):
                model.Add(z[i] + 1 <= z[j] + M * (1 - x[i][j]))
                model.Add(z[j] <= z[i] + 1 + M * (1 - x[i][j]))
            for j in range(self.n + 1, 2 * self.n + 1):
                model.Add(z[i] - 1 <= z[j] + M * (1 - x[i][j]))
                model.Add(z[j] <= z[i] - 1 + M * (1 - x[i][j]))

        model.Minimize(sum(self.costs[i][j] * x[i][j] for i in range(2 * self.n + 1) for j in range(2 * self.n + 1)))
        solver = cp_model.CpSolver()
        status = solver.Solve(model)
        if status == cp_model.OPTIMAL:
            return int(solver.ObjectiveValue())
        else:
            raise Exception('No solution found')
