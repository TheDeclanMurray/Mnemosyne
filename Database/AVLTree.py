from Database.DArray import DArray

class Tnode():

    def __init__(self, data):
        self.right = None
        self.left = None
        self.data = data
        self.height = 1

    def calcHeight(self):
        """
            Calculate the height of this node

            ;return rtn: the height of this node
        """
        Lheight = 0
        Rheight = 0
        if self.left != None:
            Lheight = self.left.height
        if self.right != None:
            Rheight = self.right.height
        rtn = self.height = max(Lheight,Rheight) + 1
        return rtn

    def toString(self):
        """
            return this node as a string
            data type needs a toString() meathod
        """
        rtn = self.data.toString()
        return "["+rtn+"]"


class AVLTree():
    """
        self ballencing binary search tree
        node data must have a .compareTo() function
            takes another nodes data
            returns:
                -1 if self is smaller than other
                 0 if the same
                 1 if self is larger than other
    """

    def __init__(self):
        self.root = None
        self.tracked = ""
    
    def add(self, data):
        """
            add a new peice of data to the AVL tree

            ;param data: new data
        """
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

        # if empty tree
        if curr == None:
            self.root = baby
            return baby
        
        # if new data is less than or equal to curr.data go left
        if baby.data.compareTo(curr.data) <= 0:

            # when to add baby
            if curr.left == None:
                curr.left = baby
                curr.calcHeight()
                return curr
            
            # send baby to be added to left sub-tree, get ballenced sub-tree
            curr.left = self.__adder__(curr.left, baby)
            curr.calcHeight()

        else:

            # when to add baby
            if curr.right == None:
                curr.right = baby
                curr.calcHeight()
                return curr

            # send baby to be added to right sub-tree, get balanced sub-tree
            curr.right = self.__adder__(curr.right, baby)
            curr.calcHeight()


        curr = self.__ballenceNode__(curr)
        return curr
        

    def __ballenceNode__(self, rotationNode):
        """
            ballence a node by rotating its decendents
        
            ;param rotationNode: node that will be rotated around (root of subtree)
            :param mode: one of 4 posible rotations ("LL","LR","RL","RR")
            :return new root subtree
        """

        """preventing crashs"""
        if rotationNode == None:
            return None
        
        # calculate if tree needs to rotate right, left, or not at all from this node
        if rotationNode.left == None and rotationNode.right == None:
            return rotationNode
        elif(rotationNode.right == None):
            bal = rotationNode.left.height - 0
        elif(rotationNode.left == None):
            bal = 0-rotationNode.right.height
        else:
            bal = rotationNode.left.height - rotationNode.right.height
        
        # node rotates to the left
        if bal < -1:
            # calculate secondary rotation
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

        # node rotates to the right
        elif bal > 1:
            # calculate secondary rotation
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
            
        """semi-unnecisary, but it helped me conseptualize the prosses"""
        parent = rotationNode

        """rotation if the path to where baby was added begins from rotationNode with Left-Left"""
        if mode == "LL":

            """do the rotation"""
            parent.left = spot.right
            spot.right = parent
            parent.calcHeight()
            spot.calcHeight()
            return spot

        """rotation for Right-Right path"""
        if mode == "RR":

            """do the rotation"""
            parent.right = spot.left
            spot.left = parent
            parent.calcHeight()
            spot.calcHeight()
            return spot

        """roation for Left-Right path"""
        if mode == "LR":

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

            ;param data: data to find and remove from the tree
            :return: True if no errors
        """

        self.root = self.__remHelper(self.root,data)
        return True

    def __remHelper(self, curr, data):
        """
            recursive function to help remove() find the node to be removed
            backtracks up the tree to calculate the new heights

            ;param curr: current node
            :param data: data to find and remove from the tree
            ;return curr: new subtree
        """
        if curr == None:
            return None

        if data == curr.data:
            return self.__removeNode(curr)

        curr.left = self.__remHelper(curr.left, data)
        curr.right = self.__remHelper(curr.right, data)

        curr.calcHeight()
        curr = self.__ballenceNode__(curr)
        return curr

    def __removeNode(self, curr):
        """
            remove a given node and return the new subtree of this removed node 

            ;param curr: node to remove from the tree
            :return curr: new subtree
        """
    
        """"No Children"""
        if curr.right == None and curr.left == None:
            return None

        """1 Child"""
        if curr.right == None:
            return curr.left
        if curr.left == None:
            return curr.right

        """2 Children"""
        curr.left = self.__findChild(curr, curr.left)
        curr.calcHeight()
        return curr

    def __findChild(self, rem, curr):
        """
            recursive function to fine right most left child
        
            ;param rem: node that is being removed
            :param curr: node left of the removal node (left of rem)
            :return curr: the new left subtree of node to be removed
        """

        # base case of this recursive function
        if curr.right == None:
            rem.data = curr.data
            return curr.left

        curr.right = self.__findChild(rem, curr.right)
        curr.calcHeight()
        curr = self.__ballenceNode__(curr)
        return curr

    def append(self, data):
        """
            add data to the tree without the self-balencing feature

            ;param data: data to be added
            :return: True if no errors encountered 
        """
        baby = Tnode(data)

        # if tree is empty
        if self.root == None:
            self.root = baby
            return True

        # find the right spot in the BST to add baby
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
        """
            take an in order traversal of the tree

            ;return rtn: DArray containing the inputed data in order
        """
        rtn = DArray()    
        return self.__LCR(self.root,rtn)

    def __LCR(self, curr, rtn):
        """
            takes the current node and the inOrder list and adds the node and its 
            decendents to the list

            ;param curr: the current node in the traversal
            :param rtn: the list of node data
            :return rtn: returns the updated list of node data
        """
        # base case
        if(curr == None):
            return rtn

        # go left, take current data, then go right
        rtn = self.__LCR(curr.left, rtn)
        rtn.append(curr.data)
        rtn = self.__LCR(curr.right, rtn)

        return rtn

    def toString(self):
        """
            Hardcoded termninal display of an AVLTree to assist with errors in this class
        """
        
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
        """
            helper function for toString()
        """
        if curr == None:
            return prt
        prt[spot] = curr.toString()
        prt = self.__strHelper(curr.left,2*spot+1,prt)
        prt = self.__strHelper(curr.right,2*spot+2,prt)
        return prt