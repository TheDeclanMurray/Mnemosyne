

class Tnode():

    def __init__(self, data):
        self.right = None
        self.left = None
        self.data = data
        self.height = 0

class AVLTree():

    def __init__(self):
        self.root = None
        self.tracked = ""
    
    def add(self, data):
        """
            add a new peice of data to the AVL tree

            ;param data: new data
        """
        baby = Tnode(data)
        self.__adder__(self.root, baby)
        return True

    def __adder__(self, curr, baby):
        """
            Helper function for add
        
            ;param curr: current node
            :param baby: new node yet to be added to the tree
            :retern curr: the current node after ballencing the sub-tree
        """

        """if empty tree"""
        if curr == None:
            self.head = baby
            return baby
        
        """if new data is less than curr.data go left"""
        if baby.data <= curr.data:

            """when to add baby"""
            if curr.left == None:
                curr.left = baby
                self.tracked = "L"
                return curr
            
            """send baby to be added to left sub-tree, get ballenced sub-tree"""
            curr.left = self.__adder__(curr.left, baby)
            curr.height = curr.left.height+1
            nextTracked = "L"

            """calculate height difference at node"""
            if curr.right == None:
                bal = curr.left.height - 0
            else:
                bal = curr.left.height - curr.right.height
            
            """determin and then ballence if required"""
            if bal > 1:
                curr = self.__ballenceNode__(curr, nextTracked+self.tracked)

        else:

            """when to add baby"""
            if curr.right == None:
                curr.right = baby
                self.tracked = "R"
                return curr

            """send baby to be added to right sub-tree, get ballenced sub-tree"""
            curr.right = self.__adder__(curr.right, baby)
            curr.height = curr.right.height+1
            nextTracked = "R"

            """calculate height difference at node"""
            if curr.left == None:
                bal = 0 - curr.right.height
            else:
                bal = curr.left.height - curr.right.height
            
            """determin and then ballence if required"""
            if bal < -1:
                curr = self.__ballenceNode__(curr, nextTracked+self.tracked)
                
        """Update tracking info"""
        self.tracked = nextTracked
        return curr
        

    def __ballenceNode__(self, rotationNode, mode):
        """
            ballence a node by rotating its decendents
        
            ;param rotationNode: node that will be rotated around (root of subtree)
            :param mode: one of 4 posible rotations ("LL","LR","RL","RR")
            :return new root subtree
        """

        """preventing crashs"""
        if rotationNode == None:
            return None

        """semi-unnecisary, but it helped me conseptualize the prosses"""
        parent = rotationNode

        """rotation if the path to where baby was added begins from rotationNode with Left-Left"""
        if mode == "LL":

            """keep track of nodes"""
            spot = parent.left
            if spot == None:
                return None

            """do the rotation"""
            parent.left = spot.right
            spot.right = parent
            return spot

        """rotation for Right-Right path"""
        if mode == "RR":

            """keep track of nodes"""
            spot = parent.right
            if spot == None:
                return None

            """do the rotation"""
            parent.right = spot.left
            spot.left = parent
            return spot 

        """roation for Left-Right path"""
        if mode == "LR":

            """keep track of nodes"""
            spot = parent.left
            if spot == None:
                return None
            child = spot.right
            if child == None:
                return None

            """do the rotation"""
            spot.right = child.left
            child.left = spot
            parent.left = child.right 
            child.right = parent 
            return child

        """rotation for Right-Left path"""
        if mode == "RL":

            """keep track of nodes"""
            spot = parent.right
            if spot == None:
                return None
            child = spot.left
            if child == None:
                return None

            """do the rotation"""
            spot.left = child.right
            child.right = spot
            parent.right = child.left 
            child.left = parent 
            return child

        """if Mode is not suported return None"""
        return None
                
    def remove(self, data):
        # we could just create a new AVL Tree every time so we dont have to deal 
        # with removal, or with changing the sorting data
        pass

    def inOrder(self):
        pass
