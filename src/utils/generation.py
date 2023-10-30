def generate_real_subset(number):
    for i in range(1, (1 << number) - 1):
        yield [j for j in range(number) if i & (1 << j)]
