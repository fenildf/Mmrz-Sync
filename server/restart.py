import os

print("killing server.py")
os.system("ps -ef | grep server.py | grep -v grep | cut -c 9-15 | xargs kill -s 9")

print("restarting server.py")
os.system("nohup python server.py&")
