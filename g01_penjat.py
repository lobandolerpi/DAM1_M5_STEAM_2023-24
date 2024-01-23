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
import f00_functions as f00

# Aquesta funcio printa un conjunt de lletres amb un missatge
def wordToTiles(stringIn):
    # Afegeixo (join) l'string "][" cada 1 caracter [i:i+1]
    # despres de cada 1 caracter de tot el rang de la paraula (0,len(stringIn), 1)
    middleOfTheWord = "][".join(stringIn[i:i+1]
                                for i in range(0, len(stringIn), 1))
    # Afegeixo els caràcters inicials i finals
    middleOfTheWord = "[" + middleOfTheWord + "]"
    return middleOfTheWord


def updateWordHidden(wordSecret, lettersCorrect):
    wordHidden = '_' * len(wordSecret)
    # Canvio les lletres que ja he endevinat
    for i in range(len(wordSecret)):
        # recorro totes les posicions i si la lletra esta entre les correctes
        if wordSecret[i] in lettersCorrect:
            # La canvio
            wordHidden = wordHidden[:i] + wordSecret[i] + wordHidden[i+1:]
    return wordHidden

# Aquesta funció va mostrant l'estat del joc a cada jugada.


def displayBoard(guessesSoFar, guessesMaximum, lettersIncorrect, lettersCorrect, wordSecret):
    # Mostro les jugades que queden
    print("--- Duus " + str(guessesSoFar) + " de " +
          str(guessesMaximum) + " intents de lletra fallits---")
    print("T'en queden(a) " + str(guessesMaximum -
          guessesSoFar) + " intent(s) fallit(s)")
    # Mostro les lletres incorrectes amb un missatge
    print("Lletres incorrectes usades : ", colored(lettersIncorrect, 'red'))
    # Creo una "Paraula Amagada" de guions baixos
    wordHidden = updateWordHidden(wordSecret, lettersCorrect)
    # Mostro la paraula a endevinar amb missatge
    wordHidden = wordToTiles(wordHidden)
    print("Paraula a endevinar: ", wordHidden)

# La funcio que controla si totes las lletres del string 2
# estan a l'string 1
def allCharOnStrInGroup(lettersGroup, stringToCheck):
    # suposo d'entrada hi estan totes al grup
    allInGroup = True
    # comprovo totes les lletres de la paraula
    for lett in stringToCheck:
        # si almenys 1 no està al grup, ja és fals
        if lett not in lettersGroup:
            # per tant actualitzo la variable
            allInGroup = False
            # no he de seguir buscant
            break
    # I la retorno el resultat final, sigui quin sigui
    return allInGroup


def startAhorcado(player):
    # Joc del Penjat en castellà
    # Defineixo un nom provisional pel jugador,
    # Després quan vingui la versió 2.0 s'haureu de canviar com es defineix player
    # Variable a tornar per que el main general sàpiga que fer
    errorsInExecution = 0
    # Inicialitzo el llistat de lletres usades correctes i incorrectes
    lettersWrong = ""
    lettersRight = ""
    # Imposo que la paraula tingui entre 6 i 9 lletres.
    numberOfLettersImposed = random.randint(6, 9)
    # genero la paraula vàlida aleatòria amb la API i altres funcions
    wordObjective = f00.generateSpanishWordNormalised(numberOfLettersImposed)
    # inicialitzo el nombre d'intents i d'oportunitats
    numberOfGuessesPerformed = 0
    numberOfGuessesMaximum = 8
    # Missatge Benviguda
    print('Benvingut ' + player + '! Juguem al Penjat en Castellà')
    print('Tens ' + str(numberOfGuessesMaximum) +
          'intents de lletra, per endevinar la paraula de ' + str(numberOfLettersImposed)+' lletres')
    print('Els intents encertats no resten oportunitats')
    print('Cal pitjar totes les lletres 1 a 1 encara que sàpigues la paraula.')
    # Inicialitzo la variable per entrar al loop
    endGame = False
    # Loop fins que indiqui que el joc s'ha acabat.
    while endGame == False:
        # El primer que faig a cada jugada és actualitzar el marcador
        displayBoard(numberOfGuessesPerformed, numberOfGuessesMaximum,
                     lettersWrong, lettersRight, wordObjective)
        # Li demano a l'usuari la nova lletra amb el paràmetre de totes les lletres emprades
        letterNew = f00.chooseLetterMsg('Endevina una lletra:',
                                        ['inv', lettersWrong + lettersRight,
                                            'Ja has provat aquesta lletra. Prova\'n una altra.'],
                                        ['val', f00.abcd, 'Només pots introduir una lletra de l\'abecedari castellà, exceptuant la ñ'],
                                        ['len', 1, 'Introdueix una sola lletra.'])
        # Comprovo si la paraula estpa a la Paraula a endevinar
        if letterNew in wordObjective:
            # Si està la fico dintre de les lletres correctes
            lettersRight = lettersRight + letterNew
            # A més inicialitzo la condició encert com a True
            conditionOk = True
        else:
            # Si no està la fico dintre de les lletres in correctes
            lettersWrong = lettersWrong + letterNew
            # A més inicialitzo la condició encert com a False
            conditionOk = False
        # Miro si el joc s'ha acabat per victoria o per derrota
        if conditionOk:
            # Si la darrera jugada era un encert puc haver guanyat
            endGame = allCharOnStrInGroup(lettersRight, wordObjective)
            if endGame:
                # si el joc ha acabat amb victoria ho especifico
                winner = True
        else:
            # com he fallat, primer pujo el número d'intents fallits
            numberOfGuessesPerformed = numberOfGuessesPerformed+1
            # I comprovo si em queden intents o no.
            endGame = numberOfGuessesPerformed >= numberOfGuessesMaximum
            if endGame:
                # si el joc ha acabat amb derrota ho especifico
                winner = False
    # Accions finals del joc un cop endGame es True
    f00.messageEnd(winner, player) 
    print("La paraula era : " + colored(wordToTiles(wordObjective), 'green'))
    return errorsInExecution, winner
    # Quan vingui la versió 2.0 aquí haureu d'afegir més coses al return


# Aquesta línia és només per comprobar que el programa et funciona
# Ja per la versió 1.0 hauries de comentar-la i passar-la al codi principal d'alguna manera
# startAhorcado()
