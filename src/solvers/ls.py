from .solver import Solver
import numpy as np
import random

MAX_INT = 1e9
def Greedy1(n,k,costs):
        # Init paths and visited array
        paths = [0] * (2 * n + 2)
        visited = [0] * (2 * n + 1) 
        passengers = 0
        for i in range(1, 2*n + 1):
            paths[i] = 0
            visited[i] = 0
            visited[0] = 1

        # Check if node can visit
        def check_can_visit(i):
            nonlocal passengers
            if visited[i] == 1:
                return False
            if passengers == k:
                if i <= n:
                    return False
                else:
                    if visited[i - n] == 0:
                        return False
                    else:
                        return True
            else:
                if i > n:
                    if visited[i - n] == 0:
                        return False
                    else:
                        return True
            return True
        
        # Visit node, update passengers and visited array
        def visit(order_node, value_position):
            nonlocal passengers
            paths[order_node] = value_position
            visited[value_position] = 1
            if value_position > n:
                passengers -= 1
            else:
                passengers += 1
        # Greedy algorithm
        def Greedy(i):
            min_length = MAX_INT
            if i <= 2 * n:
                node = 1
                prevNode = paths[i-1]
                for j in range(1, 2*n + 1):
                    cost = costs[prevNode][j]
                    if (check_can_visit(j) and cost < min_length):
                        min_length = cost
                        node = j
                visit(i, node)
                # cost_paths = cost_paths + max_length    
                Greedy(i + 1)
            # else:
                # cost_paths += costs[2*n][0]
                # print(paths)
                # print(cost_paths)
        Greedy(1)
        return paths

def Greedy2(n,k,costs):
    def weight_j(r, i):
        ln = -np.log(r+1e-5)
        if ln < 1e-4:
            return 0
        return np.power(ln, 1 + 50*np.sqrt(i/n))

    def valid(sol, city, visited):
        #check if node is visited
        if visited[city] == 1:
            return False

        next_sol = sol.copy()
        next_sol.append(city)

        mark = [0]*(n+1)
        n_passengers = 0
        for _city in next_sol[1:]:
            if _city <= n:
                n_passengers += 1
                mark[_city] = 1
            else:
                n_passengers -= 1
                mark[_city-n] = 0
            if n_passengers > k:
                return False

        if np.sum(mark)-n_passengers != 0:
            return False
        return True

    def solve():
        solution = []
        solution.append(0) # start at city 0
        fitness = 0 # objective value
        visited = [0]*(2*n+1)
        visited[0] = 1
        for _ in range(1, 2*n + 1):

            #current city
            c_city = solution[-1]

            weights = [] # probability distribution
            possible_move = []
            d_max = 0

            for city in range(1, 2*n+1):
                if valid(solution, city, visited) == False:
                    continue
                d_i = costs[c_city][city]
                possible_move.append([city, d_i]) #[city, distance]
                # if d_i > d_max:
                #     d_max = d_i

            possible_move = sorted(possible_move, key=lambda x: x[1])

            if len(possible_move) > 20:
                possible_move = possible_move[:20]

            for city in possible_move:
                if d_max < city[1]: d_max=city[1]

            # print(solution)
            # print(possible_move)
            # print(weights)

            if d_max == 0:
                next_city = possible_move[0]
            else:
                # cal weights
                for move in possible_move:
                    r = move[1]/d_max
                    weights.append(weight_j(r, _))

                if np.sum(weights) == 0:
                    next_city = possible_move[0]
                else:
                    # choices next city
                    next_city = random.choices(possible_move, k=1, weights=weights)[0]

            #update solution
            solution.append(next_city[0])

            #mark visited
            visited[next_city[0]] = 1

            fitness += next_city[1]

        return solution, fitness

    def solver():
        record = 10e9
        best_sol = None
        for seed in range(10):
            random.seed(seed)
            sol, fit = solve()
            # print(fit + costs[sol[-1]][0])
            if record > fit:
                record = fit
                best_sol = sol.copy()
        return best_sol, record
    
    best_sol, best_fitness = solver()

    # print("Objective value: ", best_fitness + costs[best_sol[-1]][0])
    # print("Solution: ", best_sol)
    return best_sol

class LSSolver(Solver):
    def solve(self) -> int:
        k = self.k
        n = self.n
        costs = self.costs

        # Greedy algorithm
        paths = Greedy2(n, k, costs)

        sum = 0
        for i in range(1, 2*n + 1):
            sum += costs[paths[i-1]][paths[i]]
        sum += costs[paths[2*n]][0]

        # Init current cost and current paths
        self.current_cost_path = sum
        current_paths = paths.copy()

        # def find_max_node_in_path(arr):
        #     max_node = 1
        #     max_two_edges = costs[arr[max_node - 1]][arr[max_node]] + costs[arr[max_node]][arr[max_node + 1]]
        #     for i in range(2, 2*n + 1):
        #         two_edges = costs[arr[i - 1]][arr[i]] + costs[arr[i]][arr[i + 1]]
        #         if two_edges > max_two_edges:
        #             max_two_edges = two_edges
        #             max_node = i
        #     return max_node
        
        # Check the condition passengers when swap 2 node in path
        def check_condition(newArr):
            visitedNode = [0] * (2 * n + 1)
            passengers_in_condition = 0

            for t in range(1, 2*n + 1):
                if newArr[t] <= n:
                    if passengers_in_condition < k:
                        passengers_in_condition += 1
                        visitedNode[newArr[t]] = 1
                    else:
                        return False
                else:
                    if passengers_in_condition > 0 and visitedNode[newArr[t] - n] == 1:
                        passengers_in_condition -= 1
                        visitedNode[newArr[t]] = 1
                    else:
                        return False
            return True
        # Check the condition when swap 2 node in path
        def can_swap(i, j):
            if i == j:
                return False
            if i == 0 or j == 0:
                return False
            if check_condition(
                new_arr_when_swap(i, j, current_paths)
            ) == False:
                return False
            return True

        def new_arr_when_swap(i, j, oldArr):
            newArr = oldArr.copy()
            newArr[i], newArr[j] = newArr[j], newArr[i]
            return newArr

        # Calculate cost when swap 2 node in path
        def calculate_cost(arr):
            sum = 0
            for i in range(1, 2*n + 1):
                sum += costs[arr[i-1]][arr[i]]
            sum += costs[arr[2*n]][0]
            return sum

        # Swap 2 node in path
        def swap(i, j, arr):
            arr[i], arr[j] = arr[j], arr[i]

        # Local search
        def local_search(loop = 100):
            for _ in range(loop):
                # print("Loop ", _ )
                random_node = random.randint(1, 2*n)
                # random_node = find_max_node_in_path(current_paths)
                nodes_can_swap = []
                max_costs = self.current_cost_path
                for j in range(1, 2*n + 1):
                    if can_swap(random_node, j):
                        new_arr = new_arr_when_swap(random_node, j, current_paths)
                        cost_when_swap = calculate_cost(new_arr)
                        if cost_when_swap < max_costs:
                            max_costs = cost_when_swap
                            nodes_can_swap = [j]
                        elif cost_when_swap == max_costs:
                            nodes_can_swap.append(j)
                if len(nodes_can_swap) >= 1: 
                    node_swap = random.choice(nodes_can_swap)
                    swap(random_node, node_swap, current_paths)
                    self.current_cost_path = max_costs
            # print(current_cost_path)
        local_search(100)
        print('Greedy: ', sum)
        return self.current_cost_path
    
