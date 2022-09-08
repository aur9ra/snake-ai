import time, random

WIDTH,HEIGHT = 500,500
gameWidth, gameHeight = 10,10
game = [[0 for x in range(gameWidth)] for y in range(gameHeight)]

#below in px
marginLeft, marginTop, marginBottom, marginRight = 50, 50, 50, 50
marginBetween = 5

#now to automatically make the cell positions and sizes
cellWidth = int((WIDTH - ((gameWidth-1)*marginBetween + marginLeft + marginRight))/gameWidth)
cellHeight = int((HEIGHT - ((gameHeight-1)*marginBetween + marginTop + marginBottom))/gameHeight)
positions = []
snakePosition = (())
snakeLength = 1
movesSinceExtent = 2
for i in range(gameHeight):
    for j in range(gameWidth):
        positions.append(((cellWidth*j)+marginLeft+(marginBetween*j),(cellHeight*i)+marginTop+(marginBetween*i)))

colors = {
    -1: (200,0,0),
    0: (100,100,200)
}


def showgame():
    for i in game:
        print(i)

def getRandomUnpopulatedCoordinates():
    x, y = random.randint(0,gameWidth-1), random.randint(0,gameHeight-1)
    while game[x][y] > 0:
        x, y = random.randint(0,gameWidth-1), random.randint(0,gameHeight-1)
    return((x,y))

def spawnApple():
    #defining apple, which will always be represented by -1
    x,y = getRandomUnpopulatedCoordinates()
    game[x][y] = -1

def initgame():
    global snakeLength, snakePosition
    # direction: 0 = north, 1 = east, 2 = south, 3 = west
    direction = 1
    snakeLength = 1

    for i in range(1,snakeLength+1):
        colors[i] = ((snakeLength/(i))*255),((snakeLength/(i))*255),((snakeLength/(i))*255)

    #defining start of snake
    x,y = getRandomUnpopulatedCoordinates()
    game[x][y] = snakeLength * 1
    snakePosition = ((x,y))

    spawnApple()



def movement(dir):
    global snakeLength, snakePosition, movesSinceExtent
    toCheckDirection = {
        0: ((snakePosition[0]-1,snakePosition[1])),
        1: ((snakePosition[0],snakePosition[1]+1)),
        2: ((snakePosition[0]+1,snakePosition[1])),
        3: ((snakePosition[0],snakePosition[1]-1))
    }

    #this mess of code checks if the snake is on one of the edges. if it is, it removes the snake's ability to look at a
    #nonexistent tile outside of the game (which would raise an error)
    adjacentAngleTile = dict()

    for i in toCheckDirection:
        if i % 2 == 0:
            diff = toCheckDirection[i][0] - snakePosition[0]
            if diff == -1 and not ((snakePosition[0] - 1) < 0):
                adjacentAngleTile[i] = toCheckDirection[i]
            elif (diff == 1 and not ((snakePosition[0] + 1) > gameWidth-1)):
                adjacentAngleTile[i] = toCheckDirection[i]
        elif i % 2 == 1:
            diff = toCheckDirection[i][1] - snakePosition[1]
            if (diff == -1 and not ((snakePosition[1] - 1) < 0)):
                adjacentAngleTile[i] = toCheckDirection[i]
            elif (diff == 1 and not ((snakePosition[1] + 1) > gameHeight-1)):
                adjacentAngleTile[i] = toCheckDirection[i]

    contractSnake, canMove, tileMoveTo, moveTo = True, False, 999, (-1,-1)
    if dir in adjacentAngleTile:
        moveTo = adjacentAngleTile[dir]
        tileMoveTo = game[moveTo[0]][moveTo[1]]
    canMove = False if (tileMoveTo > 1 or dir not in adjacentAngleTile) else True
    contractSnake = False if (tileMoveTo == -1) else True
    movesSinceExtent = 0 if not contractSnake else movesSinceExtent
    if canMove:
        snakePosition = moveTo

    if (not contractSnake) and canMove:
        updategame(0, True)
        snakeLength += 1
        game[moveTo[0]][moveTo[1]] = snakeLength
        spawnApple()
    elif canMove:
        game[moveTo[0]][moveTo[1]] = snakeLength + 1
        for i in range(gameWidth*gameHeight):
            currentRow, currentColumn = int(i/gameWidth), i % gameWidth
            if game[currentRow][currentColumn] > 0:
                game[currentRow][currentColumn] -= 1

#this function controls movement and updates the snake accordingly. right now, it runs whenever an arrow key is pressed, but soon it should run at a regular interval.

def updategame(dir, colorOnly):

    colors["hey"] = "hey"
    if not colorOnly:
        movement(dir)
    for i in range(1,snakeLength+2):
        if not i == snakeLength+1:
            colors[i] = (
            ((int(i/snakeLength) * 50) + 200),
            ((int(i/snakeLength) * 50) + 200),
            ((int(i/snakeLength) * 50) + 200)
            )
        else:
            colors[i] = (180,180,250)

initgame()

def on_key_down(key):

    if key == (keys.UP):
        movement(0)
    if key == (keys.RIGHT):
        movement(1)
    if key == (keys.DOWN):
        movement(2)
    if key == (keys.LEFT):
        movement(3)

def draw():
    screen.fill((0,0,50))
    for i in range(len(positions)):
        currentRow, currentColumn = int(i/gameWidth), i % gameWidth
        randShade = random.randint(-10,10)
        colors[0] = (100+randShade,100+randShade,100+randShade)
        colorToUse = colors.get(game[currentRow][currentColumn])

        if game[currentRow][currentColumn] > 1:
            print()
            print("Starting to color.")
            print("Using ",colorToUse," at (",currentRow,",",currentColumn,") for value",game[currentRow][currentColumn])
            print(colors)
            for j in colors:
                screen.draw.filled_rect(Rect(0,0,15,15),(colorToUse))
                print("In testing, ",colorToUse," was used successfully.")

        screen.draw.filled_rect(Rect(positions[i][0],positions[i][1],cellWidth,cellHeight),(colorToUse))
        if game[currentRow][currentColumn] > 1:
            print("Success.")
