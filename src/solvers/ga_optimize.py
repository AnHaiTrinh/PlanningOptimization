import random
import numpy as np
import time
from .solver import Solver


class GASolver(Solver):
    def __init__(self, n, k, cost, optimal):
        super().__init__(n, k, cost, optimal)
        self.min_distance = 10000

    def totalDistance(self, inv):
        summ = np.sum([self.costs[int(inv[i])][int(inv[i + 1])] for i in range(2 * self.n - 1)])
        # print("summ:", summ)
        return summ + self.costs[0][int(inv[0])] + self.costs[int(inv[-1])][0]

    def nOfBlindingConstrains(self, inv):
        count = 0
        mark = [0] * (self.n + 1)
        n_passengers = 0
        for i in range(2 * self.n):
            if inv[i] <= self.n:
                n_passengers += 1
                mark[inv[i]] = 1
            else:
                n_passengers -= 1
                mark[inv[i] - self.n] = 0
            if n_passengers > self.k:
                count += 1

        return count + np.sum(mark)

    def fitness(self, inv):  # O(N)
        pen = self.totalDistance(np.arange(1, len(inv) + 1))
        distance = self.totalDistance(inv)
        return 5 * pen * self.nOfBlindingConstrains(inv) / np.sqrt(distance) + distance

    # khởi tạo quần thể ban đầu
    def initPopulation(self, cities, size):
        population = []

        for i in range(size):
            invi = list(cities)
            random.shuffle(invi)
            distance = self.fitness(invi)
            population.append([distance, invi, 0])

        return population

    # Toán tử lai 1 điểm cắt
    #   father1: 2,3,5|1,4    father2: 1,3,5|4,2     điểm cắt: 3
    # new_invi1: 1,3,5,2,4  new_invi2: 2,3,5,1,4
    def singlePointCrossover(self, father1, father2):
        point = random.randint(0, len(father1) - 1)

        new_invi1 = father2[0:point]
        for invi in father1:
            if invi not in new_invi1:
                new_invi1.append(invi)

        new_invi2 = father1[0:point]
        for invi in father2:
            if invi not in new_invi2:
                new_invi2.append(invi)

        return new_invi1, new_invi2

    # Toán tử lai 2 điểm cắt
    #   father1: 6,2|4,3|1,5    father2: 6,1|3,5|4,2     điểm cắt: 2,4
    # new_invi1: 6,2,3,5,4,1  new_invi2: 6,1,4,3,5,2
    def multiPointCrossover(self, father1, father2):  # O(N^2)
        points = sorted(random.sample(father1, 2))
        point1 = int(points[0]) - 1
        point2 = int(points[1]) - 1

        new_invi1 = father2[point1:point2]
        c1 = 0
        for invi in father1:
            if invi not in new_invi1:
                c1 += 1
                if c1 <= point1:
                    new_invi1.insert(c1 - 1, invi)
                else:
                    new_invi1.append(invi)
        new_invi2 = father1[point1:point2]
        c1 = 0
        for invi in father2:
            if invi not in new_invi2:
                c1 += 1
                if c1 <= point1:
                    new_invi2.insert(c1 - 1, invi)
                else:
                    new_invi2.append(invi)

        return new_invi1, new_invi2

    def multiPointCrossover1(self, father1, father2):
        points = sorted(random.sample(father1, 2))
        point1 = int(points[0]) - 1
        point2 = int(points[1]) - 1

        new_invi1 = father2[point1:point2]
        c1 = 0
        c2 = 0
        for invi in father1:
            if invi not in new_invi1:
                c1 += 1
                if c1 <= point1:
                    new_invi1.append(invi)
                else:
                    new_invi1.insert(c2, invi)
                    c2 += 1
        new_invi2 = father1[point1:point2]
        c1 = 0
        c2 = 0
        for invi in father2:
            if invi not in new_invi2:
                c1 += 1
                if c1 <= point1:
                    new_invi2.append(invi)
                else:
                    new_invi2.insert(c2, invi)
                    c2 += 1

        return new_invi1, new_invi2

    def nDiffCities(self, inv1, inv2):  # O(N)
        return np.sum(np.array(inv1) != np.array(inv2))

    def chooseFather(self, population):  # O(p*N)
        father1 = random.choice(population)[1]
        tabu = []
        max_diff = 0
        for invi in population:
            diff = self.nDiffCities(father1, invi[1])
            tabu.append([diff, invi[1]])
            if diff > max_diff:
                max_diff = diff
        threshold = max_diff / 2
        nonTabuList = []
        for tabu_i in tabu:
            if tabu_i[0] < threshold:
                continue
            nonTabuList.append(tabu_i[1])
        if len(nonTabuList) == 0:
            return None, None
        return father1, random.choice(nonTabuList)

    # đột biến: chọn ngẫu nhiên 2 thành phố rồi đổi chỗ cho nhau, thực hiện 2 lần
    # 2,1,5,3,4 => 4,1,5,3,2 => 1,4,5,3,2
    def mutation(self, father):  # O(N)
        new_invi = father.copy()
        for _ in range(5):
            points = random.sample(new_invi, 2)
            temp = new_invi[int(points[0]) - 1]
            new_invi[int(points[0]) - 1] = new_invi[int(points[1]) - 1]
            new_invi[int(points[1]) - 1] = temp

        return new_invi

    def tournaments(self, old_population, new_invivduals, pop_size=100):  # O(plogp)
        merge = sorted(old_population + new_invivduals, key=lambda x: (x[0], -x[2]))
        best_fitness = merge[0][0]
        new_population = merge[:10]
        selected = []
        for inv in merge[10:]:
            if inv[0] / best_fitness > 0.75 or inv[2] < 50:
                selected.append(inv)

        new_population = new_population + random.choices(selected, k=pop_size - 10)

        for inv in new_population:
            inv[2] += 1

        return new_population

    def GA(self,
           population,
           pop_size=100,
           num_of_generations=200,
           crossover_rate=0.99,
           mutation_rate=0.2,
           crossover_func=multiPointCrossover1
           ):
        for _ in range(num_of_generations):
            new_inviduals = []
            # sinh pop_size cá thể mới
            n_i = int(pop_size / 2)
            for _i in range(n_i):  # O(g*[p/2*(p*N + N^2 + N) + plogp]) = O(g*p(p*N + N^2 + p*logp))

                father1, father2 = self.chooseFather(population)
                if father1 is not None:
                    # xảy ra quá trình lai ghép (crossover)
                    if random.random() <= crossover_rate:
                        # thực hiện lai ghép 2 cá thể này
                        inv1, inv2 = crossover_func(father1, father2)
                        # xảy ra quá trình đột biến (mutation)
                        if random.random() <= mutation_rate:
                            inv1 = self.mutation(inv1)
                            inv2 = self.mutation(inv2)
                    # không có lai ghép xảy ra
                    else:
                        inv1, inv2 = father1, father2
                else:
                    return sorted(population)
                new_inviduals.append([self.fitness(inv1), inv1, 0])
                new_inviduals.append([self.fitness(inv2), inv2, 0])

            population = self.tournaments(population, new_inviduals, pop_size)
            population = sorted(population)
            best_invi = population[0]
            # print("Best invi: ", best_invi)
            # print(population[0])
            if self.totalDistance(best_invi[1]) < self.min_distance and self.nOfBlindingConstrains(best_invi[1]) == 0:
                self.min_distance = self.totalDistance(best_invi[1])
            if best_invi[2] > 20 * (self.n ** 0.5):
                return population

        return population

    def solve(self):
        total_distance = 0
        total_time = 0
        total_bCons = 0
        for n_seed in range(10):
            random.seed(n_seed)
            cities = np.arange(1, 2 * self.n + 1)
            population = self.initPopulation(cities, size=100)  # Khởi tạo quần thể đầu tiên
            t1 = time.time()
            pop = self.GA(population=population, crossover_func=self.multiPointCrossover)
            # print("Min distance: ", self.min_distance)
            total_distance += self.totalDistance(pop[0][1])
            total_time += (time.time() - t1)
            total_bCons += self.nOfBlindingConstrains(pop[0][1])
        print(f"Objective value: {total_distance / 10}")
        # print(f"Solution: {[0] + pop[0][s1]}")
        print(f"Number of blinding constrains: {total_bCons / 10}")
        print(f"Time: {total_time / 10}")
        print("Min distance:", self.min_distance)
        return self.min_distance
