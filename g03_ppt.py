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

def startPPT(player):
    # Joc del Pedra Paper Tisores
    # Defineixo un nom provisional pel jugador,
    # Després quan vingui la versió 2.0 s'haureu de canviar com es defineix player
    # Variable a tornar per que el main general sàpiga que fer
    errorsInExecution = 0
    # inicialitzo el nombre de victories dels jugadors i la total.
    numberOfVictoriesToWin = 3
    numberOfVictoriesPlayer = 0
    numberOfVictoriesCPU = 0
    # Creo un diccionari de pedra paper tisores
    dicPPT = {0: "Pedra   ", 1: "Paper   ", 2: "Tisores "}
    # Missatge Benviguda
    print('Benvingut ' + player + '! Juguem a Pedra, Paper o Tisores')
    print('La victoria es per qui guanyi ' + str(numberOfVictoriesToWin) + ' rondes')
    print('Pedra guanya a Tissores, Tissores guanya a Paper, Paper guanya a pedra')
    # Inicialitzo la variable per entrar al loop
    endGame = False
    # Loop fins que indiqui que el joc s'ha acabat.
    while endGame == False: 
        # Li demano a l'usuari la seva jugadao. Input amb condicionants
        playPlayer = f00.chooseLetterMsg('Introdueix Pedra [0], Paper [1] o Tisores [2] :  ',
            ['len',1,'Longitud de l\'input incorrecta'],
            ['val','012','Has de triar amb 0, 1 o 2'])
        # Canvio a sencers
        playPlayer=int(playPlayer)
        # La jugada de la CPU es aleatòria
        playCPU = random.randint(0, 2)
        # Miro qui ha guanyat i actualitzo variables de missatges i victòries
        # Ho faig amb mòdul 3
        if playPlayer%3 == (playCPU + 1)%3:
            # pedra   0%3 = 0 guanya a tissores (2+1)%3=0
            # paper   1%3 = 1 guanya a pedra    (0+1)%3=1
            # tisores 2%3 = 2 guanya a paper    (1+1)%3=2
            partialResult='guanyat'
            numberOfVictoriesPlayer = numberOfVictoriesPlayer + 1
        elif playPlayer%3 == (playCPU + 2)%3:
            # pedra   0%3 = 0 perd vs paper   (1+2)%3=0
            # paper   1%3 = 1 perd vs tisores (2+2)%3=1
            # tisores 2%3 = 2 perd vs pedra   (0+2)%3=2
            partialResult='perdut'
            numberOfVictoriesCPU = numberOfVictoriesCPU +1
        else:
            # en cas contrari es empat 
            # (aquest era el facil si, però així veieu com emprar mòdul)
            partialResult='empatat'
        # Informo dels resultats de la ronda
        print("------Resultat-Ronda--------")
        print(colored(player,'green') + ": " + colored(dicPPT[playPlayer],'yellow') + "  vs  " + colored(dicPPT[playCPU],'yellow') + " :" + colored("CPU",'red'))
        print("En aquesta ronda has :" + partialResult)
        print("------Resultat-Partida------")
        print(colored(player,'green') + ":    [ " + colored(str(numberOfVictoriesPlayer),'yellow') + " ]  vs  [ " + colored(str(numberOfVictoriesCPU),'yellow') + " ]    :" + colored("CPU",'red'))
        
        # Miro si el joc s'ha acabat per victoria o per derrota
        if numberOfVictoriesPlayer >= numberOfVictoriesToWin :
            endGame = True
            winner = True
        elif numberOfVictoriesCPU >= numberOfVictoriesToWin:
            endGame = True
            winner = False
    f00.messageEnd(winner, player)
    return errorsInExecution, winner
    # Quan vingui la versió 2.0 aquí haureu d'afegir més coses al return

# Aquesta línia és només per comprobar que el programa et funciona
# Ja per la versió 1.0 hauries de comentar-la i passar-la al codi principal d'alguna manera
#startPPT()
