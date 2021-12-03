from Database import AVLTree
from Database.Data import Data

class intNode():

    def __init__(self, int, id):
        self.val = int
        self.id = id
        pass

    def compareTo(self, node):
        if self.val < node.val:
            return -1
        if self.val > node.val:
            return 1
        return 0

    def toString(self):
        rtn = str(self.id) + str(self.val)
        if len(rtn) == 1:
            rtn = " "+rtn
        return rtn

class AVLTester():

    def __init__(self):

        if False:
            self.newStuff()
        if False:
            self.AVL()
        if True:
            self.data()



        pass

    def newStuff(self):
        import numpy
        simp = [3,5,9]
        arr = numpy.array([1,2,4])
        arr = numpy.array(simp)
        simp = [1,1,1,1]
        print("arr",arr)
        prev = numpy.array(simp)
        print("prev",prev)
        print("arr[1]",arr[1])
        i = 0
        for a in arr:
            print("tab",a)

            numpy.put(prev,i,a)
            i +=1
        print(prev)

        pass

    def data(self):

        data = Data()
        
        data.addCol("num")
        data.addCol("Name")
        data.addCol("Age")
        data.addCol("Size")
        
        data.addRow()
        data.addRow()
        data.addRow()
        data.addRow()
        


        data.insert("James",0,1)
        data.insert("Bob Jefferson",3,1)
        data.insert("Zebra",2,1)
        data.insert("Apple",1,1)

        data.insert("32",0,2)
        data.insert("32",1,2)
        data.insert("30",2,2)
        data.insert("32",3,2)

        data.insert("0",0,0)
        data.insert("1",1,0)
        data.insert("2",2,0)
        data.insert("3",3,0)  
          
             
        
        data.addCol("Plus")
        data.addRow()
        data.addRow()

        data.insert("4",4,0)
        data.insert("5",5,0)
        


        
        

        data.toString()
        instructions = "Q quit, I insert, D delete row or column, R add row, C add column, S search, T sort"
        print(instructions)
        input1 = input("Input: ")
        while input1 != "Q":
            if input1 == "I":
                row = int(input("Row: "))
                col = int(input("Column: "))
                info = input("Data: ")
                data.insert(info,row,col)
            elif input1 == "D":
                rem = input("Row or Column: ")
                if rem.lower() == "row":
                    row = int(input("Row: "))
                    data.removeRow(row)
                elif rem.lower() == "col" or rem.lower == "column":
                    col = int(input("Column: "))
                    data.removeCol(col)
            elif input1 == "C":
                name = input("Column Name: ")
                data.addCol(name)
            elif input1 == "R":
                data.addRow()
            elif input1 == "S":
                search = input("Search: ")
                data.search(search)
            elif input1 == "T":
                primary = input("Primary: ")
                secondary = input("Secondary: ")
                data.sort(primary,secondary)

            data.toString()
            print(instructions)
            input1 = input("Input: ")

    def AVL(self):

        print("AVLTester running")
        AVL = AVLTree.AVLTree()
    
        inputs = [20,10,25,22,15,8,30] 
        #inputs = ["BB","AAAA"] 
        #inputs = [8,10,15,20,22,25,30]
        inputs = [30,25,22,20,14,10,8]
        #inputs = [10,8,20,30,15,12]
        inputs = [20,10,25,22,8,12,9,7,11,13]
        inputs = [0,0,0]

        input = self.toIntNode(inputs)
        for a in input:
            print("    Adding:",a.toString(),"----------------------------------")
            AVL.add(a)
            AVL.toString()
            print("    Added:",a.toString(),"-----------------------------------")
    
        # AVL.remove(input[3])
        AVL.toString()

        print(" - - - Input:",inputs)
        prt = []
        rtn = AVL.inOrder()
        for b in rtn:
            prt.append(b.toString())
        print(" - - -Output:",prt)
    
    def toIntNode(self, list):
        rtn = []
        p = 0
        for i in list:
            n = intNode(i,p)
            rtn.append(n)
            p += 1
        return rtn