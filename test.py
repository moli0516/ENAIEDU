from http.client import GATEWAY_TIMEOUT
import json

gay = open("D:\git-repos\ENAIEDU\server\question\m\\1\\1.json", 'r', encoding="utf-8")
gay = json.load(gay)

print(type(gay))
print(type(gay[1]))
gayDump = json.dumps(gay)
print(type(gayDump))
gayload = json.loads(gayDump)
print(type(gayload))
print(gayload[0])
print(gayload[1])