#!/usr//bin/python3
import os,sys

sys.path.append('/usr/local/lib/python3.7/')
sys.path.append('/usr/local/Cellar/numpy')
import hashlib
import random
import string
import json
import binascii
import numpy as np
import pandas as pd
import pylab as pl
import logging
import datetime
import collections

from Crypto import Random
from Crypto.PublicKey import RSA
import base64

def generate_keys():
	# RSA modulus length must be a multiple of 256 and >= 1024
	modulus_length = 256*4 # use larger value in production
	privatekey = RSA.generate(modulus_length, Random.new().read)
	publickey = privatekey.publickey()
	return privatekey, publickey

def encrypt_message(a_message , publickey):
	encrypted_msg = publickey.encrypt(a_message, 32)[0]
	encoded_encrypted_msg = base64.b64encode(encrypted_msg) # base64 encoded strings are database friendly
	return encoded_encrypted_msg

def decrypt_message(encoded_encrypted_msg, privatekey):
	decoded_encrypted_msg = base64.b64decode(encoded_encrypted_msg)
	decoded_decrypted_msg = privatekey.decrypt(decoded_encrypted_msg)
	return decoded_decrypted_msg

def verify_sign(public_key_loc, signature, data):
    '''
    Verifies with a public key from whom the data came that it was indeed 
    signed by their private key
    param: public_key_loc Path to public key
    param: signature String signature to be verified
    return: Boolean. True if the signature is valid; False otherwise. 
    '''
    from Crypto.PublicKey import RSA 
    from Crypto.Signature import PKCS1_v1_5 
    from Crypto.Hash import SHA256 
    from base64 import b64decode 
    pub_key = open(public_key_loc, "r").read() 
    rsakey = RSA.importKey(pub_key) 
    signer = PKCS1_v1_5.new(rsakey) 
    digest = SHA256.new() 
    # Assumes the data is base64 encoded to begin with
    digest.update(b64decode(data)) 
    if signer.verify(digest, b64decode(signature)):
        return True
    return False

def sha256(message):
    return hashlib.sha256(message.encode('ascii')).hexdigest()

def hexDifficultyTag(size=1):
    """ 
    Description:
        This returns a string of random hex values to be used as our 
        fake mining value to verify a transaction. 
    Used By:
        mine(message, difficulty) - where difficulty is a string from
                                    this function (long = harder)
    Returns:
        string : hex values if given size
    """
    tag = ""
    digits = [x for x in range(10)]
    digits.extend(['a','b','c','d','e','f'])

    random.shuffle(digits)

    for i in range(size):
        tag += str(digits[0])
        random.shuffle(digits)
    return tag

def mine(message, difficulty=1):
    """
    Description:
        This method is our fake "miner" that will continue to generate sha256
        strings until the first 'x' "digits" match the prefix we obtained from
        the `hexDifficultyTag` function
    """
    assert difficulty >= 1
    # prefix = '1' * difficulty

    prefix = hexDifficultyTag(difficulty)

    i = 0
    #for i in range(1000):
    while True:
        i = i + 1
        # if i % 1000 == 0:
        #     print(f"{str(i)} iterations ...")
        digest = sha256(str(hash(message)) + str(i))
        if digest.startswith(prefix):
            print (f"Found {prefix} in {digest} after {i} iterations ...")
            return digest

if __name__=='__main__':

    # for i in range(5,100):
    #     mine("hello world",i)

    a_message = "The quick brown fox jumped over the lazy dog".encode('utf-8')
    privatekey , publickey = generate_keys()
    encrypted_msg = encrypt_message(a_message , publickey)
    decrypted_msg = decrypt_message(encrypted_msg, privatekey)

    pubkeyf = open("public_rsa.pem","w") 
    pubkeyf.write(str(publickey))
    pubkeyf.close()

    privkeyf = open("private_rsa.pem","w") 
    privkeyf.write(str(privatekey))
    privkeyf.close()


    print ("%s - (%d)" % (privatekey.exportKey() , len(privatekey.exportKey())))
    print ("%s - (%d)" % (publickey.exportKey() , len(publickey.exportKey())))
    print (" Original content: %s - (%d)" % (a_message, len(a_message)))
    print ("Encrypted message: %s - (%d)" % (encrypted_msg, len(encrypted_msg)))
    print ("Decrypted message: %s - (%d)" % (decrypted_msg, len(decrypted_msg)))

    print(verify_sign("public_rsa.pem", "private_rsa.pem", encrypted_msg))