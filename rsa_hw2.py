# -*- coding: utf-8 -*-
"""
Created on Mon Feb 28 17:45:01 2022

@author: Steve
"""

import math
import sys
import random

def primeNum(x):
    i = 2
    while i <= math.sqrt(x):
        if (x % i) < 1:
            return False
        i = i + 1
    return x > 1

def checkRange(x):
    if x > 50 and x < 100:
        return True
    else:
        return False
    
def inputInRange(x, N):
    if x > 0 and x < N:
        return True
    else:
        return False

def extended_gcd(a,b):
    old_r, r = a, b
    old_s, s = 1, 0
    old_t, t = 0, 1
    
    while r != 0:
        quotient = math.floor(old_r / r)
        
        old_r, r = r, old_r - quotient * r
        old_s, s = s, old_s - quotient * s
        old_t, t = t, old_t - quotient * t
        
    #old_t is inverse of e    
    return [old_r, old_s, old_t]


def main():
    if len(sys.argv) != 5:
        return sys.stderr.write("Number of arguments is  incorrect, please check command line.\n")
    else:
        operation = sys.argv[1]
        inputStr = sys.argv[2]
        strM = sys.argv[3]
        strN = sys.argv[4]
        
        inputNum = int(inputStr)
        p = int(strM)
        q = int(strN)
    
        
        if operation == 'encrypt':
            if checkRange(p) == False:
                return sys.stderr.write("m is NOT within appropriate range.")
            if checkRange(q) == False:
                return sys.stderr.write("n is NOT within appropriate range.")
            
            if primeNum(p) == False:
                return sys.stderr.write("p is NOT a prime number, try again.")
            if primeNum(q) == False:
                return sys.stderr.write("q is NOT a prime number, try again.")
            
            
            N = p * q
            
            if inputInRange(inputNum, N) == False:
                return sys.stderr.write("Unacceptable input number, try again.")
            
            phiN = (q - 1) * (p - 1)
            #print(phiN)
            
            potentialE = []
            for x in range(2, phiN):
                findGCD = extended_gcd(phiN, x)
                if findGCD[0] == 1:
                    potentialE.append(x)
            #print(potentialE)
            
            e = random.choice(potentialE)
            #print(e)
            ePhi_gcd = extended_gcd(phiN, e)
            inverseE = ePhi_gcd[2]
            d = (inverseE) % phiN
            #print(d)
            
            cipherText = pow(inputNum, e) % N
            
            FinalString = "ciphertext = " + str(cipherText) + ", Private Key: (" + str(d) + ", " + str(N) + "), Public Key: (" + str(e) + ", " + str(N) + ")"
            
            print(FinalString)
            
            print(pow(4279, 479) % 5141)
            
        elif operation == 'decrypt':
            d = int(strM)
            N = int(strN)
            
            plaintxt = pow(inputNum, d) % N
            
            print("Plaintext = " + str(plaintxt))
            
        else:
            return sys.stderr.write("Operation not available.")
        
        
        
        
            
if __name__ == "__main__":
    main()