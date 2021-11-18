from Database import AVLTree


class AVLTester():

    def __init__(self):
        print("AVLTester running")
        AVL = AVLTree.AVLTree()
    
        inputs = [20,10,25,22,15,8,30] 
        inputs = [8,10,15,20,22,25,30]
        inputs = [30,25,22,20,14,10,8]
        inputs = [10,8,20,30,15,12]
        for a in inputs:
            print("    Adding:",a,"----------------------------------")
            AVL.add(a)
            AVL.toString()
            print("    Added:",a,"-----------------------------------")
            
            
        print ("FINAL TREE:")
        AVL.toString()
    
        print(" - - - Input:",inputs)
        print(" - - -Output:",AVL.inOrder())
        return
