Steven Garcia
Computer Security
HW2
28 February 2022

All coding was done using Python 3.

For Problems 1 and 2, input file arguments are expected as binary files, but the key file should be a .txt file 
containing a string of 1's and 0's

Problem 1

Note: KeySize argument should represent the size of the key in bits, the program handles pads it if it is not a 
multiple of 8 and converts it to its byte equivalant.

py rc4_hw2.py 56 rc4_keyFile.txt a.plaintext a.ciphertext encrypt
py rc4_hw2.py 56 rc4_keyFile.txt a.ciphertext b.plaintext decrypt

Problem 2

Please note that for my AES program I generated a random 8-byte array that was used as the nonce/IV for encryption,
I than appened those bytes to the begining of the output file. The reason I chose an 8-byte array and not 16 was to
avoid this reoccuring error I kept getting that said, "counter wrap arround." That means that when decrypting, the 
first 8-bytes are expected to be the IV, in order to get the correct plaintext output.

py aes_hw2.py 128 aes_keyFile.txt a.plaintext a.ciphertext encrypt
py aes_hw2.py 128 aes_keyFile.txt a.ciphertext b.plaintext decrypt

Problem 3

py rsa_hw2.py encrypt 5000 53 97
py rsa_hw2.py decrypt 1624 1757 5141

Problem 4

Only input3.pdf was corrupted.

py verify_hw2.py in1.pdf fa07c3b6d8016ef612044188eacef
py verify_hw2.py in2.pdf pq07c3b6d801213456044188eacef