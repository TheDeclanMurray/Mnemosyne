from typing import Iterable, Iterator 
import numpy

class DArray(Iterable):

    def __init__(self, length = 2):        
        self.__arr__ = numpy.array(length*[""], dtype = 'object')
        self.length = 0
        self.size = length

    def addArray(self, add):
        """
            takes a DArray, returns a DArray
        
        """
    
        totalLength = self.length + add.length + 1
        rtn = DArray(totalLength)
        print("    rtn len:",rtn.size)

        i = 0
        while i < self.length:
            plus = self.__arr__[i]
            rtn.append(plus)
            i += 1
        while i < self.length + add.length:
            plus = add.get(i-self.length)
            rtn.append(plus)
            i += 1

        return rtn


    def put(self, data, spot):

        if spot >= self.length:
            return False
        if spot < 0:
            return False

        self.__arr__[spot] = data
    
    def get(self, spot):

        if spot >= self.length:
            return False
        if spot < 0:
            return False
        
        return self.__arr__[spot]

    def remove(self, spot):
    
        while spot+1 < self.length:
            self.__arr__[spot] = self.__arr__[spot+1]
            spot += 1
        self.__arr__[spot] = ""
        self.length -= 1

        if self.length == 0:
            self.__arr__ = numpy.array(["",""],dtype='object')
            return True

        if 4*self.length < self.size:
            print("self.length:",self.length)
            sizeDown = numpy.array(2*self.length*[""], dtype='object')
            i = 0
            while i < self.size:
                sizeDown[i] = self.__arr__[i]
                i+=1

            self.__arr__ = sizeDown
            self.size /= 2

        # print(selfsecondarySet = DArray().printable())
        
        return True

    def append(self, data):

        self.__arr__[self.length] = data
        self.length += 1
        

        if self.length == self.size:
            sizeUp = numpy.array(2*self.length*[""],dtype = 'object')
            
            i = 0
            while i < self.size:
                sizeUp[i] = self.__arr__[i]
                i += 1

            self.__arr__ = sizeUp
            self.size *= 2

        # print(self.printable())
    
    def printable(self):
        rtn = []
        i = 0
        while i < self.length:
            rtn.append(self.__arr__[i])
            i += 1
        return rtn

    def copy(self):
        rtn = DArray()
        rtn.__arr__ = self.__arr__.copy()
        rtn.length = self.length
        rtn.size = self.size

        return rtn

    def __iter__(self):
        return DArrayItorator(self.__arr__,self.length)

   
class DArrayItorator(Iterator):

    def __init__(self, dArray, len):
        self.currSpot = 0
        self.dArray = dArray
        self.length = len

    def __next__(self):
        if self.currSpot >= self.length:
            raise StopIteration
        
        rtn = self.dArray[self.currSpot]
        self.currSpot += 1
    
        return rtn
