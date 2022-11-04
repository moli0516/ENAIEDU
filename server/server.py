import socket
import threading
import language_tool_python
import json
import time
import os

#dataExamples:
#   onLogin: {"task":"login","sid":"000000000","passw":"qwerty"}
#   onGetAvaliablePapers: {"task":"getallpaper"}
#   onGetPaper: {"task":"getpaper","paperType":"mock","paper":"1"}
#   onCalculateWritingResult: {"task":"calcwriting","writing":"Hello! World!"}
#   onSendReport: {"task":"sendreport","sid":"000000000","name":"abc","grade":"A","score":'5/5'}
#

paperPaths = {
    'Mock':'m',
    'Assignment':'a',
    'Self practice':'s'
}
currentDir = os.path.dirname(os.path.abspath(__file__))

grammarChecker = language_tool_python.LanguageTool('en-US')

class server:
    def __init__(self):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
        self.server.bind(("0.0.0.0",1234))
        self.server.listen(200)
        print("listening...port:1234")
        self.listen()
    
    def listen(self):
        while True:
            c, addr = self.server.accept()
            print(addr , " connected")
            #c.sendall(b'Connected')
            t = threading.Thread(target=self.handleClient,args=(c,))
            t.daemon = True
            t.start()

    def sendClient(self,s,data):
        s.send(data.encode('utf-8')+b'\r\nSocketEnd\r\n')

    def handleClient(self,c):
        while True:
            try:
                sdata = b''
                while True:
                    d = c.recv(2)
                    sdata += d
                    if sdata.endswith(b'\r\nSocketEnd\r\n'):break
                sdata = sdata.decode()[:-13] #remove b'\r\nSocketEnd\r\n'
                data = json.loads(sdata)
            except: #user might disconnected
                print('Disconnected')
                c.close()
                break
            if data['task'] == "login":
                SID = []
                PASSW = []
                NAME = []
                SCHOOL = []
                GRADE = []
                with open(currentDir+"\\users\\user.json","r",encoding="utf-8") as f:
                    userData = json.load(f)
                for i in userData:
                    SID.append(i['SID'])
                    PASSW.append(i['PASSW'])
                    NAME.append(i['SNAME'])
                    SCHOOL.append(i['SCHOOL'])
                    GRADE.append(i['GRADE'])
                    inputSID = data['sid']
                print(inputSID)
                print(SID)
                inputPassw = data['passw']
                print(inputPassw)
                print(PASSW)
                if str(inputSID) in SID:
                    i = SID.index(inputSID)
                    if str(inputPassw) == str(PASSW[i]):
                        print("login success")
                        self.sendClient(c,json.dumps({
                            "state":1,
                            "name":NAME[i],
                            "grade":GRADE[i],
                            "school":SCHOOL[i]
                        }))
                    else:
                        print("Wrong Password")
                        self.sendClient(c,json.dumps({"state":0}))
                else:
                    print("Wrong ID")
                    self.sendClient(c,json.dumps({"state":0}))
            if data['task'] == "getpaper":
                paperPath = currentDir+"\\question\\"+paperPaths[data['paperType']]+"\\"+data['paper']+"\\"+data['paper']
                passage = open(paperPath+'.txt', 'r', encoding="utf-8")
                passage = passage.read()
                quest = open(paperPath+'.json', 'r', encoding="utf-8")
                quest = json.load(quest) 
                print(passage,quest)
                self.sendClient(c,json.dumps({
                    "text":passage,
                    "questions":quest
                }))
                print("transfered")    
            if data['task'] == 'calcwriting':
                writing = data['writing']
                mistakes = []
                matches = grammarChecker.check(writing)
                for m in matches:
                    wordNo = str(len(writing[:m.errorLength+m.offset].split(' ')))
                    if len(m.replacements):
                        mistakes.append(m.ruleIssueType+' in '+wordNo+['th','st','nd','rd',*['th']*7][int(wordNo[-1])]+" word: '"+writing[m.offset:m.errorLength+m.offset]+"' may change to '"+m.replacements[0]+"'")
                        m.replacements = ["[color=e0483a]"+writing[m.offset:m.errorLength+m.offset]+"[/color]|[color=58e02b]"+m.replacements[0]+'[/color]'+' ']
                correction = language_tool_python.utils.correct(writing,matches)
                self.sendClient(c,json.dumps({
                    "mistakes":mistakes,
                    "correction":correction
                }))
            if data['task'] == "sendreport":
                path = currentDir+"\\report\\"+data['sid']
                if not os.path.exists(path): os.mkdir(path)
                with open(path + "\\report.txt", 'w') as f:
                    f.write("SID: "+data['sid']+"\nName: "+data['name']+"\nGrade: "+data['grade']+"\nScore: "+data['score']+'\n')
                    f.close()
                self.sendClient(c,json.dumps({"state":1}))
            else:
                pass

server()