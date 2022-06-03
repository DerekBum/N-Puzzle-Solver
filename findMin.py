from z3 import *

filePath = sys.argv[1]

fileInput = open(filePath)

fieldSize = int(fileInput.readline())

field = [[] for i in range(fieldSize)]

for i in range(fieldSize):
    field[i] = list(map(int, fileInput.readline().split()))

fileInput.close()

fileOutput = open(filePath, 'a')
fileOutput.write("1\n")
fileOutput.close()

left = 1
right = 1

while True:
    try:
        with open(filePath, 'r') as fr:
            lines = fr.readlines()
            ptr = 1
            with open(filePath, 'w') as fw:
                for line in lines:
                    if ptr != fieldSize + 2:
                        fw.write(line)
                    else:
                        fw.write(str(right) + '\n')
                    ptr += 1
        exec(open("./checker.py").read())
    except Z3Exception:
        right += 6
    else:
        break

while left != right - 1:
    mid = (left + right) // 2
    try:
        with open(filePath, 'r') as fr:
            lines = fr.readlines()
            ptr = 1
            with open(filePath, 'w') as fw:
                for line in lines:
                    if ptr != fieldSize + 2:
                        fw.write(line)
                    else:
                        fw.write(str(mid) + '\n')
                    ptr += 1
        exec(open("./checker.py").read())
    except Z3Exception:
        left = mid
    else:
        right = mid

with open(filePath, 'r') as fr:
    lines = fr.readlines()
    ptr = 1
    with open(filePath, 'w') as fw:
        for line in lines:
            if ptr != fieldSize + 2:
                fw.write(line)
            else:
                fw.write(str(right) + '\n')
            ptr += 1
exec(open("./checker.py").read())

print(right)

with open(filePath, 'r') as fr:
    lines = fr.readlines()
    ptr = 1
    with open(filePath, 'w') as fw:
        for line in lines:
            if ptr != fieldSize + 2:
                fw.write(line)
            ptr += 1
