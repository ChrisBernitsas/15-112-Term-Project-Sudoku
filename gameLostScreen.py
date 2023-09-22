from cmu_graphics import *

from startScreen import *
from playScreen import *

def gameLostScreen_onScreenStart(app):
    app.cx=1000

def gameLostScreen_redrawAll(app):
    drawRect(0, 0, app.width, app.height, fill="lightCoral")
    drawRect(app.cx, 200, 100, 100, fill=None, border = "Black")
    drawLabel("Return (R)", 1050, 250, size = 20)

    drawLabel("GAME OVER. You Lost!! Do better.", app.width/2, app.height/2, size=25)

def withinReturnButton(app, x, y):
    if 1000<=x<=1100 and 200<=y<=300:
        return True
    return False

def gameLostScreen_onMousePress(app, mouseX, mouseY):
    if withinReturnButton(app, mouseX, mouseY):
        reset(app)
        setActiveScreen('playScreen')

def gameLostScreen_onKeyPress(app, key):
    if key=='r' or key =='R':
        reset(app)
        setActiveScreen('playScreen')