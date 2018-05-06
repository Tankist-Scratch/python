import random as r
name = "A"

def go(matrix):
    while True:
        x = r.randint(0, 19)
        y = r.randint(0, 19)
        if matrix[y][x] == 0:
            return [x, y]


if __name__ == '__main__':
    print(*go([list(map(int, input().split())) for i in range(20)]), end="", sep=" ")
