from cmu_graphics import *

def helpScreen_onScreenStart(app):
    pass
def helpScreen_redrawAll(app):
    keyboardControlsHeight= 200
    drawLabel("HELP SCREEN", app.width/2, 100, size=24, bold=True)
    drawLabel("Keyboard Controls", app.width/2-app.width/4, keyboardControlsHeight, size=16)
    drawLabel("e: Generate an EASY board", app.width/2-app.width/4, keyboardControlsHeight+20, size=16)
    drawLabel("m: Generate a MEDIUM board", app.width/2-app.width/4, keyboardControlsHeight+50, size=16)
    drawLabel("h: Generate a HARD board", app.width/2-app.width/4, keyboardControlsHeight+80, size=16)
    drawLabel("x: Generate an EXPERT board", app.width/2-app.width/4, keyboardControlsHeight+110, size=16)
    drawLabel("v: Generate an EVIL board", app.width/2-app.width/4, keyboardControlsHeight+130, size=16)
    drawLabel("o: Cycle between showing all legal values", app.width/2-app.width/4, keyboardControlsHeight+180, size=16)
    drawLabel("and manually entering desired legal values", app.width/2-app.width/4, keyboardControlsHeight+200, size=16)
    drawLabel("←↑→ to move the celected cell", app.width/2-app.width/4, keyboardControlsHeight+230, size=16)
    drawLabel(" ↓", 263, keyboardControlsHeight+245, size=16)
    drawLabel("The numbers 1-9 will place a value in the selected square", app.width/2-app.width/4, keyboardControlsHeight+270, size=16)
    drawLabel("For medium and harder boards:", app.width/2-app.width/4, keyboardControlsHeight+300, size=16)
    drawLabel("Pressing s will play the next singleton", app.width/2-app.width/4, keyboardControlsHeight+320, size=16)
    drawLabel("Pressing S will play all of the next possible singletons", app.width/2-app.width/4, keyboardControlsHeight+350, size=16)
    drawLabel("Pressing l will toggle between entering legals and entering board values", app.width/2-app.width/4, keyboardControlsHeight+380, size=16)
    drawLabel("Finally, Pressing M (capital) will toggle manual mode where you can make your own boards!", app.width/2-app.width/4, keyboardControlsHeight+410, size=16)
    
    drawLabel("; or H Will give you a hint if there exists among singles, tuples, thruples, quadruplets, etc...", app.width/2+app.width/4, keyboardControlsHeight+20, size=16)
    drawLabel("p Will remove the current hint and you will no loner see it on the board", app.width/2+app.width/4, keyboardControlsHeight+50, size=16)
    drawLabel("t Will transform your current board to a board that looks completely different", app.width/2+app.width/4, keyboardControlsHeight+80, size=18)
    drawLabel("r Will generate a random board of the given difficulty and variation chosen", app.width/2+app.width/4, keyboardControlsHeight+110, size=18)
    drawLabel("[ Will undo your preious move", app.width/2+app.width/4, keyboardControlsHeight+140, size=18)
    drawLabel("] Will redo any undone moves", app.width/2+app.width/4, keyboardControlsHeight+170, size=18)
    drawLabel("The follow buttons will toggle VARIATIONS of Sudoku:", app.width/2+app.width/4, keyboardControlsHeight+240, size=18)
    drawLabel("w, generate Wordoku boards", app.width/2+app.width/4, keyboardControlsHeight+270, size=18)
    drawLabel("k, will open a prompt for Sumdoku (s) or Multiplicationdoku (m)", app.width/2+app.width/4, keyboardControlsHeight+300, size=18)
    drawLabel("j, will generate Kropki boards", app.width/2+app.width/4, keyboardControlsHeight+330, size=18)
    drawLabel("u, will allow you to enter values onto your Sudoku board", app.width/2+app.width/4, keyboardControlsHeight+360, size=18)
    drawLabel("with your keyboard while you are in Wordoku", app.width/2+app.width/4, keyboardControlsHeight+390, size=18)
    drawLabel("b or B will bring up the rules for the Sudoku Variations", app.width/2+app.width/4, keyboardControlsHeight+420, size=18)
    drawLabel("c will cancel the manual board and y will create the manual board", app.width/2+app.width/4, keyboardControlsHeight+450, size=18)

    drawReturnButton(app)

def drawReturnButton(app):
    drawRect(200, 200, 50, 50, fill=None, border='Black')
    drawLabel("Return (R)", 225, 225, fill="Green")

def withinReturn(app, x, y):
    if (200<=x<=250) and (200<=y<=250):
        return True
    return False
def helpScreen_onKeyPress(app, key):
    if key =='r' or key=='R':
        setActiveScreen('playScreen')
def helpScreen_onMousePress(app, mouseX, mouseY):
    if withinReturn(app, mouseX, mouseY):
        setActiveScreen('playScreen')