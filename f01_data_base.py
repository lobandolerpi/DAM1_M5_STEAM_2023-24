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
import os
from collections import defaultdict
from termcolor import colored

# De moment, per la versió 0.0 aquest fitxer no fa res.
# Pero el poso perque més tard vegem els canvis.

def tmpMsgDB():
    # Funció absurda per comprobar que està ben carregar el mòdul
    print("Base de dades no implementada en aquesta versió")


def openDB():
    # Funció per obrir la base de dades
    dataBase = None
    return dataBase

def checkUserPassword(userIn, passIn, dbIn):
    # Funció per comprobar si un usuari i contrassenya són a la dase de dades
    outBool = False
    return outBool

def askCredentials(userIn, passIn, dbIn):
    # Funció per demanar usuari i contrassenya
    outBool = False
    return outBool

def askNewUser(userInput):
    # Funció demanar si es vol crear un nou usuari o usar un existent
    outBool = False
    return outBool

def createNewUser(userIn, passIn, dbIn):
    # Funció per crear un nou usuari
    outBool = False
    return outBool

def updateVictories(userIn, resultIn, gameIn, dbIn):
    # Funció per actualitzar el registre de victòries.
    outBool = False
    return outBool