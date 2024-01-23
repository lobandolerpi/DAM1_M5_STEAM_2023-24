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

def startChinos(player):
    # Joc del Punyet o dels Chinos
    # Defineixo un nom provisional pel jugador,
    # Després quan vingui la versió 2.0 s'haureu de canviar com es defineix player
    # Variable a tornar per que el main general sàpiga que fer
    errorsInExecution = 0
    # inicialitzo el nombre de victories dels jugadors i la total.
    numberOfVictoriesToWin = 3
    numberOfVictoriesPlayer = 0
    numberOfVictoriesCPU = 0
    # Missatge Benviguda
    print('\n Benvingut ' + player + '!!! \n Juguem al Punyet (chinos en castellà)')
    print('Cada jugador tria en secret de 0 a 3 fitxes')
    print('Després s\'aposta per la suma total (mínim 0+0 màxim 3+3)')
    print('Cada torn s\'alterna qui anuncia primer la aposta')
    print('Una ronda es guanya endefinant la suma total de fitxes')
    print('La victoria és per qui guanyi ' + str(numberOfVictoriesToWin) + ' rondes')
    # Inicialitzo la variable per entrar al loop
    endGame = False
    # Inicialitzo la variable de torn
    turn = 1
    # Loop fins que indiqui que el joc s'ha acabat.
    while endGame == False: 
        # Printo que és un torn nou
        print("")
        print(colored("========== TORN " + str(turn)+ " ==========",'blue'))
        print(colored("La CPU no fa servir aquesta dada",'grey'))
        # Creo la jugada de la CPU aleatòria.
        playCPU = random.randint(0, 3)
        # Demano la jugada del jugador amb input i condicionants
        playPlayer = f00.chooseLetterMsg('Introdueix quantes fitxes poses a la teva ma (de 0 a 3) :  ',
            ['len',1,'Longitud de l\'input incorrecta'],
            ['val','0123','Has de triar un sencer del 0 al 3'])
        # canvio l'input a sencers
        playPlayer=int(playPlayer)
        # calculo la suma que és el que cal endevinar
        playTotal = playPlayer + playCPU
        # Els torns senars i els parells son diferents (qui aposta primer)
        # Per tant faig un if amb mòdul 2 (%) 
        if turn%2 == 1:
            # Si el torn és senar, la CPU aposta primer
            # declaro una variable errònia per entrar al loop
            guessCPU = -1
            # Faig un Loop per l'aposta de la CPU
            while guessCPU < 0 or guessCPU > 6:
                # Sempre aposta el que ella a tret, més el que pot treure el jugador
                guessCPU = playCPU + random.randint(0, 3)
            # Informo de l'aposta de la CPU
            print (colored("La CPU ha triat per aquesta ronda \n una suma total de ",'yellow') + colored(str(guessCPU),'red') )
            # Demano l'aposta del player amb els condicionants
            guessPlayer = f00.chooseLetterMsg('Tria quan creus que serà la suma de les 2 jugades \n  (sencer del 0 al 6): ',
            ['len',1,'Longitud de l\'input incorrecta'],
            ['val','0123456','Mínim 0+0, Màxim 3+3. Has de triar un número del 0 al 6'],
            ['inv',str(guessCPU),'Això ho ha triat la CPU, tria una altra opció'])
            # Ho paso a sencer
            guessPlayer=int(guessPlayer)
        else:
            # Si el torn es parell, el jugador aposta primer
            print("Tú tries primer")
            # Demano l'aposta al player amb input i condicionants
            guessPlayer = f00.chooseLetterMsg('Tria quan creus que serà la suma de les 2 jugades (sencer del 0 al 6): ',
            ['len',1,'Longitud de l\'input incorrecta'],
            ['val','0123456','Mínim 0+0, Màxim 3+3. Has de triar un número del 0 al 6'])
            # Converteixo a sencers
            guessPlayer=int(guessPlayer)
            # Declaro variable fora de rang per entrar al while
            guessCPU = -1
            # Faig un while per l'aposta de la CPU mentre el valor sigui invàlid
            while guessCPU < 0 or guessCPU > 6 or guessCPU == guessPlayer:
                # La CPU suposa que més o menys apostes al doble del que tens.
                guessCPU = round(guessPlayer/2) + playCPU + random.randint(-1, 1)
        # Comprovo qui ha guanyat i canvio les variables de puntuació i missatge
        if playTotal == guessPlayer:
            partialResult='guanyat'
            numberOfVictoriesPlayer = numberOfVictoriesPlayer + 1
        elif playTotal == guessCPU:
            partialResult='perdut'
            numberOfVictoriesCPU = numberOfVictoriesCPU +1
        else:
            partialResult='empatat '
        # Missatges de com ha anat el torn 
        print("Fitxes jugades " +colored(player,'green') + ": " + colored(str(playPlayer),'yellow') + " + " + colored(str(playCPU),'yellow') + " : fitxes jugades " + colored("CPU",'red'))
        print("Suma total de fitxes :    " + colored(str(playPlayer + playCPU),'yellow') )
        print("Aposta de suma " +colored(player,'green') + ": " + colored(str(guessPlayer),'yellow') + "/ \\" + colored(str(guessCPU),'yellow') + " : aposta de suma " + colored("CPU",'red'))
        print("En aquesta ronda has :" + partialResult)
        print("------Resultat-Partida------")
        print(colored(player,'green') + ": [ " + colored(str(numberOfVictoriesPlayer),'yellow') + " ] vs [ " + colored(str(numberOfVictoriesCPU),'yellow') + " ] :" + colored("CPU",'red'))
        # Actualitzo el torn
        turn = turn + 1
        # Miro si el joc s'ha acabat per victoria o per derrota i actualitzo variables
        if numberOfVictoriesPlayer >= numberOfVictoriesToWin :
            endGame = True
            winner = True
        elif numberOfVictoriesCPU >= numberOfVictoriesToWin:
            endGame = True
            winner = False
    f00.messageEnd(winner, player)
    return errorsInExecution, winner
    # Quan vingui la versió 2.0 aquí haureu d'afegir més coses al return

# Aquesta línia és només per comprobar que el programa et funciona sense el main
# Ja per la versió 1.0 hauries de comentar-la i passar-la al codi principal d'alguna manera
startChinos()

