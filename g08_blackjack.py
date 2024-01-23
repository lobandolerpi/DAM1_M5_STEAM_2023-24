"""Blackjack, by Al Sweigart al@inventwithpython.com
The classic card game also known as 21. (This version doesn't have
splitting or insurance.)
More info at: https://en.wikipedia.org/wiki/Blackjack
This code is available at https://nostarch.com/big-book-small-python-programming
Tags: large, game, card game

Edited by Pedro Bonilla for adaptation to jocs Calamot
Removed the betting aspect of the game (used for a school)"""

import random, sys
import f00_functions as f00
from termcolor import colored
import main_jocs as mj

# Aqui defineix el símbol dels 4 pals de la baralla:
SUIT_HEART = chr(9829) # Caracter 9829 és '♥'.
SUIT_DIAMO = chr(9830) # Caracter 9830 és '♦'.
SUIT_SPADE = chr(9824) # Caracter 9824 és '♠'.
SUIT_CLUBS = chr(9827) # Caracter 9827 és '♣'.
# (Per si voleu, una llista de codis de caràcters especials aquí https://inventwithpython.com/charactermap)
BACKSIDE = 'backside'

def getDeck():
    #Torna una llista de 52 cartes (tupples amb (num, pal)).
    deck = []
    # doble for, per pals (suits) i número (rank)
    for suit in (SUIT_HEART, SUIT_DIAMO, SUIT_SPADE, SUIT_CLUBS):
        for rank in range(2, 11):
            deck.append((str(rank), suit))  # Add the numbered cards.
        for rank in ('J', 'Q', 'K', 'A'):
            deck.append((rank, suit))  # Add the face and ace cards.
    # crida a la funció random.shuffle que desorganitza una llista a l'atzar.
    random.shuffle(deck)
    # Torna la baralla mesclada
    return deck


def displayHands(playerHand, dealerHand, showDealerHand):
    # Prepara la ma (totes les cartes) del jugador i la CPU
    # Oculta la 1a carta de la CPU si showDealerHand es False
    print()
    if showDealerHand:
        # Mostra la jugada de la CPU amb la suma getHandValue(dealerHand)
        print('CPU:', getHandValue(dealerHand))
        # I mostra tota la ma(jugada de la CPU) displayCards(dealerHand) 
        displayCards(dealerHand)
    else:
        # Mostra la jugada de la CPU amb interrogants 
        print('CPU: ???')
        # I mostra una carta boca abaix i ka ma de la CPU des de la posicio 1 (excloent la 0, que esta girada)
        displayCards([BACKSIDE] + dealerHand[1:])

    # Mostra la ma del jugador
    print('PLAYER:', getHandValue(playerHand))
    displayCards(playerHand)


def getHandValue(listCards):
    # Suma els calors de la llista de cartas.
    # Calcula si els asos va millor un 1 o un 11.
    # Inicialitzo variables
    value = 0
    numberOfAces = 0

    # Loop per cada carta de la llista
    for card in listCards:
        rank = card[0]  # El numero de la carta es la posicio 0 del tuple (la 1 es el pal)
        if rank == 'A':
            # si tinc un as, afegeixo per calcular que es millor
            numberOfAces += 1
        elif rank in ('K', 'Q', 'J'):  # si és una figura, el seu valor es deu
            value += 10
        else:
            value += int(rank)  # Si es un número, el seu valor es el numèric.

    # Afegeixo els calors dels assos al final
    value += numberOfAces  # Començo afegint 1
    for i in range(numberOfAces):
        # Mentre no em passi de 21, afegeixo 10 (perque l'as valgui 11)
        if value + 10 <= 21:
            value += 10

    return value


def displayCards(cards):
    # Printa cartesl a una llista de cartes rebuda
    rows = ['', '', '', '', '']  # Declara la llista.
    # per cada carta
    for i, card in enumerate(cards):
        rows[0] += colored(' ___  ','blue','on_white')  # Desa a la posició 0 de la llista la part de dalt de la carta.
        if card == BACKSIDE:
            # Si la carta es BACKSIDE (girada) desa a les files 1-3 el revers
            rows[1] += colored('|## | ','blue','on_white')
            rows[2] += colored('|###| ','blue','on_white')
            rows[3] += colored('|_##| ','blue','on_white')
        else:
            # Si la carta no es BAckside, desa a la llista els text formatat. 
            rank, suit = card  # Extreu del tuple de la varta les variables.
            if suit in [chr(9829), chr(9830)]:
                c = 'red'
            else:
                c = 'black'
            # com el número pot tenir 1 caràcter o 2, fa servir ljust(2) o rjust2
            # això el que fa és que justifica a esquerra o detra i omple primer amb valors
            # i després amb espais.
            rows[1] += colored('|{} | ','blue','on_white').format(rank.ljust(2)) # posa el número de la carta justificat a l'esquerra
            rows[2] += colored('| ','blue','on_white')+colored('{}',c,'on_white').format(suit)+ colored(' | ','blue','on_white') # posa el pal de la carta
            rows[3] += colored('|_{}| ','blue','on_white').format(rank.rjust(2, '_'))# posa el número de la carta justificat a la dreta

    # Printa la carta a la terminal:
    for row in rows:
        print(row)

# Demana al jugador si vol una altra carta o plantarse.
def getMove():
    while True:  # Loop infinit fins que el trenqui perque l'input es satisfactori
        moves = ['(C)arta', '(P)lantar-se']

        # Mostra el prompt 
        movePrompt = ', '.join(moves) + '> '
        # demana un input sense missatge i ho transforma a majúscules.
        move = input(movePrompt).upper()
        if move in ('C', 'P'):
            return move  # Si el moviment és vàlid surto de la funció

def playerTurn(playerHand, CPUHand):
    moreCardsAvailable = True
    # Mostro i sumo les cartes, la de la CPU boca abaix (False) 
    displayHands(playerHand, CPUHand, False)
    print()
    # Demano al jugador que vol fer
    move = getMove()
    if move in ('P'):
        # si es planta, indico que el loop pari
        moreCardsAvailable = False 
    elif move in ('C'):
        # Si el jugador demana carta l'agafo del deck
        newCard = deck.pop()
        rank, suit = newCard # Estrec número i pal
        print('La nova carta es un {} de {}.'.format(rank, suit))
        # La mostro i la afegeixo a la ma del jugador
        playerHand.append(newCard)
    playerTotal = getHandValue(playerHand)    
    if playerTotal > 21:
        # Comprobo si el jugador s'ha passat per parar
        moreCardsAvailable = False
    return moreCardsAvailable , playerTotal

def CPUTurn(playerHand, CPUHand):
    # La CPU juga fins que arriba a 17
    CPUTotal = getHandValue(CPUHand) 
    while CPUTotal < 17: 
        CPUHand.append(deck.pop())
        # Per mantenir el suspens anem mostrant les jugades 1 a 1 amb la 1 girada.
        displayHands(playerHand, CPUHand, False)
        input('Pitja Enter per continuar...')
        print('\n\n')
        CPUTotal = getHandValue(CPUHand)
    return CPUHand, CPUTotal

def startBlackjack(player):
    # Joc del BlackJack
    # Defineixo un nom provisional pel jugador,
    # Després quan vingui la versió 2.0 s'haureu de canviar com es defineix player
    # Variable a tornar per que el main general sàpiga que fer
    errorsInExecution = 0
    # Missatge Benviguda
    print(' Benvingut ' + player + '!!! \n Juguem a :')
    print('''Blackjack, by Al Sweigart al@inventwithpython.com
    Edited for jocs Calamot by Pedro Bonilla

    NORMES:
      Intenta arribar el més a prop de 21 sense passar-te.
      K (reis), Q (reines), i J (caballers) valen 10.
      A (assos) poedne valdre 1 o 11 el més convenient. 
      La resta de cartas val el seu valor numéric. 
      (C)arta per demanar una altra carta.(P)lantar-se per plantarse.
      La CPU para a 17 per defecte.''')
    # Entro al loop fin que no hi hagi un empat
    tie = True
    while tie:
        # Genero una baralla que ja esta mesclada i el faig global, pq totes les funcions el vegin
        global deck
        deck = getDeck()
        # Genero la ma del jugador treient 2 vegades la darrera carta de la llista de la baralla
        # llista.pop() extreu el darrer item de la llista. Es pot indicar una posició llista.pop(5) 
        CPUHand = [deck.pop(), deck.pop()]
        # Faig el mateix amb el jugador.
        playerHand = [deck.pop(), deck.pop()]

        moreCardsAvailable = True
        while moreCardsAvailable: 
            # Mentre el jugador no es planti o es passi, cal una nova tria del jugador
            moreCardsAvailable , playerTotal = playerTurn(playerHand, CPUHand) 
        # Si el jugador no s'ha passat juga la CPU, pero necessito el valor
        if playerTotal  <= 21: 
            CPUHand , CPUTotal = CPUTurn(playerHand, CPUHand)
        else:
            CPUTotal = getHandValue(CPUHand)
    
        # El JOC ha acabat, mostrem totes les cartes:
        displayHands(playerHand, CPUHand, True)

        if CPUTotal > 21:
            print('La CPU s\'ha passat.')
            winner = True
            tie = False
        elif playerTotal > 21:
            print('T\'has passat')
            winner = False
            tie = False
        elif playerTotal < CPUTotal:
            print('La jugada de la CPU és millor que la teva')
            winner = False
            tie = False
        elif playerTotal > CPUTotal:
            print('La teva jugada de és millor que la de la CPU')
            winner = True
            tie = False
        elif playerTotal == CPUTotal:
            print('Heu empatat')
            tie = True
    f00.messageEnd(winner, player)
    return errorsInExecution
    # Quan vingui la versió 2.0 aquí haureu d'afegir més coses al return

# Aquesta línia és només per comprobar que el programa et funciona sense el main
# Ja per la versió 1.0 hauries de comentar-la i passar-la al codi principal d'alguna manera
# startBlackjack()
