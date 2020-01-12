import tkinter as tk
import random

WIDTH = 555
HEIGHT = 700
SIZE = 4
TILE_SIZE = 100
BIG_PADDING = 40
SMALL_PADDING = 15
FONT = 'Helvetica'

game_over = False
game_score = 0
best_score = 0 

bg_color = '#FAF8EF'
board_color = '#BBADA0'
tile_color = {0: '#CEBEB5', 2: '#EEE4DA', 4:'#ECE0C8', 8: '#F3B177', 16: '#EA8D52', 32:'#F57C5F', 64:'#E85939', 128:'#F2D86A',256:'#EFCE63',512:'#E5BE33', 1024:'#E3B71A', 2048:'#ECC400', 4096: '#64D792'}
dark_text_color = '#776E65'
light_text_color = '#F9F6F2'

#LET'S START
root = tk.Tk() #starts UI part
root.title('2048')

canvas = tk.Canvas(root, height = HEIGHT, width = WIDTH, bg = bg_color)
canvas.pack()

tk_bg = tk.Frame(root, bg = bg_color)
tk_bg.place(x = 0, y = 0, relwidth = 1, relheight = 1)

game_name = tk.Label(root, font = (FONT, 60, 'bold'), text='2048', bg = bg_color, fg = dark_text_color)
game_name.place(x = BIG_PADDING, y = 30, width = 200, height = 70)

#BEST SCORE
score_width = 100

tk_best_score = tk.Label(root, font = (FONT, 10), bg = tile_color[0])
tk_best_score.place(x = WIDTH - BIG_PADDING - score_width, y = 20, width = score_width, height = 55)

tk_best_scoreDesc = tk.Label(root, font = (FONT, 12, 'bold'), bg = tile_color[0], fg = light_text_color, text='BEST')
tk_best_scoreDesc.place(x = WIDTH - BIG_PADDING - score_width + 20, y = 28, width = 60, height = 12)

tk_best_scoreValue = tk.Label(root, font = (FONT, 18, 'bold'), bg = tile_color[0], fg = light_text_color, text='0')
tk_best_scoreValue.place(x = WIDTH - BIG_PADDING - score_width + 25, y = 45, width = 50, height = 22)

#CURRENT SCORE
tk_score = tk.Label(root, font = (FONT, 10), bg = tile_color[0], fg = dark_text_color)
tk_score.place(x = WIDTH - BIG_PADDING - score_width*2 -10 , y = 20, width = score_width, height = 55)

tk_scoreDesc = tk.Label(root, font = (FONT, 12, 'bold'), bg = tile_color[0], fg = light_text_color, text='SCORE')
tk_scoreDesc.place(x = WIDTH - BIG_PADDING - score_width*2 - 10 + 20, y = 28, width = 60, height = 12)

tk_scoreValue = tk.Label(root, font = (FONT, 18, 'bold'), bg = tile_color[0], fg = light_text_color, text='0')
tk_scoreValue.place(x = WIDTH - BIG_PADDING - score_width*2 -10 + 25, y = 45, width = 50, height = 22)

#GAME BOARD
frame = tk.Frame(root, bg = board_color, bd = 0, relief = 'solid')
frame.place(x = BIG_PADDING, y = HEIGHT - SIZE*TILE_SIZE -(SIZE+1)*SMALL_PADDING - BIG_PADDING, width = SIZE*TILE_SIZE + (SIZE+1)*SMALL_PADDING, height = SIZE*TILE_SIZE + (SIZE+1)*SMALL_PADDING)

#CREATE TILES
def createTile (a,b):
    tk_tile = tk.Label(frame, font = (FONT, 30, 'bold'), bg = tile_color[0], fg = dark_text_color)
    tk_tile.place(x =  SMALL_PADDING*(a+1) + TILE_SIZE*a, y = SMALL_PADDING*(b+1) + TILE_SIZE*b, width = TILE_SIZE, height = TILE_SIZE)
    return tk_tile

def updateTile(a,b,value):
    tile_dict[a,b]['bg'] = tile_color[value]

    if value != 0:
        tile_dict[a,b]['text'] = str(value)
    else:
        tile_dict[a,b]['text'] = ''
    
    if value <= 4:
        tile_dict[a,b]['fg'] = dark_text_color
    else:
        tile_dict[a,b]['fg'] = light_text_color

tile_dict = dict() #dictionary of all tiles

for a in range (0,SIZE):
    for b in range (0,SIZE):
        tile_dict[(a,b)] = createTile(a,b)

#LOAD BEST  SCORE
try:
    f = open('BestScore.txt','r')
    best_score = int(f.read())
    tk_best_scoreValue['text'] = str(best_score)
    f.close()
except:
    best_score = 0

def getScore():
    sum = 0
    for a in range (0,SIZE):
        for b in range (0,SIZE):
            text = tile_dict[a,b]['text']
            try:
                sum += int(tile_dict[a,b]['text'])
            except:
                pass

    return sum

#NEW GAME
def resetGame():
    global game_over

    game_over = False
    tk_game_over['text'] = ''

    for a in range (0,SIZE):
        for b in range (0,SIZE):
            updateTile(a,b,0)

    updateTile(0,0,16)
    updateTile(1,0,2)
    updateTile(2,0,2)
    updateTile(0,1,2)
    updateTile(2,2,2)
    tk_scoreValue['text'] = getScore()
    game_score = getScore()

tk_new_game = tk.Button(root, font = (FONT, 12, 'bold'), bg = '#8F7A66', fg = light_text_color, text='New Game', relief='flat', command=lambda: resetGame())
tk_new_game.place(x = WIDTH  - BIG_PADDING , y = 100, width = 180, height = 40, anchor = 'ne')

#GAME OVER
tk_game_over = tk.Label(root, font = (FONT, 20, 'bold'), bg = bg_color, fg = 'red', text='', )
tk_game_over.place(x = BIG_PADDING , y = 110, width = 180, height = 40,)

#GETTING THE GAME READY
def tileIsEmpty(a,b):
    if tile_dict[a,b]['text'] == '':
        return True
    return False

def getTileValue(a,b):
    if tile_dict[a,b]['text'] == '':
        return 0
    else:
        return int(tile_dict[a,b]['text'])

def saveBestScore(game_score):
    global best_score

    if game_score > best_score:
        tk_best_scoreValue['text'] = str(game_score)
        best_score = game_score
        f = open('BestScore.txt','w')
        f.write(str(game_score))
        f.close()


def sumColRows(direction):
    """ Sums columns or rows in one direction """
    if direction == 'left': 
        for b in range(0,SIZE):
            for a in range(0, SIZE):
                if tileIsEmpty(a,b) == False:
                    #look if there is a tile with the same value on the right
                    for c in range (a+1, SIZE):
                        if getTileValue(a,b) == getTileValue(c,b):
                            updateTile(a,b,getTileValue(a,b) + getTileValue(c,b))
                            updateTile(c,b,0)
                            break
                        else:
                            break

    elif direction == 'right':
        for b in range(0,SIZE):
            for a in range(SIZE-1,-1,-1):
                if tileIsEmpty(a,b) == False:
                    #look if there is a tile with the same value on the left
                    for c in range (a-1,-1,-1):
                        if getTileValue(a,b) == getTileValue(c,b):
                            updateTile(a,b,getTileValue(a,b) + getTileValue(c,b))
                            updateTile(c,b,0)
                            break
                        else:
                            break

    elif direction == 'up': 
        for a in range(0,SIZE):
            for b in range(0, SIZE):
                if tileIsEmpty(a,b) == False:
                    #look if there is a tile with the same value on down
                    for c in range (b+1, SIZE):
                        if getTileValue(a,b) == getTileValue(a,c):
                            updateTile(a,b,getTileValue(a,b) + getTileValue(a,c))
                            updateTile(a,c,0)
                            break
                        else:
                            break

                            
    elif direction == 'down':
        for a in range(0,SIZE):
            for b in range(SIZE-1,-1,-1):
                if tileIsEmpty(a,b) == False:
                    #look if there is a tile with the same value up
                    for c in range (b-1,-1,-1):
                        if getTileValue(a,b) == getTileValue(a,c):
                            updateTile(a,b,getTileValue(a,b) + getTileValue(a,c))
                            updateTile(a,c,0)
                            break
                        else:
                            break

def moveSumTiles(direction):
    """ Sums columns or rows in one direction & moves them in one direction """
    sumColRows(direction)
    #now move them
    if direction == 'left':       
        for b in range(0,SIZE):
            for a in range(0, SIZE):
                if tileIsEmpty(a,b):
                    #look right and see if there is something
                    for c in range (a+1, SIZE):
                        if  tileIsEmpty(c,b) == False:
                            updateTile(a,b,getTileValue(c,b))
                            updateTile(c,b,0)
                            break

    elif direction == 'right':
        for b in range(0,SIZE):
            for a in range(SIZE-1,-1,-1):
                if tileIsEmpty(a,b):
                    #look left and see if there is something
                    for c in range (a-1,-1,-1):
                        if  tileIsEmpty(c,b) == False:
                            updateTile(a,b,getTileValue(c,b))
                            updateTile(c,b,0)
                            break

    elif direction == 'up':       
        for a in range(0,SIZE):
            for b in range(0, SIZE):
                if tileIsEmpty(a,b):
                    #look down and see if there is something
                    for c in range (b+1, SIZE):
                        if  tileIsEmpty(a,c) == False:
                            updateTile(a,b,getTileValue(a,c))
                            updateTile(a,c,0)
                            break

    elif direction == 'down':
        for a in range(0,SIZE):
            for b in range(SIZE-1,-1,-1):
                if tileIsEmpty(a,b):
                    #look up and see if there is something
                    for c in range (b-1,-1,-1):
                        if  tileIsEmpty(a,c) == False:
                            updateTile(a,b,getTileValue(a,c))
                            updateTile(a,c,0)
                            break

def spawnRandomTile():
    global game_over

    empty_tiles = []
    for a in range(0,SIZE):
        for b in range(0,SIZE): 
            if tileIsEmpty(a,b):
                empty_tiles.append((a,b))
    if len(empty_tiles) == 0:
        game_over = True
        tk_game_over['text'] = 'GAME OVER!'
    else:
        choice = random.choice(empty_tiles)
        updateTile(choice[0],choice[1],2)

def keyActions(direction):
    if game_over == False:
        moveSumTiles(direction)
        tk_scoreValue['text'] = getScore()
        game_score = getScore()
        spawnRandomTile()
        saveBestScore(game_score)

def leftKey(event):
    keyActions('left')

def rightKey(event):
    keyActions('right')

def upKey(event):
    keyActions('up')

def downKey(event):
    keyActions('down')

resetGame()

root.bind('<Left>', leftKey)
root.bind('<Right>', rightKey)
root.bind('<Up>', upKey)
root.bind('<Down>', downKey)

root.mainloop() #ends UI part