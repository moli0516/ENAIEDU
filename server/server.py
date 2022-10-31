import socket
import threading
import json
import time

lines = []

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
                lines.append(data)
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
                        inputSID = "['" + str(lines[1])[3:] + "']"
                        print(inputSID)
                        print(SID)
                        inputPassw = "['" + str(lines[2])[6:] + "']"
                        print(inputPassw)
                        print(PASSW)
                        time.sleep(5)
                        for i in range(len(SID)):
                            if str(inputSID) == str(SID[i]):
                                if str(inputPassw) == str(PASSW[i]):
                                    print("login success")
                                    s.sendall(NAME[i].encode())
                                else:
                                    print("Wrong Password")
                            else:
                                print("Wrong ID")

                if data == "report":
                    with open("D:\git-repos\ENAIEDU\server\\report\\report.txt", 'w') as f:
                        for i in range(len(lines)):
                            if i == 6:
                                f.write(lines[i])
                                f.write(lines[i+1])
                                f.write('\n')
                            elif i>9:
                                pass

t = threading.Thread(target=handleClient)
t.start()