from cmu_graphics import *

# from startScreen import *
from playScreen import *

def chooseVariations_onScreenStart(app):
    app.listOfVariations=["Wordoku", "SumDoku", "MultiplicationDoku", "Kropki", "xSums"]
    app.highlightedVariation =None
    app.listOfCoords=[]
def chooseVariations_redrawAll(app):
    count=0
    for variation in app.listOfVariations:
        color = "red" if count==app.highlightedVariation else "Black"
        fontSize = 45 if count==app.highlightedVariation else 35
        if count<3:
            xOffSet = 350*count
            yOffSet=0
        elif count>=3:
            xOffSet=150+350*(count-3)
            yOffSet=250
        drawRect(app.width/2-500+xOffSet, app.height/2-200+yOffSet, 300, 200, fill=None, border="Black")
        app.listOfCoords.append((app.width/2-500+xOffSet, app.height/2-200+yOffSet, app.width/2-500+xOffSet+300, app.height/2-200+yOffSet+200))
        drawLabel(f"{app.listOfVariations[count]} ({app.listOfVariations[count][0]})", app.width/2-500+xOffSet+150, app.height/2-200+100+yOffSet, fill=color, size=fontSize, bold=True)
        count+=1

def getVariationNum(app, x, y):
    count=0
    for coords in app.listOfCoords:
        x1, y1, x2, y2 = coords
        if x1<=x<=x2 and y1<=y<=y2:
            return count
        count+=1
    return None
    
def chooseVariations_onMouseMove(app, mouseX, mouseY):
    app.highlightedVariation = getVariationNum(app, mouseX, mouseY)
def chooseVariations_onMousePress(app, mouseX, mouseY):
    if app.difficultyChosen ==None:
        app.difficultyChosen='medium'

    if app.highlightedVariation==0: 
        resetVariations(app)
        app.wordokuChosen = True
        startGame(app, app.difficultyChosen)
        setActiveScreen('playScreen')
    elif app.highlightedVariation==1: 
        resetVariations(app)
        app.mathdokuChosen = True
        app.sumdokuChosen = True
        startGame(app, app.difficultyChosen)
        setActiveScreen('playScreen')
    elif app.highlightedVariation==2: 
        resetVariations(app)
        app.mathdokuChosen = True
        app.multiplicationdokuChosen = True
        startGame(app, app.difficultyChosen)
        setActiveScreen('playScreen')
    elif app.highlightedVariation==3: 
        resetVariations(app)
        app.kropkiChosen = True
        startGame(app, app.difficultyChosen)
        setActiveScreen('playScreen')
    elif app.highlightedVariation ==4:
        resetVariations(app)
        app.xSumsChosen = True
        startGame(app, app.difficultyChosen)
        setActiveScreen('playScreen')

def chooseVariations_onKeyPress(app, key):
    if app.difficultyChosen ==None:
        app.difficultyChosen='medium'
    if key in 'WSMKX': 
        key =key.lower()
        resetVariations(app)
    if key in 'wsmkx':
        resetVariations(app)
    if key=='w': 
        app.wordokuChosen = True
    elif key=='s': 
        app.mathdokuChosen = True
        app.sumdokuChosen = True
    elif key=='m': 
        app.mathdokuChosen = True
        app.multiplicationdokuChosen = True
    elif key=='k': 
        app.kropkiChosen = True
    elif key =='x':
        app.xSumsChosen = True
    if key in 'wsmkx':
        startGame(app, app.difficultyChosen)
        setActiveScreen('playScreen')