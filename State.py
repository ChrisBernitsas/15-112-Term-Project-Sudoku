from cmu_graphics import *
import copy 
import itertools

class State():
    def __init__(self, board, legals):
        self.board= board
        self.legals =legals
    def set(self, row, col, value):
        self.board[row][col]=value
        State.ban(self, row, col, {1, 2, 3, 4, 5, 6, 7, 8, 9})
        for colm in range(9):
            if colm!=col:
                State.ban(self, row, colm, {value})
        for banRow in range(9):
            if banRow!=row:
                State.ban(self, banRow, col, {value})
        curBlock = col//3 + (row//3)*3
        for blockRow in range((curBlock//3)*3, (curBlock//3)*3+ 3):
            for blockCol in range((curBlock%3)*3, (curBlock%3)*3+3):
                if blockRow!=row and blockCol!=col:
                    State.ban(self, blockRow, blockCol, {value})
    def ban(self, row, col, values):
        for value in values:
            self.legals[row][col].discard(value)
    def remove(self, row, col):
        self.board[row][col]=0
        legalsRows, legalsCols = len(self.legals), len(self.legals[0])
        self.legals =makeLegalsList()
        rows, cols = len(self.board), len(self.board[0])
        for row in range(rows):
            for col in range(cols):
                val = self.board[row][col]
                if val!=0:
                    State.set(self, row, col, val)
    def unban(self, row, col, values):
        for value in values:
            self.legals[row][col].add(value)
    def getLegalList(self):
        return self.legals
    def getBoard(self):
        return self.board

    def getAllLegalRegions(self):
        allRegions =[]
        for row in range(9):
            allRegions.append(State.getLegalRowRegion(self, row))
        for col in range(9):
            allRegions.append(State.getLegalColRegion(self, col))
        for row in range(3):
            row=row*3
            for col in range(3):
                col=col*3
                allRegions.append(State.getLegalBlockRegion(self, row, col))
        return allRegions
    def getLegalRowRegion(self, row):
        return self.legals[row]
    def getLegalColRegion(self, col):
        colRegion = []
        for row in range(9):
            colRegion.append(self.legals[row][col])
        return colRegion
    def getLegalBlockRegion(self, row, col):
        blockRegion = []
        curBlock = col//3 + (row//3)*3
        for blockRow in range((curBlock//3)*3, (curBlock//3)*3+ 3):
            for blockCol in range((curBlock%3)*3, (curBlock%3)*3+3):
                blockRegion.append(self.legals[blockRow][blockCol])
        return blockRegion
    def getBansForAllRegions(self, values, targets):
        pass
        # The values (to ban) can stay in the targets, but they must be
        # banned from all other cells in all regions that contain all
        # the targets
        bans = [ ]
        for region in self.getAllRegionsThatContainTargets(targets):
            pass
def makeLegalsList():
    M=[set(), set(), set(),set(),set(),set(),set(),set(),set()]
    for s in M:
        for n in range(1, 10):
            s.add(n)
    L=[]
    for _ in range(1, 10):
        L=L+copy.deepcopy([copy.deepcopy(M)])
    return L