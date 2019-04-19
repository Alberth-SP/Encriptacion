from django.shortcuts import render
from random import random 
from django.http import JsonResponse
from django.conf import settings
from django.conf.urls.static import static
from django.http import HttpResponse
from django.utils.encoding import smart_str

from wsgiref.util import FileWrapper
from random import random 
import json
import re
import math
import os


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


def checkKey(_key, _size):
    _count = 0    
    _points = {}

    for _k in _key:
        X = _key[_k][0]
        Y = _key[_k][1]
        K = str(X)+'-'+str(Y)   
        _keys = []
        _x = X
        _y = Y

        for i in range(4):
            _k = str(_x)+'-'+str(_y)                
            _keys.append(_k)
            _temp = _x
            _x = _y
            _y = _size - (_temp + 1) 

        _lista = [ k for k in _keys if k in _points.keys() ]

        if not _lista:            
            _points[K] = [X, Y]
        else:
            print(_lista)
            print(_lista)
            return False

    return True


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

        _newKey = rotateKey(_newKey, _size)
        _tmpKey = [[_newKey[_k][0], _newKey[_k][1]] for _k in _newKey]
        _keyOrd = sorted(_tmpKey, key = lambda x: (x[0], x[1]))        

    for _i in range(_size):
        for _j in range(_size):            
            _descipher += _table[_i][_j]
            
    return _descipher, _desciphers, _keys, _table

def down_descipher(request):  

    file_path = os.path.join(settings.MEDIA_ROOT, "descipher.txt")    
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="text/plain")
            response['Content-Disposition'] = 'attachment; filename=' + os.path.basename(file_path)           
            return response

def down_cipher(request):  

    file_path = os.path.join(settings.MEDIA_ROOT, "cipher.txt")    
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="text/plain")
            response['Content-Disposition'] = 'attachment; filename=' + os.path.basename(file_path)           
            return response

def down_key(request):  

    file_path = os.path.join(settings.MEDIA_ROOT, "key.txt")    
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="text/plain")
            response['Content-Disposition'] = 'attachment; filename=' + os.path.basename(file_path)           
            return response


def cipher(request):
    
    _size = request.GET.get('size')
    _message = request.GET.get('message')
    _message = preprocess(_message) 
    _result = {}
    _size = int(_size)

    if(len(_message) == 0):
        _result['error'] = "MENSAJE NO VALIDO"
        return HttpResponse(json.dumps(_result))
    if((_size <= 1) or ((_size%2) != 0) or ((_size * _size) < len(_message))):
        _result['error'] = "TAMAÑO DE LA CLAVE NO VALIDA"
        return HttpResponse(json.dumps(_result))

    _keysRotate = {}
    _tabsRotate = {}

    key = generateTabKey(_message, int(_size))    
    cipher, ciphers, keys, table = encrypt(_message, key, int(_size))   
   
    _result['preproc'] = _message
    _result['table'] = table
    _result['keys'] = keys
    _result['ciphers'] = ciphers
    _result['cipher'] = cipher
   
    writeFile(json.dumps(key), "key.txt")
    writeFile(json.dumps(cipher), "cipher.txt")

    return HttpResponse(json.dumps(_result))

def writeFile(text,name_file):

    file_path = os.path.join(settings.MEDIA_ROOT, name_file)
    if len(text)>0:
        f = open( file_path, 'w')
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
    
    _key= request.GET.get('key')
    _message = request.GET.get('message')
    _size = 0
    _result = {}
    try:
        _key = eval(_key)
        _message = eval(_message)
        _size = len(_message)
        _size = int(math.sqrt(_size)) 
        print(_key)
        print(_message)       
        print(_size)
    except:
        _result['error'] = "MENSAJE O CLAVE NO VALIDOS"
        return HttpResponse(json.dumps(_result))  

    if (_size%2) != 0:
        _result['error'] = "TAMAÑO DEL MENSAJE NO VALIDO"
        return HttpResponse(json.dumps(_result))

    if (not checkKey(_key,_size)) or (len(_key)*4 != len(_message)):
        _result['error'] = "TAMAÑO DE LA CLAVE NO VALIDA"
        return HttpResponse(json.dumps(_result))

    descipher, desciphers, keys, table = desencrypt(_message, _key, _size)  

    _result['size'] = _size
    _result['message'] = _message
    _result['table'] = table
    _result['keys'] = keys
    _result['desciphers'] = desciphers
    _result['descipher'] = descipher
    writeFile(json.dumps(descipher), "descipher.txt")

    return HttpResponse(json.dumps(_result)) 


def getPage(request):    
    
    return render(request, 'index.html', {})
