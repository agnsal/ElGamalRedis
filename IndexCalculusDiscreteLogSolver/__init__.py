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
import numpy
import sympy
from collections import OrderedDict


class IndexCalculus:
    '''
    a^(x) = b (mod p); find x.
    '''
    __a = None
    __b = None
    __p = None
    __x = None

    def __init__(self, a, b, p):
        '''
        :param a: integer.
        :param b: integer.
        :param p: integer (a prime number).
        '''
        assert isinstance(a, int)
        assert isinstance(b, int)
        assert isinstance(p, int)
        assert sympy.isprime(p)
        while a >= p:
            a -= p
        while a < 0:
            a += p
        while b >= p:
            b -= p
        while b < 0:
            b += p
        self.__a = a
        self.__b = b
        self.__p = p

    def getA(self):
        return self.__a

    def getB(self):
        return self.__b

    def getP(self):
        return self.__p

    def getX(self):
        return self.__x

    def getPhi(self):  # Euler Totient Function
        return self.__p - 1

    def __setX(self, newX):
        '''
        Updates x, modulo p - 1 (because x is an exponent modulo p).
        :param newX: integer.
        :return:
        '''
        phi = self.getPhi()
        while newX >= phi:
            newX = newX - phi
        if newX < 0:
            newX = newX + phi
        self.__x = newX

    def printProblem(self):
        '''
        Prints the current state.
        :return:
        '''
        print(str(self.getA()) + '^(x) = ' + str(self.getB()) + ' (mod ' + str(self.getP()) + ').')
        print('p is prime.')
        print('x = ?')

    def generatePrimeVector(self, start, end):
        '''
        Finds all prime in the interval [start, end].
        :param start: integer.
        :param end: integer.
        :return: list.
        '''
        assert isinstance(start, int)
        assert isinstance(end, int)
        primes = list(sympy.primerange(start, end))
        if start < 0:
            primes.insert(0, -1)
        # print('Prime Vector in [' + str(start) + ', ' + str(end) + ']: ' + str(primes)) # Test
        return primes

    def generateBaseFromFile(self, start, end, path):
        '''
        Generates the base (a list of primes) reading them from a file.
        :param start: integer.
        :param end: integer.
        :param path: string.
        :return: list of integers.
        '''
        assert isinstance(start, int)
        assert isinstance(end, int)
        assert isinstance(path, str)
        ma = ModularArithmetics()
        return ma.listOfPrimesFromFile(path)[start:end]

    def findFactors(self, n, base):
        '''
        Finds all the exponents of the factors (that are in the base) of integer n.
        :param n: integer.
        :param base: list of (primes) integers.
        :return: OrderedDict or False if it is impossible a factorization for the given base.
        '''
        assert isinstance(n, int)
        assert isinstance(base, list)
        orderedFactors = OrderedDict()
        factors = sympy.ntheory.factorint(n)
        # print('n: ' + str(n)) # Test
        # print('Factors: ' + str(factors)) # Test
        for key in factors.keys():
            if key not in base:  # If base primes are not sufficient to have a factorization.
                # print('KEY NOT IN BASE') # Test
                return False
        for elem in base:
            assert isinstance(elem, int)
            if elem in factors.keys():
                exp = factors[elem]
                orderedFactors.update({elem: exp})
            else:
                orderedFactors.update({elem: 0})
        # print('Ordered Factors: ' + str(orderedFactors)) # Test
        count0 = 0
        for key in orderedFactors.keys():
            if orderedFactors[key] == 0:
                count0 += 1
        # If all exponent are 0, we don't have a factorization:
        if count0 == len(orderedFactors):
            # print('ALL ZEROES FACTORIZATION')  # Test
            return False
        return orderedFactors

    def deleteZeroColumns(self, m, base):
        '''
        Deletes columns that are made of all zeros from matrix m, updating the base of the matrix.
        :param m: bidimensional list (matrix).
        :param base: list.
        :return: matrix; list (the updated base).
        '''
        assert isinstance(m, list)
        assert isinstance(m[0], list)
        res = m.copy()
        newBase = base
        i = 0
        toDel = []
        while i < len(m[0]):
            column = numpy.array(res)[:, i]
            if numpy.sum(column) == 0:
                toDel.append(i)
            i += 1
        # print('To Delete: ' + str(toDel)) # Test
        deleted = 0
        for elem in toDel:
            res = numpy.delete(res, elem - deleted, axis=1)
            del newBase[elem - deleted]
            deleted += 1
        return res, newBase

    def isNewRowLI(self, row, m):
        '''
        Check is a candidate row is Linear Independent with matrix m rows.
        :param row: list.
        :param m: bidimensional list.
        :return:
        '''
        assert isinstance(row, list)
        assert isinstance(m, list)
        # print('row: ' + str(row)) # Test
        if m == []:
            return True
        else:
            assert isinstance(m[0], list)
            testM = m.copy()
            testM.append(row)
            # print('testM: ' + str(testM)) # Test
            testM = numpy.array(testM)
            _, LIRowsNumber = sympy.Matrix(testM).T.rref()
            if len(LIRowsNumber) == len(testM):
                # print('True') # Test
                return True
            else:
                return False

    def generateCongruencesMatrix(self, r, path=False):
        '''
        Generate congruences: b^(k) = (-1)^(e0) * 2^(e1) * 3^(e2) * 5^(e3) ... p^(er)
        :param r: integer, range of primes in the base.
        :return: bidimensional list (congruences matrix); list of integers (base).
        '''
        assert isinstance(r, int)
        assert r > 0
        ma = ModularArithmetics()
        a = self.getA()
        p = self.getP()
        if not path:
            base = self.generatePrimeVector(start=0, end=r)
        else:
            base = self.generateBaseFromFile(start=0, end=r, path=path)
        # print('Base of primes: ' + str(base)) # Test
        matrix = []
        numberList = []  # Powers mod n are circular (after the period, the relations are Linear Dependent)
        i = 1
        number = ma.modularPower(a=a, e=i, m=p)
        while number not in numberList and len(matrix) < len(base):
            numberList.append(number)
            factors = self.findFactors(number, base=base)
            # print('Factors: ' + str(factors)) # Test
            if factors:
                # print('Congruece '+ str(i) + ': ' + str(factors)) # Test
                row = list(factors.values())  # row = [e0, e1, ..., er, k]
                row.append(i)
                if self.isNewRowLI(row, matrix):
                    # print('Valid Row')  # Test
                    matrix.append(row)
            i += 1
            number = ma.modularPower(a=a, e=i, m=p)
            # print('Number: ' + str(number))  # Test
            # print('Number List: ' + str(numberList))  # Test
            # print('i = ' + str(i))  # Test
        return matrix, base

    def matrix2ReducedEchelonForm(self, m):
        '''
        Returns Row Echelon Form of matrix m.
        :param m: matrix.
        :return: matrix, list of pivots.
        '''
        if not isinstance(m, list):
            assert isinstance(m, numpy.matrix)
            m.tolist()
        # `print('m: ' + str(m)) # Test
        sympyM = sympy.Matrix(m)
        RREF, pivots = sympyM.rref()
        return numpy.asmatrix(RREF), pivots

    def solveSystemOfEq(self, systemMatrix):
        '''
        Find the solution of a system of equations.
        :param systemMatrix: bidimentional list.
        :return: list.
        '''
        a = numpy.array(systemMatrix)[:, 0:-1]
        b = numpy.array(systemMatrix)[:, -1]
        print('a: ' + str(a))  # Test
        print('b: ' + str(b))  # Test
        return numpy.linalg.solve(a, b)

    def computeLogarithms(self, m, base):
        '''
        Computes the discrete logarithms of base primes, given the congruence matrix.
        :param m: bidimensional list (the congruence matrix).
        :param base: list (of primes).
        :return: list.
        '''
        assert isinstance(m, list)
        assert isinstance(m[0], list)
        assert isinstance(base, list)
        m, base = self.deleteZeroColumns(m, base)
        m = numpy.asmatrix(m)
        while len(m[0]) > len(m):
            m = m[0:-1]
        print('Base of primes: ' + str(base))  # Test
        print('Congruence Matrix: M')
        print(m)  # Test
        rm, pivots = self.matrix2ReducedEchelonForm(m)
        print('M in Reduced Row Echelon Form: RM')
        print(rm)
        print('Pivots: ' + str(pivots))
        primesLogarithms = list(numpy.array(rm)[:, -1])  # The last column is composed of base primes logarithms.
        while numpy.sum(primesLogarithms[0:-1]) == 0:
            print('Congruence Matrix: M')
            print(m)  # Test
            rm, pivots = self.matrix2ReducedEchelonForm(m)
            print('M in Reduced Row Echelon Form: RM')
            print(rm)
            print('Pivots: ' + str(pivots))
            primesLogarithms = list(numpy.array(rm)[:, -1])  # The last column is composed of base primes logarithms.
            print('Logs: ' + str(primesLogarithms))
            m = m[0:-1]
        return primesLogarithms

    def solveDiscreteLog(self, r, path=False, maxRounds=100):
        '''
        Find the solution of a Discrete Logarithm problem.
        :param r: integer, the range of the base.
        :param path: string (optional).
        :param maxRounds: integer.
        :return: integer (the result).
        '''
        assert isinstance(r, int)
        assert r > 4
        assert isinstance(maxRounds, int)
        a = self.getA()
        b = self.getB()
        p = self.getP()
        ma = ModularArithmetics()
        self.printProblem()
        m, base = self.generateCongruencesMatrix(r, path)
        print('m: ' + str(numpy.asmatrix(m)))
        print('base: ' + str(base))
        primesLogarithms = self.computeLogarithms(m=m, base=base)
        print('Logarithms of Base elements: ' + str(primesLogarithms))  # Test
        res = None
        self.printProblem()
        k = 1
        l = 0
        found = False
        while k in range(1, maxRounds) and not found:
            l += 1
            powerA = ma.modularPower(a=a, e=l, m=p)
            print('powerA = a^(' + str(l) + ') = ' + str(powerA))
            mult = ma.modularMultiplication(x=b, y=powerA, m=p)
            print('b * powerA (mod p) = ' + str(mult))
            candidate = self.findFactors(n=mult, base=base)
            print('Candidate: ' + str(candidate))  # Test
            if candidate:
                print('Found: ' + str(candidate) + '; l = ' + str(l))
                exponents = list(candidate.values())  # exponents = [e0, e1, ..., er]
                print('Exponents: ' + str(exponents))
                while len(primesLogarithms) < len(exponents):
                    primesLogarithms.append(0)
                products = [a * b for a, b in zip(exponents, primesLogarithms)]
                print('Products: ' + str(products))
                res = numpy.sum(products)
                if not res == 0:
                    found = True
            k += 1
        self.__setX(res - l)
        finalRes = self.getX()
        print('Final Result = x = ' + str(finalRes))
        return finalRes
