import copy
import random

def noZerosInBoard(board):
    for row in board:
        if 0 in row:
            return False
    return True

def getLegals(board):
    legalList = makeLegalsListForSolution()
    for row in range(len(board)):
        for col in range(len(board[0])):
            value = board[row][col]
            if value!=0:
                legalList = setLegal(board, row, col, value, legalList)
    return legalList
    

def returnFastestLegal(legalList):
    rows, cols = len(legalList), len(legalList[0])
    
    minLegalPos=None
    smallestLegal=10
    for row in range(rows):
        for col in range(cols):
            legalSet=legalList[row][col]
            if len(legalSet)<smallestLegal and len(legalSet)!=0:
                smallestLegal=len(legalSet)
                minLegalPosition=(row, col)
    if smallestLegal==10:
        return None
    return minLegalPosition
def setLegal(board, row, col, value, legalList):
    for n in range(1, 10):
        legalList[row][col].discard(n)
    for colm in range(9):
        legalList = legalBan(row, colm, {value}, legalList)
    for banRow in range(9):
        legalList = legalBan(banRow, col, {value}, legalList)
    curBlock= col//3 + (row//3)*3
    for blockRow in range((curBlock//3)*3, (curBlock//3)*3+3):
        for blockCol in range((curBlock%3)*3, (curBlock%3)*3+3):
            legalList = legalBan(row, col, {value}, legalList)
    return legalList
        
def legalBan(row, col, values, legalList):
    for value in values:
        legalList[row][col].discard(value)
    return legalList
    
def solveRandomSudoku(board):
    solutions=[]
    return solveRandomSudokuHelper(copy.deepcopy(board), solutions)

def solveRandomSudokuHelper(board, solutions):
    legals=getLegals(board)
    smallestLegalPosition =returnFastestLegal(legals)
    if noZerosInBoard(board)==True:
        if board not in solutions:
            solutions.append(board)
        if len(solutions)>1:
            return False
        elif len(solutions)==1:
            return solutions
    else:
        if smallestLegalPosition==None:
            return None
        (row, col) = smallestLegalPosition
        newBoard = copy.deepcopy(board)
        legalSet = legals[row][col]
        for num in legalSet:
            legalSet.discard(num)
            newBoard[row][col]=num
            if isLegalSudoku(newBoard):
                solution =solveRandomSudokuHelper(newBoard, solutions)
                if solution!=None:
                    return solution
            newBoard[row][col]=0
            #legals=getLegals(board)
        return None

                
def makeLegalsListForSolution():
    M=[set(), set(), set(), set(), set(), set(), set(), set(), set()]
    for s in M:
        for n in range(1, 10):
            s.add(n)
    L=[]
    for _ in range(1, 10):
        L=L+copy.deepcopy([copy.deepcopy(M)])
    return L
def areLegalValues(L):
    seen = set()
    n=len(L)
    
    for v in L:
        if not isinstance(v, int):
            return False
        if v<0 or v>n:
            return False
        if v!=0 and v in seen:
            return False
        seen.add(v)
    return True

def isLegalRow(grid, row):
    return areLegalValues(grid[row])
def isLegalCol(grid, col):
    rows = len(grid)
    values = [grid[row][col] for row in range(rows)]
    return areLegalValues(values)
    
def isLegalBlock(grid, block):
    n=len(grid)
    blockSize=round(n**0.5)
    startRow=block//blockSize * blockSize
    startCol=block%blockSize * blockSize
    values=[]
    for drow in range(blockSize):
        for dcol in range(blockSize):
            row, col = startRow  + drow, startCol + dcol
            values.append(grid[row][col])
    return areLegalValues(values)

def isLegalSudoku(grid):
    rows, cols = len(grid), len(grid[0])
    if rows!=4 and rows!=9:
        return False
    if rows!=cols:
        return False
    for row in range(rows):
        if not isLegalRow(grid, row):
            return False
    for col in range(cols):
        if not isLegalCol(grid, col):
            return False
    blocks = rows
    for block in range(blocks):
        if not isLegalBlock(grid, block):
            return False
    return True           
