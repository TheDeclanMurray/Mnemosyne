from pynput.keyboard import Key, Controller
from Database.Data import Data
import os
import time

class Prompter():

    def __init__(self):
        self.controler = Controller()
        self.dataBase = Data()
        self.saveStatus = True
        self.errorText = []
        self.instructions = """   Q quit, I insert, D delete row or column R add row, C add column, 
   F search, T sort, S save , A save as, O open, K delete page, N new page """


    def terminalPrompter(self):

        input1 = self.handleTerminal()
        while input1 != "Q":

            if input1 == "I":
                row = input("Row: ")
                col = input("Column: ")
                info = input("Cell Contents: ")
                self.dataBase.insert(info,row,col)
                self.saveStatus = False

            elif input1 == "D":
                rem = input("Row or Column: ")
                if rem.lower() == "row":
                    row = int(input("Row: "))
                    self.dataBase.removeRow(row)
                elif rem.lower() == "col" or rem.lower() == "column":
                    col = int(input("Column: "))
                    self.dataBase.removeCol(col)
                self.saveStatus = False

            elif input1 == "C":
                name = input("Column Name: ")
                self.dataBase.addCol(name)
                self.saveStatus = False

            elif input1 == "R":
                self.dataBase.addRow()
                self.saveStatus = False

            elif input1 == "F":
                search = input("Search: ")
                self.dataBase.search(search)

            elif input1 == "T":
                primary = input("Primary: ")
                secondary = input("Secondary: ")
                self.dataBase.sort(primary,secondary)

            elif input1 == "O":

                if not self.saveStatus:
                    self.savePrompt(self.dataBase)

                inputfile = input("Open: ")
                inputfile = "storage/" + inputfile + ".txt"
                 
                rtn = False
                try: 
                    rtn = self.openData(inputfile)
                except Exception as a:
                    self.errorText.append(a)

                if rtn != False:
                    self.dataBase = rtn

            elif input1 == "S":
                outputFile = "storage/" + self.dataBase.name + ".txt"
                try: 
                    self.saveData(outputFile, self.dataBase)
                    self.saveStatus = True
                except Exception as a:
                    self.errorText.append(a)

            elif input1 == "A":
                outputFile = input("Save as: ")
                self.dataBase.name = outputFile
                outputFile = "storage/" + outputFile + ".txt"
                try: 
                    self.saveData(outputFile, self.dataBase)
                except Exception as a:
                    self.errorText.append(a)

            elif input1 == "K":
                fileName = "storage/" + self.dataBase.name + ".txt"
                try:
                    os.remove(fileName)
                except:
                    pass
                self.dataBase = Data()

            elif input1 == "N":

                if not self.saveStatus:
                    self.savePrompt()
                    
                self.dataBase = Data()
                self.saveStatus = True


            input1 = self.handleTerminal()

        if not self.saveStatus:
            self.savePrompt(self.dataBase)
        self.handleTerminal(False)

    def userInput(self):

        self.rtn = None
        from pynput import keyboard

        def on_press(key):
            # if key == keyboard.Key.esc:
            #     print("Key is esc")
            #     return False
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

            self.rtn = k
            return False
        
        listener = keyboard.Listener(on_press=on_press)
        listener.start()
        listener.join()
        
        self.controler.press(Key.esc)

        # time.sleep(1)
        
        return self.rtn

        pass

    def handleTerminal(self, rePrint = True):

        if(True):
            comand = 'clear'
            if os.name in ('nt', 'dos'):
                comand = "cls"
            os.system(comand)

        if rePrint:
            for a in self.errorText:
                print(a)
            self.errorText = []
            self.dataBase.toString()
            print(self.instructions)
            # rtn = input("Input: ")
            rtn = self.userInput()
            return rtn

    def savePrompt(self, data):
        saveSugestion = input("Save Work(Y/N)? ")
        
        if saveSugestion == "Y":
            outputFile = "storage/" + data.name + ".txt"
            try: 
                self.saveData(outputFile, data)
            except Exception as a:
                self.errorText.append(a)
        self.saveStatus = True


    def openData(self, inputFile):

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

        data.removeRow(data.rows.length-1) 
        return data
        

    def saveData(self, saveFile, currDataBase):

        print("SaveData Running")
        if(saveFile != None):
            with open(saveFile, "w") as f:
                Lines = currDataBase.save()
                print("line",Lines.printable())
                for line in Lines:
                    f.write(line)
            f.close()
        else:
            return False