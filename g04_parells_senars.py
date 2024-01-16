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

def startParellsSenars():
    # Joc del Pedra Paper Tisores
    # Defineixo un nom provisional pel jugador,
    # Després quan vingui la versió 2.0 s'haureu de canviar com es defineix player
    player = "Jugador"
    # Variable a tornar per que el main general sàpiga que fer
    errorsInExecution = 0
    # inicialitzo el nombre de victories dels jugadors i la total.
    numberOfVictoriesToWin = 3
    numberOfVictoriesPlayer = 0
    numberOfVictoriesCPU = 0
    # diccionati parells senars
    dicPS = {0: "Parell ", 1: "Senar  "}
    # Missatge Benviguda
    print('Benvingut ' + player + '! Juguem a Parells o Senars')
    print('La victoria es per qui guanyi ' + str(numberOfVictoriesToWin) + ' rondes')
    # Inicialitzo el torn
    turn = 1
    # Inicialitzo la variable per entrar al loop
    endGame = False
    # Loop fins que indiqui que el joc s'ha acabat.
    while endGame == False: 
        # Anuncio el torn nou
        print("")
        print(colored("========== TORN " + str(turn)+ " ==========",'blue'))
        # Els torns senars i els parells son diferents (qui aposta primer)
        # Per tant faig un if amb mòdul 2 (%) 
        if turn%2 == 1:
            # Demano al jugador si tria parells o senars. Input amb condicionants
            parellSenar = f00.chooseLetterMsg('Aquest torn tu tries si vols parells [0] o senars [1] : ',
            ['len',1,'Longitud de l\'input incorrecta'],
            ['val','01','Has de triar un 0 o un 1'])
            # Ho paso a integre
            parellSenar=int(parellSenar)
            # Informo de la tria
            if parellSenar == 1:
                print("Has triat jugar amb " + colored("SENARS",'green') + " aquest torn")
            else:
                print("Has triat jugar amb " + colored("PARELLS",'green') + " aquest torn")
        else:
            # Si el torn es parell, tria la CPU.
            # Faig random la opcio forçada del jugador i la CPU tria l'altra
            parellSenar=random.randint(0, 1)
            # Informo de la tria de la CPU i de l'aposta forçada del jugador
            if parellSenar == 1: 
                print("La màquina ha triat " + colored("parells",'red'))
                print("Per tant tu jugues amb " + colored("SENARS",'green') + " aquest torn") 
            else:
                print("La màquina ha triat " + colored("senars",'red'))
                print("Per tant tu jugues amb " + colored("PARELLS",'green') + " aquest torn") 
        # Demano que el jugador faci la seva jugada. Input amb condicionants
        playPlayer = f00.chooseLetterMsg('Introdueix un número del 0 al 9 :  ',
            ['len',1,'Longitud de l\'input incorrecta'],
            ['val','0123456789','Has de triar un sencer d\'un digit'])
        # Ho passo a sencers
        playPlayer=int(playPlayer)
        # La tria de la CPU és aleatòria.
        playCPU = random.randint(0, 1)
        # Comprovo qui ha guanyat amb el mòdul de la suma (%)
        if (playCPU + playPlayer)%2 == parellSenar:
            partialResult='guanyat'
            numberOfVictoriesPlayer = numberOfVictoriesPlayer + 1
        elif (playCPU + playPlayer + 1)%2 == parellSenar:
            partialResult='perdut'
            numberOfVictoriesCPU = numberOfVictoriesCPU +1
        else:
            print('error intern, càlcul de parell o senar')
        # Informo de com ha anat la ronda
        print("------Resultats-Ronda-------")
        print(colored(player,'green') + ":    " + colored(str(playPlayer),'yellow') + "  +   " + colored(str(playCPU),'yellow') + "    :" + colored("CPU",'red'))
        print("En aquesta ronda has :" + partialResult)
        print("------Resultat-Partida------")
        print(colored(player,'green') + ": [ " + colored(str(numberOfVictoriesPlayer),'yellow') + " ] vs [ " + colored(str(numberOfVictoriesCPU),'yellow') + " ] :" + colored("CPU",'red'))
        # Actualitzo el torn
        turn = turn + 1
        # Miro si el joc s'ha acabat per victoria o per derrota
        if numberOfVictoriesPlayer >= numberOfVictoriesToWin :
            endGame = True
            winner = True
        elif numberOfVictoriesCPU >= numberOfVictoriesToWin:
            endGame = True
            winner = False
    f00.messageEnd(winner, player)
    return errorsInExecution
    # Quan vingui la versió 2.0 aquí haureu d'afegir més coses al return

# Aquesta línia és només per comprobar que el programa et funciona
# Ja per la versió 1.0 hauries de comentar-la i passar-la al codi principal d'alguna manera
startParellsSenars()
