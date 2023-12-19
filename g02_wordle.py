# This file is part of jocsCalamot by Pedro Bonilla.
#
# jocsCalamot is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# jocsCalamot is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# See <https://www.gnu.org/licenses/> for details og the license

import random
import requests
import unidecode
from termcolor import colored
from collections import defaultdict
import f00_functions as f00

# Crea una llista amb les vegades que es repeteix cada lletra
def count2List(stringIn):
    # Miro la mida
    length = len(stringIn)
    # Creo llista buida de la mida adequada
    listOut = [None] * length
    for i in range(length):
        # Omplo la llista amb les vegades que es repeteix cada lletra
        listOut[i] = stringIn.count(stringIn[i])
        # Torno la llista
    return listOut

def dictOfPositions(stringIn):
    # Creo un diccionari del tipus llista per defecte
    # Això fa que el diccionari apunti a llistes i amb append pugui afergir coses a la llista
    dictLettersIndexes = defaultdict(list)
    # Loop doble per posicions a la paraula (i) lletra (letters)
    for i, letter in enumerate(stringIn):
        # Afegeixo a la clau de la lletra cada posició on hi apareix
        dictLettersIndexes[letter].append(i)
    # Filtro el diccionari perquè només inclogui les claus amb llistes de
    # longitud més gran que 1 (es a dir les repeticions)
    # dictDuplicates = {key: value for key,
    #                  value in dictLettersIndexes.items() if len(value) > 1}
    # Torno els 2 diccionaris, perque no tinc clar quin faré servir encara
    return dictLettersIndexes

# Defineixo en quins colors s'han de printar les lletres
def colorsWordle(stringIn, stringCorrect):
    # Calculo longitud de la paraula, llista de repeticions i diccionati amb els index de les lletres
    length = len(stringIn)
    listRep = count2List(stringCorrect)
    dictRep = dictOfPositions(stringCorrect)
    # Per defecte ho printo tot vermell
    listOut = ['red'] * length
    # Creo una llista de Trues per que el 1r loop es prioritari
    # pero el segon loop em podria sobresctiure el 1r i no li he de permetre
    listCheck = [True] * length
    for i in range(length):
        # loop per veure si la paraula está exactament al lloc
        letter = stringIn[i]
        if letter == stringCorrect[i]:
            # si esta al lloc, al segon loop no he de fer res, aquí
            listCheck[i] = False
            # si esta al lloc, color verd
            listOut[i] = 'green'
            # redueixo el nombre de repeticions que queden
            # accedeixo a les posicions amb el diccionari de les repeticions
            for j in dictRep[letter]:
                listRep[j]=listRep[j]-1
    for i in range(length):
        if listCheck[i]:
            letter = stringIn[i]
            # aquí només he de fer coses si la lletra està a la paraula
            if letter in stringCorrect:
                # I A MÉS! encara no s'han colorat tantes lletres com repeticions
                if listRep[dictRep[letter][0]] > 0:
                    # Sé és el cas canvio a groc
                    listOut[i] = 'yellow'
                    # i torno a reduir les repeticions.
                    for j in dictRep[letter]:
                        listRep[j]=listRep[j]-1
    return listOut

# Aquesta funció mostrant la paraules amb els color del joc.
def displayWordColors(wordTry, wordSecret):
        lenW=len(wordTry)
        # Crea una llista de colors
        listCol=colorsWordle(wordTry, wordSecret)
        # Printa amb el format de color correcte
        print("[",end="")
        for j in range(lenW-1):
            print(colored(wordTry[j],listCol[j]),end="")
            print("][",end="")
        print(colored(wordTry[lenW-1],listCol[lenW-1]),end="")
        print("]")

# Aquesta funció va mostrant l'estat del joc a cada jugada.
def displayBoard(numTries, numMax ,history, wordSecret):
    print("Et queden " + str(numMax - numTries) + " intent(s)")
    # Aqui mostra totes les paraules jugades amb colors
    for i in range(numTries+1):
        wordPrint=history[i]
        displayWordColors(wordPrint, wordSecret)

def startWordle():
    # Joc del Penjat en castellà
    # Defineixo un nom provisional pel jugador,
    # Després quan vingui la versió 2.0 s'haureu de canviar com es defineix player
    player = "Jugador"
    # Variable a tornar per que el main general sàpiga que fer
    errorsInExecution = 0
    # Inicialitzo el llistat de lletres usades correctes i incorrectes
    lettersUsed = ""
    # Imposo que la paraula tingui entre 5 lletres.
    numberOfLettersImposed = 5
    # genero la paraula vàlida aleatòria amb la API i altres funcions
    wordObjective = f00.generateSpanishWordNormalised(numberOfLettersImposed)
    # inicialitzo el nombre d'intents i d'oportunitats
    numberOfGuessesPerformed = 0
    numberOfGuessesMaximum = 8
    # Missatge Benviguda
    print('Benvingut ' + player + '! Juguem al casi Wordle en Castellà')
    print('Tens ' + str(numberOfGuessesMaximum) + ' intents de paraules')
    print(' per endevinar la paraula correcta')
    print('Si una lletra està al seu joc es veurà en verd')
    print('Si una lletra no està a la paraula final es veurà en vermell')
    print('Si una lletra està a la paraula, però no on toca es veurà en groc')
    print('Qualsevol combinació de 5 caràcters s\'accepta com a input')
    print('La paraula secreta pot ser plural o conjugació')
    print('[_][_][_][_][_]')
    wordsHistory=[None]*numberOfGuessesMaximum
    # Inicialitzo la variable per entrar al loop
    endGame = False
    # Loop fins que indiqui que el joc s'ha acabat.
    while endGame == False:  
        # Li demano a l'usuari la nova paraulla amb les condicionants
        wordNew = f00.chooseLetterMsg('Introdueix la següent paraula :  ',['len',5,'La paraula ha de ser de 5 lletres'],['val',f00.abcd,'Només s\'accepten paraules amb caràcters de la a a la z sense tildes (com la ñ)'])
        # Afegeixo lletres usades
        for let in wordNew:
            if let not in lettersUsed:
                lettersUsed = lettersUsed + let
        # Fico la paraula al històric de paraules jugades
        wordsHistory[numberOfGuessesPerformed]=wordNew
        # El primer que faig a cada jugada és actualitzar el marcador
        displayBoard(numberOfGuessesPerformed, numberOfGuessesMaximum, wordsHistory, wordObjective)
        numberOfGuessesPerformed = numberOfGuessesPerformed+1
        print("Lletres usades :" + lettersUsed)
        # Miro si el joc s'ha acabat per victoria o per derrota
        if wordNew == wordObjective :
            endGame = True
            winner = True
        elif numberOfGuessesPerformed >= numberOfGuessesMaximum:
            endGame = True
            winner = False
    f00.messageEnd(winner, player)
    print("La paraula era : " )
    displayWordColors( wordObjective, wordObjective)
    return errorsInExecution
    # Quan vingui la versió 2.0 aquí haureu d'afegir més coses al return

# Aquesta línia és només per comprobar que el programa et funciona
# Ja per la versió 1.0 hauries de comentar-la i passar-la al codi principal d'alguna manera