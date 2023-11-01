def generate_real_subset(number):
    for i in range(1, (1 << number) - 1):
        yield [j for j in range(number) if i & (1 << j)]


def generate_non_empty_subset(number_list):
    n = len(number_list)
    for i in range(1, (1 << n)):
        yield [number_list[j] for j in range(n) if i & (1 << j)]
