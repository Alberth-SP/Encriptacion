from django.shortcuts import render
from random import random 
from django.http import JsonResponse
from django.http import HttpResponse
from random import random 
import json
import re

_susti =  {'ñ':'n', 'Ñ':'N'}
def preprocess(_message):
    _mes = str(_message).replace(' ','')
    _mes = _mes.replace('\t','')
    _mes = _mes.upper()
    _mes = re.findall("[A-Z0-9]",_mes)
    _string = ''
    for x in _mes:
        _string += str(x)
    return _string


def showTable(_rejilla):
    _string = ''
    for _row in _rejilla:
        for _col in _row:
            _string += _col + "\t"
        _string += "\n"
    print(_string)

def showKey(_rejilla, _size):
    _string = ''
    for _x in range(_size):
        for _y in range(_size):
            _k = str(_x)+'-'+str(_y)
            if _k in _rejilla.keys():
                _string += 'X' + "\t"
            else:
                _string += ' ' + "\t"
        _string += '\n'
    print(_string)

def generateTabKey(_mess,_size):
    _count = 0
    _table = [ [' '] * _size for x in range(_size)]
    _points = {}


    while _count < (len(_mess)/3):
        _x = int(random() * _size)
        _y = int(random() * _size)       

        if _table[_x][_y] == ' ':
            _table[_x][_y] = 'X'
            _count += 1
            _k = str(_x)+'-'+str(_y)
            if not _k in _points.keys():
                _points[_k] = [_x, _y]

    return _table, _points

def rotateKey(_table, _size):
    _ntable = {}
    for _cel in _table:
        _x = _table[_cel][1]
        _y = _size - (_table[_cel][0] + 1)
        _k = str(_x)+'-'+str(_y)
        if not _k in _ntable.keys():
            _ntable[_k] = [_x, _y]
    return _ntable

def encrypt(_message, _key, _size):   
    
    _tmpKey = [[_key[_k][0], _key[_k][1]] for _k in _key]
    _keyOrd = sorted(_tmpKey, key = lambda x: (x[0], x[1]))
    _newKey = _key
    _keysRotate = {}
    _tabsRotate = {}
    _tmpTab = [ [''] * _size for x in range(_size)] 

    _table = [ [''] * _size for x in range(_size)]  
    _i = 0

    for _turn in range(4):
        _keysRotate['rotate'+str(_turn)] = _newKey 
        for _pts in _keyOrd:
            if _i < len(_message):
                _table[_pts[0]][_pts[1]] += _message[_i]
                _tmpTab[_pts[0]][_pts[1]] += _message[_i]
                _i += 1
            else:
                if len(_table[_pts[0]][_pts[1]]) == 0:
                    _let = 65
                    _inc = int(random() * (26))
                    _table[_pts[0]][_pts[1]] += chr(_let+_inc) 
                    _tmpTab[_pts[0]][_pts[1]] += chr(_let+_inc)       

        _tabsRotate['rotate'+str(_turn)] = _tmpTab    
        _tmpTab = [ [''] * _size for x in range(_size)]       

        _keyOrd = []
        _newKey = rotateKey(_newKey, _size)
        _tmpKey = [[_newKey[_k][0], _newKey[_k][1]] for _k in _newKey]
        _keyOrd = sorted(_tmpKey, key = lambda x: (x[0], x[1]))

    for _x in range(_size):
        for _y in range(_size):
            if len(_table[_x][_y]) == 0:
                _let = 65
                _inc = int(random() * (26))
                _table[_x][_y] = chr(_let+_inc)

    return _table, _tabsRotate, _keysRotate

def desencrypt(_tab, _key, _size):
    _table = _tab
    _tmpKey = [[_key[_k][0], _key[_k][1]] for _k in _key]
    _keyOrd = sorted(_tmpKey, key = lambda x: (x[0], x[1]))
    _newKey = _key
    _tempTable = [ [''] * _size for x in range(_size)] 
    _keysRotate = {}
    _tabsRotate = {}
    _string = ''
    _i = 0
    for _turn in range(4):
        for _pts in _keyOrd:

            _keysRotate['rotate'+str(_turn)] = _newKey
            _letters = _table[_pts[0]][_pts[1]]

            if len(_letters) > 1:
                _table[_pts[0]][_pts[1]] = _letters[1:]
            _string += _letters[0]
            _tempTable[_pts[0]][_pts[1]] = _letters[0]

        _tabsRotate['rotate'+str(_turn)] = _tempTable
        _tempTable = [ [''] * _size for x in range(_size)]


        
        _keyOrd = []
        _newKey = rotateKey(_newKey, _size)
        _tmpKey = [[_newKey[_k][0], _newKey[_k][1]] for _k in _newKey]
        _keyOrd = sorted(_tmpKey, key = lambda x: (x[0], x[1]))  

    return _string, _tabsRotate, _keysRotate

def cipher(request):
    
    _size= request.GET.get('size')
    _message = request.GET.get('message')
    _message = preprocess(_message)       
    _keysRotate = {}
    _tabsRotate = {}
    table, key = generateTabKey(_message,int(_size))    
    _tab, _tabsRotate, _keyRotate = encrypt(_message, key, int(_size))    
    _result = {}
    _result['preproc'] = _message
    _result['tabs'] = _tabsRotate
    _result['rotations'] = _keyRotate
    _result['cipher'] = _tab
    writeFile(json.dumps(key), "clave.txt")
    writeFile(json.dumps(_tab), "salida.txt")

    return HttpResponse(json.dumps(_result))

def writeFile(text,name_file):
    if len(text)>0:
        f = open( name_file, 'w')
        f.write(text)
        f.close()

def readFile(name_file):
    f = open(name_file, "r")
    _string = ''
    for x in f:
        _string += x
    f.close()
    return _string;

def descipher(request):
    
    _key = readFile("clave.txt")
    _table = readFile("salida.txt")  
    _key = eval(_key)
    _table = eval(_table)
    _size = len(_table)

    string, _tabsRotate, _keyRotate = desencrypt(_table, _key, int(_size))
    _result = {}
    _result['tabs'] = _tabsRotate
    _result['descipher'] = string 

    return HttpResponse(json.dumps(_result)) 


def getPage(request):    
    
    return render(request, 'index.html', {})
