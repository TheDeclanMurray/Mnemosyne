from pynput.keyboard import Key, Controller, Listener
from Database.Data import Data
import os
from colorama import Fore, Style
import keyboard as kb

class Prompter():
    """
        Class that handles (for the most part) terminal interactions
    """

    def __init__(self):
        self.controler = Controller()
        self.dataBase = Data()
        self.errorText = []
        self.instructions = Fore.RED + """   Q quit, I insert, D delete row or column, R add row, C add column, 
   F search, T sort, S save , A save as, O open, K delete page, N new page, P Pause""" + Style.RESET_ALL


    def terminalPrompter(self):
        """
            Open a new dataBase and wait for keyboard comand
        """
        input1 = self.handleTerminal()
        while input1 != "Q":

            # insert into the database at the selected cell
            if input1 == "I":
                currtext = self.dataBase.get(self.dataBase.selectedRow,self.dataBase.selectedCol)
                for l in currtext:
                    kb.press_and_release("shift")
                    press = '' 
                    if l.isupper() and not l.isnumeric():
                        press = "shift + "
                    press += l.lower()
                    print("  leter:",press)
                    kb.press_and_release(press)
                info = input(Fore.GREEN + "Cell Contents: ")
                self.dataBase.insert(info)
                self.dataBase.saveStatus = False

            # Delete a row or column
            elif input1 == "D":
                rem = input("Row or Column: ")
                if rem.lower() in ["r","row"]:
                    # sugest a row to remove and remove the specified row
                    currRow = str(self.dataBase.selectedRow)
                    for char in currRow:
                        kb.press(char)
                    row = int(input(Fore.GREEN + "Row: "))
                    self.dataBase.removeRow(row)
                elif rem.lower() in ["c","col","column"]:
                    # sugest a column to remove and remove the specified column
                    currCol = str(self.dataBase.selectedCol)
                    for char in currCol:
                        kb.press(char)
                    col = int(input(Fore.GREEN +  "Column: "))
                    self.dataBase.removeCol(col)
                self.dataBase.saveStatus = False

            # add a column
            elif input1 == "C":
                name = input(Fore.GREEN + "Column Name: ")
                self.dataBase.addCol(name)
                self.dataBase.saveStatus = False

            # add a row
            elif input1 == "R":
                self.dataBase.addRow()
                self.dataBase.saveStatus = False

            # search for something in the database
            elif input1 == "F":
                search = input(Fore.GREEN + "Search: ")
                self.dataBase.search(search)

            # sort the database
            elif input1 == "T":
                primary = input(Fore.GREEN + "Primary: ")     # primary sort priority
                secondary = input(Fore.GREEN + "Secondary: ") # secondary sort priority
                self.dataBase.sort(primary,secondary)

            elif input1 == "O":
                # sugest saving the database if unsaved
                if not self.dataBase.saveStatus:
                    self.savePrompt()

                # ask for the database name
                inputfile = input(Fore.GREEN + "Open: ")
                inputfile = "storage/" + inputfile + ".txt"
                 
                # open the given database if file exists
                rtn = False
                try: 
                    rtn = self.openData(inputfile)
                    if rtn != False:
                        self.dataBase = rtn
                except Exception as a:
                    prt = Fore.RED + "File "+inputfile + " does not exist"
                    self.errorText.append(prt)

            # Save database
            elif input1 == "S":
                if self.dataBase.name == "Untitled Document":
                    self.saver(True)
                else:
                    self.saver()

            # Save data base under a new name
            elif input1 == "A":
                self.saver(True)

            # Delete the database from the screen and from storage
            elif input1 == "K":
                fileName = "storage/" + self.dataBase.name + ".txt"
                try:
                    os.remove(fileName)
                except:
                    pass
                self.dataBase = Data()

            # open a new/empty database
            elif input1 == "N":

                if not self.dataBase.saveStatus:
                    self.savePrompt()
                    
                self.dataBase = Data()
                self.dataBase.saveStatus = True

            # Pause the keyboard listener
            elif input1 == "P":
                keepGoing = input("Ready to Continue Y/N? ")
                while keepGoing != "Y":
                    keepGoing = input("Ready to Continue Y/N? ")

            # wait for next comand
            input1 = self.handleTerminal()

        # prompt a save, reset the colorpalate and clear the screen
        if not self.dataBase.saveStatus:
            self.savePrompt()
        print(Style.RESET_ALL)
        self.handleTerminal(False)
        kb.release("shift")

    def saver(self,saveAs = False):
        if saveAs:
            outputFile = input("Save as: ")
            self.dataBase.name = outputFile
        outputFile = "storage/" + self.dataBase.name + ".txt"
        try: 
            self.saveData(outputFile)
            self.dataBase.saveStatus = True
        except Exception as a:
            prt = Fore.RED + "Can not save to " + outputFile
            self.errorText.append(prt)

    def userInput(self):
        """
            wait for a valid user input and then return that input

            ;return rtn: string of a character
        """

        self.rtn = None
        def on_press(key):
            if key == Key.shift:
                return

            try:
                k = key.char
            except:
                k = key.name

            if k == "right":
                self.dataBase.selectCell("right")
                return False
            if k == "left":
                self.dataBase.selectCell("left")
                return False
            if k == "up":
                self.dataBase.selectCell("up")
                return False
            if k == "down":
                self.dataBase.selectCell("down")
                return False

            if k in ["Q","P","I","D","R","C","S","A","T","O","N","K","F"]:
                self.rtn = k
                return False
        
        # Keyboard listener
        listener = Listener(on_press=on_press)
        listener.start()
        listener.join()
        
        # clear the recorded keystrokes and return
        self.controler.press(Key.esc)
        return self.rtn

    def handleTerminal(self, rePrint = True):
        """
            Clears the terminal, then if rePrint is true, prints the current database

            ;param rePrint: wether or not to print the current database again, defalts to true
        """
        if(True):
            comand = 'clear'
            if os.name in ('nt', 'dos'):
                comand = "cls"
            os.system(comand)

        # print the current database and wait for a valid user input via keyboard
        if rePrint:
            for a in self.errorText:
                print(a)
            self.errorText = []
            self.dataBase.toString()
            print(self.instructions)
            # rtn = input("Input: ")
            rtn = self.userInput()
            return rtn

    def savePrompt(self):
        """
            Prompt the user to save their work on the current database
        """
        saveSugestion = input("Save Work(Y/N)? ")
        
        if saveSugestion == "Y":
            if self.dataBase.name == "Untitled Document":
                self.saver(True)
            else:
                self.saver()
        self.dataBase.saveStatus = True

    def openData(self, inputFile):
        """
            Open a specified file and read it into a database

            ;param inputFile: string name of a file
            :return: True if no erros
        """
        try: 
            if(inputFile != None):    
                with open(inputFile) as f:
                    text = f.readlines()
                f.close()
            else:    
                return False
        except Exception as a:
            prt = Fore.RED + "File "+inputFile +" does not exist"
            self.errorText.append(prt)
            return False

        data = Data()
        row = 0
        col = 0
        colLength = 0

        for line in text:
            txt = line[2:len(line)-1] # gets the data in each line
            type = line[0:1]          # gets the datatype
            
            # Database Name
            if type == "0": 
                data = Data()
                data.name = txt
                data.addRow()
                
            # Column Title
            elif type == "1":
                data.addCol(txt)
                colLength += 1

            # Cell contents
            elif type == "2":
                data.insert(txt,row,col)
                col +=1
                if col == colLength:
                    data.addRow()
                    row +=1
                    col = 0

        # An extra row gets added so remove that
        data.removeRow(data.rows.length-1) 
        return data
        
    def saveData(self, saveFile):
        """
            Save current database to a given file, create the file if it does not exist
        
            ;param saveFile: file location
            :return: True if no errors
        """
        if(saveFile != None):
            with open(saveFile, "w") as f:
                Lines = self.dataBase.save()
                for line in Lines:
                    f.write(line)
            f.close()
            return True
        else:
            return False