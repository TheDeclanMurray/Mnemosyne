from Database.AVLTree import AVLTree
from Database.DArray import DArray
from colorama import Fore, Back 

class RowNode():

    def __init__(self, len = 4):
        self.row = DArray(len)
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

        if node.row.get(self.sortPriority) == "":
            return -1
        if self.row.get(self.sortPriority) == "":
            return 1
        if self.row.get(self.sortPriority) < node.row.get(self.sortPriority):
            return -1
        if self.row.get(self.sortPriority) > node.row.get(self.sortPriority):
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
        self.row.put(data,col)
        return True

    def save(self):
        """
            returns a python array of how to save the cell data

            ;return rtn: python array
        """

        rtn = DArray()
        for cell in self.row:
            add = "2 "+cell +"\n"
            rtn.append(add)
        return rtn
        

class Data:

    def __init__(self):
        self.name = "Untitled Document"
        self.title = DArray() # Array of the names of each column
        self.rows = DArray() # Array of all Row nodes
        self.visible = DArray() # Array of visible Row nodes
        self.columnLength = DArray() # Array keeping track of the max lenght of each collum
        self.__AVLs = DArray() # Array of AVLTrees, one for each column
        self.__primarySort = -1 # the column number of the primary sort priority (-1 if none)
        self.__secondarySort = -1 # the column number of the secondary sort priorty (-1 if none)
        self.selectedRow = 0
        self.selectedCol = 0
        self.saveStatus = True

    def selectCell(self, comand):

        if comand == "right":
            if self.selectedCol+1 < self.title.length:
                self.selectedCol +=1
                return True
        if comand == "left":
            if self.selectedCol > 0:
                self.selectedCol -=1
                return True
        if comand == "up":
            if self.selectedRow > 0:
                self.selectedRow -=1
                return True
        if comand == "down":
            if self.selectedRow +1 < self.rows.length:
                self.selectedRow +=1
                return True

        return False

    def save(self):
        rtn = DArray(self.title.length+1)
        """Database Name"""
        rtn.append("0 "+self.name+"\n")

        """Titles"""
        for col in self.title:
            rtn.append("1 "+col+"\n")

        """Data"""
        for row in self.rows:
            rowStrings = row.save()
            rtn = rtn.addArray(rowStrings)
        
        return rtn

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
        self.visible = DArray()

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
        while spot + sl <= dl:
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
        self.__primarySort = -1
        self.__secondarySort = -1
            
        """Cicle through titles to deturmine sorting"""
        spot = 0
        while spot < self.title.length:
            if self.title.get(spot) == sortPrimary:
                self.__primarySort = spot
            elif self.title.get(spot) == sortSecondary:
                self.__secondarySort = spot
            spot += 1

        """Stop if primary sorting not properly specified"""
        if self.__primarySort == -1 :
            return True

        """get the in order of the right AVL tree"""
        primary = self.__AVLs.get(self.__primarySort).inOrder()
        secondarySet = DArray()

        """if no secondary sort"""
        if self.__secondarySort == -1:
            self.rows = primary
            self.visible = self.rows.copy()
            return True

        """if secondary sort specified"""
        i = 1
        prev = primary.get(0)
        temp = DArray()
        temp.append(prev)
        while i < self.rows.length:
            curr = primary.get(i)

            """if curr is the same as prev, add curr to the temp list"""
            if prev.row.get(self.__primarySort) == curr.row.get(self.__primarySort):
                temp.append(curr)
            else:
                """create a new AVLTree and add temp list of the same primary value to it"""
                secondaryAVL = AVLTree()
                for t in temp:
                    t.sortPriority = self.__secondarySort
                    secondaryAVL.add(t)
                temp = secondaryAVL.inOrder()
                
                """add the secondary order to the final order"""
                secondarySet = secondarySet.addArray(temp)
                temp = DArray()
                temp.append(curr)
            i += 1
            prev = curr
        
        """do this one last time for the last bit of data"""
        secondaryAVL = AVLTree()
        for t in temp:
            t.sortPriority = self.__secondarySort
            secondaryAVL.add(t)
        temp = secondaryAVL.inOrder()
        secondarySet = secondarySet.addArray(temp)

        self.rows = secondarySet
        self.visible = self.rows.copy()

        return True

    def addRow(self):
        """
            Add an empty row to the bottom of the table
       
            ;retern boolean: True if no errors 
        """

        baby = RowNode(self.title.size)

        """Fill in new row with apropriate number of columns"""
        for i in range(self.title.length):
            baby.row.append("")

        """add the row to the bottom of the rows"""
        self.rows.append(baby)

        """add new row to the AVL Trees with correct sort priority"""
        i = 0
        while i < self.__AVLs.length:
            for node in self.rows:
                node.sortPriority = i
            self.__AVLs.get(i).add(baby)
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
        self.__AVLs.append(avl)
        
        """add each row to the new avl tree, with apropriate sortPriority"""
        for row in self.rows:
            row.row.append("")
            row.sortPriority = self.title.length-1
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
        if row < self.visible.length:
            """remove node from visible and rows"""
            node = self.visible.get(row)
            self.visible.remove(row)
            self.rows.remove(row)

            """remove the row from every AVL tree"""
            col = 0
            for avl in self.__AVLs:
                for row in self.rows:
                    row.sortPriority = col
                avl.remove(node)
                col +=1

            self.__calcColLen__()
            if self.selectedRow >= self.rows.length:
                self.selectedRow -= 1
            return True
        return False

    def removeCol(self,col):
        """
            Remove specifed column
        
            ;param col: column to remove
            :retern boolean: True if no errors 
        """

        """if valid input"""
        if col < self.title.length:
            """remove column from every row"""
            self.title.remove(col)
            self.__AVLs.remove(col)
            self.columnLength.remove(col)
            for node in self.rows:
                node.row.remove(col)

            if self.selectedCol >= self.title.length:
                self.selectedCol -= 1
            return True
        return False

    def insert(self, data, row = None, col = None):
        """
            Insert data at a specific cell
        
            ;param data: data to be inserted
            :param row: row to be inserted at
            :param col: column to be inserted at
            :retern boolean: True if no errors 
        """
        if row == None:
            row = self.selectedRow
        if col == None:
            col = self.selectedCol

        """checking for valid inputs"""
        if type(data) != type.__str__:
            data = str(data)

        try:
            col = int(col)
            if col >= self.title.length:
                return False
        except:
            return False

        if row == "t":
            self.title.put(data, col)
            self.__calcColLen__()
            return True

        try:
            row = int(row)
        except:
            return False
            

        if row >= self.visible.length:
            return False
        if col >= self.title.length:
            return False

        """get the rowNode"""
        r = self.visible.get(row)

        """set sorting prioity for all nodes"""
        for node in self.rows:
            node.sortPriority = col

        """remove the row node from the AVL of the column"""
        self.__AVLs.get(col).remove(r)

        """change the data of the correct column and row"""
        r.put(data,col)

        """add the row back to the AVL of the column"""
        self.__AVLs.get(col).add(r)

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
        if col >= self.title.length:
            return None
        if row >= self.visible.length:
            return None

        """return"""
        node = self.visible.get(row)
        data = node.row.get(col)
        return data

    def __calcColLen__(self):
        """
            private method to calculate the column length of each column. This is used
            to keep track of the max width of each column
        
            ;retern boolean: True if no errors 
        """

        self.columnLength = DArray()

        """goes through each column"""
        col = 0
        while col < self.title.length:
            """check if the title is the longest string"""
            self.columnLength.append(len(self.title.get(col)))

            """check wich row holds the largest string for the column"""
            for r in self.rows:
                if len(r.row.get(col)) > self.columnLength.get(col):
                    self.columnLength.put(len(r.row.get(col)), col)
            col += 1
        return True

    def toString(self):
        """
            Print the data base to the terminal
        
            ;retern boolean: True if no errors 
        """

        prtName = Fore.GREEN + self.name
        if self.saveStatus == False:
            prtName += "*"
        print(prtName)

        if self.title.length == 0:
            print("Database Empty, add Column and Rows")
            print()
            return False


        currRow = DArray()

        """Print title"""
        spot = 0
        while spot < self.title.length:
            
            """add ' ' to reach len"""
            numSpace = self.columnLength.get(spot) - len(self.title.get(spot))
            full = self.title.get(spot) + " "*(numSpace)
            currRow.append(full)
            spot += 1
            
        self.__printRow__(currRow,True)

        """print visible rows"""
        col = 0
        for row in self.visible:
            currRow = DArray()
            spot = 0
            """goes through all the spots in row"""
            while spot < self.title.length:

                """add ' ' to reach len"""
                numSpace = self.columnLength.get(spot) - len(row.row.get(spot))
                full = " "*(numSpace) + row.row.get(spot)
                if col == self.selectedRow and spot == self.selectedCol:
                    full = Back.WHITE +Fore.BLACK + full + Back.BLACK + Fore.GREEN
                currRow.append(full)
                spot += 1
            
            self.__printRow__(currRow,False)
            col += 1

        print("")
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