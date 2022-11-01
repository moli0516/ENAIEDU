from base64 import encode
import socket
import threading
import json
import time
import os

datas = []

def handleClient():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("0.0.0.0",1234))
        s.listen()
        while True:
            c, addr = s.accept()
            print(addr , " connected")
            c.sendall(b'Connected')
            while True:
                data = c.recv(1024)
                data = data.decode()
                datas.append(data)
                if data.startswith("passw"):
                    SID = []
                    PASSW = []
                    NAME = []
                    SCHOOL = []
                    GRADE = []
                    with open("D:\\git-repos\ENAIEDU\\server\\users\\user.json","r",encoding="utf-8") as f:
                        userData = json.load(f)
                    for i in userData:
                        SID.append(i['SID'])
                        PASSW.append(i['PASSW'])
                        NAME.append(i['SNAME'])
                        SCHOOL.append(i['SCHOOL'])
                        GRADE.append(i['GRADE'])
                        inputSID = str(datas[1])[3:] 
                    print(inputSID)
                    print(SID)
                    inputPassw = str(datas[2])[6:]
                    print(inputPassw)
                    print(PASSW)
                    time.sleep(2)
                    if str(inputSID) in SID:
                        i = SID.index(inputSID)
                        if str(inputPassw) == str(PASSW[i]):
                            print("login success")
                            c.sendall(NAME[i].encode())
                            time.sleep(0.5)
                            c.sendall(GRADE[i].encode())
                            time.sleep(0.5)
                            c.sendall(SCHOOL[i].encode())
                            time.sleep(0.5)
                            c.sendall(SID[i].encode())
                        else:
                             print("Wrong Password")
                    else:
                        print("Wrong ID")

                if data.endswith(".json"):
                    passage = open(datas[3], 'r', encoding="utf-8")
                    passage = passage.read()
                    quest = open(datas[4], 'r', encoding="utf-8")
                    quest = json.load(quest)
                    quest = json.dumps(quest)
                    c.sendall(passage.encode())
                    print("transfered")
                    time.sleep(0.5)
                    c.sendall(quest.encode())
                    print("transfered")

                if data == "report":
                    repDict = str(datas[5])[5:]
                    parDict = "D:/git-repos/ENAIEDU/server/report/"
                    path = os.path.join(parDict, repDict)
                    try:
                        os.mkdir(path)
                    except FileExistsError:
                        pass
                    with open(path + "\\report.txt", 'w') as f:
                        f.write(datas[5])
                        f.write('\n')
                        f.write(datas[6])
                        f.write('\n')
                        f.write(datas[7])
                        f.write('\n')
                        f.write(datas[8])
                        f.write('\n')
                else:
                    pass

t = threading.Thread(target=handleClient)
t.start()
