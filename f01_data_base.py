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
# See <https://www.gnu.org/licenses/> for details of the license

import random
import requests
import unidecode
import os
from collections import defaultdict
from termcolor import colored
import f00_functions as f00

pathDB = os.path.abspath("./dataBase/dbPlayers.txt")
pathDB2 = os.path.abspath("./dataBase/dbPlayers2.txt") # Debug

# De moment, per la versió 0.0 aquest fitxer no fa res.
# Pero el poso perque més tard vegem els canvis.

def tmpMsgDB():
    # Funció absurda per comprobar que està ben carregar el mòdul
    print("Base de dades no implementada en aquesta versió")


def loadPlayersDB(pathDB):
    # Funció per obrir la base de dades  
    dataPlayersPython = {} # Creo un diccionari buit
    fileDB = open(pathDB,"r") # Obro l'arxiu de la BdD com a lectura
    lines = fileDB.readlines() # Llegeixo per línies (a una llista)
    fileDB.close() # El tanco.
    titlesDict=0 # Només per distingir entre la línia dels titols i la resta
    for line in lines: # Loop per totes les línies del fitxer
        valuesLine = line.strip().split(',') # strip treu \n, split separa pel valor indicat
        if titlesDict == 0: # Si no he canviat això és la línia del titol
            titlesDict =[] # Ara ho canvio, pq la propera línia ja no serà el títol.
            for i in range(len(valuesLine)): # Loop per la longitud de la llista de valors llegits (5)
                titlesDict.append(valuesLine[i]) # Afegeixo a una llista el valor de cada vey del diccionari.
                dataPlayersPython[titlesDict[i]] = [] # ceo una llista buida amb aquest key dins del diccionari
        else:
            for i in range(len(valuesLine)): # Loop per la resta de línies.
                if i in [0,3,4]: # els valors 1, 4 i 5 de la Base de Dades son numèrics, però a readlines no li he dit res.
                    dataPlayersPython[titlesDict[i]].append(int(valuesLine[i])) # per tant li he de dir ara
                else:
                    dataPlayersPython[titlesDict[i]].append(valuesLine[i])  # La resta append normal       
    return dataPlayersPython # Torno les dades llegides (en format diccionari)

def checkUserPassword(userIn, passIn, dbIn):
    # Funció per comprobar si un usuari i contrassenya són a la dase de dades
    if userIn in dbIn['username']: # Si l'usuari és a la llista d'usuaris
        indU = dbIn['username'].index(userIn) # Agafo l'index
    else:
        print("checkUserPassword: L'usuari no és a la base de dades")
        return -2 # Si no, torno un codi d'error negatiu, pq no pot haver-hi index negatius
    paswDB = dbIn['passw'][indU] # Extrec el password per aquest usuari.
    if passIn == paswDB: # Si el password coincideix.
        return indU # Torno l'index pq el faré servir per actualitzar la BdD
    else:
        print("checkUserPassword: La contrassenya no coincideix amb la de la BdD.")
        return -1 # Si no coincideix un codi d'error negatiu diferent

def askCredentials(dbIn):
    # Funció per demanar usuari i contrassenya
    indU = -3 # Valor negatiu per entrar al while
    while indU < 0: # Demano usuari i contrassenya
        userAsk = f00.chooseLetterMsg('Introdueix el nom d\'usuari de la BdD : ', 
                                    ['val', f00.aA1, '  - Només lletres i números : '])
        paswAsk = f00.chooseLetterMsg('Introdueix el password de l\'usuari   : ', 
                                    ['val', f00.aA1, '  - Només lletres i números : '])
        indU = checkUserPassword(userAsk, paswAsk, dbIn) # Checkejo amb la BdD
        print("post-check ind U , ", end="")
        print(indU)
        if indU < 0: # si rebo un error pregunto si es vol reintentar
            retryU = f00.chooseLetterMsg('Vols tornar a intentar registrar-te  s/n ? :', 
                                    ['len', 1, '  - Introdueix només 1 caràcter, s o n : '],
                                    ['val', 'snSN', '  - Introdueix només s o n : '])
            if retryU == "n" or retryU == "N":
                return indU # si no es vol reintentar surto amb el codi d'error
        else:
            return indU # si he validat torno l'index.

def askNewUser(dbIn):
    # Funció per crear un nou usuari o usar un existent
    listKeys = list(dbIn.keys())
    newID = max(dbIn[listKeys[0]]) + 1 # Creo una nova ID
    inDB = True
    while inDB: # Demano un nom d'usuari que no pot estar ja a la BdD 
        userAsk = f00.chooseLetterMsg('Introdueix el nou nom d\'usuari per la BdD \n (només lletres i números) : ', 
                                    ['val', f00.aA1, 'Només lletres i números : '])
        inDB = userAsk in dbIn[listKeys[1]] # comprovo si ja estaba a la BdD
        if inDB:
            print("Aquest nom d'usuari ja existeix")
    paswAsk = f00.chooseLetterMsg('Introdueix el password de l\'usuari \n (només lletres i números) : ', 
                                    ['val', f00.aA1, 'Només lletres i números : '])
    # Actualitzo la BdD i extrec l'index de l'usuari a les llistes de la BdD
    dbIn[listKeys[0]].append(newID) 
    dbIn[listKeys[1]].append(userAsk)
    indU = dbIn[listKeys[1]].index(userAsk)
    dbIn[listKeys[2]].append(paswAsk)
    dbIn[listKeys[3]].append(0)
    dbIn[listKeys[4]].append(0)
    return dbIn , indU


def updateVictories(userInd, db2Update, playerWon):
    # Funció per actualitzar el registre de victòries.
    listKeys = list(db2Update.keys()) # Extrec la llista de claus
    db2Update[listKeys[3]][userInd]=db2Update[listKeys[3]][userInd]+1 # Actualitzo el num Partides jugades
    if playerWon: # Si es True que el jugafor ha guanyat
        db2Update[listKeys[4]][userInd]=db2Update[listKeys[4]][userInd]+1 # Actualitzo el num Partides Guanyades
    return db2Update # Torno la BdD

def writePlayersDB(pathDBw, db2Write):
    # Funció per obrir la base de dades
    fileDB = open(pathDBw,"w") # Obro
    listKeys = list(db2Write.keys()) # Extrec claus
    line ="" # Inicialitzo linia a escriure
    for iK in range(len(listKeys)): # Loop, nombre de claus a la 1a línia del fitxer
        line = line + listKeys[iK] # Afegeixo nom de clau
        if iK == len(listKeys)-1:
            line = line + "\n" # Si és la darrera, afegeixo canvi de línia
        else:
            line = line + "," # Si no, afegeixo una coma
    fileDB.write(line) # escric 1a línia
    for iNumP in range(len(db2Write['id'])): # Loop del número d'entrades a la BdD
        line ="" # Re-Inicialitzo linia a escriure
        for iK in range(len(listKeys)): # Loop, nombre de claus a la 1a línia del fitxer
            line = line + str(db2Write[listKeys[iK]][iNumP]) # Afegeixo la dada de la BdD
            if iK == len(listKeys)-1:
                line = line + "\n" # Si és la darrera, afegeixo canvi de línia
            else:
                line = line + "," # Si no, afegeixo una coma
        fileDB.write(line) # escric següent línia
    fileDB.close() # Tanco
    return 0

def whoPlays(dbLoaded):
    indU = -3
    while indU <= 0: 
        # Simplement selecciona si es vol triar jugador existent o nou i la funció corresponent
        # Fins que una de les 2 funcions respon amb un index de jugador valid ( >= 0)
        existOrNew = f00.chooseLetterMsg('Vols jugar amb un jugador existent (e) o un de nou (n) e/n ? :', 
                                    ['len', 1, '  - Introdueix només 1 caràcter, e o n : '],
                                    ['val', 'esnESN', '  - Introdueix només e o n : '])
        if existOrNew in ['e','E', 's', 'S']: # jugador existent
            indU = askCredentials(dbLoaded)
        else:
            dbLoaded, indU = askNewUser(dbLoaded)
    return dbLoaded, indU

def printVictories(dbOK, indU):
    listKeys = list(dbOK.keys())
    player = dbOK[listKeys[1]][indU]
    numPlays = dbOK[listKeys[3]][indU]
    numWins = dbOK[listKeys[4]][indU]
    print("El jugador " + player + " du :")
    print("  " + str(numWins) + " victòries de " + str(numPlays) + " partides.")
    if numPlays == 0:
        print("  Sense cap partida, no es pot calcular el % de victòries")
    else:
        print("  Un " + str(round(100*(numWins/numPlays))) + "% de victòries")
