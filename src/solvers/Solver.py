from abc import ABC, abstractmethod
import numpy as np


class Solver(ABC):
    def __init__(self, n, k, costs, optimal):
        self.n = n
        self.k = k
        self.costs = costs
        self.optimal = optimal

    @abstractmethod
    def solve(self):
        pass

    def evaluate(self):
        if not self.optimal:
            print('Optimal solution is not given')
            return

        status, result = self.solve()
        if status == 'Optimal':
            print(f'Found results: {result}')
            print(f'Optimal results: {self.optimal}')
            if result == self.optimal:
                print('Verdict: Optimal')
            elif result < self.optimal:
                print('Verdict: More optimal')
            else:
                print('Verdict: Suboptimal')

        elif status == 'Unbounded':
            print('Verdict: Unbounded')

        else:
            print('Verdict: Infeasible')