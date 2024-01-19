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

# constants del main
abcd = 'abcdefghijklmnopqrstuvwxyz'

# Funció per demanar un input amb condicions
def chooseLetterMsg(*args):
    # INFO PER USAR LA FUNCIO
    # argument 1 es un string am la pregunta de l'input per l'usuari
    # la resta d'arguments son OPCIONALS i son llistes de 3 elements 
    # [ codi (str exacte), condicio (depèn), missatge d'error  (str lliure)] 
    #  1 ['val' , (str) amb caràcters acceptats a l'input, err ] 
    #  2 ['inl' , (str) amb caràcters NO acceptats a l'input, err ]
    #  3 ['len' , (int) mida exacta de characters dessitjada, err ]
    numArgIn = len(args)
    # deso quants arguments he rebut pel loop
    # Això és un while que es repeteix per sempre fins que arriba al return.
    while True:
        validInput=False
        while validInput == False:
            # Pregunta inicial a l'usuari
            letterInput = input(args[0])
            # passa les lletres a minuscules
            letterInput = letterInput.lower()
            # inicialitzo a no hi ha errores en les condicions
            # abans de les condicions
            errorsHere = False
            # comprovo les condicions una per una.
            for i_arg in range(1,numArgIn):
                # Selecciono la clau de la condicio
                keyW = args[i_arg][0]
                # i trio que fer en cunció de la clau anb el if else
                if keyW == 'val':
                    # creo el bolea check per mantenir el contro
                    check = False
                    # a totes les lletres de l'input
                    for letter in letterInput:
                        # comprobo que la lletra estigui entre les admeses
                        if letter not in args[i_arg][1]:
                            # si no està, activo el check
                            check = True
                    if check:
                        # si el check està activat, printo l'error
                        print (args[i_arg][2]) 
                        # i activo l'error
                        errorsHere = True
                        # L'error i el check, no son el mateix, perque 
                        # reinicio el check a cada condició i l'error no
                elif keyW == 'inv':
                    #Exactament el mateix que amb vel, però amb in en comtes de not in 
                    check = False
                    for letter in letterInput:
                        if letter in args[i_arg][1]:
                            check = True
                    if check:
                        print (args[i_arg][2])
                        errorsHere = True
                elif keyW == 'ivi':
                    #Com inv però combinacions de caràcters en una llista 
                    check = False                      
                    if letterInput in args[i_arg][1]:
                        check = True
                        print(letterInput)
                        print("in")
                        print(args[i_arg][1])
                    if check:
                        print (args[i_arg][2])
                        errorsHere = True
                elif keyW == 'len':
                    # Comprovo si la longitud és la especificada
                    if len(letterInput) != args[i_arg][1]:
                        print(args[i_arg][2])
                        errorsHere = True
            if errorsHere == False:
                validInput == True
                return letterInput
                # torna la nova lletra triada despres de validar que es triable

def messageEnd(winner, player):
    # Accions finals del joc un cop endGame es True
    if winner:
        print("FELICITATS " + colored(player, 'blue') + " !!! Has guanyat.")
    else:
        print("Ho sento " + colored(player, 'blue') +", has perdut.")

# Aquesta funció genera una paraula aleatoria consultant a l'api (com el clima)
def apiGetRandomSpanishWords(numberOfWords, numberOfLetters):
    # Fa la consulta a l'API de la paraula/es
    jsonRandomWords = requests.get(
        "https://clientes.api.greenborn.com.ar/public-random-word?c="+str(numberOfWords)+"&l="+str(numberOfLetters))
    # Transforma el format a una llista amb el nombre de paraules
    listRandomWords = jsonRandomWords.json()
    return listRandomWords

# Genera 1 paraula d'un número de lletres concret sense ñ
# i les normalitza (minuscules i sense accent) 
def generateSpanishWordNormalised(numberOfLetters):
    # Loop infinit a trencar amb el return
    while True:
        listWords = apiGetRandomSpanishWords(1, numberOfLetters)
        wordTmp = listWords[0]
        if "ñ" not in wordTmp:
            # Si no té ñ la vull. Elimino els accents i diéresi.
            wordOk = unidecode.unidecode(wordTmp)
            # I surto de la funció tornant la paraula.
            return wordOk
