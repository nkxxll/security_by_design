from threading import Thread
from subprocess import Popen, PIPE

# TODO: command must be changed for the production server ... later
CMD = ['python', 'manage.py', 'runserver']

# start the webserver
def start():
    p = Popen(CMD, stdin=PIPE, stdout=PIPE, stderr=PIPE)
    p.wait()
    # TODO: handle log output
    
# spawn a thread to start the webserver
t = Thread(target=start)
t.start()
t.join()
