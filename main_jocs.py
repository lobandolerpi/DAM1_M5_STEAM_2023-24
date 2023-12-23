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
import g08_blackjack as g08
# Versió 1.0 cal importar el teu fitxer de jocs
import g09_anagrama as g09

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
def playGame(whatGame):
    # Si no pasa res torno un 0. El programa continua normal
    errorsInExecution = 0
    if whatGame == 0:
        # en veritat això no es un error, sino el codi d'error per sortir
        errorsInExecution = 1
    elif whatGame == 8:
        g08.startBlackjack()
    # A la versió 1.0 hauréu de modificar aquest codi afegint alguna cosa
    # similar al que poso a baix
    elif whatGame == 9:
       #return(s) de la funció = com he anomenat el paquet del joc  .   funció per executar el joc seleccionat ()
        errorsInExecution = g09.startAnagrames()

    else:
        # Hi ha un error no identificat.
        errorsInExecution = 2
    return errorsInExecution


def main():
    # A la versió 2.0 aquí anirà la selecció de jugador i 
    # consulta a la base de dades (Ho farà el professor)
    fdb.tmpMsgDB() # Comprobació que la base de dades 
    print()
    print('Benvigut a JOCS CALAMOT')

    # creo un diccionari amb els jocs instal·lats
    dictGames={
        0: "Vull deixar de jugar",
        8: "BlackJack",
        9: "Anagrama"
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
        whatToDoNext = playGame(numGame)
        # I tornar si s'ha guanyat o perdut.

        # A la versió 2.0 aquí anirà l'actualització de les victòries del jugador a la base de dades 
        # Ho farà el professor, però necessitarà una variable que ha d'extreure playGame
        # I per tant el teu joc, l'haurà de subministrar.



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