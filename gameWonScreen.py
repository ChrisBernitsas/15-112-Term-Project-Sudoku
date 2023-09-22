from cmu_graphics import *

from startScreen import *
from playScreen import *

def gameWonScreen_onScreenStart(app):
    pass
def gameWonScreen_redrawAll(app):
    drawRect(0, 0, app.width, app.height, fill="lightGreen")
    drawRect(1000, 200, 100, 100, fill=None, border = "Black")
    drawLabel("Return (R)", 1050, 250, size = 20)

    drawLabel("YOU WON!! Very Very Smart!", app.width/2, app.height/2, size=25)

def withinReturnButton(app, x, y):
    if 1000<=x<=1100 and 200<=y<=300:
        return True
    return False

def gameWonScreen_onMousePress(app, mouseX, mouseY):
    if withinReturnButton(app, mouseX, mouseY):
        reset(app)
        setActiveScreen('playScreen')

def gameWonScreen_onKeyPress(app, key):
    # PLAYING AUDIO SOUNDS AREN'T WORKING BUT THEY ARE WORKING IN SANDBOX AAAAAAAAAAAAAH
    if key=='r' or key =='R':
        reset(app)
        setActiveScreen('playScreen')