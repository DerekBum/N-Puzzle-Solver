from z3 import *

filePath = sys.argv[1]

fileInput = open(filePath)
fileOutput = open("output.txt", 'w+')

fieldSize = int(fileInput.readline())

field = [[] for i in range(fieldSize)]

for i in range(fieldSize):
    field[i] = list(map(int, fileInput.readline().split()))

maxMoves = int(fileInput.readline()) + 1

moves = Int('moves')
fieldState = Array('T_X_Y', IntSort(), ArraySort(IntSort(), ArraySort(IntSort(), IntSort())))
emptyX = Array('Empty Row', IntSort(), IntSort())  # Position of the empty tile on i-th step on x-axis
emptyY = Array('Empty Col', IntSort(), IntSort())  # Position of the empty tile on i-th step on y-axis
emptyMovX = Array('Move Row', IntSort(), IntSort()) # Movement of the empty tile between i-th and (i+1)-th steps on x-axis
emptyMovY = Array('Move Col', IntSort(), IntSort()) # Movement of the empty tile between i-th and (i+1)-th steps on y-axis

s = Solver()

''' Initial state '''

s.add(And(moves >= 0, moves < maxMoves))

for step in range(maxMoves):  # Empty tile can't go outside the field
    s.add(And(emptyX[step] >= 0, emptyX[step] < fieldSize))
    s.add(And(emptyY[step] >= 0, emptyY[step] < fieldSize))

for i in range(fieldSize):  # Initial state of the field (aka step = 0)
    for j in range(fieldSize):
        s.add(fieldState[0][i][j] == field[i][j])
        if field[i][j] == 0:
            s.add(emptyX[0] == i)
            s.add(emptyY[0] == j)

''' Step correctness '''

for step in range(maxMoves):  # Position of the empty tile on i-th step correctness
    for i in range(fieldSize):
        for j in range(fieldSize):
            s.add((fieldState[step][i][j] == 0) == And(emptyX[step] == i, emptyY[step] == j))

for step in range(maxMoves):  # No duplicates on field at any moment
    for i in range(fieldSize):
        for j in range(fieldSize):
            for i2 in range(fieldSize):
                for j2 in range(fieldSize):
                    s.add(Implies(
                        fieldState[step][i][j] == fieldState[step][i2][j2],
                        And(i == i2, j == j2)
                    ))

for step in range(maxMoves):  # Bounds for numbers on tiles
    for i in range(fieldSize):
        for j in range(fieldSize):
            s.add(And(fieldState[step][i][j] >= 0, fieldState[step][i][j] < fieldSize * fieldSize))

''' Transitions '''

for step in range(maxMoves):  # Movement of the empty tile between i-th and (i+1)-th steps correctness
    s.add(And(emptyMovX[step] >= -1, emptyMovX[step] <= 1))
    s.add(And(emptyMovY[step] >= -1, emptyMovY[step] <= 1))
    s.add(
        Or(
            And(emptyMovX[step] == 0, emptyMovY[step] != 0),
            And(emptyMovX[step] != 0, emptyMovY[step] == 0),
            And(emptyMovX[step] == 0, emptyMovY[step] == 0)
        ))

for step in range(maxMoves - 1):  # We can hold the tile, it's position then do not change
    s.add(Implies(
        And(
            emptyMovX[step] == 0,
            emptyMovY[step] == 0
        ),
        And(
            emptyX[step] == emptyX[step + 1],
            emptyY[step] == emptyY[step + 1]
        )
    ))

for step in range(maxMoves - 1):  # If we move the tile, we can find its next position
    for moveX in {-1, 0, 1}:
        for moveY in {-1, 0, 1}:
            s.add(Implies(
                And(
                    Xor(moveX == 0, moveY == 0),
                    emptyMovX[step] == moveX,
                    emptyMovY[step] == moveY
                ),
                And(
                    emptyX[step] + moveX >= 0,
                    emptyX[step] + moveX < fieldSize,
                    emptyY[step] + moveY >= 0,
                    emptyY[step] + moveY < fieldSize,
                    emptyX[step] + moveX == emptyX[step + 1],
                    emptyY[step] + moveY == emptyY[step + 1]
                )
            ))

for step in range(maxMoves - 1):  # For any tiles (except swapped ones), their numbers didn't change
    for i in range(fieldSize):
        for j in range(fieldSize):
            s.add(Implies(
                Not(
                    Or(
                        And(
                            emptyX[step] == i,
                            emptyY[step] == j
                        ),
                        And(
                            emptyX[step + 1] == i,
                            emptyY[step + 1] == j
                        )
                    )
                ),
                fieldState[step][i][j] == fieldState[step + 1][i][j]
            ))

''' End status '''

for i in range(fieldSize):  # We can get final state somewhere
    for j in range(fieldSize):
        if (i == fieldSize - 1) and (j == fieldSize - 1):
            s.add(fieldState[moves][i][j] == 0)
        else:
            s.add(fieldState[moves][i][j] == i * fieldSize + j + 1)

''' Printing answer '''

s.check()

m = s.model()

ll = [m.evaluate(emptyMovX[x]) for x in range(maxMoves)]
rr = [m.evaluate(emptyMovY[x]) for x in range(maxMoves)]

for step in range(maxMoves - 1):
    if (ll[step] == -1) and (rr[step] == 0):
        fileOutput.write("up\n")
    elif (ll[step] == 1) and (rr[step] == 0):
        fileOutput.write("down\n")
    elif (ll[step] == 0) and (rr[step] == -1):
        fileOutput.write("left\n")
    elif (ll[step] == 0) and (rr[step] == 1):
        fileOutput.write("right\n")
    elif ((ll[step] == 1)    and (rr[step] == -1)) or (
            (ll[step] == -1) and (rr[step] == -1)) or (
            (ll[step] == 1)  and (rr[step] == 1))  or (
            (ll[step] == -1) and (rr[step] == 1)):
        fileOutput.write("Congratulations, there is a problem with my solver!\n")
    else:
        fileOutput.write("hold\n")
