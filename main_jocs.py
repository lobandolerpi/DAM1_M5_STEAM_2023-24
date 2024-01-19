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
from collections import defaultdict
from termcolor import colored
import f00_functions as f00
import f01_data_base as fdb
# Versió 1.0 cal importar el teu fitxer de jocs
import f01_data_base as fdb
import g01_penjat as g01
import g02_wordle as g02
import g03_ppt as g03
import g04_parells_senars as g04
import g05_chinos as g05
import g06_buscamines as g06
<<<<<<< HEAD
import g07_3ratlla as g07
import g08_blackjack as g08
import g09_anagrama as g09
import g10_ppt as g10

=======
import g05_chinos as g05
>>>>>>> g05
# Aquesta funció, demana a l'usuari un sencer per triar jocs
def chooseIntegerDictionaryMessages(dictIn, listStrMsg):
    # Demana a l'usuari un número de la llista de keys de la llista
    listNumbers = list(dictIn.keys())
    # Això és un while que es repeteix fins que es canvia rejected
    rejected = True
    while rejected:
        # Printo el missatge 1 que és triar un joc
        print(listStrMsg[0])
        # Printo el llistat d'opcions de jocs disponibles.
        for i in range(0,len(listNumbers)):
            # es a dir el número a la key, i el joc al que accedeixo amb el diccionari
            print(str(listNumbers[i]),"__",dictIn[listNumbers[i]])
        # recollida de l'input de l'usuari
        # amb try faix que si em dona un error int() executi la seccio d'except. 
        try:
            # deso l'input de l'usuari a numTmp
            numTmp = int(input(""))
            if numTmp in listNumbers:
                # Si el número està a la llista de keys, deixo de rebutjo per sortir del loop
                rejected = False
            else:
                # Rebutjo tota la resta de números amv el missatge d'error
                print(listStrMsg[1])
        except ValueError:
            # si rebo un error amb try, mostro el missatge
            print(listStrMsg[2])
    # Torno el sencer validat
    return numTmp

# Aquesta funció només executa la funció del correcte.
# Depeent del paràmetre. L'haureu de tocar a la Versio 1.0
def playGame(whatGame,player):
    # Si no pasa res torno un 0. El programa continua normal
    errorsInExecution = 0
    if whatGame == 0:
        # en veritat això no es un error, sino el codi d'error per sortir
        errorsInExecution = 1
    elif whatGame == 1:
        errorsInExecution = g01.startAhorcado()
    elif whatGame == 2:
        errorsInExecution = g02.startWordle()
    elif whatGame == 3:
        errorsInExecution = g03.startPPT()
    elif whatGame == 4:
        errorsInExecution = g04.startParellsSenars()
    elif whatGame == 5:
        errorsInExecution = g05.startChinos()
    elif whatGame == 6:
        errorsInExecution = g06.startBuscamines()
    elif whatGame == 7:
        errorsInExecution = g07.start3EnRatlla()
    elif whatGame == 8:
        errorsInExecution = g08.startBlackjack()
    elif whatGame == 9:
        errorsInExecution = g09.startAnagrames()
<<<<<<< HEAD
    elif whatGame == 10:
        errorsInExecution = g10.startPPT()
=======
    elif whatGame == 5:
	errorsInExecution = g05.startChinos()

>>>>>>> g05
    else:
        # Hi ha un error no identificat.
        errorsInExecution = 2
    return errorsInExecution


def main():
    # A la versió 2.0 aquí anirà la selecció de jugador i 
    # consulta a la base de dades (Ho farà el professor)
    BdD = fdb.loadPlayersDB(fdb.pathDB)  # Carrego la Base de dades
    BdD, indU = fdb.whoPlays(BdD) # Pregunto qui jugarà
    player = BdD['username'][indU] # Extrec la info del player de la BdD a una variable
    print()
    print(player + ', benvigut a JOCS CALAMOT') # Saludo

    # creo un diccionari amb els jocs instal·lats
    dictGames={
        1: "Penjat en castellà",
        2: "Wordle en castellà",
        3: "Pedra, Paper o Tissores",
        4: "Parells o Senars",
        5: "Punyet (los chinos)",
        6: "Buscamines",
<<<<<<< HEAD
        7: "3 en ratlla",
        8: "Black Jack (el 21)",
        9: "Anagrama",
        10: "PPT",
        0: "Vull deixar de jugar"
=======
        9: "Anagrama" ,
	5: "Chinos"
>>>>>>> g05
    }
    # A la versió 1.0 has d'afegir aquó el nom del teu joc.
    # Creo una llista de missatges per mostrar a la funció
    listMsg2User=['Tria un joc del llistat següent : ',
        "El número no està al rang",
        "No has introduit un número sencer"]
    # Li demano a l'usuari a què vol jugar
    
    whatToDoNext = 0 # Defineixo variable per entrar al while (i jugar a jocs consecutius)
    while whatToDoNext == 0:

        # Si no inclous el teu joc a la llista durant la versió 1.0, no sortirà al menú d'opcions !!!!
        numGame = chooseIntegerDictionaryMessages(dictGames, listMsg2User)
        # A jugar una partida!
        # A la versió 2.0 el playGame hauria de acceptar el paràmetre recollir el jugador 
        whatToDoNext, victory = playGame(numGame, player) # !!! FES SERVIR PLAYER AL TEU CODI !!!!!
        # I tornar si s'ha guanyat o perdut.

        # A la versió 2.0 aquí anirà l'actualització de les victòries del jugador a la base de dades 
        # Ho farà el professor, però necessitarà una variable que ha d'extreure playGame
        # I per tant el teu joc, l'haurà de subministrar.
        BdD = fdb.updateVictories(indU, BdD, victory) # Actualitzo la BdD amb el resultat
        fdb.writePlayersDB(fdb.pathDB, BdD) # guardo la BdD al .txt (si no el jugador pot apagar l'ordinador per no perdre)
        fdb.printVictories(BdD, indU) # Printo les estadístiques del jugador
        # Que fer després de jugar. Si hi ha un error al joc s'hauria de tractar aquí.
        if whatToDoNext == 2:
            print("Hi ha hagut un error al joc, tornant al menu de selecció...")
            whatToDoNext = 0
        # L'usuari vol seguir jugant?
        if whatToDoNext !=1:
            yesOrNot = f00.chooseLetterMsg('Vols seguir jugant  [s]/[n]?',['val','sn','Només s\'accepta  s  o  n'],['len',1,'L\'entrada ha de 1 unic caracter s o n'])
            if yesOrNot == 'n':
                whatToDoNext = 1
        # Si l'usuari vol parar de jugar. Comiat i sortir
        if whatToDoNext == 1:
            print("Fins una altra !")
            return 0

# Executo el main, com a única funció del carregador de jocs (la resta, es carreguen des del main).
main()
