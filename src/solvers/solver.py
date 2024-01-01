from abc import ABC, abstractmethod
import time


class Solver(ABC):
    def __init__(self, n, k, costs, optimal):
        self.n = n
        self.k = k
        self.costs = costs
        self.optimal = optimal

    @abstractmethod
    def solve(self) -> int:
        pass

    def evaluate(self, return_time: bool) -> None:
        start_time = time.time()
        result = self.solve()
        duration = round(time.time() - start_time, 4)
        f = open('logs.txt', 'a')
        f.write(f'\t{self.n} - {self.k} - {result} - time: {duration}\n')
        f.close()
        if return_time:
            print(f'Time taken: {duration} seconds')
            print('----------------------------------')

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

