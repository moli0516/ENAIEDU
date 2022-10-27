import nltk
from nltk.tokenize import word_tokenize
import json
import sys
import socket

class main:
    def __init__(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(("192.168.50.15",1234))
        s.sendall(b"hi, nigger")
        self.data = s.recv(1025)
        print(self.data.decode())
        nltk.download('punkt')
        print('''          _____                    _____                    _____                    _____                            _____                    _____                    _____          
         /\    \                  /\    \                  /\    \                  /\    \                          /\    \                  /\    \                  /\    \         
        /::\    \                /::\____\                /::\    \                /::\    \                        /::\    \                /::\    \                /::\____\        
       /::::\    \              /::::|   |               /::::\    \               \:::\    \                      /::::\    \              /::::\    \              /:::/    /        
      /::::::\    \            /:::::|   |              /::::::\    \               \:::\    \                    /::::::\    \            /::::::\    \            /:::/    /         
     /:::/\:::\    \          /::::::|   |             /:::/\:::\    \               \:::\    \                  /:::/\:::\    \          /:::/\:::\    \          /:::/    /          
    /:::/__\:::\    \        /:::/|::|   |            /:::/__\:::\    \               \:::\    \                /:::/__\:::\    \        /:::/  \:::\    \        /:::/    /           
   /::::\   \:::\    \      /:::/ |::|   |           /::::\   \:::\    \              /::::\    \              /::::\   \:::\    \      /:::/    \:::\    \      /:::/    /            
  /::::::\   \:::\    \    /:::/  |::|   | _____    /::::::\   \:::\    \    ____    /::::::\    \            /::::::\   \:::\    \    /:::/    / \:::\    \    /:::/    /      _____  
 /:::/\:::\   \:::\    \  /:::/   |::|   |/\    \  /:::/\:::\   \:::\    \  /\   \  /:::/\:::\    \          /:::/\:::\   \:::\    \  /:::/    /   \:::\ ___\  /:::/____/      /\    \ 
/:::/__\:::\   \:::\____\/:: /    |::|   /::\____\/:::/  \:::\   \:::\____\/::\   \/:::/  \:::\____\        /:::/__\:::\   \:::\____\/:::/____/     \:::|    ||:::|    /      /::\____\.
\:::\   \:::\   \::/    /\::/    /|::|  /:::/    /\::/    \:::\  /:::/    /\:::\  /:::/    \::/    /        \:::\   \:::\   \::/    /\:::\    \     /:::|____||:::|____\     /:::/    /
 \:::\   \:::\   \/____/  \/____/ |::| /:::/    /  \/____/ \:::\/:::/    /  \:::\/:::/    / \/____/          \:::\   \:::\   \/____/  \:::\    \   /:::/    /  \:::\    \   /:::/    / 
  \:::\   \:::\    \              |::|/:::/    /            \::::::/    /    \::::::/    /                    \:::\   \:::\    \       \:::\    \ /:::/    /    \:::\    \ /:::/    /  
   \:::\   \:::\____\             |::::::/    /              \::::/    /      \::::/____/                      \:::\   \:::\____\       \:::\    /:::/    /      \:::\    /:::/    /   
    \:::\   \::/    /             |:::::/    /               /:::/    /        \:::\    \                       \:::\   \::/    /        \:::\  /:::/    /        \:::\__/:::/    /    
     \:::\   \/____/              |::::/    /               /:::/    /          \:::\    \                       \:::\   \/____/          \:::\/:::/    /          \::::::::/    /     
      \:::\    \                  /:::/    /               /:::/    /            \:::\    \                       \:::\    \               \::::::/    /            \::::::/    /      
       \:::\____\                /:::/    /               /:::/    /              \:::\____\                       \:::\____\               \::::/    /              \::::/    /       
        \::/    /                \::/    /                \::/    /                \::/    /                        \::/    /                \::/____/                \::/____/        
         \/____/                  \/____/                  \/____/                  \/____/                          \/____/                  ~~                       ~~              
                                                                                                                                                                                       ''')
        self.initmode = input("Writing or reading?(w/r)")
        self.initmodeLower = self.initmode.lower()
        if self.initmodeLower == "r":
            self.mode = input("Mock paper/Assignment/Self practice?(m/a/s)")
            self.modeLower = self.mode.lower
            if self.modeLower == "m":
                self.location = "D:\git-repos\ENAIEDU\server\question\m\""
                s.send(b"D:\git-repos\ENAIEDU\server\question\m\"")
            elif self.modeLower == "a":
                self.location = "D:\git-repos\ENAIEDU\server\question\a\""
                s.send(b"D:\git-repos\ENAIEDU\server\question\a\"")
            elif self.modeLower == "p":
                self.location = "D:\git-repos\ENAIEDU\server\question\p\""
                s.send(b"D:\git-repos\ENAIEDU\server\question\p\"")
            self.user = input("Are you ready to do the comprehansion?(y/n)")
            self.user = self.user.lower()
            while (self.user != "n"):
                if (self.user == "y"):
                    self.no = input("Which passage you want to do?(1/2)")
                    self.p = (self.location + self.no + ".txt")
                    self.q = (self.location + self.no + ".json")
                    self.fp = open(self.p, "r", encoding="utf-8")
                    self.fq = open(self.q, "r", encoding="utf-8")
                    self.question = []
                    self.answer = []
                    self.advise = []
                    self.prescore = []
                    self.type = []
                    self.keypoint = []
                    with open(self.q) as f:
                        self.data = json.load(f)
                    for i in self.data:
                        self.question.append(i['question'])
                        self.answer.append(i['answer'])
                        self.advise.append(i['advise'])
                        self.prescore.append(int(i['score']))
                        self.type.append(i['type'])
                        self.keypoint.append(i['keypoint'])
                    self.passage()
                    self.questions()
        elif self.initmodeLower == "w":
            return
        self.quit()
    def passage(self):
        print(self.fp.read())
    def questions(self):
        self.score = 0
        self.result = []
        for i in range(len(self.question)):
                inputAnswer = input(self.question[i])
                if (inputAnswer == self.answer[i] and self.type[i] == "short"):
                    print("System: You are correct!")
                    self.score += self.prescore[i]
                    print(self.score)
                elif (self.type[i] == "long"):
                    self.reqKeypoint = self.keypoint[i]
                    self.score1 = self.prescore[i]
                    self.noKeypoint = 0
                    self.text = inputAnswer
                    self.tokenizedText = word_tokenize(self.text)
                    for l in range(len(self.tokenizedText)):
                        for i in range(len(self.reqKeypoint)):
                            if self.tokenizedText[l] == self.reqKeypoint[i]:
                                self.noKeypoint += 1
                    self.score += self.noKeypoint
                elif (inputAnswer == "x"):
                    self.quit()
                else:
                    print("System: Oh no! You are wrong!")
                    self.result.append(self.advise[i])
        print("score: " + str(self.score) + "/"  + str(sum(self.prescore)))
        if self.result == []:
            return
        else:
            print("advice:")
            for i in range(len(self.result)):
                self.index = str(i+1)
                print(self.index + ". " + self.result[i])
    def quit(self):
        print("System: Exiting...")
        sys.exit()
main()