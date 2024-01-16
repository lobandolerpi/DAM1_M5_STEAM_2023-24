import random
from termcolor import colored
from collections import defaultdict
import f00_functions as f00

global VALID_PLAYS
VALID_PLAYS ='a1 a2 a3 b1 b2 b3 c1 c2 c3'
# La seguent variable és una llista de les 8 llistes de possible caselles guanyadores
VECTORS_WIN =[[(0, 0), (1, 1), (2, 2)],
                 [(0, 2), (1, 1), (2, 0)],
                 [(0, 0), (0, 1), (0, 2)],
                 [(1, 0), (1, 1), (1, 2)],
                 [(2, 0), (2, 1), (2, 2)],
                 [(0, 0), (1, 0), (2, 0)],
                 [(0, 1), (1, 1), (2, 1)],
                 [(0, 2), (1, 2), (2, 2)]]
# Això és per generar una IA molt cutre on anar sumant prioritats de jugada
global PRIORITY
PRIORITY =[0]*8

def printTile(tile, leftCha, rightCha):
    # Printa una casella amb els caràcters dels costats negres
    print(colored(leftCha,'black','on_white'), end="") # casella esquerra
    if tile == 1: # Si el contingut es un 1, una X verda
        print(colored("X",'green','on_white'), end="")
    elif tile == -1:  # Si el contingut es un 0, una O vermella
        print(colored("O",'red','on_white'), end="")
    elif tile == 0: # Si el contingut es un 0, un espai (casella buida)
        print(colored(" ",'red','on_white'), end="")
    else:
        print(colored(tile,'black','on_white'), end="")
    print(colored(rightCha,'black','on_white'), end="") # casella esquerra

def printBoard(logicBoard):
    # transformo el taulell de números a taulell de coses per printar
    # Llista de 4 Llistes [charLeft, charRight, string_abans_que_tauless, taulell_0, taulell_1, taulell_2 ] 
    # La 1 es la fila de dalt
    boardPrint = [[" "," ","   ","1","2","3"],[],[],[]] 
    # les altres 3 són combinació del taulell de números la lletra que indica la fila
    boardPrint[1] = ["[","]","a :"] + logicBoard[0]
    boardPrint[2] = ["[","]","b :"] + logicBoard[1]
    boardPrint[3] = ["[","]","c :"] + logicBoard[2]
    # Faig un loop per totes les files
    for iRow in range(len(boardPrint)):
        # Extrec els caracters charLeft i charRight
        leftCha = boardPrint[iRow][0]
        rightCha = boardPrint[iRow][1]
        # Printo l'string d'abans del tauler
        print(colored(boardPrint[iRow][2],'black','on_white'), end="")
        # Faig un loop per printar les 3 casellse de cada fila del tauler
        for iCol in range(3,6):
            tile = boardPrint[iRow][iCol]
            printTile(tile, leftCha, rightCha)
        print("") # I l'intro al final

def initBoard():
    # El taulell lògic es 3 x 3, i comença amb tot 0
    # quan jugui el jugador s'omplirà amb un 1
    # I quan jugui la CPU amb -1
    logicBoard=[[0,0,0],[0,0,0],[0,0,0]]
    return logicBoard

def playerPlays(logicBoard, ALREADY_PLAYED ):
    # Demana al jugador on vol jugar, comprova que es pot
    # i Actualitza el taulell lògic.
    playPlayer = f00.chooseLetterMsg('A quina casella vols jugar (De a1 fins c3 en minúscula)? :  ',
            ['len',2,'Longitud de l\'input incorrecta'],
            ['val',VALID_PLAYS,'Has de triar un valor NO JUGAT entre a1 a2 a3 b1 b2 b3 c1 c2 c3'],
            ['ivi',ALREADY_PLAYED,'Ja s\'ha jugat en aquesta casella'])
    # Transformo a índex
    row , col = tile2Pos(playPlayer)
    # Actualitzo valors
    ALREADY_PLAYED.append(playPlayer)
    print(ALREADY_PLAYED)
    logicBoard[row][col] = 1
    return logicBoard, ALREADY_PLAYED 

def tile2Pos(strTile):
    # Transforma la elecció de casella del jugador en index de la Llista de llistes
    let = strTile[0]
    if let == 'a': # Index en funció de la lletra
        row = 0
    elif let == 'b':
        row = 1
    else:
        row = 2
    column = int(strTile[1])-1 # la columna 1 és l'index 0, etc...
    return row, column

def updatePriority(logicBoard, VECTORS_WIN, PRIORITY):
    tie = True # Per defecte segueix l'empat
    # Actualitzo la prioritat
    for i_LT in range(8): # Loop per les 8 direccions de possible victoria
        listTuples = VECTORS_WIN[i_LT] # Extrect la llista de 3 caselles 
        v_n=[None]*3 # Creo un vector buit per les jugades
        for i in range(3): # omplo el vector amb les jugades
            row = listTuples[i][0]
            col = listTuples[i][1]
            v_n[i]=logicBoard[row][col]
        if abs(sum(v_n))==3: # si suma 3 o -3 hi ha un guanyador
            tie = False
            PRIORITY[i_LT] = -99999999
            #print("abs()=3") # per debug
        elif v_n[0] != 0 and v_n[1] != 0 and v_n[2] != 0:
            PRIORITY[i_LT] = -99999999 # Si no es pot jugar, ha de tenir la darrera prioritat o tinc un error
            #print("3 != 0 ands") # per debug
        elif sum(v_n) == -2: # Si suma -2 es que hi ha 2 fitxes de la CPU i una buida
            PRIORITY[i_LT] = 9999999 # Per tant jugant aquí la CPU guanya !!!
            #print("sum=-2") # per debug
        elif sum(v_n) == 2: # Si suma 2 es que hi ha 2 fitxes del jugador i una buida
            PRIORITY[i_LT] = PRIORITY[i_LT] + 10000 # He de jugar aquí perquè el jugador no guanyi
            #print("sum=2") # per debug
        elif 1 in v_n and -1 in v_n: # Si hi ha una de cada. Aquesta combinació no pot guanyat.
            PRIORITY[i_LT] = -100
            #print("1 y -1") # per debug
        elif 0 in v_n and sum(v_n)== 1: # Si només ha jugat el jugador. Jugant aquí previnc combos
            PRIORITY[i_LT] = PRIORITY[i_LT] + 20
            #print(" solo 1") # per debug
        elif 0 in v_n and sum(v_n)== -1: # Millor jugar on tinc fitxes que on no.
            PRIORITY[i_LT] = PRIORITY[i_LT] + 10
            #print(" solo -1") # per debug
    return PRIORITY, tie
        
def CPUPlays(logicBoard, VECTORS_WIN, PRIORITY, ALREADY_PLAYED ):
    # La jugada de la CPU
    maxPri=max(PRIORITY) # Busco el valor de màxima prioritat
    # i faig una llista de indexes on està aquest valor màxim
    indMax = [idx for idx, val in enumerate(PRIORITY) if val == maxPri]
    # genero un index aleatori per triar el valor dins de indMax
    indTmp=random.randint(0,len(indMax)-1)
    # i trio l'index entre els de màxima prioritat
    indVectorToPlay = indMax[indTmp]
    # amb l'index trio el vector on jugar
    vectorToPlay = VECTORS_WIN[indVectorToPlay]
    # Faig una llista amb les jugades i l'omplo
    v_n=[None]*3
    for i in range(3):
        row = vectorToPlay[i][0]
        col = vectorToPlay[i][1]
        v_n[i]=logicBoard[row][col]
    # com només puc jugar a un zero, torno a fer la cerca dels indexos
    ind0 = [idx for idx, val in enumerate(v_n) if val == 0]
    indPlay=random.randint(0,len(ind0)-1)
    indPlay=ind0[indPlay]
    CPUPlayTuple = vectorToPlay[indPlay]
    # Ara juga la CPU
    logicBoard[CPUPlayTuple[0]][CPUPlayTuple[1]] = -1
    if CPUPlayTuple[0] == 0:
        let = 'a'
    elif CPUPlayTuple[0] == 1:
        let = 'b'
    else:
        let = 'c'
    ALREADY_PLAYED.append(let + str(CPUPlayTuple[1] + 1))
    print(ALREADY_PLAYED)
    return logicBoard, ALREADY_PLAYED  # I torna el taulell actualitzat

def start3EnRatlla():
    # Joc del 3 en Ratlla
    # Defineixo un nom provisional pel jugador,
    # Després quan vingui la versió 2.0 s'haureu de canviar com es defineix player
    player = "Jugador"
    # Variable a tornar per que el main general sàpiga que fer
    errorsInExecution = 0
    # Missatge Benviguda
    print('\n Benvingut ' + player + '!!! \n Juguem al 3 en ratlla')
    print('Comences posant una fitxa a una casella lliure del tauler')
    print('Després ho fa la CPU, i axí successivament')
    print('Guanya qui aconsegueixi tenir 3 fitxes alineades.')
    print('Si s\'acaben els moviments és un empat i es recomença')
    # Loop mentre hi hagi empat
    tie = True
    whoStarts = 0
    while tie:
        ALREADY_PLAYED =[]
        print(ALREADY_PLAYED)
        whoStarts = whoStarts+1
        PRIORITY =[0]*8
        # Inicialitzo la variable del tauler
        board = initBoard()
        for i in range(9): # Loop pels 9 turns de joc
            printBoard(board) # començo el torn dibuixant el tauler.
            print("")
            print(colored("========== TORN " + str(i+1)+ " ==========",'blue'))
            if (whoStarts+i)%2 == 1: # "supra-torn" senar, torn del jugador
                board, ALREADY_PLAYED  = playerPlays(board, ALREADY_PLAYED )
            else: # "supra-torn" parell, torn de la CPU
                board, ALREADY_PLAYED  =CPUPlays(board, VECTORS_WIN, PRIORITY, ALREADY_PLAYED )
                print("La CPU juga ...")
            # Analitzo el tauler per saber prioritats i si algú ha guanyat
            PRIORITY, tie = updatePriority(board, VECTORS_WIN, PRIORITY)
            if tie == False and (whoStarts+i)%2 == 1:
                winner = True # Ha guanyat el jugador
                break
            elif tie == False and (whoStarts+i)%2 == 0:
                winner = False # Ha guanyat la jugador
                break
        printBoard(board)
        if tie:
            print("EMPAT !!!!")
            input('Pitja Enter per recomençar la partida...')
    f00.messageEnd(winner, player)
    return errorsInExecution
    # Quan vingui la versió 2.0 aquí haureu d'afegir més coses al return

# Aquesta línia és només per comprobar que el programa et funciona sense el main
# Ja per la versió 1.0 hauries de comentar-la i passar-la al codi principal d'alguna manera
#start3EnRatlla()