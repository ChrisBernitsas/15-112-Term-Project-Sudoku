from cmu_graphics import *

from startScreen import *
from helpScreen import *
from solution import *
from State import *
from instructionsScreen import *
from gameWonScreen import *
from gameLostScreen import *
from playScreen import *
from chooseVariations import *

def main():
    runAppWithScreens(initialScreen = 'startScreen', width = 1425, height = 825)

main()

