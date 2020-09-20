#Elaborado por Alejandra María Flores Rodríguez.
#El siguiente juego consiste en que se tienen que encontrar la pareja de diversas figuras.
#Se mostrarán por unos determinados segundos las figuras, dependerá de la memoria de cada quien en encontrarlas todas. :)
#Espero se disfrute el juego.

import pygame
import random
import sys
from pygame.locals import*

FPS = 15 #Velocidad general del juego.
WINDOWWIDTH = 640 #Tamaño de la altura.
WINDOWHEIGHT = 480 
REVEALSPEED = 8 #velocidad de las cajas deslizándose.
BOXSIZE = 40 #Tamaño del cuadro, ancho y alto.
GAPSIZE = 10 #Espacio entre las cajas
BOARDWIDTH = 10 #Número de columnas
BOARDHEIGHT = 7 #Número de filas de los iconos
assert (BOARDWIDTH * BOARDHEIGHT) % 2==0, "El tablero debe tener un número variable de casillas para que los pares coincidan."
XMARGIN = int((WINDOWWIDTH - (BOARDWIDTH * (BOXSIZE + GAPSIZE))) / 2)
YMARGIN = int((WINDOWHEIGHT - (BOARDHEIGHT * (BOXSIZE + GAPSIZE))) / 2)

                                         
GRAY = (100, 100, 100)
NAVYBLUE = (60, 60, 100)
WHITE = (125, 25, 255)
RED   = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE  = (0, 0, 255)
YELLOW = (255, 255, 0)
ORANGE = (255, 128, 0)
PURPLE = (255, 0, 255)
CYAN = (0, 255, 255)

BGCOLOR= NAVYBLUE
LIGHTBGCOLOR = GRAY
BOXCOLOR = WHITE
HIGHLIGHTCOLOR = BLUE

DONUT = "dona"
SQUARE = "cuadrado"
DIAMOND = "diamante"
LINES = "lineas"
OVAL = "ovalo"

ALLCOLORS = (RED, GREEN, BLUE, YELLOW, ORANGE, PURPLE, CYAN)
ALLSHAPES = (DONUT, SQUARE, DIAMOND, LINES, OVAL)
assert len(ALLCOLORS) * len(ALLSHAPES) * 2 >= BOARDWIDTH * BOARDHEIGHT, "El tablero debe tener un número variable de casillas para que los pares coincidan."



def main():
    global FPSCLOCK, DISPLAYSURF
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF =pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT)) 
    mousex = 0#utilizado para almacenar la coordenada x
    mousey = 0#utilizado para almacenar la coordenada x
    pygame.display.set_caption("AF VideoGame")

    mainBoard = getRandomizedBoard()
    revealedBoxes = generateRevealedBoxesData(False)

    firstSelection = None #almacena el (x, y) del primer cuadro en el que se hizo clic.

    DISPLAYSURF.fill(BGCOLOR)
    startGameAnimation(mainBoard)





    while True: #Bucle principal del juego.
        mouseClicked = False

        DISPLAYSURF.fill(BGCOLOR)
        drawBoard(mainBoard, revealedBoxes)
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEMOTION:
                mousex, mousey = event.pos
            elif event.type == MOUSEBUTTONUP:
                mousex, mousey = event.pos
                mouseClicked = True    

        boxx, boxy = getBoxAtPixel(mousex, mousey)
        if boxx != None and boxy != None:
            #El mouse en la caja.
            if not revealedBoxes[boxx][boxy]:
                drawHighlightBox(boxx, boxy)
            if not revealedBoxes[boxx][boxy] and mouseClicked:
                revealBoxesAnimation(mainBoard, [(boxx, boxy)])
                revealedBoxes[boxx][boxy] = True #Como se revela la caja.
                if firstSelection == None: #La caja actual fué la primera.
                    firstSelection = (boxx, boxy)

                else: #el cuadro actual fue el segundo cuadro en el que se hizo clic.
                    icon1shape, icon1color = getShapeAndColor(mainBoard, firstSelection[0], firstSelection[1])
                    icon2shape, icon2color = getShapeAndColor(mainBoard, boxx, boxy)
                    if icon1shape != icon2shape or icon1color != icon2color:
                        #Los iconos no coinciden. Vuelva a cubrir ambas selecciones
                        pygame.time.wait(1000) #1000 milisegundos=1s
                        coverBoxesAnimation(mainBoard, [(firstSelection[0], firstSelection[1]), (boxx, boxy)])
                        revealedBoxes[firstSelection[0]][firstSelection[1]] = False
                        revealedBoxes[boxx][boxy] = False

                    elif hasWon(revealedBoxes): #Comprobación de que se encontraron todos los pares
                        gameWonAnimation(mainBoard)
                        pygame.time.wait(2000)

                        #Restablecimiento del tablero.
                        mainBoard = getRandomizedBoard()
                        revealedBoxea = generateRevealedBoxesData(False)

                        #Muestre0 del tablero completamente no revelado por un segundo.
                        drawBoard(mainBoard, revealedBoxes)
                        pygame.display.update()
                        pygame.time.wait(1000)

                        #Reproducción de la animación de inicio de juego.
                        startGameAnimation(mainBoard)
                    firstSelection = None #restablececimiento de la primera variable de selección.

        #vuelva a dibujar la pantalla y espere un tic del reloj.
        pygame.display.update()
        FPSCLOCK.tick(FPS)

def generateRevealedBoxesData(val):
    revealedBoxes = []
    for i in range(BOARDWIDTH):
        revealedBoxes.append([val] * BOARDHEIGHT)
    return revealedBoxes

def getRandomizedBoard():
    # Obtención de una lista de todas las formas posibles con todos los colores posibles.
    icons =[]
    for color in ALLCOLORS:
        for shape in ALLSHAPES:
            icons.append( (shape, color) )

    random.shuffle(icons) #Aleatorizar el orden de los iconos.
    numIconsUsed = int (BOARDWIDTH * BOARDHEIGHT / 2) # Calcula cuantos iconos se necesitan.
    icons = icons [:numIconsUsed] *2 #Hacer 2 de cada uno.
    random.shuffle(icons)

    #Crea la estructura de datos del tablero, con íconos colocados al azar.
    board=[]

    for x in range(BOARDWIDTH):
        column = []
        for y in range(BOARDHEIGHT):
            column.append(icons[0])
            del icons[0] #removes the icons as we assigned them
        board.append(column)
    return board

def splitIntoGroupsOf(groupSize, theList):
    # divide una lista en una lista de listas, donde las listas internas tienen en
    # número de elementos del tamaño de la mayoría del grupo.
    result = []
    for i in range(0, len(theList), groupSize):
        result.append(theList[i:i + groupSize])
    return result

def leftTopCoordsOfBox(boxx, boxy):
    #convierte las coordenadas de la placa a coordenadas de píxeles
    left = boxx *(BOXSIZE + GAPSIZE) + XMARGIN
    top = boxy * (BOXSIZE + GAPSIZE) + YMARGIN
    return (left, top) 

def getBoxAtPixel(x, y):
    for boxx in range(BOARDWIDTH):
        for boxy in range(BOARDHEIGHT):
            left, top = leftTopCoordsOfBox(boxx, boxy)
            boxRect = pygame.Rect(left, top, BOXSIZE, BOXSIZE)
            if boxRect.collidepoint(x, y):
                return (boxx, boxy)
    return (None, None)

def drawIcon(shape, color, boxx, boxy):
    quarter = int(BOXSIZE * 0.25)
    half = int(BOXSIZE * 0.5)

    left, top = leftTopCoordsOfBox(boxx, boxy) #obtiene coordenadas de los píxeles de los cables de la placa.
    #dibujar formas.
    if shape == DONUT:
        pygame.draw.circle(DISPLAYSURF, color, (left + half, top + half), half - 5)
        pygame.draw.circle(DISPLAYSURF, BGCOLOR, (left +half, top + half), quarter - 5)

    elif shape == SQUARE:
        pygame.draw.rect(DISPLAYSURF, color, (left + quarter, top + quarter, BOXSIZE - half, BOXSIZE -half))

    elif shape== DIAMOND:
        pygame.draw.polygon(DISPLAYSURF, color, ((left + half, top), (left + BOXSIZE - 1, top + half), (left + half, top + BOXSIZE - 1), (left, top + half)))

    elif shape == LINES:
        for i in range(0, BOXSIZE, 4):
            pygame.draw.line(DISPLAYSURF, color, (left, top+ i), (left + i, top))
            pygame.draw.line(DISPLAYSURF, color, ( left + i, top + BOXSIZE - 1), (left + BOXSIZE -1, top + i ))

    elif shape == OVAL:
        pygame.draw.ellipse(DISPLAYSURF, color, (left, top + quarter, BOXSIZE, half))

def getShapeAndColor( board, boxx, boxy):
    #valor de color para el punto x, y se almacena en el tablero.
    return board[boxx][boxy][0], board[boxx][boxy][1]

def drawBoxCovers(board, boxes, coverage):
    #dibuja cajas que se cubren y/o revelan.
    for box in boxes:
        left, top = leftTopCoordsOfBox(box[0], box[1])
        pygame.draw.rect(DISPLAYSURF, BGCOLOR, (left, top, BOXSIZE, BOXSIZE))
        shape, color = getShapeAndColor(board, box[0], box[1])
        drawIcon(shape, color, box[0], box[1])
        if coverage > 0: #dibuja la portada solo si hay cobertura.
            pygame.draw.rect(DISPLAYSURF, BOXCOLOR, (left, top, coverage, BOXSIZE))
    pygame.display.update()
    FPSCLOCK.tick(FPS)

def revealBoxesAnimation(board, boxesToReveal):
    for coverage in range(BOXSIZE, (-REVEALSPEED) -1, - REVEALSPEED):
        drawBoxCovers(board, boxesToReveal, coverage)

def coverBoxesAnimation(board, boxesToReveal):
    for coverage in range(0, BOXSIZE + REVEALSPEED, REVEALSPEED):
        drawBoxCovers(board, boxesToReveal, coverage)

def drawBoard(board, revealed):
    for boxx in range(BOARDWIDTH):
        for boxy in range(BOARDHEIGHT):
            left, top = leftTopCoordsOfBox(boxx, boxy)
            if not revealed[boxx][boxy]:
                #Dibuja una caja cubierta
                pygame.draw.rect(DISPLAYSURF, BOXCOLOR, (left, top, BOXSIZE, BOXSIZE))
            else:
                #Dibuja el ícono
                shape, color = getShapeAndColor(board, boxx, boxy)
                drawIcon(shape, color, boxx, boxy)

def drawHighlightBox(boxx, boxy):
    left, top = leftTopCoordsOfBox(boxx, boxy)
    pygame.draw.rect(DISPLAYSURF, HIGHLIGHTCOLOR, (left - 5, top - 5, BOXSIZE + 10, BOXSIZE + 10), 4)

def startGameAnimation(board):
    #Nuevas Cajas.
    coveredBoxes = generateRevealedBoxesData(False)
    boxes = []
    for x in range(BOARDWIDTH):
        for y in range(BOARDHEIGHT):
            boxes.append( (x, y) )
    random.shuffle(boxes)
    boxGroups = splitIntoGroupsOf(8, boxes)

    drawBoard(board, coveredBoxes)
    for boxGroup in boxGroups:
        revealBoxesAnimation(board, boxGroup)
        coverBoxesAnimation(board, boxGroup)

def gameWonAnimation(board):
    # Aquí parpadea el color de fondo cuando el jugador ha ganado.
    coveredBoxes = generateRevealedBoxesData(True)
    color1 = LIGHTBGCOLOR
    color2 = BGCOLOR

    for i in range (13):
        color1, color2= color2, color1 #Aquí se ntercambian colores.
        DISPLAYSURF.fill(color1)
        drawBoard(board, coveredBoxes)
        pygame.display.update()
        pygame.time.wait(300)

def hasWon(revealedBoxes):
    #Esto devuelve verdadero si se han revelado todas las casillas, de lo contrario es falso.
    for i in revealedBoxes:
        if False in i:
            return False #Devuelve false si alguna caja está abierta.
    return True

    font_path = "./fonts/newfont.ttf"
    font=pygame.font.Font(font_path, font_size)

if __name__== "__main__":
    main()