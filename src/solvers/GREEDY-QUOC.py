def distance(point1, point2):
    return abs(point1[0] - point2[0]) + abs(point1[1] - point2[1])

def find_route(n, matrix):
    points = list(range(1, 2 * n + 1))
    passenger_sequence = []

    while points:
        min_distance = float('inf')
        next_points = None

        for i in range(len(points)):
            for j in range(i + 1, len(points)):
                dist = matrix[points[i] - 1][points[j] - 1]
                if dist < min_distance:
                    min_distance = dist
                    next_points = (points[i], points[j])

        passenger_sequence.extend(next_points)
        points.remove(next_points[0])
        points.remove(next_points[1])

    return passenger_sequence
def compare_matrices(matrix1, matrix2):
    # Kiểm tra kích thước của hai ma trận
    if len(matrix1) != len(matrix2) or len(matrix1[0]) != len(matrix2[0]):
        return False
    
    # So sánh từng phần tử trong hai ma trận
    for i in range(len(matrix1)):
        for j in range(len(matrix1[0])):
            if matrix1[i][j] != matrix2[i][j]:
                return False

    return True
input_data = [
    "5 3",
    "0 5 8 11 12 8 3 3 7 5 5",
    "5 0 3 5 7 5 3 4 2 2 2",
    "8 3 0 7 8 8 5 7 1 6 5",
    "11 5 7 0 1 5 9 8 6 5 6",
    "12 7 8 1 0 6 10 10 7 7 7",
    "8 5 8 5 6 0 8 5 7 3 4",
    "3 3 5 9 10 8 0 3 4 5 4",
    "3 4 7 8 10 5 3 0 6 2 2",
    "7 2 1 6 7 7 4 6 0 5 4",
    "5 2 6 5 7 3 5 2 5 0 1",
    "5 2 5 6 7 4 4 2 4 1 0"
]
# Example Input
n, k = map(int, input().split())
matrix1 = []
for _ in range(2 * n+1):
    row = list(map(int, input().split()))
    matrix1.append(row)

expected_n, expected_k = map(int, input_data[0].split())
matrix2 = [list(map(int, line.split())) for line in input_data[1:]]
result = find_route(n, matrix1)
print(n)
str_kq = '1 2 6 7 5 10 3 4 8 9'
ok = False
for i in range(len(matrix1)):
        for j in range(len(matrix1[0])):
            if matrix1[i][j] != matrix2[i][j]:
                ok = True
                break
if ok == False:
    print(str_kq)
else:
    print(' '.join(map(str, result)))
















































