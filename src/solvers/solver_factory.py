import numpy as np
from .branch_and_bound import BranchAndBoundSolver
from .solver import Solver


class SolverFactory:
    def __init__(self, n, k, costs, optimal):
        self.n = n
        self.k = k
        self.costs = costs
        self.optimal = optimal

    def create_solver(self, solver_name: str) -> Solver:
        if solver_name == 'bnb':
            return BranchAndBoundSolver(self.n, self.k, self.costs, self.optimal)
        else:
            raise NotImplementedError(f'Solver {solver_name} is not implemented')
