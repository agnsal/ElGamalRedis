
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

# Dependencies:
import random


class ModularArithmetics:

    def changeToPositive(self, x, m):
        '''
        Turns the negative integer x into a positive integer (mod m).
        :param x: negative integer.
        :param m: integer.
        :return: integer.
        '''
        assert isinstance(x, int)
        assert isinstance(m, int)
        while x < 0:
            x += m
        return x

    def isPrime(self, num):
        '''
        Verifies if num is prime.
        :param num: integer.
        :return: boolean.
        '''
        assert isinstance(num, int)
        assert num > 0
        if num < 2:
            return True
        else:
            for i in range(2, num):
                if (num % i) == 0:
                    return False
            return True

    def findPrimitiveRootsOfPrime(self, primeNumber): # Time consuming!!!
        '''
        Finds primitive roots of primeNumber.
        :param primeNumber: integer (a prime number).
        :return: list of integers.
        '''
        from sympy.ntheory.residue_ntheory import _primitive_root_prime_iter
        assert isinstance(primeNumber, int)
        assert self.isPrime(primeNumber)
        return list(_primitive_root_prime_iter(primeNumber))

    def randomInteger(self, infBound=1, supBound=10):
        '''
        Gives a random integer between infBount and supBound.
        :param infBound: integer.
        :param supBound: integer.
        :return: integer.
        '''
        assert isinstance(infBound, int)
        assert isinstance(supBound, int)
        return random.randint(infBound, supBound)

    def randomPrime(self, infBound=1, supBound=10):
        '''
        Gives a random prime between infBound and supBound.
        :param infBound: integer.
        :param supBound: integer.
        :return: integer.
        '''
        assert isinstance(infBound, int)
        assert isinstance(supBound, int)
        candidatePrime = random.randint(infBound, supBound)
        while not self.isPrime(candidatePrime):
            candidatePrime = random.randint(infBound, supBound)
        return candidatePrime

    def randomPrimeFromFile(self, filePath='primes50.txt'):
        '''
        https://primes.utm.edu/lists/small/millions/
        :param: filePath: string; the path of the file containing primes.
        :return: integer; a random prime.
        '''
        assert isinstance(filePath, str)
        file = open(filePath, 'r')
        fileList = file.readlines()
        primes = []
        for line in fileList:
            line = ' '.join(line.split())
            linePrimes = line.split(' ')
            for p in linePrimes:
                primes.append(p)
        return int(random.choice(primes))

    def randomPrimitiveRoot(self, primeNumber): # Uses a time consuming function to find primitive roots!!!
        '''
        Returns a random primitive root of primeNumber.
        :param primeNumber: integer (a prime number).
        :return: integer.
        '''
        assert isinstance(primeNumber, int)
        primitiveRoots = self.findPrimitiveRootsOfPrime(primeNumber)
        return random.choice(primitiveRoots)

    def listOfPrimesFromFile(self, filePath='smallPrimes.txt'):
        '''
        https://primes.utm.edu/lists/small/millions/
        :param: filePath: string; the path of the file containing primes.
        :return: list of integer.
        '''
        file = open(filePath, 'r')
        fileList = file.readlines()
        primes = []
        for line in fileList:
            line = ' '.join(line.split())
            linePrimes = line.split(' ')
            for p in linePrimes:
                if not p == '':
                    primes.append(int(p))
        return primes


    def modularMultiplication(self, x, y, m):
        '''
        Computes x * y (mod m).
        :param x: integer.
        :param y: integer.
        :param m: integer.
        :return: integer.
        '''
        assert isinstance(x, int)
        assert isinstance(y, int)
        assert isinstance(m, int)
        return x * y % m

    def modularPower(self, a, e, m):
        '''
        Computes a^(e) (mod m).
        :param a: integer.
        :param e: integer.
        :param m: integer.
        :return: integer.
        '''
        assert isinstance(a, int)
        assert isinstance(e, int)
        assert isinstance(m, int)
        res = 1
        a = a % m
        while (e > 0):
            # If e is odd, multiply x with result
            if ((e & 1) == 1):
                res = (res * a) % m
            # e must be even now
            e = e >> 1 # y = y/2
            a = (a * a) % m
        return res


    def findGCD(self, x, y):
        '''
        Finds Greatest Common Divisor of x and y.
        :param x: integer.
        :param y: integer.
        :return: integer.
        '''
        assert isinstance(x, int)
        assert isinstance(y, int)
        if x < y:
            return self.findGCD(y, x)
        elif x % y == 0:
            return y;
        else:
            z = x % y
            return self.findGCD(y, z)

    def egcd(self, a, b):
        '''
        Euclidean Extended Algorithm.
        :param a: integer.
        :param b: integer.
        :return: (g, x, y) such that a*x + b*y = g = gcd(a, b).
        '''
        assert isinstance(a, int)
        assert isinstance(b, int)
        if a == 0:
            return (b, 0, 1)
        else:
            g, y, x = self.egcd(b % a, a)
            return g, x - (b // a) * y, y

    def modularInverse(self, a, m):
        '''
        Computes a^(-1) (mod m).
        :param a: integer.
        :param m: integer.
        :return: integer.
        '''
        assert isinstance(a, int)
        assert isinstance(m, int)
        g, x, y = self.egcd(a, m)
        if g != 1:
            raise Exception('Modular inverse does not exist!')
        else:
            return x % m

##################################TEST############################


def main():
    ma = ModularArithmetics()
    print('Is 13 prime? ' + str(ma.isPrime(13)))
    print('Is 121 prime? ' + str(ma.isPrime(121)))
    print('Random prime [1, 20]: ' + str(ma.randomPrime(1, 20)))
    print('Modular power 9^2 (mod 1000): ' + str(ma.modularPower(2, 4, 1000)))
    print('GCD 12, 400: ' + str(ma.findGCD(12, 400)))
    # print('Prime from file: ' + str(ma.randomPrimeFromFile()))
    print('Modular Inverse 5 (mod 11) = ' + str(ma.modularInverse(a=5, m=11)))

if __name__ == '__main__':
    main()
