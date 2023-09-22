from cmu_graphics import *
from playScreen import *

def variationRulesScreen_onScreenStart(app):
    pass
def variationRulesScreen_redrawAll(app):
    startYValue = 100
    dy=40
    drawLabel("Rules of: WORDOKU!", app.width/4, startYValue, size=30, bold=True)
    drawLabel("In Wordoku, the numbers 1-9 are replaced with letters", app.width/4, startYValue+dy, size=20)
    drawLabel("The letters follow the same rules and properties as classical Sudoku", app.width/4, startYValue+dy*2, size=20)
    drawLabel("However, the unfamiliarity may provide a challenge!", app.width/4, startYValue+dy*3, size=20)
    drawLabel("Finally, once solved, a hidden 9 letter word", app.width/4, startYValue+dy*4, size=20)
    drawLabel("will appear in one of the columns or rows", app.width/4, startYValue+dy*5, size=20)
    drawLabel("Best of Luck!", app.width/4, startYValue+dy*6, size=20)

    secondStartYValue = startYValue+dy*5+130
    drawLabel("Rules of: Mathdoku", app.width/4, secondStartYValue, size=30, bold=True)
    drawLabel("In Mathdoku, colored regions are generated for you", app.width/4, secondStartYValue+dy, size=20)
    drawLabel("A number will be displayed on the top left of the regions", app.width/4, secondStartYValue+dy*2, size=20)
    drawLabel("This number indicates the total sum (if sumdoku chosen)", app.width/4, secondStartYValue+dy*3, size=20)
    drawLabel("or the total product (if multiplicationdoku chosen)", app.width/4, secondStartYValue+dy*4, size=20)
    drawLabel("The same rules apply as classical sudoku", app.width/4, secondStartYValue+dy*5, size=20)
    drawLabel("This variation is quite beautiful and colorful! Good Luck!", app.width/4, secondStartYValue+dy*6, size=20)

    drawLabel("Rules of: Kropki!", 3*app.width/4, startYValue, size=30, bold=True)
    drawLabel("In Kropki, no intiial values are given whatsoever (fun right)", 3*app.width/4, startYValue+dy, size=20)
    drawLabel("Gray circles and White circles are drawn with arrows inside of them", 3*app.width/4, startYValue+dy*2, size=20)
    drawLabel("Gray circles indicate that one cell is double the cell it is connected to", 3*app.width/4, startYValue+dy*3, size=20)
    drawLabel("White circles indicate that the cells are consecutive (E.X. (3 and 4) or (7 and 8)", 3*app.width/4, startYValue+dy*4, size=20)
    drawLabel("The direction of the arrow indicates which way the pairs are increasing.", 3*app.width/4, startYValue+dy*5, size=20)
    drawLabel("This variation provides some clever tricks and thought patterns. Do not give up!!", 3*app.width/4, startYValue+dy*6, size=20)
    drawLabel("Best of Luck!", 3*app.width/4, startYValue+dy*7, size=20)


    drawLabel("Rules of: xSums!", 3*app.width/4, secondStartYValue, size=30, bold=True)
    drawLabel("In xSum, 5 random columns and rows contian a number outside of the Sudoku", 3*app.width/4, secondStartYValue+dy, size=20)
    drawLabel("These numbers represent the sum of the first n elemnts in that row of columm", 3*app.width/4, secondStartYValue+dy*2, size=20)
    drawLabel("Where n represents the first element in that row or column", 3*app.width/4, secondStartYValue+dy*3, size=20)
    drawLabel("For example, if a row started with 3, the xSum number would be", 3*app.width/4, secondStartYValue+dy*4, size=20)
    drawLabel("the sum of the first 3 elements in that row (including 3)", 3*app.width/4, secondStartYValue+dy*5, size=20)
    drawLabel("It's a fun variation of Sudoku that allows for some fun deductions!", 3*app.width/4, secondStartYValue+dy*6, size=20)    
    drawLabel("Good luck! You got this!", 3*app.width/4, secondStartYValue+dy*7, size=20)
    drawReturnButton(app)

def drawReturnButton(app):
    drawRect(100, 50, 50, 50, fill=None, border='Black')
    drawLabel("Return", 125, 68, fill="Green")
    drawLabel("(R)", 125, 82, fill="Green")

def withinReturn(app, x, y):
    if (100<=x<=150) and (50<=y<=100):
        return True
    return False
def variationRulesScreen_onKeyPress(app, key):
    if key =='r' or key=='R':
        setActiveScreen('playScreen')
def variationRulesScreen_onMousePress(app, mouseX, mouseY):
    if withinReturn(app, mouseX, mouseY):
        setActiveScreen('playScreen')