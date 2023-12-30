import numpy as np
from .branch_and_bound import BranchAndBoundSolver
from .ip import IpSolver
from .cp import CpSolver
from .solver import Solver
from .ls import LSSolver


class SolverFactory:
    def __init__(self, n, k, costs, optimal):
        self.n = n
        self.k = k
        self.costs = costs
        self.optimal = optimal

    def create_solver(self, solver_name: str) -> Solver:
        if solver_name == 'bnb':
            return BranchAndBoundSolver(self.n, self.k, self.costs, self.optimal)
        elif solver_name == 'ip':
            return IpSolver(self.n, self.k, self.costs, self.optimal)
        elif solver_name == 'cp':
            return CpSolver(self.n, self.k, self.costs, self.optimal)
        elif solver_name == 'ls':
            return LSSolver(self.n, self.k, self.costs, self.optimal)
        else:
            raise NotImplementedError(f'Solver {solver_name} is not implemented')
