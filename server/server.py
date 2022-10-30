import socket
from types import NoneType

lines = []
s = socket.socket()
s.bind(("0.0.0.0",1234))
s.listen()
c, addr = s.accept()
with c:
    print(addr , " connected")
    c.sendall(b"System: connected to the server")
    while True:
        data = c.recv(1024)
        data = data.decode()
        print(data)
        lines.append(data)
        print(lines)
        if data == "report":
            with open("D:\git-repos\ENAIEDU\server\\report\\report.txt", 'w') as f:
                for i in range(len(lines)):
                    if i<5:
                        f.write(lines[i+5])
                        f.write('\n')
                    elif i>7:
                        continue
