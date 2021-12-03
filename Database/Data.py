

from numpy.core.fromnumeric import partition
from Database.AVLTree import AVLTree

import numpy 

class RowNode():

    def __init__(self):
        self.row = []
        self.sortPriority = 0
        pass
    
    def compareTo(self, node):
        """
            compares this node's value to another node's value at the sort priority
        
            ;param node: the node to compare to
            :return: 
                0  if the same
                -1 if self < node
                1  if self > node
        """
       
        if(node == None):
            return 1

        if node.row[self.sortPriority] == "":
            return -1
        if self.row[self.sortPriority] == "":
            return 1
        if self.row[self.sortPriority] < node.row[self.sortPriority]:
            return -1
        if self.row[self.sortPriority] > node.row[self.sortPriority]:
            return 1
        return 0

    def put(self, data, col):
        """
            put data in a specified column of this row
        
            ;param data: the data to insert
            :param col: the column of this row to insert at
            :retern: True if no errors
        """
        if type(data) != type.__str__:    
            data = str(data)
        self.row[col] = data
        return True

class Data:

    def __init__(self):
        self.title = [] # Array of the names of each column
        self.rows = [] # Array of all Row nodes
        self.visible = [] # Array of visible Row nodes
        self.columnLength = [] # Array keeping track of the max lenght of each collum
        self.AVLs = [] # Array of AVLTrees, one for each column
        self.primarySort = -1 # the column number of the primary sort priority (-1 if none)
        self.secondarySort = -1 # the column number of the secondary sort priorty (-1 if none)

    def search(self, search):
        """
            Search for something in the database
        
            ;param search: string of what is being searched for
            :retern: True if no errors 
        """

        """if search is blank, everything becomes visible"""
        if search == "":
            self.visible = self.rows.copy()
            return True

        """create new visible list"""
        self.visible = []

        """Cycle through the Rows"""
        for node in self.rows:
            """Cycle through the data in each row"""
            for data in node.row:
                """if the row contains the search add it to visible"""
                if self.__find__(search, data):
                    self.visible.append(node)
                    break
        return True

    def __find__(self,search,data):
        """
            Helper function for search()
        
            ;param search: string that is being searched for
            :param data: string of a single cell
            :retern boolean: True if data contains search
        """

        """save computations"""
        sl = len(search)
        dl = len(data)

        """if length is too big return false"""
        if sl > dl:
            return False
        """if length is the same compare directly"""
        if sl == dl:
            if search == data:
                return True
            else:
                return False

        """if length is smaller, then cycle through each substring"""
        spot = 0
        while spot + sl < dl:
            if data[spot:spot+sl] == search:
                return True
            spot +=1

        return False

    def sort(self,sortPrimary = None,sortSecondary = None):
        """
            Sort all the rows given a primary and secondary sorting priority
            If the primary value of multiple nodes is the same, they are orgonized 
            in relation to each other in terms of their secondary sorting priority
        
            ;param sortPrimary: primary sorting priority
            :param sortSecondary: secondary sorting priority
            :retern boolean: True if no errors 
        """

        """base case is no search"""
        self.primarySort = -1
        self.secondarySort = -1
            
        """Cicle through titles to deturmine sorting"""
        spot = 0
        while spot < len(self.title):
            if self.title[spot] == sortPrimary:
                self.primarySort = spot
            elif self.title[spot] == sortSecondary:
                self.secondarySort = spot
            spot += 1

        """Stop if primary sorting not properly specified"""
        if self.primarySort == -1 :
            return True

        """get the in order of the right AVL tree"""
        primary = self.AVLs[self.primarySort].inOrder()
        secondarySet = []

        """if no secondary sort"""
        if self.secondarySort == -1:
            self.rows = primary
            self.visible = self.rows.copy()
            return True

        """if secondary sort specified"""
        i = 1
        prev = primary[0]
        temp = [prev]
        while i < len(self.rows):
            curr = primary[i]
            # print(curr.toString())

            """if curr is the same as prev, add curr to the temp list"""
            if prev.row[self.primarySort] == curr.row[self.primarySort]:
                temp.append(curr)
                # print(curr.toString(),"prev is the same")
            else:
                """create a new AVLTree and add temp list of the same primary value to it"""
                secondaryAVL = AVLTree()
                for t in temp:
                    t.sortPriority = self.secondarySort
                    secondaryAVL.add(t)
                # secondaryAVL.toString()
                temp = secondaryAVL.inOrder()
                
                """add the secondary order to the final order"""
                secondarySet += temp
                temp = [curr]
            i += 1
            prev = curr
        
        """do this one last time for the last bit of data"""
        secondaryAVL = AVLTree()
        for t in temp:
            t.sortPriority = self.secondarySort
            secondaryAVL.add(t)
        # secondaryAVL.toString()
        temp = secondaryAVL.inOrder()
        secondarySet += temp

        self.rows = secondarySet
        self.visible = self.rows.copy()

        return True

    def addRow(self):
        """
            Add an empty row to the bottom of the table
        
       
            ;retern boolean: True if no errors 
        """

        baby = RowNode()

        """Fill in new row with apropriate number of columns"""
        for r in self.title:
            baby.row.append("")

        """add the row to the bottom of the rows"""
        self.rows.append(baby)

        """add new row to the AVL Trees with correct sort priority"""
        i = 0
        while i < len(self.AVLs):
            for node in self.rows:
                node.sortPriority = i
            self.AVLs[i].add(baby)
            i += 1
        
        self.visible = self.rows.copy()

        return True
            
    def addCol(self,name):
        """
            Add an empty column to the right side
        
            ;param name: name of the column to go in title bar
            :retern boolean: True if no errors 
        """

        """make sure the type is a string"""
        if type(name) != type.__str__:
            name = str(name)

        """add the title to the title list and change column lenth"""
        self.title.append(name)
        self.columnLength.append(len(name))

        """add a new AVL tree to the list of AVL trees"""
        avl = AVLTree()
        self.AVLs.append(avl)
        
        """add each row to the new avl tree, with apropriate sortPriority"""
        for row in self.rows:
            row.row.append("")
            row.sortPriority = len(self.title)-1
            avl.add(row)

        self.visible = self.rows.copy()

        return True

    def removeRow(self,row):
        """
            Remove a specified row

            ;param row: the row number to be removed
            :retern boolean: True if no errors 
        """

        """if valid input"""
        if row < len(self.visible):
            """remove node from visible and rows"""
            node = self.visible[row]
            self.visible.pop(row)
            self.rows.remove(node)
            return True
        return False

    def removeCol(self,col):
        """
            Remove specifed column
        
            ;param col: column to remove
            :retern boolean: True if no errors 
        """

        """if valid input"""
        if col < len(self.title):
            """remove column from every row"""
            self.title.pop(col)
            self.AVLs.pop(col)
            self.columnLength.pop(col)
            for node in self.rows:
                node.row.remove(node.row[col])
            return True
        return False

    def insert(self, data, row, col):
        """
            Insert data at a specific cell
        
            ;param data: data to be inserted
            :param row: row to be inserted at
            :param col: column to be inserted at
            :retern boolean: True if no errors 
        """

        """checking for valid inputs"""
        if type(data) != type.__str__:
            data = str(data)
        if row >= len(self.visible):
            return False
        if col >= len(self.title):
            return False

        """get the rowNode"""
        r = self.visible[row]

        """set sorting prioity for all nodes"""
        for node in self.rows:
            node.sortPriority = col

        """remove the row node from the AVL of the column"""
        self.AVLs[col].remove(r)

        """change the data of the correct column and row"""
        r.put(data,col)

        """add the row back to the AVL of the column"""
        self.AVLs[col].add(r)

        """re-calculate column length with the new addition"""
        self.__calcColLen__()
        
        return True

    def get(self,row,col):
        """
            Get data from a specific cell
        
            ;param row: row of the cell
            :param col: column of the cell
            :retern data: return data as a string, None if illigitimate parameters  
        """

        """checking for valid inputs"""
        if col >= len(self.title):
            return None
        if row >= len(self.visible):
            return None

        """return"""
        node = self.visible[row]
        data = node.row[col]
        return data

    def __calcColLen__(self):
        """
            private method to calculate the column length of each column. This is used
            to keep track of the max width of each column
        
            ;retern boolean: True if no errors 
        """

        """goes through each column"""
        col = 0
        while col < len(self.title):
            """check if the title is the longest string"""
            if len(self.title[col]) > self.columnLength[col]:
                self.columnLength[col] = len(self.title[col])

            """check wich row holds the largest string for the column"""
            for r in self.rows:
                if len(r.row[col]) > self.columnLength[col]:
                    self.columnLength[col] = len(r.row[col])
            col += 1
        return True

    def toString(self):
        """
            Print the data base to the terminal
        
            ;retern boolean: True if no errors 
        """

        if len(self.title) == 0:
            print("Database Empty")
            return False

        print("")

        currRow = []

        """Print title"""
        spot = 0
        while spot < len(self.title):
            
            """add ' ' to reach len"""
            numSpace = self.columnLength[spot] - len(self.title[spot])
            full = self.title[spot] + " "*(numSpace)
            currRow.append(full)
            spot += 1
            
        self.__printRow__(currRow,True)

        """print visible rows"""
        for row in self.visible:
            currRow = []
            spot = 0
            """goes through all the spots in row"""
            while spot < len(self.title):

                """add ' ' to reach len"""
                numSpace = self.columnLength[spot] - len(row.row[spot])
                full = " "*(numSpace) + row.row[spot]
                currRow.append(full)
                spot += 1
            
            self.__printRow__(currRow,False)

        return True
            
    def __printRow__(self, row, isTitle):
        """
            helper funcion to toString(), executes all the printing 
        
            ;param row: row to print
            :param isTitle: boolean stating if the row is the Title
            :retern boolean: True if no errors 
        """

        """edge print"""
        prt = "|"
        for spot in row:
            prt = prt + spot + "|"
        print(prt)

        """title seperation"""
        if(isTitle == True):
            prt = "+"
            for num in self.columnLength:
                prt = prt + num*"-" + "+"
            print(prt)

        return True