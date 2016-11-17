import os

app_name = "Mmrz-Sync.py"

print("killing {0}".format(app_name))
os.system("ps -ef | grep {0} | grep -v grep | cut -c 9-15 | xargs kill -s 9".format(app_name))

print("restarting {0}".format(app_name))
os.system("nohup python {0}&".format(app_name))
