from cmu_graphics import *

from playScreen import *
from instructionsScreen import *

def startScreen_onScreenStart(app):
    pass
def startScreen_redrawAll(app):
    #From 15-112 Lecture 3 website: https://www.cs.cmu.edu/~112-3/index.html
    courseCoolDragonImage = 'https://www.cs.cmu.edu/~112-3/images/112-dragon.png'
    #From 15-112 LEcture 3 Website: https://www.cs.cmu.edu/~112-3/staff.html
    staffImage = 'https://i.ibb.co/9yNJ9Gn/staff-fence.jpg'
    drawImage(staffImage, 0, 0)
    drawImage(courseCoolDragonImage, 0, 545)
    drawRect(app.width/2-100, app.height/2+150, 200, 200, fill="white", border="Black")
    drawLabel("Press here or 'P' to start SUDOKU!", app.width/2, app.height/2+250)
    drawLabel("S  U  D  O  K  U!!!", app.width/2, 50, fill=gradient("darkRed", "orangeRed", "Gold", "limeGreen", "blue", "darkMagenta", "deepPink", start="left"), size=80, bold=True)

    drawRect(1000, 600, 100, 100, fill="white", border = "Black")
    drawLabel("Instrustions (I)", 1050, 650, size = 14)

def withinInstructionsButton(app, x, y):
    if 1000<=x<=1100 and 600<=y<=700:
        return True
    return False
   
def withinStart(app, x, y):
    if ((app.width/2-100)<=x<=(app.width/2+100) and (app.height/2+150)<=y<=(app.height/2+350)):
        return True
    return False
def startScreen_onMousePress(app, mouseX, mouseY):
    if withinStart(app, mouseX, mouseY):
        setActiveScreen('playScreen')
    if withinInstructionsButton(app, mouseX, mouseY):
        setActiveScreen('instructionsScreen')
def startScreen_onKeyPress(app, key):
    if key=='p' or key=='P':
        setActiveScreen('playScreen')
    if key=='i' or key=='I':
        setActiveScreen('instructionsScreen')