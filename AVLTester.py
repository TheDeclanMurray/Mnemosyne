from typing import Collection
from Database import AVLTree
from Database.Data import Data
import os

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


        if False:
            self.readTxt("input.txt")



        pass

    def saveData(self, saveFile, currDataBase):

        if(saveFile != None):
            with open(saveFile, "w") as f:
                Lines = currDataBase.save()
                for line in Lines:
                    f.write(line)
            f.close()
        else:
            return False

    def readTxt(self, inputFile):

        if(inputFile != None):    
            with open(inputFile) as f:
                text = f.readlines()
            f.close()
        else:    
            return False

        data = Data()
        row = 0
        col = 0
        colLength = 0

        for line in text:
            txt = line[2:len(line)-1]
            type = line[0:1]
            if type == "0":
                name = txt
                data = Data()
                data.name = name
                data.addRow()
                
                
            elif type == "1":
                data.addCol(txt)
                colLength += 1

                
            elif type == "2":
                data.insert(txt,row,col)
                col +=1
                if col == colLength:
                    data.addRow()
                    row +=1
                    col = 0

        data.removeRow(len(data.rows)-1) 
        return data
        

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
        saved = True
        ErrorTxt = ""
        
        comand = 'clear'
        if os.name in ('nt', 'dos'):
            comand = "cls"
        os.system(comand)
        
        print("")
        data.toString()
        instructions = """   Q quit, I insert, D delete row or column R add row, C add column, 
   F search, T sort, S save , A save as, O open, K delete page, N new page """

        print(instructions)
        input1 = input("Input: ")
        while input1 != "Q":
            if input1 == "I":
                row = input("Row: ")
                col = input("Column: ")
                info = input("Data: ")
                data.insert(info,row,col)
                saved = False
            elif input1 == "D":
                rem = input("Row or Column: ")
                if rem.lower() == "row":
                    row = int(input("Row: "))
                    data.removeRow(row)
                elif rem.lower() == "col" or rem.lower() == "column":
                    col = int(input("Column: "))
                    data.removeCol(col)
                saved = False
            elif input1 == "C":
                name = input("Column Name: ")
                data.addCol(name)
                saved = False
            elif input1 == "R":
                data.addRow()
                saved = False
            elif input1 == "F":
                search = input("Search: ")
                data.search(search)
            elif input1 == "T":
                primary = input("Primary: ")
                secondary = input("Secondary: ")
                data.sort(primary,secondary)
            elif input1 == "O":

                if not saved:
                    saveSugestion = input("Save Work(Y/N)? ")
                    if saveSugestion == "Y":
                        outputFile = "storage/" + data.name + ".txt"
                        try: 
                            self.saveData(outputFile, data)
                            saved = True
                        except Exception as a:
                            ErrorTxt = a

                inputfile = input("Open: ")
                inputfile = "storage/" + inputfile + ".txt"
                 
                rtn = False
                try: 
                    rtn = self.readTxt(inputfile)
                except Exception as a:
                    ErrorTxt = a

                if rtn != False:
                    data = rtn

                saved = True
            elif input1 == "S":
                outputFile = "storage/" + data.name + ".txt"
                try: 
                    self.saveData(outputFile, data)
                    saved = True
                except Exception as a:
                    ErrorTxt = a
            elif input1 == "A":
                outputFile = input("Save as: ")
                data.name = outputFile
                outputFile = "storage/" + outputFile + ".txt"
                try: 
                    self.saveData(outputFile, data)
                except Exception as a:
                    ErrorTxt = a
            elif input1 == "K":
                fileName = "storage/" + data.name + ".txt"
                try:
                    os.remove(fileName)
                except:
                    pass
                data = Data()
            elif input1 == "N":

                if not saved:
                    saveSugestion = input("Save Work(Y/N)? ")
                    if saveSugestion == "Y":
                        outputFile = "storage/" + data.name + ".txt"
                        try: 
                            self.saveData(outputFile, data)
                            saved = True
                        except Exception as a:
                            ErrorTxt = a
                
                data = Data()

            comand = 'clear'
            if os.name in ('nt', 'dos'):
                comand = "cls"
            os.system(comand)

            print(ErrorTxt)
            ErrorTxt = ""
            data.toString()
            print(instructions)
            input1 = input("Input: ")

        if not saved:
            saveSugestion = input("Save Work(Y/N)? ")
            if saveSugestion == "Y":
                outputFile = "storage/" + data.name + ".txt"
                try: 
                    self.saveData(outputFile, data)
                    saved = True
                except Exception as a:
                    ErrorTxt = a
        
        comand = 'clear'
        if os.name in ('nt', 'dos'):
            comand = "cls"
        os.system(comand)



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