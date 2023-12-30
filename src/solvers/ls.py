from .solver import Solver
import numpy as np
import random

class LSSolver(Solver):
    def solve(self) -> int:
        MAX_INT = 1e9
        n = self.n
        k = self.k
        costs = self.costs
        # Init paths and visited array
        paths = [0] * (2 * n + 2)
        visited = [0] * (2 * n + 1) 
        self.passengers = 0
        for i in range(1, 2*n + 1):
            paths[i] = 0
            visited[i] = 0
            visited[0] = 1

        # Check if node can visit
        def check_can_visit(i):
            if visited[i] == 1:
                return False
            if self.passengers == k:
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
            paths[order_node] = value_position
            visited[value_position] = 1
            if value_position > n:
                self.passengers -= 1
            else:
                self.passengers += 1
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
        local_search(15000)
        return self.current_cost_path