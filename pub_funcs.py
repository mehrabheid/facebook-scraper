from datetime import datetime
import socket
from time import sleep
from datetime import datetime
from db_funcs import execute_commit
def saveLogs(logs):
    logsTime_now = datetime.utcnow()
    logsTime = logsTime_now.strftime('%Y/%m/%d %H:%M:%S')
    webSiteName = "website"
    with open(webSiteName, 'a') as saver :
        savedLog='{'+'"time":"{}", "domain":"{}", "error":"{}"'.format(logsTime,webSiteName,logs)+'} \n'
        saver.write(savedLog)
        saver.close()

def saveErrorLogs(logs):
    logsTime_now = datetime.utcnow()
    logsTime = logsTime_now.strftime('%Y/%m/%d %H:%M:%S')
    webSiteName = "website"
    with open(webSiteName, 'a') as saver :
        savedLog='{'+'"time":"{}", "domain":"{}", "error":"{}"'.format(logsTime,webSiteName,logs)+'} \n'
        saver.write(savedLog)
        saver.close()    

def ping():
    try:
        socket.setdefaulttimeout(3)
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        host = "8.8.8.8"
        port = 53
        server_address = (host, port)
        s.connect(server_address)
    except OSError as error:
        return False
    else:
        s.close()
        return True

def connect():
    while True:
        if not ping():
            saveLogs('network disconnected sleep for 10 sec')
        else:
            break  
        sleep(10)        

def savePID(proccess_id,proccess_name):
    pid=proccess_id
    pname=proccess_name
    proccessTime = datetime.now()
    sqlquery='insert into your_table_for_PID (pid, rundate, pid_name)VALUES(%s, %s, %s)'
    sqlvals=(pid, proccessTime, pname)
    execute_commit(sqlquery,sqlvals)       