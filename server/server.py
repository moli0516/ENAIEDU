import socket
from types import NoneType

s = socket.socket()
s.bind(("0.0.0.0",1234))
s.listen()
c, addr = s.accept()
with c:
    print(addr , " connected")
    c.sendall(b"System: connected to the server")
    while True:
        data = c.recv(1024)
        print(data.decode())
        lines = []
        lines = lines.append(data.decode())
        print(lines)
        if data.decode() == "report":
            with open("D:\git-repos\ENAIEDU\server\\report\\report.txt", 'w') as f:
                for i in range(len(lines)):
                    f.write(lines[i])
                    f.write('\n')

