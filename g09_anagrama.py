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

def string2List(wordIn):  # transforma string a llista de lletres
    l = len(wordIn)  # Longitud de l'string
    listW = [None]*l  # Defineixo la llista buida (per més velocitat)
    for i in range(l):
        listW[i] = wordIn[i]  # Omplo la llista amb les lletres
    return listW

def list2String(listIn):  # transforma llista string
    l = len(listIn)  # Longitud de la llista
    word = ""  # Defineixo paraula buida
    for i in range(l):
        word = word + str(listIn[i])  # Formo l'string amb les lletres
    return word

def shuffleString(parameter1):  # desordrena una paraula
    # Transformo a llista per poder fer shuffle
    parameter1 = string2List(parameter1)
    random.shuffle(parameter1)  # Desordreno la llista
    parameter1 = list2String(parameter1)  # La torno a String desordrenat
    return parameter1

# Aquesta funció mostrant la paraules amb els color del joc.
def printWordSigns(*args):
    numArgIn = len(args) # Miro el nombre d'arguments
    word2Print = args[0] # El primer ha de ser la paraula 
    lenW = len(word2Print) # N'extrec la mida.
    lenPrints = lenW*3 # I afegeixo els caràcrers de dreta i esquerra per cada lletra.
    if numArgIn > 1:  
        left = args[1] # Si hi ha 2 arguments, el 2n ha de ser els caractes a l'esquerra de cada lletra
    else:
        left = "" # Si no n'hi ha declaro string buit 
    if numArgIn > 2:
        right = args[2]  # Si hi ha 3 arguments, el 3r ha de ser els caractes a la dreta de cada lletra
    else:
        right = "" # Si no n'hi ha declaro string buit 
    if numArgIn > 3:
        tmpCol = args[3] # Si hi ha 4 arguments, he especificat coses sobre el color de la font
        listCol = checkListColors(tmpCol, lenW, lenPrints, 'black')
    else:
        listCol = ['black']*lenPrints # si no hi ha argument tot blanc
    if numArgIn > 4:
        tmpBkg = args[4] # Si hi ha 5 arguments, he especificat coses sobre el color del fons
        listBkg = checkListColors(tmpBkg, lenW, lenPrints, 'on_white')
    else:
        listBkg = ['on_white']*lenPrints # si no hi ha argument tot blanc
    # Printa amb el format de color correcte
    for j in range(lenW):
        print(colored(left, listCol[j*3+0], listBkg[j*3+0] ),end="")
        print(colored(word2Print[j], listCol[j*3+1], listBkg[j*3+1]), end="")
        print(colored(right, listCol[j*3+2], listBkg[j*3+2] ),end="")
    print("")

def checkListColors(argIn, lenW, lenPrints, defColor):
    if isinstance(argIn, str): # Si li he passat un string, creo la llista amb tot
        listOut = [argIn]*lenPrints
    elif isinstance(argIn, list) and len(argIn) == lenPrints:
        listOut = argIn # Si li passo una llista de mida igual als prints, la llista ja està 
    elif isinstance(argIn, list) and len(argIn) == lenW:    
        # Si li passo una llista de mida igual a les lletres
        listOut = ['white']*lenPrints # Omplo tota la llista de colors de blancs
        for i in range(lenW):
            listOut[i*3+1]=argIn[i] # I substitueixo els colors de les lletres
    elif isinstance(argIn, list) and len(argIn) == lenW +1 : 
        # Si li passo una llista de mida igual a les lletres +1
        listOut = [argIn[0]]*lenPrints # El primer color és el dels caràcters adicionals
        for i in range(lenW):
            listOut[i*3+1]=argIn[i+1] # I substitueixo els colors de les lletres
    elif isinstance(argIn, list) and len(argIn) == 2 : 
        # Si li passo una llista de 2, 
        listOut = [argIn[0]]*lenPrints # El primer color és el dels caràcters adicionals
        for i in range(lenW):
            listOut[i*3+1]=argIn[2] # I la resta, les lletres
    elif isinstance(argIn, list) : 
        print("heckListColors: Error mida de la llista no reconeguda")
        listOut = [argIn[0]]*lenPrints # Si es una llista pero les mides no coincideixen, agafo el 1r per tots. 
    else:
        print("printWordSigns: Error al 4t argument d'entrada, els colors han de ser o un string o una llista")
        listOut = [defColor]*lenW # en cas contrari tot blanc    
    return listOut

def startAnagrames(player):
    # Joc dels anagrames en castellà
    # Defineixo un nom provisional pel jugador,
    # Després quan vingui la versió 2.0 s'haureu de canviar com es defineix player

    # Variable a tornar per que el main general sàpiga que fer
    errorsInExecution = 0
    # Imposo que la paraula tingui entre 6 i 9 lletres.
    numberOfLettersImposed = random.randint(5, 6)
    # genero la paraula vàlida aleatòria amb la API i altres funcions
    wordObjective = f00.generateSpanishWordNormalised(numberOfLettersImposed)
    wordShuffled = shuffleString(wordObjective)
    # inicialitzo el nombre d'intents i d'oportunitats
    numberOfGuessesPerformed = 0
    numberOfGuessesMaximum = 3
    # Missatge Benviguda
    print('Benvingut ' + player + '! Juguem als anagrames en Castellà')
    print('Tens ' + str(numberOfGuessesMaximum) + ' intent per endevinat')
    print(' la paraula en castellà feta amb les lletres desordrenades.')
    wordsHistory = [None]*numberOfGuessesMaximum
    # Inicialitzo la variable per entrar al loop
    endGame = False
    winner = False
    # Loop fins que indiqui que el joc s'ha acabat.
    while endGame == False:
        print("")
        print("Intent " + str(numberOfGuessesPerformed +1) + " de " + str(numberOfGuessesMaximum))
        print("La paraula desordrenada (en castellà) és:")
        printWordSigns(wordShuffled, "[","]","red","on_white")
        # Li demano a l'usuari la nova paraulla amb les condicionants
        wordNew = f00.chooseLetterMsg('Introdueix el següent intent de paraula :  ', ['len', len(wordObjective), 'La paraula ha de ser de '+ str(len(wordObjective))+ ' lletres'], [
                                      'val', wordShuffled, 'Només s\'accepten paraules amb caràcters de la paraula desordrenada'])
        numberOfGuessesPerformed = numberOfGuessesPerformed +1
        # Miro si el joc s'ha acabat per victoria o per derrota
        if wordNew == wordObjective:
            endGame = True
            winner = True
        elif numberOfGuessesPerformed >= numberOfGuessesMaximum:
            endGame = True

    f00.messageEnd(winner, player)
    print("La paraula era : ")
    printWordSigns(wordObjective, "[","]","green","on_white")
    return [errorsInExecution, winner]
    # Quan vingui la versió 2.0 aquí haureu d'afegir més coses

# Aquesta línia és només per comprobar que el programa et funciona
# Ja per la versió 1.0 hauries de comentar-la i passar-la al codi principal d'alguna manera
# startAnagrames()
