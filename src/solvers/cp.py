from abc import ABC
from ortools.sat.python import cp_model
from .solver import Solver
from ..utils.generation import generate_real_subset, generate_non_empty_subset


class AbstractCpSolver(Solver, ABC):
    def cp_modelling(self):
        M = 2 * self.n + 1
        model = cp_model.CpModel()

        x = [[model.NewIntVar(0, 1, f'x({i}, {j})') for j in range(2 * self.n + 1)] for i in range(2 * self.n + 1)]
        y = [model.NewIntVar(0, 2 * self.n, f'y({i})') for i in range(2 * self.n + 1)]
        z = [model.NewIntVar(0, self.n, f'z({i})') for i in range(2 * self.n + 1)]

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
                    model.Add(y[i] <= y[j] + 2 * self.n + M * (1 - x[i][j]))
                    model.Add(y[j] + 2 * self.n <= y[i] + M * (1 - x[i][j]))
                else:
                    model.Add(y[i] + 1 <= y[j] + M * (1 - x[i][j]))
                    model.Add(y[j] <= y[i] + 1 + M * (1 - x[i][j]))

        # Visit point i before point i + n
        for i in range(1, self.n + 1):
            model.Add(y[i] < y[i + self.n])

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

        # Maximum capacity constraint
        for i in range(1, 2 * self.n + 1):
            model.Add(z[i] <= self.k)

        model.Minimize(sum(self.costs[i][j] * x[i][j] for i in range(2 * self.n + 1) for j in range(2 * self.n + 1)))
        return x, y, z, model


class CpSolver(AbstractCpSolver):
    def solve(self) -> int:
        x, _, _, model = self.cp_modelling()
        # Add no cycles constraint
        for subset in generate_real_subset(2 * self.n):
            model.Add(sum(x[i][j] for i in subset for j in subset) <= len(subset) - 1)
        solver = cp_model.CpSolver()
        status = solver.Solve(model)
        if status == cp_model.OPTIMAL:
            return int(solver.ObjectiveValue())
        else:
            raise Exception('No solution found')


class DynamicCpSolver(AbstractCpSolver):
    def get_cycles(self, solver, x):
        visited = set()
        cycles = []
        for i in range(2 * self.n + 1):
            if i not in visited:
                current = i
                current_cycle = []
                while current not in current_cycle:
                    current_cycle.append(current)
                    visited.add(current)
                    for j in range(2 * self.n + 1):
                        if solver.Value(x[current][j]) == 1:
                            current = j
                            break
                cycles.append(current_cycle)
        return cycles

    def solve(self) -> int:
        x, _, _, model = self.cp_modelling()
        cp_solver = cp_model.CpSolver()
        current_cycles = []
        # Dynamically add new no cycles constraints
        while True:
            for current_cycle in current_cycles:
                for non_empty_subset in generate_non_empty_subset(current_cycle):
                    model.Add(
                        sum(x[i][j] for i in non_empty_subset for j in non_empty_subset) <= len(non_empty_subset) - 1)
            status = cp_solver.Solve(model)
            if status == cp_model.OPTIMAL:
                current_cycles = self.get_cycles(cp_solver, x)
                if len(current_cycles) == 1:
                    break
            else:
                raise Exception('No solution found')
        return int(cp_solver.ObjectiveValue())
