class Tnode():

    def __init__(self, data):
        self.right = None
        self.left = None
        self.data = data
        self.height = 1

    def calcHeight(self):
        Lheight = 0
        Rheight = 0
        if self.left != None:
            Lheight = self.left.height
        if self.right != None:
            Rheight = self.right.height
        # print("H",self.toString()+".L =",Lheight)
        # print("H",self.toString()+".R =",Rheight)
        self.height = max(Lheight,Rheight) + 1
        return self.height

    def toString(self):
        rtn = self.data.toString()
        return "["+rtn+"]"


class AVLTree():

    def __init__(self):
        self.root = None
        self.tracked = ""
    
    def add(self, data):
        """
            add a new peice of data to the AVL tree

            ;param data: new data
        """
        # print("adding",data.toString())
        baby = Tnode(data)
        self.root = self.__adder__(self.root, baby)

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
            self.root = baby
            return baby
        
        """if new data is less than or equal to curr.data go left"""
        if baby.data.compareTo(curr.data) <= 0:

            """when to add baby"""
            if curr.left == None:
                curr.left = baby
                curr.calcHeight()
                return curr
            
            """send baby to be added to left sub-tree, get ballenced sub-tree"""
            curr.left = self.__adder__(curr.left, baby)
            curr.calcHeight()

        else:

            """when to add baby"""
            if curr.right == None:
                curr.right = baby
                curr.calcHeight()
                return curr

            """send baby to be added to right sub-tree, get balanced sub-tree"""
            curr.right = self.__adder__(curr.right, baby)
            curr.calcHeight()


        curr = self.__ballenceNode__(curr)
        return curr
        

    def __ballenceNode__(self, rotationNode):
    
        # print("TREE BEFORE")
        # self.toString()
        """
            ballence a node by rotating its decendents
        
            ;param rotationNode: node that will be rotated around (root of subtree)
            :param mode: one of 4 posible rotations ("LL","LR","RL","RR")
            :return new root subtree
        """

        """preventing crashs"""
        if rotationNode == None:
            return None
        
        if rotationNode.left == None and rotationNode.right == None:
            return rotationNode
        elif(rotationNode.right == None):
            bal = rotationNode.left.height - 0
        elif(rotationNode.left == None):
            bal = 0-rotationNode.right.height
        else:
            bal = rotationNode.left.height - rotationNode.right.height
        
        if bal < -1:
            spot = rotationNode.right
            if spot.left == None and spot.right == None:
                return None
            elif(spot.right == None):
                bal = spot.left.height - 0
            elif(spot.left == None):
                bal = 0-spot.right.height
            else:
                bal = spot.left.height - spot.right.height

            if bal <= 0:
                mode = "RR"
                child = spot.right
            if bal > 0:
                mode = "RL"
                child = spot.left

        elif bal > 1:
            spot = rotationNode.left
            if spot.left == None and spot.right == None:
                return None
            elif(spot.right == None):
                bal = spot.left.height - 0
            elif(spot.left == None):
                bal = 0-spot.right.height
            else:
                bal = spot.left.height - spot.right.height

            if bal <= 0:
                mode = "LR"
                child = spot.right
            if bal > 0:
                mode = "LL"
                child = spot.left

        else:
            return rotationNode
            
        # print("Ballencing Node",rotationNode.toString(),mode)

        """semi-unnecisary, but it helped me conseptualize the prosses"""
        parent = rotationNode

        """rotation if the path to where baby was added begins from rotationNode with Left-Left"""
        if mode == "LL":

            if False:
                """keep track of nodes"""
                spot = parent.left
                if spot == None:
                    return None

            """do the rotation"""
            parent.left = spot.right
            spot.right = parent
            parent.calcHeight()
            spot.calcHeight()
            return spot

        """rotation for Right-Right path"""
        if mode == "RR":

            if False:
                """keep track of nodes"""
                spot = parent.right
                if spot == None:
                    return None

            """do the rotation"""
            parent.right = spot.left
            spot.left = parent
            parent.calcHeight()
            spot.calcHeight()
            return spot

        """roation for Left-Right path"""
        if mode == "LR":

            if False:
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
            spot.calcHeight()
            parent.calcHeight()
            child.calcHeight()
            return child

        """rotation for Right-Left path"""
        if mode == "RL":

            if False:
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
            spot.calcHeight()
            parent.calcHeight()
            child.calcHeight()
            return child

        """if Mode is not suported return None"""
        return parent
                
    def remove(self, data):
        """
        public starter function for removal methods
        """

        self.root = self.__remHelper(self.root,data)
        return True

    def __remHelper(self, curr, data):
        """
        recursive function to help remove() find the node to be removed

        backtracks up the tree to calculate the new heights
        """
        if curr == None:
            return None

        if data == curr.data:
            # print(curr.toString(),"is removal node")
            return self.__removeNode(curr)

        curr.left = self.__remHelper(curr.left, data)
        curr.right = self.__remHelper(curr.right, data)

        curr.calcHeight()
        curr = self.__ballenceNode__(curr)
        return curr

    def __removeNode(self, curr):
        """
        remove a given node
        returns the new subtree of this removed node to parent node
        """
    
        """"No Children"""
        if curr.right == None and curr.left == None:
            # print(curr.toString(),"0 Child")
            return None

        """1 Child"""
        if curr.right == None:
            # print(curr.toString(),"1 Child Left")
            return curr.left
        if curr.left == None:
            # print(curr.toString(),"1 Child Right")
            return curr.right

        """2 Children"""
        # print(curr.toString(), "2 Children")
        curr.left = self.__findChild(curr, curr.left)
        curr.calcHeight()
        return curr


    def __findChild(self, rem, curr):
        """
        recursive function to fine right most left child
        
        input left of the removal node
        return is the new left subtree of node to be removed
        """

        if curr.right == None:
            # print(curr.toString(),"is right most child")
            rem.data = curr.data
            return curr.left

        curr.right = self.__findChild(rem, curr.right)
        curr.calcHeight()
        curr = self.__ballenceNode__(curr)
        return curr

    def append(self, data):
        """add data without ballencing"""
        baby = Tnode(data)
        if self.root == None:
            self.root = baby
            return True

        curr = self.root
        while curr != None:
            if data <= curr.data:
                if curr.left == None:
                    curr.left = baby
                    return True
                curr = curr.left
            else:
                if curr.right == None:
                    curr.right = baby
                    return True
                curr = curr.right
        return False

    def inOrder(self):
        rtn = []
        if self.root == None:
            print("Root is None")

        return self.LCR(self.root,rtn)

    def LCR(self, curr, rtn):
        if(curr == None):
            return rtn
        rtn = self.LCR(curr.left, rtn)
        rtn.append(curr.data)
        rtn = self.LCR(curr.right, rtn)

        return rtn

    def toString(self):

        if False:
            return
        
        prt = []
        i = 0
        while i < 15:
            prt.append("[  ]")
            i+=1
        prt = self.__strHelper(self.root,0,prt)
        
        print("")
        print("0:"+17*" "+prt[0])
        print("1:"+7*" "+prt[1]+16*" "+prt[2])
        print("2:  "+prt[3]+6*" "+prt[4]+6*" "+prt[5]+6*" "+prt[6])
        print("3:"+prt[7]+prt[8]+"  "+prt[9]+prt[10]+"  "+prt[11]+prt[12]+"  "+prt[13]+prt[14])
        print("")

    def __strHelper(self, curr, spot, prt):
        if curr == None:
            return prt
        prt[spot] = curr.toString()
        prt = self.__strHelper(curr.left,2*spot+1,prt)
        prt = self.__strHelper(curr.right,2*spot+2,prt)
        return prt