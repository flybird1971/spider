#!/usr/bin/env python
# coding:utf-8

import base64
from Crypto import Random
from Crypto.PublicKey import RSA


"""
    install PyCrpyto 
        windows : pip install PyCrpyto
        linux   : pip install PyCrpyto

"""


class MyRsa(object):

    def __init__(self, privateKeyFile=None, publicKeyFile=None):

        self.privateKeyFile = privateKeyFile
        self.publicKeyFile = publicKeyFile
        self.privateKey = None
        self.publicKey = None

    def setPrivateKeyFile(self, privateKeyFile):

        self.privateKeyFile = privateKeyFile
        return self

    def setPublicKeyFile(self, publicKeyFile):

        self.publicKeyFile = publicKeyFile
        return self

    def readPrivateKey(self):

        if not self.privateKey:
            privatekey = open(self.privateKeyFile, "r")
            self.privateKey = RSA.importKey(privatekey)

        return self.privateKey

    def readPublicKey(self):

        if not self.publicKey:
            publickey = open(self.privateKeyFile, "r")
            self.publicKey = RSA.importKey(publickey)

        return self.publicKey

    def encrypt(self, plaintext):

        m = self.readPrivateKey()
        random_generator = Random.new().read
        ciphertuple = m.encrypt(plaintext, random_generator)
        return base64.b64encode(ciphertuple[0])

    def decrypt(self, ciphertext):

        m = self.readPublicKey()
        ciphertext = base64.b64decode(ciphertext)
        plaintext = m.decrypt(ciphertext)
        return plaintext

    def generateKeyPairs(self):

        keys = RSA.generate(1024)
        privHandle = open(self.privateKeyFile, 'wb')
        privHandle.write(keys.exportKey('PEM'))
        privHandle.close()

        pubHandle = open(self.publicKeyFile, 'wb')
        pubHandle.write(keys.publickey().exportKey("PEM"))
        pubHandle.close()
        return self

rsa = MyRsa('private_key.pem', 'public_key.pem')
# rsa.generateKeyPairs()
ciphertext = rsa.encrypt('hello222')
print ciphertext
print rsa.decrypt(ciphertext)
