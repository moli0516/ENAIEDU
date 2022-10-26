import socket

s = socket.socket()
s.bind(("0.0.0.0",1234))
s.listen()
c, addr = s.accept()
with c:
    print(addr , " connected")
    c.sendall(b"System: connected to the server")
    while True:
        data = c.recv(1024)
        if data.decode() != "":
            print(data.decode())
