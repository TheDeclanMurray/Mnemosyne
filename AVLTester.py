
from Database import AVLTree


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

        self.temp = "Nothing: "

        if True:
            self.frontEnd()
        if False:
            self.AVL()

    def frontEnd(self):
        
        pass

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