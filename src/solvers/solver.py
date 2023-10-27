from abc import ABC, abstractmethod


class Solver(ABC):
    def __init__(self, n, k, costs, optimal):
        self.n = n
        self.k = k
        self.costs = costs
        self.optimal = optimal

    @abstractmethod
    def solve(self) -> int:
        pass

    def evaluate(self) -> None:
        result = self.solve()
        if not self.optimal:
            print('Optimal solution is not given')
            print(f'Calculated optimal: {result}')

        else:
            print(f'Found results: {result}')
            print(f'Optimal results: {self.optimal}')
            if result == self.optimal:
                print('Verdict: Optimal')
            elif result < self.optimal:
                print('Verdict: More optimal')
            else:
                print('Verdict: Suboptimal')