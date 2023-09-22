from cmu_graphics import *

from State import *
from randomSolution import *
from solution import *
from wordList import *
# from gameLostScreen import *
# from gameWonScreen import *
from helpScreen import *
from variationRulesScreen import *

import os
import random
import math
import copy
import itertools
import time
def reset(app):
    app.contents = None

    app.tryingToClickManualMode = False
    app.rows = 9
    app.cols = 9
    spaceFromTop =100
    app.boardTop = spaceFromTop
    app.boardHeight = app.height-2*spaceFromTop
    app.boardLeft = app.width/2-app.boardHeight/2
    app.boardWidth = app.boardHeight
    app.cellBorderWidth = 2

    app.listOfDifficulties=['easy', 'medium', 'hard', 'expert', 'evil']
    app.listOfColorDifficulties=['green', 'yellow', 'orange', 'red', 'maroon']
    app.difficultyChosen = None

    app.pressedDropDown = False

    app.initialBoard =None
    app.board=None
    app.randomBoard = None

    app.cellSelected = (0, 0)
    
    #DropDown Menu initializations
    app.leftChange, app.topChange=300, 150
    app.difficultySelectWidth=200
    app.difficultySelectHeight=40

    app.leftRect = app.width/3-app.leftChange-app.difficultySelectWidth/2
    app.topRect = app.height/4+app.topChange
    #(Right of 'Difficulty' Box)
    app.rightRect=app.width/3-app.leftChange+(app.difficultySelectWidth/3)

    app.arrowRectWidth=app.difficultySelectWidth/6

    app.boardState = None

    app.manualMode = False
    
    app.manualBoard = None
    app.tempBoard = None

    app.legalsShown= True
    app.automaticLegalMode = True

    app.selectedLegals = makeEmptyLegalsList(app)
    app.highlightedLegal = None # (row, col, val)
    app.automaticLegals=None

    app.showSingletonErrorMessage= False
    app.makeLegalBoardErrorMessage = False

    app.steps = 0
    app.stepsPerSecond =20

    app.keyboardLegalMode = False

    app.solutionBoard = None

    app.incorrectValuesOrLegals = [[False]*app.cols for row in range(app.rows)]

    app.movesToUndo=[] #When the user plays a move these are the moves to undo
    app.movesToRedo=[] #When the user undoes a move these are the moves to redo

    app.hint1Cell = None
    app.hint2Cells = None

    app.displayWrongBoardError=False

    app.competitionMode = False

    app.wordokuChosen = False
    app.wordokuNumsToLetters =None
    app.wordokuEnterValueMode = False

    app.mathdokuChosen = False
    app.mathdokuBoard=None
    app.mathdokuAreasToColors=dict()
    app.mathdokuNumsAndValues=dict()
    app.mathdokuValuesToLocations=dict()
    app.mathdokuSelectedRegion=None
    app.sumdokuChosen = False
    app.multiplicationdokuChosen = False

    app.kropkiChosen=False

    app.xSumsChosen = False
    app.xSumNumsAndLocations=[]
    
    app.currentVariation=None
def playScreen_onScreenStart(app):
    reset(app)
def playScreen_redrawAll(app):
    if app.displayWrongBoardError:
        drawLabel("You have one of more incorrect values you cannot do this", 400, 65)
    drawBoard(app)
    drawBoardBorder(app)
    drawHelpButton(app)
    drawDropDownMenu(app)
    drawValuesOfSudoku(app)
    drawNumPad(app)
    drawLegalButton(app)
    drawVariationRulesButton(app)
    if app.board!=None:
        currentVariation = app.currentVariation if app.currentVariation!=None else "Normal"
        if currentVariation!=None:
            drawNormalizeButton(app)
        drawLabel(f"Current Mode: ", 325, 40, bold=True, size=20)
        drawLabel(f'{currentVariation}', 470, 40, bold=True, size=18, fill="red")
    if not app.manualMode:
        drawRedoAndUndoButtons(app)
        drawToggleAutomaticLegals(app)
        drawManualModeButton(app)
        drawHintButton(app)
        drawNextSingletonButton(app)
        drawAllSingletonButton(app)
        drawChooseVariationButton(app)
        if app.hint1Cell!=None or app.hint2Cells!=None:
            drawRemoveHintButton(app)
        if not app.pressedDropDown:
            drawTransformButton(app)
            drawRandomButton(app)
        if app.wordokuChosen:
            drawEnterLettersButton(app)
    if app.tryingToClickManualMode:
        drawLabel("Pick a diffiulty first :)", app.width/2, app.height-84, size=20)
    if app.manualMode:
        drawManualButtons(app)
        drawFileButton(app)
    if app.board!=None and not app.manualMode:
        #Draw Either Automatic or Selected Legal Values
        if app.automaticLegalMode:
            drawAutomaticLegalValues(app)
        else:
            drawSelectedLegalValues(app)
        #Draw Highlighted Legal
        if app.highlightedLegal!=None:
            row, col, val = app.highlightedLegal
            if app.board[row][col]==0:
                drawLegals(app, row, col, {val})
        drawRedDots(app)
    if app.showSingletonErrorMessage and not app.displayWrongBoardError:
        drawLabel("NO SINGLETONS AT THIS TIME", app.width/2, 65, fill="red", size=25)
    if app.makeLegalBoardErrorMessage and not app.displayWrongBoardError and not app.showSingletonErrorMessage:
        drawLabel("Not a valid board to create.", app.width/2, 65, fill="crimson", size=25)
    
    if app.board!=None and app.board!=[] and noZerosInBoard(app.board):
        #Don't check if app.board==app.solutionBoard in case the user found another solution I suppose
        if isLegalSudoku(app.board):
            if app.competitionMode and app.contents!=None:
                content = makeBoardToContent(copy.deepcopy(app.board))
                writeFile("/Users/chrisbernitsas/Desktop/15-112 Term Project FINAL/competition mode answers/competition-mode-answer-1.png.txt", content)
            setActiveScreen('gameWonScreen')
        else:
            setActiveScreen('gameLostScreen')
def drawNumPad(app):
    totalSpace = 1325-1100
    gap = totalSpace/2
    startX, startY = 1100, 240
    for num in range(1, 10):
        row, col = (num-1)//3, (num-1)%3
        drawCircle(startX + col*gap, startY+row*gap, 50, fill=None, border="red")
        if app.wordokuChosen:
            num = app.wordokuNumsToLetters[num].upper()
        drawLabel(f"{num}", startX+col*gap, startY+row*gap, size = 30)
    drawOval(startX+gap, startY+gap, 3.2*gap, 5.5*gap, fill=None, border="Black")
    drawLabel(f"NUMPAD", startX+gap, startY+gap-2.25*gap, size=30, bold=True, fill="red")
    drawLabel(f"(Click to enter value)", startX+gap, startY+gap-1.75*gap, size=24, bold=False, fill="red")

    yValue=40
    drawLabel(f"Press E: easy", 150, yValue, bold=True, size=20)
    drawLabel(f"Press M: medium", 150, yValue+30, bold=True, size=20)
    drawLabel(f"Press H: Hard", 150, yValue+60, bold=True, size=20)
    drawLabel(f"Press X: expert", 150, yValue+90, bold=True, size=20)
    drawLabel(f"Press V: evil", 150, yValue+120, bold=True, size=20)

    if app.difficultyChosen !=None:
        drawLabel(f"Difficulty Chosen: ", app.width/2, 40, bold=True, size=20)
        drawLabel(f'{app.difficultyChosen}', app.width/2+140, 40, fill=app.listOfColorDifficulties[app.listOfDifficulties.index(app.difficultyChosen)], bold=True, size=24)
def drawRedDots(app):
    rows, cols = len(app.incorrectValuesOrLegals), len(app.incorrectValuesOrLegals[0])
    for row in range(rows):
        for col in range(cols):
            if app.incorrectValuesOrLegals[row][col]==True:
                cellLeft, cellTop = getCellLeftTop(app, row, col)
                cellWidth, cellHeight = getCellSize(app)
                drawCircle(cellLeft+cellWidth*(2/3), cellTop+cellHeight*(2/3), 5, fill="red")
def drawRedoAndUndoButtons(app):
    drawRect(700, 750, 100, 50, fill=None, border ="black")
    drawLabel("Undo", 750, 775, size =15)
    drawRect(900, 750, 100, 50, fill=None, border ="black")
    drawLabel("Redo", 950, 775, size =15)
def drawNormalizeButton(app):
    drawRect(1050, 650, 100, 50, fill=None, border ="black")
    drawLabel("Click to reset", 1100, 665, size =13)
    drawLabel("Varations (n)", 1100, 680, size =13)
def drawRemoveHintButton(app):
    drawRect(950, 40, 100, 50, fill=None, border="Black")
    drawLabel("Remove Hint (p)", 1000, 65, bold=False, size=13)
def drawRandomButton(app):
    drawRect(75, 450, 100, 50, fill=None, border="Black")
    drawLabel("Random Board(r)", 125, 475, size=12)
def drawTransformButton(app):
    drawRect(225, 450, 100, 50, fill=None, border="Black")
    drawLabel("Transform Board(t)", 275, 475, size=12)
def drawEnterLettersButton(app):
    drawRect(1050, 725, 100, 50, fill=None, border="Black")
    drawLabel("Toggle placing", 1100, 740)
    drawLabel("with keyboard", 1100, 760)
def withinEnterLettersButton(app, x, y):
    if 1050<=x<=1150 and 725<=y<=750:
        return True
    return False
def withinNormalizeButton(app, x, y):
    if 1050<=x<=1150 and 650<=y<=700:
        return True
    return False
def withinRandomButton(app, x, y):
    if 75<=x<=175 and 450<=y<=500 and not app.pressedDropDown:
        return True
    return False
def withinTransformButton(app, x, y):
    if 225<=x<=325 and 450<=y<=550 and not app.pressedDropDown:
        return True
    return False
def withinRemoveHintButton(app, x, y):
    if 950<=x<=1050 and 40<=y<=90:
        return True
    return False
def withinUndoButton(app, x, y):
    if 700<=x<=800 and 750<=y<=800:
        return True
    return False
def withinRedoButton(app, x, y):
    if 900<=x<=1000 and 750<=y<=800:
        return True
    return False
def drawLegalButton(app):
    drawRect(1200, 725, 100, 50, fill=None, border="Black")
    drawLabel("Toggle Placing", 1250, 750, size=14)
    drawLabel("Legals", 1250, 765, size=14)
def withinLegalButton(app, x, y):
    if 1100<=x<=1300 and 675<=y<=775:
        return True
    return False
def drawFileButton(app):
    drawRect(100, 700, 100, 100, fill=None, border="Black")
    drawLabel("Choose custom", 150, 750, size=16)
    drawLabel("Text File", 150, 770, size=16)
def withinFileButton(app, x, y):
    if 100<=x<=200 and 700<=y<=800:
        return True
    return False
def drawHintButton(app):
    drawRect(350, 750, 100, 50, fill=None, border="Black")
    drawLabel("Get Hint", 400, 770, size=16)
def drawNextSingletonButton(app):
    drawRect(475, 750, 100, 50, fill=None, border="Black")
    drawLabel("Play Next", 525, 760, size=16)
    drawLabel("Singleton", 525, 775, size=16)
def drawAllSingletonButton(app):
    drawRect(575, 750, 100, 50, fill=None, border="Black")
    drawLabel("Play All", 625, 760, size=16)
    drawLabel("Singletons", 625, 775, size=16)
def withinHintButton(app, x, y):
    if 350<=x<=450 and 750<=y<=800:
        return True
    return False
def withinNextSingletonButton(app, x, y):
    if 475<=x<=575 and 750<=y<=800:
        return True
    return False
def withinAllSingletonButton(app, x, y):
    if 575<=x<=675 and 750<=y<=800:
        return True
    return False
def getLegals(app):
    if app.boardState!=None:
        return app.boardState.getLegalList()
def drawAutomaticLegalValues(app):
    legals = app.automaticLegals
    for row in range(app.rows):
        for col in range(app.cols):
            if str(app.board[row][col]) not in '123456789':
                drawLegals(app, row, col, legals[row][col])
def drawLegals(app, row, col, legalSet):
    cellLeft, cellTop = getCellLeftTop(app, row, col)
    cellWidth, cellHeight = getCellSize(app)
    for legal in legalSet:
        legalRow, legalCol = (legal-1)//3, (legal-1)%3
        if app.mathdokuChosen:
            newWidth=cellWidth*(4/5)
        else:
            newWidth=cellWidth
        if app.multiplicationdokuChosen:
            newHeight=cellHeight*(4/5)
        else:
            newHeight=cellHeight
        x=cellLeft+(newWidth/6)+(newWidth)*((legalCol)/3)
        y=cellTop+(newHeight/6) + (newHeight)*((legalRow)/3)
        if (row, col, legal) == app.highlightedLegal:
            isBold=True
            legalSize = 20
        else:
            isBold = False
            legalSize=12
        if app.wordokuChosen:
            legal=app.wordokuNumsToLetters[legal].upper()
        if app.mathdokuChosen:
            x=x+9
        if app.multiplicationdokuChosen:
            y=y+9
        drawLabel(f'{legal}', x, y, size=legalSize, fill="gray", bold = isBold)
def drawSelectedLegalValues(app):
    rows, cols = len(app.selectedLegals), len(app.selectedLegals[0])
    for row in range(rows):
        for col in range(cols):
            if str(app.board[row][col]) not in '123456789':
                legalSet=app.selectedLegals[row][col]
                drawLegals(app, row, col, legalSet)
def drawManualButtons(app):
    drawRect(100, 500, 100, 100, fill=None, border ="Black")
    drawLabel("Make board(y)", 150, 550)

    drawRect(300, 500, 100, 100, fill=None, border ="Black")
    drawLabel("Cancel Board(c)", 350, 550)
def drawManualModeButton(app):
    drawRect(200, 720, 100, 100, fill=None, border ="Black")
    drawLabel("Enter Manual", 250, 770)
    drawLabel("Mode (M, shift+M)", 250, 785)
def withinManualModeButton(app, x, y):
    if 200<=x<=300 and 720<=y<=820:
        return True
    return False
def drawValuesOfSudoku(app):
    if not app.manualMode:
        if app.board ==None:
            return
        num=0
        for row in app.board:
            for v in row:
                if v!=0:
                    drawValueInCell(app, num, v)
                num+=1
    else:
        if app.manualBoard!=None:
            num=0
            for row in app.manualBoard:
                for v in row:
                    if v!=0:
                        drawValueInCell(app, num, v)
                    num+=1
def drawValueInCell(app, num, v):
    row, col = num//9, num%9
    cellLeft, cellTop = getCellLeftTop(app, row, col)
    cellWidth, cellHeight = getCellSize(app)
    color= 'blue' if app.initialBoard[row][col]==0 else 'black'
    if app.manualMode: color = "purple"
    if app.wordokuChosen:
        v=app.wordokuNumsToLetters[v].upper()
    drawLabel(f"{v}", cellLeft+cellWidth/2, cellTop+cellHeight/2, bold = True, size =24, fill=color)
def drawDropDownMenu(app):
    drawRect(app.leftRect, app.topRect, app.difficultySelectWidth*(5/6), app.difficultySelectHeight, fill=None, border="Black")
    drawLabel("Difficulty", app.leftRect+app.difficultySelectWidth/2, app.topRect+app.difficultySelectHeight/2)

    drawRect(app.rightRect, app.topRect, app.difficultySelectWidth*(1/6), app.difficultySelectHeight, fill=None, border="Black")
    drawPolygon(app.rightRect+app.arrowRectWidth/8, app.topRect+app.difficultySelectHeight/4, 
                app.rightRect+app.arrowRectWidth*(7/8), app.topRect+app.difficultySelectHeight/4, 
                app.rightRect+app.arrowRectWidth/2, app.topRect+app.difficultySelectHeight*(7/8), 
                fill="Black")
    listOfDifficulties=['easy', 'medium', 'hard', 'expert', 'evil']
    listOfColorDifficulties=['green', 'yellow', 'orange', 'red', 'maroon']
    if app.pressedDropDown:
        for i in range(len(listOfDifficulties)):
            #120 difficulty select width, 20 height
            drawRect(app.leftRect, app.topRect+app.difficultySelectHeight*(i+1), app.difficultySelectWidth, app.difficultySelectHeight, fill=listOfColorDifficulties[i], border="Black")
            drawLabel(f"{listOfDifficulties[i]}", app.leftRect+app.difficultySelectWidth/2, app.topRect+app.difficultySelectHeight*(i+1)+app.difficultySelectHeight/2)
def getDifficulty(app, x, y):
    #1425, 825
    if ((app.leftRect)<=x<=(app.leftRect+app.difficultySelectWidth)):
        if y<app.topRect+app.difficultySelectHeight:
            return None
        i =int((y-(app.topRect+app.difficultySelectHeight))//app.difficultySelectHeight)
        if i>4:
            return None
        else:
            return app.listOfDifficulties[i]
    else:
        return None
def withinDropDown(app, x, y):
    if ((app.rightRect)<=x<=(app.leftRect+app.difficultySelectWidth) and (app.topRect)<=y<=(app.topRect+app.difficultySelectHeight)):
        return True
    return False       
def getHint1(app):
    legals = getLegals(app)
    singletonCells = []
    for row in range(app.rows):
        for col in range(app.cols):
            if len(legals[row][col])==1:
                singletonCells.append((row, col))
    if len(singletonCells)!=0:
        singletonCell = random.choice(singletonCells)
        row, col = singletonCell
        app.hint1Cell = (row, col)
        app.hint2Cells=None
        return True
    else:
        return None
def getHint2(app):
    regionNum=0
    for region in app.boardState.getAllLegalRegions():
        newRegion=[]
        count=0
        for eachSet in region:
            newRegion.append((eachSet, count))
            count+=1
        regionWithoutEmptySets=[]
        for (eachSet, count) in newRegion:
            if len(eachSet)!=0:
                regionWithoutEmptySets.append((eachSet, count))
        regionWithoutEmptySets=tuple(regionWithoutEmptySets)
        for N in range(2, 6):
            result = applyRule2(newRegion, N)
            if result != None and result!=regionWithoutEmptySets and restrictToHelpfulHint(result, regionWithoutEmptySets):
                cellPositions=extractCells(result, regionNum)
                app.hint2Cells=cellPositions
                app.hint1Cell=None
                return True
        regionNum+=1
    return None
def restrictToHelpfulHint(result, regionWithoutEmptySets):
    regionWithoutEmtpySetsAndOverlaps=[]
    for v in regionWithoutEmptySets:
        regionWithoutEmtpySetsAndOverlaps.append(v)
    for locationAndCount in result:
        if locationAndCount in regionWithoutEmtpySetsAndOverlaps:
            regionWithoutEmtpySetsAndOverlaps.remove(locationAndCount)
    allLegalsInSets=set()
    for (eachSet, count) in result:
        allLegalsInSets=allLegalsInSets.union(eachSet)
    for eachLegal in allLegalsInSets:
        for (eachSet, count) in regionWithoutEmtpySetsAndOverlaps:
            if eachLegal in eachSet:
                return True
    return False
def applyRule2(region, N):
    newRegion=[]
    for (eachSet, count) in region:
        if len(eachSet)!=0:
            newRegion.append((eachSet, count))
    if N>len(newRegion):
        return
    for combination in itertools.combinations(newRegion, N):
        allLegalsInSets=set()
        for (eachSet, count) in combination:
            allLegalsInSets=allLegalsInSets.union(eachSet)
        if len(allLegalsInSets)==N:
            return combination
def extractCells(result, regionNum):
    listOfCellPositions=[]
    if 0<=regionNum<=8:
        for (_, index) in result:
            listOfCellPositions.append((regionNum, index))
    elif 9<=regionNum<=17:
        col=regionNum-9
        for (_, index) in result:
            listOfCellPositions.append((index, col))
    elif 18<=regionNum<=26:
        blockNum=regionNum-18
        for (_, index) in result:
            insideRow, insideCol = index//3, index%3
            cellRow, cellCol = (blockNum//3)*3, (blockNum%3)*3
            listOfCellPositions.append((cellRow+insideRow, cellCol+insideCol))
    return listOfCellPositions
def playNextSingleton(app):
    rows, cols =len(app.incorrectValuesOrLegals), len(app.incorrectValuesOrLegals[0])
    for row in range(rows):
        for col in range(cols):
            if app.incorrectValuesOrLegals[row][col]:
                app.displayWrongBoardError=True
                return
    updateLegals(app)

    legals = getLegals(app)
    singletonCells = []
    for row in range(app.rows):
        for col in range(app.cols):
            if len(legals[row][col])==1:
                singletonCells.append((row, col))
    if singletonCells==[]:
        app.showSingletonErrorMessage = True
        if noZerosInBoard(app.board):
            app.showSingletonErrorMessage =False
            app.makeLegalBoardErrorMessage = False
        return False
    nextSingleton = random.choice(singletonCells)
    row, col = nextSingleton
    app.board[row][col]=list(legals[row][col])[0]
    val = list(legals[row][col])[0]

    addMovesToUndo(app, row, col, val)

    updateLegals(app)
    return True
def addMovesToUndo(app, row, col, val, dontClearRedo = False):
    shouldAppend = True
    appendPos=None
    for move in app.movesToUndo:
        (moveRow, moveCol, moveVal) = move
        if (row, col) ==(moveRow, moveCol):
            shouldAppend = False
            appendPos = app.movesToUndo.index(move)
    if shouldAppend==True:   
        app.movesToUndo.append((row, col, val))
    else:
        app.movesToUndo.pop(appendPos)
        app.movesToUndo.insert(appendPos, (row, col, val))
    if not dontClearRedo:
        app.movesToRedo.clear()
def enterManualMode(app):
    app.manualBoard = [[0]*app.cols for row in range(app.rows)]
    app.manualMode = True
    app.tempBoard = copy.deepcopy(app.board)
    if app.board!=None:
        app.board.clear() 
    app.hint1Cell, app.hint2Cells = None, None
    app.cellSelected = (0, 0)
def isRightValue(app, row, col, val):
    if val==app.solutionBoard[row][col]:
        return True
    return False
def updateRedDotValues(app, isFromBoard=False):
    app.incorrectValuesOrLegals = [[False]*app.cols for row in range(app.rows)]
    if not app.manualMode:
        #updateLegals(app)
        if not app.automaticLegalMode and app.selectedLegals!=None:
            legalRows, legalCols = len(app.selectedLegals), len(app.selectedLegals[0])
            actualLegals = getLegals(app)
        elif app.automaticLegalMode and app.automaticLegals!=None:
            legalRows, legalCols = len(app.automaticLegals), len(app.automaticLegals[0])
            actualLegals = getLegals(app)
        else:
            pass
        if not isFromBoard:
            for legalRow in range(legalRows):
                for legalCol in range(legalCols):
                    # for legal in app.selectedLegals[legalRow][legalCol]:
                        # if legal not in actualLegals[legalRow][legalCol]:
                        #     app.incorrectValuesOrLegals[legalRow][legalCol]=True
                    if not app.automaticLegalMode:
                        if app.solutionBoard[legalRow][legalCol] not in app.selectedLegals[legalRow][legalCol]:
                            if str(app.initialBoard[legalRow][legalCol]) not in '123456789' and len(app.selectedLegals[legalRow][legalCol])>0 and app.board[legalRow][legalCol]==0:
                                app.incorrectValuesOrLegals[legalRow][legalCol]=True
                                if app.competitionMode:
                                    setActiveScreen('gameLostScreen')
                    elif app.automaticLegalMode:
                        if app.solutionBoard[legalRow][legalCol] not in app.automaticLegals[legalRow][legalCol]:
                            if str(app.initialBoard[legalRow][legalCol]) not in '123456789' and len(app.automaticLegals[legalRow][legalCol])>0 and app.board[legalRow][legalCol]==0:
                                app.incorrectValuesOrLegals[legalRow][legalCol]=True
                                if app.competitionMode:
                                    setActiveScreen('gameLostScreen')
        boardRows, boardCols = len(app.board), len(app.board[0])
        for boardRow in range(boardRows):
            for boardCol in range(boardCols):
                val = app.board[boardRow][boardCol]
                if val!=app.solutionBoard[boardRow][boardCol] and val!=0:
                    app.incorrectValuesOrLegals[boardRow][boardCol]=True
                    if app.competitionMode:
                        setActiveScreen('gameLostScreen')
def updateLegals(app):
    legalList =makeLegalsList(app)
    app.boardState = State(app.board, legalList)
    for row in range(app.rows):
        for col in range(app.cols):
            value = app.board[row][col]
            if value!=0:
                app.boardState.set(row, col, value)
    if app.automaticLegalMode:
        app.automaticLegals=app.boardState.legals
    return app.boardState.legals
def getCorrectLegals(app):
    legalList =makeLegalsList(app)
    solutionBoard = copy.deepcopy(app.solutionBoard)
    solutionState = State(solutionBoard, legalList)
    for row in range(app.rows):
        for col in range(app.cols):
            value = solutionBoard[row][col]
            if value!=0:
                solutionState.set(row, col, value)
    return solutionState.legals
def undoPreviousMove(app):
    if len(app.movesToUndo)>0:
        previousMove =app.movesToUndo.pop()
        app.movesToRedo.append(previousMove)
        (row, col, num) = previousMove
        app.boardState.remove(row, col)
        if app.automaticLegalMode:
            app.automaticLegals=updateLegals(app)
        updateRedDotValues(app, True)
def redoNextMove(app):
    if len(app.movesToRedo)>0:
        nextMove = app.movesToRedo.pop()
        (row, col, val) = nextMove
        dontClearRedo = True
        addMovesToUndo(app, row, col, val, dontClearRedo)
        app.boardState.set(row, col, val)
        if app.automaticLegalMode:
            app.automaticLegals=updateLegals(app)
        updateRedDotValues(app, True)
def startGame(app, difficulty):
    app.incorrectValuesOrLegals = [[False]*app.cols for row in range(app.rows)]
    app.difficultyChosen = difficulty
    app.automaticLegalMode = True if app.difficultyChosen in ['easy'] else False
    content = getFileContent(app.difficultyChosen)
    app.initialBoard = makeBoard(app, content)
    app.board = copy.deepcopy(app.initialBoard)
    app.solutionBoard = solveSudoku(copy.deepcopy(app.board))

    #app.board=app.solutionBoard

    if app.wordokuChosen:
        setupWordoku(app)
    if app.mathdokuChosen:
        setupMathdoku(app)
    if app.kropkiChosen:
        setupKropki(app)
    if app.xSumsChosen:
        setupXSums(app)
    app.showSingletonErrorMessage =False
    app.makeLegalBoardErrorMessage = False
    clearSingletonList(app)
    app.cellSelected = (0, 0)
    app.hint1Cell, app.hint2Cells = None, None
    updateLegals(app)
def startCustomGame(app, content):
    reset(app)
    app.manualMode =False
    app.difficultyChosen = 'evil'
    app.automaticLegalMode = True if app.difficultyChosen in ['easy'] else False
    app.initialBoard = makeBoard(app, content)
    app.board = copy.deepcopy(app.initialBoard)
    app.solutionBoard = solveSudoku(app.board)
    updateLegals(app)
    app.showSingletonErrorMessage =False
    app.makeLegalBoardErrorMessage = False
    clearSingletonList(app)
    app.cellSelected = (0, 0)
def setupWordoku(app):
    nineLetterWord = getRandomWord()
    rowOrCol = random.randint(1, 2)
    numberToLetter = dict()
    if rowOrCol ==1:
        rowNum = random.randint(0, 8)
        randomRow = app.solutionBoard[rowNum]
        for i in range(9):
            numberToLetter[randomRow[i]]= nineLetterWord[i]
    elif rowOrCol ==2:
        colNum = random.randint(0, 8)
        randomCol=[]
        for row in range(app.rows):
            randomCol.append(app.solutionBoard[row][colNum])
        for i in range(9):
            numberToLetter[randomCol[i]]= nineLetterWord[i]
    app.wordokuNumsToLetters = numberToLetter
def setupMathdoku(app):
    app.mathdokuBoard = [[None]*app.cols for row in range(app.rows)]
    section=0
    while not isFullBoard(app, app.mathdokuBoard):
        (row, col) = getTopLeftCellWithValue(app, app.mathdokuBoard, None)
        while True:
            app.mathdokuBoard[row][col]=section
            probablityOfMovingOn = random.randint(1, 4)
            if probablityOfMovingOn!=4:
                possibleMoves = getPossibleMoves(app, app.mathdokuBoard, row, col, section)
                if possibleMoves==[]:
                    section+=1
                    break
                else:
                    move = random.choice(possibleMoves)
                    (drow, dcol) = move
                    row, col =row+drow, col+dcol
                    app.mathdokuBoard[row][col]=section
            else:
                section+=1
                break
    app.mathdokuAreasToColors=assignColors(app, app.mathdokuBoard)
    app.mathdokuNumsAndValues = getNumsAndValues(app, app.mathdokuBoard)
    app.mathdokuValuesToLocations = getValuesAndLocations(app, app.mathdokuBoard)
def getValuesAndLocations(app, board):
    valuesAndLocationsDict=dict()
    for row in range(len(board)):
        for col in range(len(board[0])):
            sectionNum = app.mathdokuBoard[row][col]
            (regionCellRow, regionCellCol) = getTopLeftCellWithValue(app, app.mathdokuBoard, sectionNum)
            (highestCellLeft, highestCellTop) = getCellLeftTop(app, regionCellRow, regionCellCol)
            cellLeft, cellTop = getCellLeftTop(app, row, col)
            if ((cellLeft == highestCellLeft) and (cellTop==highestCellTop)):
                value = app.mathdokuNumsAndValues[sectionNum]
                curentValueLocations = valuesAndLocationsDict.get(value, [])
                curentValueLocations.append((highestCellLeft, highestCellTop))
                valuesAndLocationsDict[value]=curentValueLocations
    return valuesAndLocationsDict
def getNumsAndValues(app, board):
    dictionaryOfNumsAndValues = dict()
    maxNum =-1
    for row in range(len(board)):
        for col in range(len(board[0])):
            if board[row][col]>maxNum:
                maxNum = board[row][col]
    
    for row in range(len(board)):
        for col in range(len(board[0])):
            sectionNum = board[row][col]
            addValue =app.solutionBoard[row][col]
            if app.sumdokuChosen:
                previousValue=dictionaryOfNumsAndValues.get(sectionNum, 0)
                newValue = previousValue + addValue
            elif app.multiplicationdokuChosen:
                previousValue=dictionaryOfNumsAndValues.get(sectionNum, 1)
                newValue = previousValue * addValue
            dictionaryOfNumsAndValues[sectionNum]=newValue
    return dictionaryOfNumsAndValues
def assignColors(app, board):
    areasToColors = dict()
    maxNum =-1
    for row in range(len(board)):
        for col in range(len(board[0])):
            if board[row][col]>maxNum:
                maxNum = board[row][col]
    for sectionNum in range(0, maxNum+1):
        if sectionNum not in areasToColors:
            redValue, greenValue, blueValue = random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)
            areasToColors[sectionNum]=(redValue, greenValue, blueValue)
    return areasToColors
def getPossibleMoves(app, board, row, col, section):
    rows, cols =len(board), len(board[0])
    oldRow = row
    oldCol = col
    possibleMoves=[]
    for move in [(0, +1), (0, -1), (-1, 0), (+1, 0)]:
        (drow, dcol) = move
        newRow, newCol = oldRow+drow, oldCol+dcol
        if ((newRow<0 or newRow>=rows or newCol<0 or  newCol>=cols) or (board[newRow][newCol]!=None and board[newRow][newCol]!=section)):
            continue
        possibleMoves.append((drow, dcol))
    return possibleMoves
def getTopLeftCellWithValue(app, board, value=None):
    for row in range(len(board)):
        for col in range(len(board[0])):
            if board[row][col]==value:
                return (row, col)
    return None
def setupKropki(app):
    app.kropkiBoard=[] #Each value will be ((row, col), (row, col), 'filled' or 'empty')
    #check horizontal pairs
    for row in range(app.rows):
        for horizontalPairStart in range(app.cols-1):
            c1 = (abs(app.solutionBoard[row][horizontalPairStart]-app.solutionBoard[row][horizontalPairStart+1])==1)
            c2= ((app.solutionBoard[row][horizontalPairStart]==2*app.solutionBoard[row][horizontalPairStart+1]) or (2*app.solutionBoard[row][horizontalPairStart]==app.solutionBoard[row][horizontalPairStart+1]))
            if c1 and c2:
                filledOrEmptyH=random.randint(0, 1)
                if filledOrEmptyH==0:
                    data = ((row, horizontalPairStart), (row, horizontalPairStart+1), 'empty')
                    app.kropkiBoard.append(data)
                elif filledOrEmptyH==1:
                    data = ((row, horizontalPairStart), (row, horizontalPairStart+1), 'filled')
                    app.kropkiBoard.append(data)
            elif c1:
                data = ((row, horizontalPairStart), (row, horizontalPairStart+1), 'empty')
                app.kropkiBoard.append(data)
            elif c2:
                data = ((row, horizontalPairStart), (row, horizontalPairStart+1), 'filled')
                app.kropkiBoard.append(data)
    for col in range(app.cols):
        for verticalPairStart in range(app.rows-1):
            c1=(abs(app.solutionBoard[verticalPairStart][col]-app.solutionBoard[verticalPairStart+1][col])==1)
            c2=((app.solutionBoard[verticalPairStart][col]==2*app.solutionBoard[verticalPairStart+1][col]) or (2*app.solutionBoard[verticalPairStart][col]==app.solutionBoard[verticalPairStart+1][col]))
            if c1 and c2:
                filledOrEmptyV = random.randint(0, 1)
                if filledOrEmptyV==0:
                    data = ((verticalPairStart, col), (verticalPairStart+1, col), 'empty')
                    app.kropkiBoard.append(data)
                elif filledOrEmptyV==1:
                    data = ((verticalPairStart, col), (verticalPairStart+1, col), 'filled')
                    app.kropkiBoard.append(data)
            elif c1:
                data = ((verticalPairStart, col), (verticalPairStart+1, col), 'empty')
                app.kropkiBoard.append(data)
            elif c2:
                data = ((verticalPairStart, col), (verticalPairStart+1, col), 'filled')
                app.kropkiBoard.append(data)

    app.initialBoard = [[0]*app.cols for row in range(app.rows)]
    app.board = copy.deepcopy(app.initialBoard)
def setupXSums(app):
    app.xSumNumsAndLocations=[]
    app.initialBoard = eliminateRandomCells(copy.deepcopy(app.board), random.randint(4, 8))
    app.board = copy.deepcopy(app.initialBoard)
    board = copy.deepcopy(app.solutionBoard)

    rowChoices=[0, 1, 2, 3, 4, 5, 6, 7, 8]
    randomRows =[]
    for _ in range(5):
        rowChoice = random.choice(rowChoices)
        rowChoices.remove(rowChoice)
        randomRows.append(rowChoice)
    colChoices=[0, 1, 2, 3, 4, 5, 6, 7, 8]

    randomCols =[]
    for _ in range(5):
        colChoice = random.choice(colChoices)
        colChoices.remove(colChoice)
        randomCols.append(colChoice)
    for row in randomRows:
        nums=board[row]
        totalSumOfRow=0
        for i in range(nums[0]):
            totalSumOfRow+=nums[i]
        cellLeft, cellTop = getCellLeftTop(app, row, 0)
        cellWidth, cellHeight = getCellSize(app)
        cx = cellLeft-cellWidth/4
        cy = cellTop+cellHeight/2
        app.xSumNumsAndLocations.append((totalSumOfRow, (cx, cy)))
    for col in randomCols:
        nums=getColList(board, col)
        totalSumOfCol=0
        for i in range(nums[0]):
            totalSumOfCol+=nums[i]
        cellLeft, cellTop = getCellLeftTop(app, 0, col)
        cellWidth, cellHeight = getCellSize(app)
        cx = cellLeft+cellWidth/2
        cy = cellTop-cellHeight/4
        app.xSumNumsAndLocations.append((totalSumOfCol, (cx, cy)))
def getColList(board, col):
    rows = len(board)
    listOfNums=[]
    for row in range(rows):
        listOfNums.append(board[row][col])
    return listOfNums
def isFullBoard(app, board):
    rows, cols = len(app.mathdokuBoard), len(app.mathdokuBoard[0])
    for row in board:
        if None in row:
            return False
    return True
def giveNextHint(app):
    hint1=getHint1(app)
    if hint1==None:
        getHint2(app)
def clearSingletonList(app):
    for row in app.selectedLegals:
        for square in row:
            square.clear()
def distance(x1, y1, x2, y2):
    return ((x2-x1)**2 +(y2-y1)**2)**(1/2)
def getNumPadKey(app, mouseX, mouseY):
    totalSpace = 1325-1100
    gap = totalSpace/2
    startX, startY = 1100, 240
    r=50
    for num in range(1, 10):
        row, col = (num-1)//3, (num-1)%3
        cx, cy = startX +col*gap, startY + row*gap
        if distance(cx, cy, mouseX, mouseY)<=r:
            return num
    return None
def playScreen_onMousePress(app, mouseX, mouseY):
    app.displayWrongBoardError=False
    #within Functionality
    if withinManualModeButton(app, mouseX, mouseY) and app.board==None:
        app.tryingToClickManualMode=True
    if withinVariationRulesButton(app, mouseX, mouseY):
        setActiveScreen("variationRulesScreen")
    if not app.manualMode and app.board!=None:
        if withinManualModeButton(app, mouseX, mouseY):
            if app.board!=None:
                enterManualMode(app)
            else:
                app.tryingToClickManualMode = True
        if withinLegalButton(app, mouseX, mouseY):
            app.keyboardLegalMode = not app.keyboardLegalMode
        if withinUndoButton(app, mouseX, mouseY):
            undoPreviousMove(app)
        if withinRedoButton(app, mouseX, mouseY):
            redoNextMove(app)
        if withinHintButton(app, mouseX, mouseY):
            giveNextHint(app)
        if withinNextSingletonButton(app, mouseX, mouseY):
            playNextSingleton(app)
        if withinAllSingletonButton(app, mouseX, mouseY):
            while playNextSingleton(app):
                    playNextSingleton(app)
        if withinRandomButton(app, mouseX, mouseY):
            userDifficultyInput = app.getTextInput("Which difficulty would you like this to be? (E/e: Easy, M/m: Medium, H/h: Hard, X/x:Expert, V/v:Evil")
            userDifficultyInput =userDifficultyInput.lower()
            userRandomDifficulty = None
            while userRandomDifficulty==None:
                if userDifficultyInput=='e': userRandomDifficulty='easy'
                elif userDifficultyInput=='m': userRandomDifficulty='medium'
                elif userDifficultyInput=='h': userRandomDifficulty='hard'
                elif userDifficultyInput=='x': userRandomDifficulty='expert'
                elif userDifficultyInput=='v': userRandomDifficulty='evil'
                if userRandomDifficulty==None:
                    userDifficultyInput = app.getTextInput("Please Enter a valid difficulty")
            generateRandomBoard(app, userRandomDifficulty)
        if withinTransformButton(app, mouseX, mouseY):
            transformBoard(app)
        if withinChooseVariationButton(app, mouseX, mouseY):
            setActiveScreen("chooseVariations")
        if withinEnterLettersButton(app, mouseX, mouseY):
            app.wordokuEnterValueMode = not app.wordokuEnterValueMode
        if withinRemoveHintButton(app, mouseX, mouseY):
            app.hint1Cell = None
            app.hint2Cells = None
        if withinNormalizeButton(app, mouseX, mouseY) and app.currentVariation!=None:
            resetVariations(app)
            if app.difficultyChosen ==None:
                app.difficultyChosen = "medium"
            startGame(app, app.difficultyChosen)
        if withinToggleAutomaticLegals(app, mouseX, mouseY):
            app.automaticLegalMode = not app.automaticLegalMode
            if app.boardState!=None:
                updateLegals(app)
                updateRedDotValues(app)
    if withinDropDown(app, mouseX, mouseY):
        app.pressedDropDown = not app.pressedDropDown
    if app.pressedDropDown and not app.manualMode:
        difficulty = getDifficulty(app, mouseX, mouseY)
        if difficulty!=None:
            startGame(app, difficulty)

    cellSelected = getCell(app, mouseX, mouseY)
    if cellSelected != None:
        app.cellSelected = cellSelected

    if withinHelp(app, mouseX, mouseY):
        setActiveScreen('helpScreen')

    if app.manualMode:
        if withinMakeManualBoard(app, mouseX, mouseY):
            startManualBoard(app)
        if withinCancelManualBoard(app, mouseX, mouseY):
            startCancelManualBoard(app)
        if withinFileButton(app, mouseX, mouseY):
            userTextFile = app.getTextInput("Please enter the custom text file you desire Ex. (Custom.png.txt) Difficulty of Custom Files is Evil")
            content = getCustomFileContent(userTextFile)
            if content==None:
                pass
            else:
                startCustomGame(app, content)
    #Selects Legals
    if app.highlightedLegal!=None:
        if not app.automaticLegalMode:
            row, col, val = app.highlightedLegal
            if str(app.initialBoard[row][col]) not in '123456789':
                if val in app.selectedLegals[row][col]:
                    app.selectedLegals[row][col].remove(val)
                    if app.boardState!=None:
                        if val ==app.solutionBoard[row][col]:
                            app.incorrectValuesOrLegals[row][col]=True
                            if app.competitionMode:
                                    setActiveScreen('gameLostScreen')
                else:
                    app.selectedLegals[row][col].add(val)
                    if val==app.solutionBoard[row][col]:
                        if app.boardState!=None:
                            app.incorrectValuesOrLegals[row][col]=False
        elif app.automaticLegalMode:
            row, col, val = app.highlightedLegal
            if str(app.initialBoard[row][col]) not in '123456789':
                if val in app.automaticLegals[row][col]:
                    app.automaticLegals[row][col].remove(val)
                    if app.boardState!=None:
                        if val ==app.solutionBoard[row][col]:
                            app.incorrectValuesOrLegals[row][col]=True
                            if app.competitionMode:
                                setActiveScreen('gameLostScreen')
                else:
                    app.automaticLegals[row][col].add(val)
                    if val==app.solutionBoard[row][col]:
                        if app.boardState!=None:
                            app.incorrectValuesOrLegals[row][col]=False
    numPadKey = getNumPadKey(app, mouseX, mouseY)
    #Adds value to board, Play Move
    if str(numPadKey) in '123456789' and app.board!=None:
        if not app.keyboardLegalMode:
            app.showSingletonErrorMessage = False
            app.makeLegalBoardErrorMessage = False
            row, col = app.cellSelected
            if app.manualMode:
                app.manualBoard[row][col]= int(numPadKey)
            else:
                if str(app.initialBoard[row][col]) not in '123456789':
                    previousValue = app.board[row][col]
                    app.board[row][col] = int(numPadKey)
                    if (row, col) == app.hint1Cell:
                        app.hint1Cell = None
                    if app.hint2Cells!=None and (row, col) in app.hint2Cells:
                        app.hint2Cells=None
                    val = int(numPadKey)
                    addMovesToUndo(app, row, col, val)
                    if app.automaticLegalMode:
                        app.automaticLegals = updateLegals(app)
                    if app.boardState!=None:
                        if val==app.solutionBoard[row][col]:
                            app.incorrectValuesOrLegals[row][col]=False
                        elif val!=app.solutionBoard[row][col]:
                            app.incorrectValuesOrLegals[row][col]=True
                            if app.competitionMode:
                                setActiveScreen('gameLostScreen')
        #Keyboard Legal Mode, selects Legals
        else:
            app.showSingletonErrorMessage = False
            app.makeLegalBoardErrorMessage = False
            row, col= app.cellSelected
            val = int(numPadKey)
            if str(app.initialBoard[row][col]) not in '123456789':
                if val in app.selectedLegals[row][col]:
                    app.selectedLegals[row][col].remove(val)
                    if app.boardState!=None:
                        if val ==app.solutionBoard[row][col]:
                            app.incorrectValuesOrLegals[row][col]=True
                            if app.competitionMode:
                                setActiveScreen('gameLostScreen')
                else:
                    app.selectedLegals[row][col].add(val)
                    if val==app.solutionBoard[row][col]:
                        if app.boardState!=None:
                            app.incorrectValuesOrLegals[row][col]=False
def playScreen_onMouseMove(app, mouseX, mouseY):
    if not app.manualMode:
        hoveredCell = getCell(app, mouseX, mouseY)
        if hoveredCell==None or app.board==None:
            return 
        row, col = hoveredCell
        if hoveredCell!=None:
            cellLeft, cellTop = getCellLeftTop(app, row, col)
            cellWidth, cellHeight = getCellSize(app)
            dx, dy =mouseX-cellLeft, mouseY-cellTop
            if dx<0 or dx>cellWidth or dy<0 or dy>cellHeight:
                return
            legalRow, legalCol = int(dy//(cellHeight/3)), int(dx//(cellWidth/3))
            if app.cellSelected == hoveredCell  and str(app.board[row][col]) not in '123456789':
                app.highlightedLegal = (row, col, int(legalRow*3+legalCol+1))
            else:
                app.highlightedLegal=None
            if app.mathdokuChosen:
                app.mathdokuSelectedRegion=app.mathdokuBoard[row][col]
def withinMakeManualBoard(app, x, y):
    if (100<=x<=200) and (500<=y<=600):
        return True
    return False
def withinCancelManualBoard(app, x, y):
    if (300<=x<=400) and (500<=y<=600):
        return True
    return False
def playScreen_onKeyPress(app, key):
    app.displayWrongBoardError=False
    if app.manualMode:
        row, col = app.cellSelected
        if key in '123456789':
            app.showSingletonErrorMessage = False
            app.makeLegalBoardErrorMessage = False
            app.manualBoard[row][col]=int(key)
        if key =='y' or key=='Y':
            startManualBoard(app)
        if key =='c' or key =='C':
            startCancelManualBoard(app)
    #Not manual Mode
    else:
        if app.wordokuChosen:
            wordokuLetters=getWordokuLetters(app)
        if key=='u' and app.wordokuChosen:
            app.wordokuEnterValueMode = not app.wordokuEnterValueMode
        elif app.wordokuChosen and app.wordokuEnterValueMode:
            if key in wordokuLetters:
                for value in app.wordokuNumsToLetters:
                    if app.wordokuNumsToLetters[value]==key:
                        num = value
                playMove(app, num)
        if key =='L' or (key=='l' and (not app.wordokuChosen or (app.wordokuChosen and key not in wordokuLetters))):
            app.keyboardLegalMode=not app.keyboardLegalMode
        #Add legals in keyboard Legal Mode
        if key in '123456789' and app.keyboardLegalMode and app.board!=None:
            if not app.automaticLegalMode:
                row, col= app.cellSelected
                if str(app.initialBoard[row][col]) not in '123456789':
                    val = int(key)
                    if val in app.selectedLegals[row][col]:
                        app.selectedLegals[row][col].remove(val)
                        if app.boardState!=None:
                            if val ==app.solutionBoard[row][col]:
                                app.incorrectValuesOrLegals[row][col]=True
                                if app.competitionMode:
                                    setActiveScreen('gameLostScreen')
                    else:
                        app.selectedLegals[row][col].add(val)
                        if val==app.solutionBoard[row][col]:
                            if app.boardState!=None:
                                app.incorrectValuesOrLegals[row][col]=False
            elif app.automaticLegalMode:
                app.showingSingletonErrorMessage = False
                app.makeLegalBoardErrorMessage = False
                row, col= app.cellSelected
                if str(app.initialBoard[row][col]) not in '123456789':
                    val = int(key)
                    if val in app.automaticLegals[row][col]:
                        app.automaticLegals[row][col].remove(val)
                        if app.boardState!=None:
                            if val ==app.solutionBoard[row][col]:
                                app.incorrectValuesOrLegals[row][col]=True
                                if app.competitionMode:
                                    setActiveScreen('gameLostScreen')
                    else:
                        app.automaticLegals[row][col].add(val)
                        if val==app.solutionBoard[row][col]:
                            if app.boardState!=None:
                                app.incorrectValuesOrLegals[row][col]=False
        if not app.wordokuEnterValueMode:
            if key=='z' or key=='Z':
                setActiveScreen('helpScreen')
            if key=='b' or key=='B':
                setActiveScreen('variationRulesScreen')
            if app.board!=None:
                if key =='o':
                    app.automaticLegalMode = not app.automaticLegalMode
                    if app.boardState!=None:
                        updateLegals(app)
                        updateRedDotValues(app)
                if ((key ==';' or key=='H') and not app.competitionMode):
                    giveNextHint(app)
                if key=='p':
                    app.hint1Cell = None
                    app.hint2Cells = None
                if key=='t' and app.board!=None:
                    transformBoard(app)
                if key=='[':
                    undoPreviousMove(app)
                elif key==']':
                    redoNextMove(app)
        if key =='r':
            userDifficultyInput = app.getTextInput("Which difficulty would you like this to be? (E/e: Easy, M/m: Medium, H/h: Hard, X/x:Expert, V/v:Evil")
            userDifficultyInput =userDifficultyInput.lower()
            userRandomDifficulty = None
            while userRandomDifficulty==None:
                if userDifficultyInput=='e': userRandomDifficulty='easy'
                elif userDifficultyInput=='m': userRandomDifficulty='medium'
                elif userDifficultyInput=='h': userRandomDifficulty='hard'
                elif userDifficultyInput=='x': userRandomDifficulty='expert'
                elif userDifficultyInput=='v': userRandomDifficulty='evil'
                if userRandomDifficulty==None:
                    userDifficultyInput = app.getTextInput("Please Enter a valid difficulty")
            generateRandomBoard(app, userRandomDifficulty)
        #Add value to Board, Play Move
        if key in '123456789' and app.initialBoard!=None and app.board!=None and not app.keyboardLegalMode:
            playMove(app, key)
        if not app.competitionMode and not app.wordokuEnterValueMode and app.board!=None:
            if key =='s' and app.difficultyChosen in ['medium', 'hard', 'expert', 'evil']:
                playNextSingleton(app)
            elif key =='S' and app.difficultyChosen in ['medium', 'hard', 'expert', 'evil']:
                while playNextSingleton(app):
                    playNextSingleton(app)
        if key =='M':
            if app.difficultyChosen!=None:
                enterManualMode(app)
            elif app.difficultyChosen==None or app.board==None:
                app.tryingToClickManualMode = True
        if key =='w':
            resetVariations(app)
            if app.difficultyChosen==None:
                app.difficultyChosen ="medium"
            app.wordokuChosen = not app.wordokuChosen
            app.currentVariation="Wordoku"
            if app.difficultyChosen!=None:
                startGame(app, app.difficultyChosen)
        if key =='k':
            resetVariations(app)
            if app.difficultyChosen==None:
                app.difficultyChosen ="medium"
            app.mathdokuChosen = not app.mathdokuChosen
            typeOfMathdoku=None
            while typeOfMathdoku!='s' and typeOfMathdoku!='S' and typeOfMathdoku!='m' and typeOfMathdoku!='M':
                typeOfMathdoku = app.getTextInput("Enter S/s for SumDoku and M/m for MultiplicationDoku!")
            if typeOfMathdoku.lower()=='s':
                app.currentVariation="Mathdoku (Sum)"
                app.sumdokuChosen=True
            elif typeOfMathdoku.lower()=='m':
                app.multiplicationdokuChosen = True
                app.currentVariation = "Mathdoku (Mult)"
            if app.difficultyChosen!=None:
                startGame(app, app.difficultyChosen)
        if key =='j':
            resetVariations(app)
            if app.difficultyChosen==None:
                app.difficultyChosen ="medium"
            app.kropkiChosen = not app.kropkiChosen
            app.currentVariation = "Kropki"
            if app.difficultyChosen!=None:
                startGame(app, app.difficultyChosen)
        if key=='i':
            resetVariations(app)
            if app.difficultyChosen==None:
                app.difficultyChosen ="medium"
            app.xSumsChosen = not app.xSumsChosen
            app.currentVariation = "xSums"
            if app.difficultyChosen!=None:
                startGame(app, app.difficultyChosen)
        if key=='n' or key =='N':
            resetVariations(app)
            if app.difficultyChosen ==None:
                app.difficultyChosen = "medium"
            startGame(app, app.difficultyChosen)
        if not app.manualMode and not app.wordokuEnterValueMode:
            if key in 'emhxv':
                app.tryingToClickManualMode = False
            if key=='e':
                app.difficultyChosen = 'easy'
                startGame(app, app.difficultyChosen)
            elif key=='m':
                app.difficultyChosen = 'medium'
                startGame(app, app.difficultyChosen)
            elif key=='h':
                app.difficultyChosen = 'hard'
                startGame(app, app.difficultyChosen)
            elif key=='x':
                app.difficultyChosen = 'expert'
                startGame(app, app.difficultyChosen)
            elif key=='v':
                app.difficultyChosen = 'evil'
                startGame(app, app.difficultyChosen)
    if app.board!=None:
        if key == 'left':    moveSelection(app, 0, -1)
        elif key == 'right': moveSelection(app, 0, +1)
        elif key == 'up':    moveSelection(app ,-1, 0)
        elif key == 'down':  moveSelection(app, +1, 0)
def resetVariations(app):
    app.wordokuChosen = False
    app.mathdokuChosen = False
    app.kropkiChosen =False
    app.sumdokuChosen = False
    app.multiplicationdokuChosen = False
    app.xSumsChosen=False
    app.currentVariation=None
def playMove(app, key):
    app.displayWrongBoardError=False
    if not app.keyboardLegalMode:
        app.showSingletonErrorMessage = False
        app.makeLegalBoardErrorMessage = False
        row, col = app.cellSelected
        if str(app.initialBoard[row][col]) not in '123456789':
            previousValue =app.board[row][col]

            app.board[row][col] = int(key)
            updateLegals(app)
            if (row, col) == app.hint1Cell:
                app.hint1Cell = None
            if app.hint2Cells!=None and (row, col) in app.hint2Cells:
                app.hint2Cells = None
            val = int(key)
            addMovesToUndo(app, row, col, val)
            if app.boardState!=None:
                app.boardState.set(row, col, val)
                if val==app.solutionBoard[row][col]:
                    app.incorrectValuesOrLegals[row][col]=False
                elif val!=app.solutionBoard[row][col]:
                    app.incorrectValuesOrLegals[row][col]=True
                    if app.competitionMode:
                        setActiveScreen('gameLostScreen')
    #add legals in keyboardLegalMode
    if not app.automaticLegalMode and app.keyboardLegalMode:
        if app.highlightedLegal!=None: 
            row, col, val = app.highlightedLegal
            if str(app.initialBoard[row][col]) not in '123456789':
                if val in app.selectedLegals[row][col]:
                    app.selectedLegals[row][col].remove(val)
                    if app.boardState!=None:
                        if val ==app.solutionBoard[row][col]:
                            app.incorrectValuesOrLegals[row][col]=True
                            if app.competitionMode:
                                setActiveScreen('gameLostScreen')
                else:
                    app.selectedLegals[row][col].add(val)
                    if val==app.solutionBoard[row][col]:
                        if app.boardState!=None:
                            app.incorrectValuesOrLegals[row][col]=False
def startManualBoard(app):
    tempSolved = solveSudoku(copy.deepcopy(app.manualBoard))
    if tempSolved==None:
        app.makeLegalBoardErrorMessage = True
        return
    app.initialBoard=copy.deepcopy(app.manualBoard)
    app.solutionBoard = tempSolved
    app.manualBoard.clear()
    app.board = copy.deepcopy(app.initialBoard)
    app.automaticLegalMode = True
    app.showSingletonErrorMessage =False
    app.automaticLegals = updateLegals(app)
    if app.boardState!=None:
        updateRedDotValues(app)
    app.cellSelected = (0, 0)
    clearSingletonList(app)
    app.manualMode = False
def startCancelManualBoard(app):
    app.manualBoard.clear()
    app.board = copy.deepcopy(app.tempBoard)
    app.tempBoard.clear()
    updateLegals(app)
    app.manualMode = False
def getWordokuLetters(app):
    wordokuLetters=[]
    for num in app.wordokuNumsToLetters:
        wordokuLetters.append(app.wordokuNumsToLetters[num])
    return wordokuLetters
def transformBoard(app):
    #Rotate by 90-270 degrees
    #Transformation 1
    randomNumOfRotations =random.randint(1, 3)
    for _ in range(randomNumOfRotations):
        app.board = rotate2dListClockwise(copy.deepcopy(app.board))
        app.initialBoard = rotate2dListClockwise(copy.deepcopy(app.initialBoard))
        if app.mathdokuChosen:
            app.mathdokuBoard=rotate2dListClockwise(copy.deepcopy(app.mathdokuBoard))
        if app.automaticLegalMode:
            app.automaticLegals = rotate2dListClockwise(copy.deepcopy(app.automaticLegals))
        elif not app.automaticLegalMode:
            app.selectedLegals = rotate2dListClockwise(copy.deepcopy(app.selectedLegals))
        if app.solutionBoard!=None:
            app.solutionBoard = rotate2dListClockwise(copy.deepcopy(app.solutionBoard))
    for flip in range(2):
        if flip==0: 
            app.board = flipHorizontally(copy.deepcopy(app.board))
            app.initialBoard = flipHorizontally(copy.deepcopy(app.initialBoard))
            if app.mathdokuChosen:
                app.mathdokuBoard=flipHorizontally(copy.deepcopy(app.mathdokuBoard))
            if app.automaticLegalMode:
                app.automaticLegals = flipHorizontally(copy.deepcopy(app.automaticLegals))
            elif not app.automaticLegalMode:
                app.selectedLegals = flipHorizontally(copy.deepcopy(app.selectedLegals))
            if app.solutionBoard!=None:
                app.solutionBoard = flipHorizontally(copy.deepcopy(app.solutionBoard))
        if flip==1: 
            app.board = flipVertically(copy.deepcopy(app.board))
            app.initialBoard = flipVertically(copy.deepcopy(app.initialBoard))
            if app.mathdokuChosen:
                app.mathdokuBoard=flipVertically(copy.deepcopy(app.mathdokuBoard))
            if app.automaticLegalMode:
                app.automaticLegals = flipVertically(copy.deepcopy(app.automaticLegals))
            elif not app.automaticLegalMode:
                app.selectedLegals = flipVertically(copy.deepcopy(app.selectedLegals))
            if app.solutionBoard!=None:
                app.solutionBoard = flipVertically(copy.deepcopy(app.solutionBoard))
    
    for flipDiagnoally in range(2):
        if flipDiagnoally==0: 
            app.board = flipDiagnoallyFromTopLeft(copy.deepcopy(app.board))
            app.initialBoard = flipDiagnoallyFromTopLeft(copy.deepcopy(app.initialBoard))
            if app.mathdokuChosen:
                app.mathdokuBoard=flipDiagnoallyFromTopLeft(copy.deepcopy(app.mathdokuBoard))
            if app.automaticLegalMode:
                app.automaticLegals = flipDiagnoallyFromTopLeft(copy.deepcopy(app.automaticLegals))
            elif not app.automaticLegalMode:
                app.selectedLegals = flipDiagnoallyFromTopLeft(copy.deepcopy(app.selectedLegals))
            if app.solutionBoard!=None:
                app.solutionBoard = flipDiagnoallyFromTopLeft(copy.deepcopy(app.solutionBoard))           
        if flipDiagnoally==1: 
            app.board = flipDiagnoallyFromTopRight(copy.deepcopy(app.board))
            app.initialBoard = flipDiagnoallyFromTopRight(copy.deepcopy(app.initialBoard))
            if app.mathdokuChosen:
                app.mathdokuBoard=flipDiagnoallyFromTopRight(copy.deepcopy(app.mathdokuBoard))
            if app.automaticLegalMode:
                app.automaticLegals = flipDiagnoallyFromTopRight(copy.deepcopy(app.automaticLegals))
            elif not app.automaticLegalMode:
                app.selectedLegals = flipDiagnoallyFromTopRight(copy.deepcopy(app.selectedLegals))
            if app.solutionBoard!=None:
                app.solutionBoard = flipDiagnoallyFromTopRight(copy.deepcopy(app.solutionBoard))

    #Relabel Digits
    for _ in range(9):
        relabelDigitsList = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        num1 = random.choice(relabelDigitsList)
        relabelDigitsList.remove(num1)
        num2=random.choice(relabelDigitsList)

        app.board = relabelDigits(copy.deepcopy(app.board), num1, num2)
        app.initialBoard = relabelDigits(copy.deepcopy(app.initialBoard), num1, num2)
        if app.mathdokuChosen:
            app.mathdokuBoard=relabelDigits(copy.deepcopy(app.mathdokuBoard), num1, num2)
        if app.automaticLegalMode:
            app.automaticLegals = relabelDigits(copy.deepcopy(app.automaticLegals), num1, num2)
        elif not app.automaticLegalMode:
            app.selectedLegals = relabelDigits(copy.deepcopy(app.selectedLegals), num1, num2)
        if app.solutionBoard!=None:
            app.solutionBoard = relabelDigits(copy.deepcopy(app.solutionBoard), num1, num2)  
    
    #Swap Columns
    randomNumOfColSwaps =random.randint(1, 3)         
    for _ in range(randomNumOfColSwaps):
        band = random.randint(0, 2)
        swapColDigits=[0, 1, 2]
        newCol0 = random.choice(swapColDigits)
        swapColDigits.remove(newCol0)
        newCol1 = random.choice(swapColDigits)
        swapColDigits.remove(newCol1)
        newCol2 = random.choice(swapColDigits)
        swapColDigits.remove(newCol2)

        app.board = permuteCols(copy.deepcopy(app.board), band, newCol0, newCol1, newCol2)
        app.initialBoard = permuteCols(copy.deepcopy(app.initialBoard), band, newCol0, newCol1, newCol2)
        if app.mathdokuChosen:
            app.mathdokuBoard=permuteCols(copy.deepcopy(app.mathdokuBoard), band, newCol0, newCol1, newCol2)
        if app.automaticLegalMode:
            app.automaticLegals = permuteCols(copy.deepcopy(app.automaticLegals), band, newCol0, newCol1, newCol2)
        elif not app.automaticLegalMode:
            app.selectedLegals = permuteCols(copy.deepcopy(app.selectedLegals), band, newCol0, newCol1, newCol2)
        if app.solutionBoard!=None:
            app.solutionBoard = permuteCols(copy.deepcopy(app.solutionBoard), band, newCol0, newCol1, newCol2)
    
    #Swap Rows
    randomNumOfRowSwaps =random.randint(1, 3)         
    for _ in range(randomNumOfRowSwaps):
        band = random.randint(0, 2)
        swapRowDigits=[0, 1, 2]
        newRow0 = random.choice(swapRowDigits)
        swapRowDigits.remove(newRow0)
        newRow1 = random.choice(swapRowDigits)
        swapRowDigits.remove(newRow1)
        newRow2 = random.choice(swapRowDigits)
        swapRowDigits.remove(newRow2)

        app.board = permuteRows(copy.deepcopy(app.board), band, newRow0, newRow1, newRow2)
        app.initialBoard = permuteRows(copy.deepcopy(app.initialBoard), band, newRow0, newRow1, newRow2)
        if app.mathdokuChosen:
            app.mathdokuBoard=permuteRows(copy.deepcopy(app.mathdokuBoard), band, newRow0, newRow1, newRow2)
        if app.automaticLegalMode:
            app.automaticLegals = permuteRows(copy.deepcopy(app.automaticLegals), band, newRow0, newRow1, newRow2)
        elif not app.automaticLegalMode:
            app.selectedLegals = permuteRows(copy.deepcopy(app.selectedLegals), band, newRow0, newRow1, newRow2)
        if app.solutionBoard!=None:
            app.solutionBoard = permuteRows(copy.deepcopy(app.solutionBoard), band, newRow0, newRow1, newRow2)    
    
    #Swap Stacks
    randomNumOfStackSwaps =random.randint(1, 3)         
    for _ in range(randomNumOfStackSwaps):
        swapStacksDigits=[0, 1, 2]
        newStack0 = random.choice(swapStacksDigits)
        swapStacksDigits.remove(newStack0)
        newStack1 = random.choice(swapStacksDigits)
        swapStacksDigits.remove(newStack1)
        newStack2 = random.choice(swapStacksDigits)
        swapStacksDigits.remove(newStack2)

        app.board = permuteStacks(copy.deepcopy(app.board), newStack0, newStack1, newStack2)
        app.initialBoard = permuteStacks(copy.deepcopy(app.initialBoard), newStack0, newStack1, newStack2)
        if app.mathdokuChosen:
            app.mathdokuBoard=permuteStacks(copy.deepcopy(app.mathdokuBoard), newStack0, newStack1, newStack2)
        if app.automaticLegalMode:
            app.automaticLegals = permuteStacks(copy.deepcopy(app.automaticLegals), newStack0, newStack1, newStack2)
        elif not app.automaticLegalMode:
            app.selectedLegals = permuteStacks(copy.deepcopy(app.selectedLegals), newStack0, newStack1, newStack2)
        if app.solutionBoard!=None:
            app.solutionBoard = permuteStacks(copy.deepcopy(app.solutionBoard), newStack0, newStack1, newStack2)
    
    #Swap Bands
    randomNumOfBandSwaps =random.randint(1, 3)         
    for _ in range(randomNumOfBandSwaps):
        swapBandsDigits=[0, 1, 2]
        newBand0 = random.choice(swapBandsDigits)
        swapBandsDigits.remove(newBand0)
        newBand1 = random.choice(swapBandsDigits)
        swapBandsDigits.remove(newBand1)
        newBand2 = random.choice(swapBandsDigits)
        swapBandsDigits.remove(newBand2)
        app.board = permuteBands(copy.deepcopy(app.board), newBand0, newBand1, newBand2)
        app.initialBoard = permuteBands(copy.deepcopy(app.initialBoard), newBand0, newBand1, newBand2)
        if app.mathdokuChosen:
            app.mathdokuBoard=permuteBands(copy.deepcopy(app.mathdokuBoard), newBand0, newBand1, newBand2)
        if app.automaticLegalMode:
            app.automaticLegals = permuteBands(copy.deepcopy(app.automaticLegals), newBand0, newBand1, newBand2)
        elif not app.automaticLegalMode:
            app.selectedLegals = permuteBands(copy.deepcopy(app.selectedLegals), newBand0, newBand1, newBand2)
        if app.solutionBoard!=None:
            app.solutionBoard = permuteBands(copy.deepcopy(app.solutionBoard), newBand0, newBand1, newBand2)

    #After Transformations
    if app.kropkiChosen:
        setupKropki(app)
    if app.mathdokuChosen:
        app.mathdokuAreasToColors=assignColors(app, app.mathdokuBoard)
        app.mathdokuNumsAndValues = getNumsAndValues(app, app.mathdokuBoard)
        app.mathdokuValuesToLocations = getValuesAndLocations(app, app.mathdokuBoard)
    if app.automaticLegalMode:
        app.automaticLegals = updateLegals(app)
    elif not app.automaticLegalMode:
        app.selectedLegals =makeEmptyLegalsList(app)
    updateRedDotValues(app)
def rotate2dListClockwise(board):
    oldRows, oldCols = len(board), len(board[0])
    newRows, newCols=oldCols, oldRows
    newBoard=[[None]*newCols for col in range(newRows)]
    
    for oldRow in range(oldRows):
        for oldCol in range(oldCols):
            newRow=oldCol
            newCol=newCols-1-oldRow
            newBoard[newRow][newCol]=board[oldRow][oldCol]
    return newBoard
def flipHorizontally(L):
    rows, cols = len(L), len(L[0])
    
    M=[[None]*cols for col in range(rows)]
    
    for row in range(rows):
        for col in range(cols):
            newCol = cols-(col+1)
            M[row][newCol]=L[row][col]
    return M
def flipVertically(L):
    rows, cols = len(L), len(L[0])
    
    M=[[None]*cols for col in range(rows)]
    
    for row in range(rows):
        for col in range(cols):
            newRow = rows-(row+1)
            M[newRow][col]=L[row][col]
    return M
def flipDiagnoallyFromTopLeft(L):
    rows, cols = len(L), len(L[0])
    
    M=[[None]*cols for col in range(rows)]
    L=rotate2dListClockwise(L)
    M=flipVertically(L)
    return M
def flipDiagnoallyFromTopRight(L):
    rows, cols = len(L), len(L[0])

    M=[[None]*cols for col in range(rows)]
    L=rotate2dListClockwise(L)
    M=flipHorizontally(L)
    return M
def relabelDigits(L, num1, num2):
    rows, cols = len(L), len(L[0])

    newBoard=[[None]*cols for col in range(rows)]
    for row in range(rows):
        for col in range(cols):
            if L[row][col]==num1:
                newBoard[row][col]=num2
            elif L[row][col]==num2:
                newBoard[row][col]=num1
            else:
                newBoard[row][col]=L[row][col]
    return newBoard
def permuteCols(L, band, newCol0, newCol1, newCol2):
    rows, cols = len(L), len(L[0])
    startCol = band*3

    newBoard=[[None]*cols for col in range(rows)]
    for row in range(rows):
        for col in range(cols):
            if col==startCol: newCol=newCol0+startCol
            elif col==startCol+1: newCol=newCol1+startCol
            elif col==startCol+2: newCol=newCol2+startCol
            else: newCol=col
            newBoard[row][newCol]=L[row][col]
    return newBoard
def permuteRows(L, band, newRow0, newRow1, newRow2):
    rows, cols = len(L), len(L[0])

    newBoard=[[None]*cols for col in range(rows)]
    startRow = band*3

    for row in range(rows):
        for col in range(cols):
            if row==startRow: newRow=newRow0+startRow
            elif row==startRow+1: newRow=newRow1+startRow
            elif row==startRow+2: newRow=newRow2+startRow
            else: newRow=row
            newBoard[newRow][col]=L[row][col]
    return newBoard
def permuteStacks(L, newStack0, newStack1, newStack2):
    rows, cols = len(L), len(L[0])
    newBoard=[[None]*cols for col in range(rows)]
    
    for row in range(rows):
        for col in range(cols):
            if 0<=row<=2: newRow=newStack0*3+(row-0)
            elif 3<=row<=5: newRow=newStack1*3+(row-3)
            elif 6<=row<=8: newRow=newStack2*3+(row-6)
            newBoard[newRow][col]=L[row][col]
    return newBoard
def permuteBands(L, newBand0, newBand1, newBand2):
    rows, cols = len(L), len(L[0])

    newBoard=[[None]*cols for col in range(rows)]
    
    for row in range(rows):
        for col in range(cols):
            if 0<=col<=2: newCol=newBand0*3+(col-0)
            elif 3<=col<=5: newCol=newBand1*3+(col-3)
            elif 6<=col<=8: newCol=newBand2*3+(col-6)
            newBoard[row][newCol]=L[row][col]
    return newBoard
def generateRandomBoard(app, difficulty):
    app.randomBoard = [[0]*app.cols for row in range(app.rows)]
    for boxNum in range(3):
        randomNumsInBox = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        for row in range(boxNum*3, boxNum*3+3):
            for col in range((row//3)*3, (row//3)*3+3):
                num =random.choice(randomNumsInBox)
                randomNumsInBox.remove(num)
                app.randomBoard[row][col]=num
    solutionForRandomBoard = solveSudoku(app.randomBoard)

    eliminationNumber=0
    if difficulty=='easy': eliminationNumber = random.randint(40, 43)
    elif difficulty=='medium': eliminationNumber = random.randint(44, 47)
    elif difficulty=='hard': eliminationNumber = random.randint(48, 50)
    elif difficulty=='expert': eliminationNumber = random.randint(51, 54)
    elif difficulty=='evil': eliminationNumber = random.randint(55, 58)
    app.randomBoard = eliminateRandomCells(copy.deepcopy(solutionForRandomBoard), eliminationNumber)
    # while len(solutions)>1:
    #     app.randomBoard = giveRandomSquare(copy.deepcopy(app.randomBoard), solutionForRandomBoard)
    #     solutions = solveRandomSudoku(app.randomBoard)
    previousRandomBoard = copy.deepcopy(app.randomBoard)
    
    protectedCells = [] #row, col
    app.randomBoard = giveRandomSquare(copy.deepcopy(app.randomBoard), solutionForRandomBoard)
    solutions = solveSudoku(app.randomBoard)
    while solutionForRandomBoard!=solutions:
        #previousRandomBoard
        (row, col, value) = findFirstDifferentiation(app, solutionForRandomBoard, solutions)
        protectedCells.append((row, col))
        app.randomBoard[row][col]=value
        solutions = solveSudoku(app.randomBoard)

    startRandomGame(app, difficulty, solutionForRandomBoard)
    if app.automaticLegalMode:
        app.automaticLegals = updateLegals(app)
    elif not app.automaticLegalMode:
        app.selectedLegals =makeEmptyLegalsList(app)
    updateRedDotValues(app)
def giveRandomSquare(board, solutionForRandomBoard):
    allPossibleSquares = [n for n in range(81)]
    for _ in range(2):
        randomSquare = random.choice(allPossibleSquares)
        row, col = (randomSquare)//9, (randomSquare%9)
        if str(board[row][col])==0:
            board[row][col]=solutionForRandomBoard[row][col]
            allPossibleSquares.remove(randomSquare)
    return board
def eliminateRandomCells(board, eliminationNumber):
    allPossibleSquares = [n for n in range(81)]
    while eliminationNumber>0:
        randomSquare = random.choice(allPossibleSquares)
        row, col = (randomSquare)//9, (randomSquare%9)
        if str(board[row][col]) in '123456789':
            board[row][col]=0
            eliminationNumber-=1
            allPossibleSquares.remove(randomSquare)
    return board
def findFirstDifferentiation(app, solutionForRandomBoard, solutions):
    rows, cols = len(solutionForRandomBoard), len(solutionForRandomBoard[0])
    for row in range(rows):
        for col in range(cols):
            if solutionForRandomBoard[row][col]!=solutions[row][col]:
                return (row, col, solutionForRandomBoard[row][col])
    #Should never happened
    return None
def startRandomGame(app, difficulty, solutionForRandomBoard):
    app.difficultyChosen = difficulty
    app.automaticLegalMode = True if app.difficultyChosen in ['easy'] else False
    app.initialBoard = app.randomBoard
    app.board = copy.deepcopy(app.initialBoard)
    app.solutionBoard = solutionForRandomBoard

    if app.wordokuChosen:
        setupWordoku(app)
    if app.mathdokuChosen:
        setupMathdoku(app)
    if app.kropkiChosen:
        setupKropki(app)
    if app.xSumsChosen:
        setupXSums(app)
    app.showSingletonErrorMessage =False
    app.makeLegalBoardErrorMessage = False
    clearSingletonList(app)
    app.cellSelected = (0, 0)
    app.hint1Cell, app.hint2Cells = None, None
    updateLegals(app)
def getCell(app, x, y):
    dx = x - app.boardLeft
    dy = y - app.boardTop
    cellWidth, cellHeight = getCellSize(app)
    row = math.floor(dy / cellHeight)
    col = math.floor(dx / cellWidth)
    if (0 <= row < app.rows) and (0 <= col < app.cols):
        return (row, col)
    else:
        return None
def moveSelection(app, drow, dcol):
    if app.cellSelected != None:
        selectedRow, selectedCol = app.cellSelected
        newSelectedRow = (selectedRow + drow)
        newSelectedCol = (selectedCol + dcol)
        if newSelectedRow<0: newSelectedRow+=1
        if newSelectedRow>=app.rows: newSelectedRow-=1
        if newSelectedCol<0: newSelectedCol+=1
        if newSelectedCol>=app.cols: newSelectedCol-=1
        app.cellSelected = (newSelectedRow, newSelectedCol)
def makeBoard(app, content):
    L = [[0]*app.cols for row in range(app.rows)] #This is making your board
    numValue=0
    for v in content:
        if v in "123456789":
            row, col = numValue//9, numValue%9
            L[row][col] = int(v)
        if v in "0123456789":
            numValue+=1
    return L
def makeEmptyLegalsList(app):
    M=[set(), set(), set(),set(),set(),set(),set(),set(),set()]
    L=[]
    for i in range(1, 10):
        L=L+copy.deepcopy([copy.deepcopy(M)])
    return L
def makeLegalsList(app):
    M=[set(), set(), set(),set(),set(),set(),set(),set(),set()]
    for s in M:
        for n in range(1, 10):
            s.add(n)
    L=[]
    for _ in range(1, 10):
        L=L+copy.deepcopy([copy.deepcopy(M)])
    return L
def drawHelpButton(app):
    drawRect(1350, 20, 50, 50, fill=None, border='Black')
    drawLabel("Help(Z)", 1375, 45, fill="red")
def drawVariationRulesButton(app):
    drawRect(1030, 20, 100, 50, fill=None, border='Black')
    drawLabel("Variation", 1080, 38, fill="red")
    drawLabel("Rules(b)", 1080, 52, fill="red")
def withinVariationRulesButton(app, x, y):
    if 1030<=x<=1130 and 20<=y<=70:
        return True
    return False
def drawToggleAutomaticLegals(app):
    drawRect(75, 275, 200, 50, fill=None, border='Black')
    drawLabel("Toggle Automatic Legals", 175, 300, fill="green", bold = True)
def drawChooseVariationButton(app):
    drawRect(75, 200, 250, 50, fill=gradient('snow', 'floralWhite', 'seashell', 'mintCream', 'honeydew', start="center"), border='Black')
    drawLabel("Choose Sudoku Variation!!", 200, 225, fill="royalBlue", bold = True)
def withinChooseVariationButton(app, x, y):
    if 75<=x<=325 and 200<=y<=250:
        return True
    return False
def withinHelp(app, x, y):
    if (1350<=x<=1400) and (20<=y<=70):
        return True
    return False
def withinToggleAutomaticLegals(app, x, y):
    if 75<=x<=275 and 275<=y<=325:
        return True
    return False
#Draw Bord, Boarder, Cell, getCellLeftTop, getCellSize are all from (with only slight modifications)
# https://cs3-112-f22.academy.cs.cmu.edu/notes/4187
def drawBoard(app):
    for row in range(app.rows):
        for col in range(app.cols):
            drawCell(app, row, col)
    #Draw lines in between blocks
    #Vertical Lines
    x1, y1, x2, y2 = app.boardLeft+app.boardWidth*(1/3), app.boardTop, app.boardLeft+app.boardWidth *(1/3), app.boardTop+app.boardHeight
    x3, y3, x4, y4 = app.boardLeft+app.boardWidth*(2/3), app.boardTop, app.boardLeft+app.boardWidth *(2/3), app.boardTop+app.boardHeight

    x5, y5, x6, y6 = app.boardLeft, app.boardTop + (1/3)*app.boardHeight, app.boardLeft + app.boardWidth, app.boardTop + (1/3) * app.boardHeight
    x7, y7, x8, y8 = app.boardLeft, app.boardTop + (2/3)*app.boardHeight, app.boardLeft + app.boardWidth, app.boardTop + (2/3) * app.boardHeight

    color="dimGray"
    width =6
    drawLine(x1, y1, x2, y2, fill=color, lineWidth =width, dashes=False)
    drawLine(x3, y3, x4, y4, fill=color, lineWidth =width, dashes=False)
    drawLine(x5, y5, x6, y6, fill=color, lineWidth =width, dashes=False)
    drawLine(x7, y7, x8, y8, fill=color, lineWidth =width, dashes=False)

    if app.mathdokuChosen:
        for value in app.mathdokuValuesToLocations:
            for location in app.mathdokuValuesToLocations[value]:
                (cx, cy) = location
                gradientColor=gradient('red', 'sienna', 'maroon')
                drawLabel(f"{value}", cx+4, cy+10, fill="red", bold=True, size = 14, align ="left")
    if app.kropkiChosen:
        drawKropkiCircles(app)
    if app.xSumsChosen:
        drawXSums(app)
def drawXSums(app):
    for (value, (cx, cy)) in app.xSumNumsAndLocations:
        drawLabel(f"{value}", cx, cy, fill="darkRed", size=25, bold=True)
def drawKropkiCircles(app):
    r=20
    cellWidth, cellHeight = getCellSize(app)
    for pair in app.kropkiBoard:
        ((row1, col1), (row2, col2), state)=pair
        if state=='empty':
            fillColor="White"
        elif state=='filled':
            fillColor="lightGray"
        if col2>col1:
            #draw horizontal pair
            cellLeft, cellTop = getCellLeftTop(app, row2, col2)
            drawCircle(cellLeft, cellTop+cellHeight/2, r, fill=fillColor, border="Black")
            if True:
                if app.solutionBoard[row1][col1]>app.solutionBoard[row2][col2]:
                    drawLine(cellLeft-r/2, cellTop+cellHeight/2, cellLeft+r, cellTop+cellHeight/2, arrowStart=True, arrowEnd=False, lineWidth=1)
                elif app.solutionBoard[row1][col1]<app.solutionBoard[row2][col2]:
                    drawLine(cellLeft-r, cellTop+cellHeight/2, cellLeft+r/2, cellTop+cellHeight/2, arrowStart=False, arrowEnd=True, lineWidth=1)
        if row1<row2:
            #draw vertical pair
            cellLeft, cellTop = getCellLeftTop(app, row2, col2)
            drawCircle(cellLeft+cellWidth/2, cellTop, r, fill=fillColor, border="Black")
            if True:
                if app.solutionBoard[row1][col1]>app.solutionBoard[row2][col2]:
                    drawLine(cellLeft+cellWidth/2, cellTop+r/2, cellLeft+cellWidth/2, cellTop-r, arrowStart=False, arrowEnd=True, lineWidth=1)
                elif app.solutionBoard[row1][col1]<app.solutionBoard[row2][col2]:
                    drawLine(cellLeft+cellWidth/2, cellTop+r, cellLeft+cellWidth/2, cellTop-r/2, arrowStart=True, arrowEnd=False, lineWidth=1)
def drawBoardBorder(app):
    drawRect(app.boardLeft, app.boardTop, app.boardWidth, app.boardHeight,
           fill=None, border='black', borderWidth=2*app.cellBorderWidth)
def drawCell(app, row, col):
    cellLeft, cellTop = getCellLeftTop(app, row, col)
    cellWidth, cellHeight = getCellSize(app)
    color=None
    opacityLevel=100
    if app.mathdokuChosen:
        value =app.mathdokuBoard[row][col]
        r, g, b = app.mathdokuAreasToColors[value]
        color = rgb(r, g, b)
        opacityLevel=50
        if app.mathdokuBoard[row][col]==app.mathdokuSelectedRegion:
            opacityLevel=100
    if (row, col) ==app.hint1Cell or (app.hint2Cells!=None and (row, col) in app.hint2Cells):
        color ='RED' 
    if (row, col) == app.cellSelected:
        color = 'Coral' 
    drawRect(cellLeft, cellTop, cellWidth, cellHeight,
             fill=color, border='black',
             borderWidth=app.cellBorderWidth, opacity=opacityLevel)
def getCellLeftTop(app, row, col):
    cellWidth, cellHeight = getCellSize(app)
    cellLeft = app.boardLeft + col * cellWidth
    cellTop = app.boardTop + row * cellHeight
    return (cellLeft, cellTop)
def getCellSize(app):
    cellWidth = app.boardWidth / app.cols
    cellHeight = app.boardHeight / app.rows
    return (cellWidth, cellHeight)
def makeBoardToContent(board):
    contentString = ""
    rows, cols = len(board), len(board[0])
    count=0
    for row in range(rows):
        for col in range(cols):
            if count==0:
                contentString = f"{contentString}{str(board[row][col])}"
            elif count%9==0:
                contentString = f"{contentString}\n{str(board[row][col])}"
            else:
                contentString = f"{contentString} {str(board[row][col])}"
            count+=1
    return contentString
def getFileContent(difficulty):
    fileNamesList = os.listdir('/Users/chrisbernitsas/Desktop/15-112 Term Project FINAL/boards')
    count=0
    while True:
        if count>(len(fileNamesList)):
            break
        filename =random.choice(fileNamesList)
        if filename.endswith('.txt') and filename.startswith(f'{difficulty}'):
            pathToFile = f'boards/{filename}'
            fileContents = readFile(pathToFile)
            app.contents = fileContents
            return fileContents
        count+=1
    return None
#Code from getCustomFileContent, readFile, and writeFile are heavily taken from: https://www.cs.cmu.edu/~112-3/notes/term-project.html
def getCustomFileContent(customName):
    customName =str(customName)
    fileNamesList = os.listdir('/Users/chrisbernitsas/Desktop/15-112 Term Project FINAL/boards')
    for fileIndex in range(len(fileNamesList)):
        filename =fileNamesList[fileIndex]
        if (filename.strip()==customName.strip()):
            pathToFile = f'boards/{filename}'
            fileContents = readFile(pathToFile)
            return fileContents
    return None           
def readFile(path):
    with open(path, "rt") as f:
        return f.read()
def writeFile(path, contents):
    with open(path, "wt") as f:
        f.write(contents)