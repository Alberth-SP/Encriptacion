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

def generateTabKey(_mess, _size):
    _count = 0    
    _points = {}

    while _count < ((_size*_size)/4):
        _x = int(random() * _size)
        _y = int(random() * _size)
        X = _x
        Y = _y
        K = str(_x)+'-'+str(_y)
        _keys = []

        for i in range(4):
            _k = str(_x)+'-'+str(_y)
            _keys.append(_k)
            _temp = _x
            _x = _y
            _y = _size - (_temp + 1) 

        _lista = [ 1 for k in _keys if k in _points.keys() ]

        if not _lista:
            _points[K] = [X, Y]
            _count += 1

    return _points

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

    _table = [ [''] * _size for x in range(_size)]
    _index = 0
    _cipher = ''
    _tmpKey = [[_key[_k][0], _key[_k][1]] for _k in _key]
    _keyOrd = sorted(_tmpKey, key = lambda x: (x[0], x[1]))

    for i in range(_size):
        for j in range(_size):
            if _index < len(_message):
                _table[i][j] = _message[_index]
                _index += 1
            else:
                _let = 65
                _inc = int(random() * (26))
                _table[i][j] = chr(_let+_inc)    
    
    _newKey = _key
    _keys = {}
    _ciphers = {}
    _tmp = ""  

    for _turn in range(4):
        _keys['rotate'+str(_turn)] = _newKey 
        for _k in _keyOrd:
            _cipher += _table[_k[0]][_k[1]]
            _tmp += _table[_k[0]][_k[1]]                 

        _ciphers['rotate'+str(_turn)] = _tmp    
        _tmp = ""
        _keyOrd = [] 
        _newKey = rotateKey(_newKey, _size)
        _tmpKey = [[_newKey[_k][0], _newKey[_k][1]] for _k in _newKey]
        _keyOrd = sorted(_tmpKey, key = lambda x: (x[0], x[1]))
   
    return _cipher, _ciphers, _keys, _table

def desencrypt(_message, _key, _size):   
    
    _desciphers = {}
    _keys = {}
    _descipher = ""
    _temp = ""
    _newKey = _key
    _table = [ [''] * _size for x in range(_size)]
    _index = 0

    _tmpKey = [[_key[_k][0], _key[_k][1]] for _k in _key]
    _keyOrd = sorted(_tmpKey, key = lambda x: (x[0], x[1]))

    for _turn in range(4):
        _keys['rotate'+str(_turn)] = _newKey
        for _k in _keyOrd:
            if _index < len(_message):                
                _table[_k[0]][_k[1]] += _message[_index]           
                _temp += _message[_index]
                _index += 1        
        
        _desciphers['rotate'+str(_turn)] = _temp
        _temp = ""
        _keyOrd = []  
        print("================================")
        print(_newKey)
        print("================================")
        _newKey = rotateKey(_newKey, _size)
        _tmpKey = [[_newKey[_k][0], _newKey[_k][1]] for _k in _newKey]
        _keyOrd = sorted(_tmpKey, key = lambda x: (x[0], x[1]))

        

    for _i in range(_size):
        for _j in range(_size):            
            _descipher += _table[_i][_j]


    return _descipher, _desciphers, _keys, _table

def cipher(request):
    
    _size= request.GET.get('size')
    _message = request.GET.get('message')
    _message = preprocess(_message)  

    _keysRotate = {}
    _tabsRotate = {}

    key = generateTabKey(_message, int(_size))    
    cipher, ciphers, keys, table = encrypt(_message, key, int(_size))   

    _result = {}
    _result['preproc'] = _message
    _result['table'] = table
    _result['keys'] = keys
    _result['ciphers'] = ciphers
    _result['cipher'] = cipher
   
    writeFile(json.dumps(key), "clave.txt")
    writeFile(json.dumps(cipher), "salida.txt")

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
    _message = readFile("salida.txt")  
    _key = eval(_key)
    _message = eval(_message)
    _size = request.GET.get('size')
    print("=======================")
    print(_message)
    print(_key)
    print(_size)
    print("=======================")

    descipher, desciphers, keys, table = desencrypt(_message, _key, int(_size))  

    _result = {}
    _result['message'] = _message
    _result['table'] = table
    _result['keys'] = keys
    _result['desciphers'] = desciphers
    _result['descipher'] = descipher

    return HttpResponse(json.dumps(_result)) 


def getPage(request):    
    
    return render(request, 'index.html', {})
