import numpy as np
from .BranchAndBound import BranchAndBoundSolver


class SolverFactory:
    def __init__(self, input_file, output_file):
        try:
            n, k, costs = self._read_input(input_file)
            self.n = n
            self.k = k
            self.costs = costs
        except Exception as e:
            print(f'Error reading input file {input_file}')
            print(e)

        self.optimal = self._read_output(output_file)

    def create_solver(self, solver_name):
        if solver_name == 'bnb':
            return BranchAndBoundSolver(self.n, self.k, self.costs, self.optimal)
        else:
            raise NotImplementedError(f'Solver {solver_name} is not implemented')

    def _read_input(self, input_file):
        if input_file:
            try:
                with open(input_file, 'r') as f:
                    n, k = map(int, f.readline().split())
                    costs = np.array([list(map(int, f.readline().split())) for _ in range(2 * n + 1)])
            except Exception as e:
                raise e
        else:
            try:
                n, k = map(int, input().split())
                costs = np.array([list(map(int, input().split())) for _ in range(2 * n + 1)])
            except Exception as e:
                raise e

        return n, k, costs

    def _read_output(self, output_file):
        optimal = None
        if output_file:
            try:
                with open(output_file, 'r') as f:
                    optimal = int(f.readline())
            except Exception as e:
                print(e)

        return optimal
