# -*- coding: utf-8 -*-
"""
Created on Sat Feb 26 01:12:50 2022

@author: Steve
"""
import math
import sys
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto import Random
from Crypto.Util import Counter

print(len("11010100110111101111001011000010110111001110100111100000"))

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


#When encrypting it produces a rand 16 byte array, but only uses the first 8 to 
#avoid counter wrap arround. The rest of the IV is produced by the initial counter
#that is initialized to 0. The same goes for decrypting, only the first 8 bytes of
#the first block will be used to establish the cipher scheme.
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
        
        if int(keySize) != 128:
            return sys.stderr.write("Unacceptable key size, try again")
        
        if (len(myKey)) != int(keySize):
            return sys.stderr.write("KeySize and given key do NOT MATCH, calculation error may occur.")
        
    
        baKey = getKeyInBytes(myKey) #keyString in bytes
        
        if operation == 'encrypt':
            byteNonce = Random.get_random_bytes(8)
            
                
            #print(len(holdNonce))
            
            #byteNonce = bytearray(holdNonce)
            cipher = AES.new(baKey, AES.MODE_CTR, nonce = byteNonce)
            
            
            with open(outFile, 'ab') as f:
                f.write(byteNonce)
                
            curPT = []
            x = 0
            while x < 4096:
                curPT.append(inputBA[x])
                x = x + 1
            
            #print(len(curPT))
            bytePT = bytearray(curPT)
                
            ciphertext = cipher.encrypt(pad(inputBA, AES.block_size))
            
            with open(outFile, 'ab') as f:
                f.write(ciphertext)
            
            
            
            with open(outFile, 'rb') as f:
                content = f.read()
            
            
        elif operation == 'decrypt':
            extractIV = []
            for x in range(0, 8):
                extractIV.append(inputBA[x])
                
            extractCT = []
            for x in range(8, len(inputBA)):
                extractCT.append(inputBA[x])
                
            byteCT = bytearray(extractCT)
                
            
                
            byteNonce = bytearray(extractIV)
            
            cipher = AES.new(baKey, AES.MODE_CTR, nonce = byteNonce)
            
            plaintext = unpad(cipher.decrypt(byteCT), AES.block_size)
            
    
            with open(outFile, 'ab') as f:
                f.write(plaintext)
            
        else:
            return sys.stderr.write("Operation not available.")    
            
        
if __name__ == "__main__":
    main()        
        