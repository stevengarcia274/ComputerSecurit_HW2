# -*- coding: utf-8 -*-
"""
Created on Fri Feb 25 14:56:49 2022

@author: Steve
"""
import math
import sys



def getKeyInBytes(keyString):
    refitString = ""
    
    #check key is a multiple of 8
    #if NOT pad with zeros
    if (len(keyString) % 8) != 0: 
        x = 0
        while x < (8 - len(keyString)):
            refitString = refitString + "0"
            x = x + 1
        keyString = refitString + keyString    
        
    t = 0
    listBytes = [] #list that will contain bytes (8-bits)
    sepBytes = "" #seperate into bytees
    z = 0
    for t in range(0, len(keyString)):
        sepBytes = sepBytes + keyString[t]
        z = z + 1
        if z == 8:
            listBytes.append(int(sepBytes, 2))
            #print(sepBytes)
            sepBytes = ""
            z = 0
    
    keyBA = bytearray(listBytes)#key in byte array format
    
    return keyBA

def getByteArrayValues(inputBA):
    baSize = len(inputBA)
    regList = [None] * baSize
    
    x = 0
    while x < baSize:
        regList[x] = inputBA[x]
        x = x + 1
        
    return regList


def main():
    if len(sys.argv) != 6:
        return sys.stderr.write("Number of arguments is  incorrect, please check command line.\n")
    else:
        keySize = sys.argv[1]
        keyFile = sys.argv[2]
        inFile = sys.argv[3]
        outFile = sys.argv[4]
        operation = sys.argv[5]
        
        #key should be located in a text file, whose content is a binary string
        with open(keyFile, 'r') as f:
            myKey = f.read()
            
        with open(inFile, 'rb') as f:
            inputBA = f.read()
        
        if not(128 >= int(keySize) >= 40):
            return sys.stderr.write("Unacceptable key size, try again")
        
        if (len(myKey)) != int(keySize):
            return sys.stderr.write("KeySize and given key do NOT MATCH, calculation error may occur.")
        
    
        baKey = getKeyInBytes(myKey) #keyString in bytes
        
        x = 0
        #initialize list S with values 1 to 255
        S = []
        while x < 256:
            S.append(x)
            x = x + 1
        #print(S)
        
        #keySchedule Algorithm
        j = 0
        for i in range(0, 255):
            j = (j + S[i] + baKey[i % len(baKey)]) % 256
            temp = S[i]
            S[i] = S[j]
            S[j] = temp
            
        #print(S)
        
        if operation == 'encrypt':
            #print('encrypt')
            numItr = math.ceil(len(inputBA) / 4096) #number of 4kb chuncks needed
            
            startAt = 0 #variables to keep track of where we are in the file
            endAt = 4096
            
            for m in range(0, numItr):
                #print(m)
                curPT = []
                if m == numItr - 1:
                    lenStream = len(inputBA) - startAt #keyStreamLength
                    i = 0
                    j = 0
                    w = 0
                    
                    keyStream = [] #keyStream for cur chunk of file
                    while w < (lenStream + 3072):
                        i = (i + 1) % 256
                        j = (j + S[i]) % 256
                        temp = S[i]
                        S[i] = S[j]
                        S[j] = temp
                        apK = S[(S[i] + S[j]) % 256]
                        keyStream.append(apK)
                        w = w + 1 
                    
                    #remove first 3072 bytes from generated keyStream
                    realKey = []
                    for x in range(3072, len(keyStream)):
                        realKey.append(keyStream[x])
                    
                    #extract current chunck of PT from inputFile
                    for x in range(startAt, len(inputBA)):
                        curPT.append(inputBA[x])
                        #pass
                        
                    #print(len(curPT) == len(realKey))
                    addCT = [] #list to hold values of CT
                    
                    #calculate current chunck of CT (xor)
                    for x in range(0, len(curPT)):
                        xorData = curPT[x] ^ realKey[x]
                        addCT.append(xorData)
                        
                    with open(outFile, 'ab') as f:
                        byteCT = bytearray(addCT)
                        #append current portion of CT to binary file
                        f.write(byteCT)
                        
                else:
                    lenStream = endAt - startAt #keyStreamLength
                    i = 0
                    j = 0
                    w = 0
                    
                    keyStream = [] #keyStream for cur chunk of file
                    while w < (lenStream + 3072):
                        i = (i + 1) % 256
                        j = (j + S[i]) % 256
                        temp = S[i]
                        S[i] = S[j]
                        S[j] = temp
                        apK = S[(S[i] + S[j]) % 256]
                        keyStream.append(apK)
                        w = w + 1
                    
                    realKey = []
                    #remove first 3072 bits
                    for x in range(3072, len(keyStream)):
                        realKey.append(keyStream[x])
                    
                    #extract current chunck of PT from inputFile
                    for x in range(startAt, endAt):
                        curPT.append(inputBA[x])
                        #pass
                        #print(emptyList[x])
                    startAt = endAt
                    endAt = endAt + 4096
            
                    addCT = []
                    for x in range(0, len(curPT)):
                        xorData = curPT[x] ^ realKey[x]
                        addCT.append(xorData)
                        
                    with open(outFile, 'ab') as f:
                        byteCT = bytearray(addCT)
                        f.write(byteCT)
                    
            
        elif operation == 'decrypt':
                #print('decrypt')
                numItr = math.ceil(len(inputBA) / 4096)
                
                startAt = 0
                endAt = 4096
                
                for m in range(0, numItr):
                    #list to hold current chunck of CT we're decrypting
                    curCT = []
                    if m == numItr - 1:
                        lenStream = len(inputBA) - startAt #keyStreamLength
                        i = 0
                        j = 0
                        w = 0
                        
                        keyStream = [] #keyStream for cur chunk of file
                        while w < (lenStream + 3072):
                            i = (i + 1) % 256
                            j = (j + S[i]) % 256
                            temp = S[i]
                            S[i] = S[j]
                            S[j] = temp
                            apK = S[(S[i] + S[j]) % 256]
                            keyStream.append(apK)
                            w = w + 1 
                        
                        #remove first 3072 bytes from generated keyStream
                        realKey = []
                        for x in range(3072, len(keyStream)):
                            realKey.append(keyStream[x])
                        
                        #extract current chunck of CT from inputFile
                        for x in range(startAt, len(inputBA)):
                            curCT.append(inputBA[x])
                            #pass
                            #print(emptyList[x])
                            
                        addPT = []
                        
                        #calculate current chunck of PT
                        for x in range(0, len(curCT)):
                            xorData = curCT[x] ^ realKey[x]
                            addPT.append(xorData)
                            
                        with open(outFile, 'ab') as f:
                            bytePT = bytearray(addPT)
                            #append current portion of PT to output binary file
                            f.write(bytePT)
                            
                    else:
                        lenStream = endAt - startAt #keyStreamLength
                        i = 0
                        j = 0
                        w = 0
                        
                        keyStream = [] #keyStream for cur chunk of file
                        while w < (lenStream + 3072):
                            i = (i + 1) % 256
                            j = (j + S[i]) % 256
                            temp = S[i]
                            S[i] = S[j]
                            S[j] = temp
                            apK = S[(S[i] + S[j]) % 256]
                            keyStream.append(apK)
                            w = w + 1
                        
                        realKey = []
                        for x in range(3072, len(keyStream)):
                            realKey.append(keyStream[x])
                        
                        for x in range(startAt, endAt):
                            curCT.append(inputBA[x])
                            #pass
                            #print(emptyList[x])
                        
                        #increment startAt and endAt
                        startAt = endAt
                        endAt = endAt + 4096
                        
                        addPT = []
                        #calculate PT values to be added to output binary file
                        for x in range(0, len(curCT)):
                            xorData = curCT[x] ^ realKey[x]
                            addPT.append(xorData)
                            
                        with open(outFile, 'ab') as f:
                            bytePT = bytearray(addPT)
                            f.write(bytePT)
                #print(S)
                
        else:
            return sys.stderr.write("Operation not available.")
                
                
        #with open(outFile, 'rb') as f:
                #outputBA = f.read()
        #print(len(outputBA))   
        #print("this is the FINAL TEST")
        #print(len(inputBA))
        #print(len(outputBA) == len(inputBA))
            
if __name__ == "__main__":
    main()
