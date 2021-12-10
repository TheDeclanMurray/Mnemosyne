from typing import Iterable, Iterator 
import numpy

class DArray(Iterable):
    """
        A class based on the numpy array that is optomized, and contains  
        functions useful to do things
    """

    def __init__(self, length = 2):        
        self.__arr__ = numpy.array(length*[""], dtype = 'object')
        self.length = 0
        self.size = length

    def addArray(self, add):
        """
            takes a DArray, addes it to this DArray and returns the sum as a DArray
            *cannot store None as a value*

            ;param add: DArray to be added to self
            :return rtn: DArray of the combined arrays
        """
    
        # minimize the new DArray size, because it will never be altered
        totalLength = self.length + add.length + 1
        rtn = DArray(totalLength)
        
        #go through and add self then add to rtn
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
        """
            takes an input and a location and replaces the current information at that
            location 

            ;param data: new information to hold
            :param spot: lacation to insert data
            :return: True if valid inputs
        """
        if data == None:
            return False
        if spot >= self.length:
            return False
        if spot < 0:
            return False

        self.__arr__[spot] = data
        return True
    
    def get(self, spot):
        """
            returns the value of a given location

            ;param spot: location to get value from
            :return: value in DArray at spot or False if invalid input
        """
        if spot >= self.length:
            return None
        if spot < 0:
            return None
        
        return self.__arr__[spot]

    def remove(self, spot):
        """
            remove a value and location from DArray

            ;param spot: location to remove
            :return: True if valid input
        """
        # check if valid input
        if spot < 0 or spot >= self.length:
            return False

        # shift information down in the DArray
        while spot+1 < self.length:
            self.__arr__[spot] = self.__arr__[spot+1]
            spot += 1
        self.__arr__[spot] = ""
        self.length -= 1

        # if DArray empty
        if self.length == 0:
            self.__arr__ = numpy.array(["",""],dtype='object')
            return True

        # if DArray to large
        if 4*self.length < self.size:
            sizeDown = numpy.array(2*self.length*[""], dtype='object')
            i = 0
            while i < self.size:
                sizeDown[i] = self.__arr__[i]
                i+=1

            self.__arr__ = sizeDown
            self.size /= 2

        return True

    def append(self, data):
        """
            add to the end of the DArray, extending the length

            ;param data: value to add
            :return: True if no errors
        """
        # input data into the hiden area of the DArray
        self.__arr__[self.length] = data
        self.length += 1
        
        # if hiden area of DArray filled, double the size
        if self.length == self.size:
            sizeUp = numpy.array(2*self.length*[""],dtype = 'object')
            
            i = 0
            while i < self.size:
                sizeUp[i] = self.__arr__[i]
                i += 1

            self.__arr__ = sizeUp
            self.size *= 2
        
        return True
    
    def printable(self):
        """
            returns an array, that can be printed to the terminal for bug fixing

            ;return rtn: array of DArray values
        """
        rtn = []
        i = 0
        while i < self.length:
            rtn.append(self.__arr__[i])
            i += 1
        return rtn

    def copy(self):
        """
            get a copy of this DArray

            ;return rtn: DArray identical to self
        """
        rtn = DArray()
        rtn.__arr__ = self.__arr__.copy()
        rtn.length = self.length
        rtn.size = self.size

        return rtn

    def __iter__(self):
        """
            returns an itorator for this DArray
        """
        return DArrayItorator(self.__arr__,self.length)

   
class DArrayItorator(Iterator):

    def __init__(self, dArray, len):
        self.currSpot = 0
        self.dArray = dArray
        self.length = len

    def __next__(self):
        """
            get the next value in the Itorator

            ;param rtn: next value in the DArray
        """
        if self.currSpot >= self.length:
            raise StopIteration
        
        rtn = self.dArray[self.currSpot]
        self.currSpot += 1
    
        return rtn
