'''
Copyright 2019 Agnese Salutari.
Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on
an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and limitations under the License
'''

# Dependencies
from Utils import ModularArithmetics

class ElGamalKeyPair:
    '''
    b = a^(e) (mod p)
        public key = [b, a, p].
        private key = e.
        p is a prime.
    '''
    __MA = None # ModualrAritmetics()
    __publicKey = None # list of 3 integers: [b, a, p].
    __privateKey = None # integer: e

    def __init__(self, pBounds=False, primesFilePath='primes50.txt'):
        '''
        b = a^(e) (mod p)
            public key = (p, a, b).
            private key = e.
            p is a prime.
        :param pBounds: list of 2 integers [optional]; inferior and superior limits of p.
            p has to be bigger than any block made of 3 letter ASCII representation bits, that is 16777216 = 2^(24).
        :param primesFilePath: string [oprional]; the path to a file containing prime numbers.
        '''
        self.__MA = ModularArithmetics()
        ma = self.getModArithmetics()
        if not pBounds:
            assert isinstance(primesFilePath, str)
            p = ma.randomPrimeFromFile(filePath=primesFilePath)
        else:
            assert isinstance(pBounds, list)
            assert len(pBounds) == 2
            assert isinstance(pBounds[0], int)
            assert pBounds[0] > 16777216
            assert isinstance(pBounds[1], int)
            p = ma.randomPrime(infBound=pBounds[0], supBound=pBounds[1])
        self.generate(p=p)

    def getPrivateKey(self):
        '''
        :return: integer: e.
        '''
        return self.__privateKey

    def getPublicKey(self):
        '''
        :return: list of 3 integers: [b, a, p].
        '''
        return self.__publicKey

    def getModArithmetics(self):
        '''
        :return: ModularArithmetics().
        '''
        return self.__MA

    def generate(self, p):
        '''
        Instantiates the keys.
        :param p: prime integer: the modulus.
        :return:
        '''
        assert isinstance(p, int)
        ma = self.getModArithmetics()
        # To generate a, we don't use a function that finds primitive roots (it would be time consuming).
        a = ma.randomInteger(2, p - 1)
        e = ma.randomInteger(2, p - 2)
        b = ma.modularPower(a=a, e=e, m=p)
        print('a = ' + str(a)) # Test
        print('e = ' + str(e)) # Test
        print('b = ' + str(b)) # Test
        self.__publicKey = [p, a, b]
        self.__privateKey = e
        self.print() # Test

    def print(self):
        '''
        Prints the keys in use.
        :return:
        '''
        print('b = a^(e) (mod p)')
        print('public key = [p, a, b] = ' + str(self.getPublicKey()))
        print('p is a prime.')
        print('private key = e = ' + str(self.getPrivateKey()) + '\n')


class ElGamalEncryption:
    __keys = None # ElGamalKeyPair().
    __MA = None # ModularArithmetics().

    def __init__(self, keyBounds=False, keyFile='primes50.txt'):
        '''
        Initializes __keys and __MA.
        :param keyBounds: list of 2 integers [optional]; the bounds of the keys modulus.
        :param keyFile: string [optional]; the path of the file containing the primes.
        '''
        self.__keys = ElGamalKeyPair(pBounds=keyBounds, primesFilePath=keyFile)
        self.__MA = self.__keys.getModArithmetics()

    def getKeys(self):
        '''
        :return: ElGamalKeyPair().
        '''
        return self.__keys

    def getModArithmetics(self):
        '''
        :return: ModularArithmetics().
        '''
        return self.__MA

    def textFormatter(self, plainText):
        assert isinstance(plainText, str)
        chrV = []
        for i in range(0, len(plainText)):
            chrV.append(plainText[i])
        # print('chrV: ' + str(chrV)) # Test
        while not (len(chrV) % 3 == 0):
            chrV.append(' ')
        # print(chrV) # Test
        binV = []
        i = 0
        while i < len(chrV):
            binCombo = '{:0>8}'.format(format(ord(chrV[i]), "b")) + \
                       '{:0>8}'.format(format(ord(chrV[i + 1]), "b")) + \
                       '{:0>8}'.format(format(ord(chrV[i + 2]), "b"))
            binV.append(binCombo)
            i += 3
        # print(binV) # Test
        fText = []
        for elem in binV:
            fText.append(int(elem, 2))
        # print(fText) # Test
        return fText

    def textDeFormatter(self, fVector):
        assert isinstance(fVector, list)
        binV = []
        for elem in fVector:
            binCombo = '{:0>24}'.format(format(elem, "b"))
            binV.append(binCombo)
        # print(binV) # Test
        chrV = []
        for elem in binV:
            str1 = elem[0: 8]
            str2 = elem[8: 16]
            str3 = elem[16: 24]
            chrV.append(chr(int(str1, 2)))
            chrV.append(chr(int(str2, 2)))
            chrV.append(chr(int(str3, 2)))
            # print(chrV) # Test
        return chrV

    def encrypt(self, data, receiverPubKey):
        '''
        Encrypts data.
        :param data: string; the data to encrypt.
        :param receiverPubKey: list of 3 integers: [p, a, b] ; the public key of the receiver.
        :return: a list of 2 integers: [r, tVector] = [a^(k), data * b^(k) = data * a^(k*e)].
        '''
        print('Encrypting...')
        assert isinstance(receiverPubKey, list)
        assert len(receiverPubKey) == 3
        for rpk in receiverPubKey:
            assert isinstance(rpk, int)
        if not isinstance(data, str):
            data = str(data)
        ma = self.getModArithmetics()
        receiverP = receiverPubKey[0]
        receiverA = receiverPubKey[1]
        receiverB = receiverPubKey[2]
        k = ma.randomInteger(infBound=2, supBound=receiverP - 2)  # Secret for the sender
        y = ma.modularPower(a=receiverB, e=k, m=receiverP)
        r = ma.modularPower(a=receiverA, e=k, m=receiverP)
        print('r = a^(k) = ' + str(r))  # Test
        print('y = a^(e*k) = ' + str(y))  # Test
        tVector = self.textFormatter(data)
        print('Formatted Text: ' + str(tVector)) # Test
        for i in range(0, len(tVector)):
            print(tVector[i])
            tVector[i] = y * tVector[i]
            print(' -> ' + str(tVector[i]))
        print('Encryption Finished.')
        return [r, tVector]

    def decrypt(self, r, tVector):
        '''
        Decrypts tVector, a list containing encrypted characters.
        :param r: integer; r = a^(k).
        :param tVector: list of integers; it contains encrypted characters
        :return: string; the decrypted message.
        '''
        print('Decrypting...')
        assert isinstance(r, int)
        assert isinstance(tVector, list)
        ma = self.getModArithmetics()
        myP = self.getKeys().getPublicKey()[0]
        print('p = ' + str(myP)) # Test
        myPrivK = self.getKeys().getPrivateKey()
        print('privKey = ' + str(myPrivK)) # Test
        mVector = []
        print('r = ' + str(r))
        h = ma.modularPower(a=r, e=myPrivK, m=myP)
        print('h = ' + str(h)) # Test
        for i in range(0, len(tVector)):
            mVector.append(int(tVector[i] / h))
        print(mVector)
        print('Decryption Finished.')
        print('Formatted Text: ' + str(mVector))
        dfVector = self.textDeFormatter(mVector)
        print('Plain Text: ' + str(dfVector))
        return ''.join(dfVector)

    def decryptWithPrivK(self, r, tVector, p, privKey):
        '''
        Decrypts tVector, a list containing encrypted characters, using privKey as private key and p as modulus.
        :param r: integer; r = a^(k).
        :param tVector: list of integers; it contains encrypted characters
        :param p: prime integer; the modulus.
        :param privKey: integer; the private key.
        :return: string; the decrypted message.
        '''
        print('Decrypting...')
        assert isinstance(r, int)
        assert isinstance(tVector, list)
        ma = self.getModArithmetics()
        mVector = []
        h = ma.modularPower(a=r, e=privKey, m=p)
        print('h = ' + str(h)) # Test
        for i in range(0, len(tVector)):
            mVector.append(chr(int(tVector[i] / h)))
        print(mVector)
        print('Decryption Finished.')
        print('Formatted Text: ' + str(mVector))
        dfVector = self.textDeFormatter(mVector)
        print('Plain Text: ' + str(dfVector))
        return ''.join(dfVector)
