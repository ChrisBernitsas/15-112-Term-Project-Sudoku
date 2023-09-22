from cmu_graphics import *

def instructionsScreen_onScreenStart(app):
    pass

def instructionsScreen_redrawAll(app):
    drawRect(1000, 200, 100, 100, fill=None, border = "Black")
    drawLabel("Return (R)", 1050, 250, size = 20)
    startInstructionsHeight = 270
    drawLabel("HOW TO PLAY: Sudoku!", app.width/2, startInstructionsHeight-30, size=24)
    drawLabel("Sudoku is a puzzle that is divided into 3 regions: columns, rows, and boxes", app.width/2, startInstructionsHeight+50, size=20)
    drawLabel("Your objective is to fill the entire board with numbers from 1 to 9", app.width/2, startInstructionsHeight+100, size=20)
    drawLabel("You cannot have more than one of a digit in any given row, column, or 3 by 3 box", app.width/2, startInstructionsHeight+150, size=20)
    drawLabel("If you successfully accomplish this, YOU WIN!", app.width/2, startInstructionsHeight+200, size=20)
    drawLabel("There are 5 levels of difficulty: Easy, Medium, Hard, Expert, Evil with progressing difficulty", app.width/2, startInstructionsHeight+250, size=20)
    drawLabel("Good luck! Press return to start/continue playing!", app.width/2, startInstructionsHeight+300, size=20)



def withinInstructionsButton(app, x, y):
    if 1000<=x<=1100 and 200<=y<=300:
        return True
    return False
def instructionsScreen_onMousePress(app, mouseX, mouseY):
    if withinInstructionsButton(app, mouseX, mouseY):
        setActiveScreen('startScreen')

def instructionsScreen_onKeyPress(app, key):
    if key=='r' or key =='R':
        setActiveScreen('startScreen')