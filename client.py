import nltk
from nltk.tokenize import word_tokenize
import json
import sys
import socket
from colorama import Fore, Style, init
import language_tool_python
import time
import re
import heapq

tool = language_tool_python.LanguageTool('en-US')

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(("127.0.0.1",1234))
s.send(b"hi, nigger")
data = s.recv(1024)
data = data.decode()
class start:
    def __init__(self):
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
        self.username = "ID " + input("UserID: ")
        s.sendall(self.username.encode())
        self.password = "passw " + input("Password:")
        s.sendall(self.password.encode())
        self.login()

    def login(self):
        global name
        global grade
        global school
        global SID
        studentDatas = []
        for i in range(4):
            Data = s.recv(1024)
            studentDatas.append(Data.decode())
        name = studentDatas[0]
        grade = studentDatas[1]
        school = studentDatas[2]
        SID = studentDatas[3]
        if name:
            print("Welcome! " + str(name))
            welcome()
        else:
            pass
class welcome:
    def __init__(self):
        self.initmode = input("Writing or reading?(w/r)")
        self.initmode = self.initmode.lower()
        if self.initmode == "r":
            reading()
        elif self.initmode == "w":
            writing()

class finish:
    def __init__(self):
        self.report = input("System: Type 'y' to get the report. ")
        if self.report:
            self.report1 = "report"
            s.sendall(self.report1.encode())
        self.initmode = input("Writing or reading?(w/r)")
        self.initmode = self.initmode.lower()
        if self.initmode == "r":
            reading()
        
class reading:
    def __init__(self):
        self.mode = input("Mock paper/Assignment/Self practice?(m/a/s)")
        self.modeLower = self.mode.lower()
        if self.modeLower == "m":
            self.location = "D:\git-repos\ENAIEDU\server\question\m\\"
        elif self.modeLower == "a":
            self.location = "D:\git-repos\ENAIEDU\server\question\a\\"
        elif self.modeLower == "p":
            self.location = "D:\git-repos\ENAIEDU\server\question\p\\"
        self.no = input("Which passage you want to do?(1/2)")
        self.p = (self.location + self.no + "\\" + self.no+ ".txt")
        s.sendall(self.p.encode())
        self.q = (self.location + self.no + "\\" + self.no+ ".json")
        s.sendall(self.q.encode())
        self.receive()
    
    def receive(self):
        paperDatas = []
        print("System: Waiting to receive paper...")
        for i in range(2):
            data = s.recv(4096)
            paperDatas.append(data.decode())
            time.sleep(1)
        self.text = paperDatas[0]
        self.questBank = paperDatas[1]
        self.questBank = json.loads(self.questBank)
        self.question = []
        self.answer = []
        self.advise = []
        self.prescore = []
        self.type = []
        self.keypoint = []
        self.choice = []
        for i in self.questBank:
            self.question.append(i['question'])
            self.answer.append(i['answer'])
            self.advise.append(i['advise'])
            self.prescore.append(int(i['score']))
            self.type.append(i['type'])
            self.keypoint.append(i['keypoint'])
            self.choice.append(i['choice'])
        self.user = input("Are you ready to do the comprehansion?(y/n)")
        self.user = self.user.lower()
        if (self.user == "y"):
            self.readingComp()
        elif (self.user == "n"):
            self.quit()
    def readingComp(self):
        self.passage()
        self.questions()
    def passage(self):
        print(self.text)
    def questions(self):
        self.score = 0
        self.result = []
        for i in range(len(self.question)):
            print(self.question[i])
            if (self.type[i] == "MC"):
                self.reqChoice = self.choice[i]
                for l in range(len(self.reqChoice)):
                    print(self.reqChoice[l])
            inputAnswer = input("Answer: ")
            inputAnswer = inputAnswer.lower()
            if (inputAnswer == self.answer[i] and self.type[i] == "short"):
                print("System: You are correct!")
                self.score += self.prescore[i]
                print(self.score)
            elif (self.type[i] == "long"):
                self.reqKeypoint = self.keypoint[i]
                self.noKeypoint = 0
                self.text = inputAnswer
                self.tokenizedText = word_tokenize(self.text)
                for l in range(len(self.tokenizedText)):
                    for i in range(len(self.reqKeypoint)):
                        if self.tokenizedText[l] == self.reqKeypoint[i]:
                            self.noKeypoint += 1
                self.score += self.noKeypoint
            elif (self.type[i] == "MC"):
                if inputAnswer == self.answer[i]:
                    print("System: You are correct!")
                    self.score += self.prescore[i]
                    print(self.score)
                else:
                    print("System: Oh no! You are wrong!")
                    self.result.append(self.advise[i])
            elif (inputAnswer == "x"):
                self.quit()
            else:
                print("System: Oh no! You are wrong!")
                self.result.append(self.advise[i])
        if (self.score / sum(self.prescore)) > 0.7:
            self.grade = "A"
        elif (self.score / sum(self.prescore)) > 0.6:
            self.grade = "B"
        elif (self.score / sum(self.prescore)) > 0.5:
            self.grade = "C"
        elif (self.score / sum(self.prescore)) > 0.4:
            self.grade = "D"
        elif (self.score / sum(self.prescore)) > 0.3:
            self.grade = "E"
        else:
            self.grade = "F"
        print("score: " + str(self.score) + "/"  + str(sum(self.prescore)))
        if self.result == []:
            self.report1 = ("SID: " + SID)
            self.report2 = ("Name: " + name)
            self.report3 = ("Grade: " + self.grade)
            self.report4 = ("Score: " + str(self.score) + "/"  + str(sum(self.prescore)))
            s.sendall(self.report1.encode())
            time.sleep(0.5)
            s.sendall(self.report2.encode())
            time.sleep(0.5)
            s.sendall(self.report3.encode())
            time.sleep(0.5)
            s.sendall(self.report4.encode())
            print("----------------------------------------------------------------------------------")
            finish()
        else:
            print("advice:")
            for i in range(len(self.result)):
                self.index = str(i+1)
                print(self.index + ". " + self.result[i])
            self.report1 = ("SID: " + SID)
            self.report2 = ("Name: " + name)
            self.report3 = ("Grade: " + self.grade)
            self.report4 = ("Score: " + str(self.score) + "/"  + str(sum(self.prescore)))
            s.sendall(self.report1.encode())
            time.sleep(0.5)
            s.sendall(self.report2.encode())
            time.sleep(0.5)
            s.sendall(self.report3.encode())
            time.sleep(0.5)
            s.sendall(self.report4.encode())
            print("----------------------------------------------------------------------------------")
            finish()
            
    def quit(self):
        print("System: Exiting...")
        sys.exit()

class writing:
    def __init__(self):
        self.confirm = input("System: Have you uploaded your writing file as txt yet?(y/n) ")
        if self.confirm != "n":
            if self.confirm == "y":
                self.fileName = input("System: File name?")
                self.w = "D:\git-repos\ENAIEDU\server\writing\\1\\" + self.fileName + ".txt"
                self.fw = open(self.w, 'r', encoding="utf-8")
                self.text()

    def text(self):
        self.originText = self.fw.read()
        print("origin text")
        print(self.originText)
        self.grammarChecking()

    def grammarChecking(self):
        self.mistake = []
        self.correction = []
        self.start = []
        self.end = []
        self.rule = []
        self.matches = tool.check(self.originText)
        print("Number of grammar mistake: " + str(len(self.matches)))
        for i in self.matches:
            if len(i.replacements) > 0:
                self.start.append(i.offset)
                self.end.append(i.errorLength + i.offset)
                self.mistake.append(self.originText[i.offset:i.errorLength + i.offset])
                self.correction.append(i.replacements[0])
                self.rule.append(i.ruleIssueType)
        self.grammarMistake = list(zip(self.mistake, self.correction, self.rule))
        for i in range(len(self.grammarMistake)):
            print(self.grammarMistake[i])
        self.newText = list(self.originText)
 
        for m in range(len(self.start)):
            for i in range(len(self.originText)):
                self.newText[self.start[m]] = self.correction[m]
                self.newText[self.start[m]] = Fore.RED + self.newText[self.start[m]] + Style.RESET_ALL
                if (i>self.start[m] and i<self.end[m]):
                    self.newText[i]=""
     
        self.newText = "".join(self.newText)
        print("The new text:")
        print(self.newText)
        formattedText = re.sub('[^a-zA-Z]', ' ', self.newText)
        formattedText = re.sub(r'\s+', ' ', formattedText)
        if len(nltk.word_tokenize(formattedText)) > 200:
            self.summarise()
        else:
            self.quit()
        
    def summarise(self):
        stopwords = nltk.corpus.stopwords.words('english')
        formattedText = re.sub('[^a-zA-Z]', ' ', self.newText)
        formattedText = re.sub(r'\s+', ' ', formattedText)
        sentenceList = nltk.sent_tokenize(self.newText)
        
        wordFeq = {}
        for i in nltk.word_tokenize(formattedText):
            if i not in stopwords:
                if i not in wordFeq.keys():
                    wordFeq[i] = 1
                else:
                    wordFeq[i] += 1
        
        maxFeq = max(wordFeq.values())
        for i in wordFeq.keys():
            wordFeq[i] = (wordFeq[i]/maxFeq)
            
        sentScore = {}
        for i in sentenceList:
            for j in nltk.word_tokenize(i.lower()):
                if j in wordFeq.keys():
                    if len(i.split(' ')) < 30:
                        if i not in sentScore.keys():
                            sentScore[i] = wordFeq[j]
                        else:
                            sentScore[i] += wordFeq[j]

        summarySent = heapq.nlargest(7, sentScore, key=sentScore.get)
        summary = ' '.join(summarySent)
        print(summary)

    def quit(self):
        print("System: Exiting...")
        sys.exit()

if __name__ == '__main__':
    start()