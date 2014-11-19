import socket
import json

class EyetribeSentinel(object):
    def __init__(self, port=6555):
        self.port = port
        self.msg = json.dumps({"category":"tracker","request":"get",
                               "values":["trackerstate"]})
        self.connect()
        
    def connect(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect(("localhost", self.port))


    def checkValid(self):
        try:
            self.sock.send(self.msg)
            msg = json.loads(self.sock.recv(1024))
        except socket.error as e:
            self.connect()
            self.sock.send(self.msg)
            msg = json.loads(self.sock.recv(1024))            
        try:
            return msg['values']['trackerstate'] == 0
        except KeyError:
            return False
        
    def close(self):
        self.sock.close()
        
    def getDeviceName(self):
        return "TheEyeTribe eyetracker"
        
if __name__ == "__main__":
    import time
    s = EyetribeSentinel()
    valid = s.checkValid()
    print "Valid : {}".format(valid)
    valid = s.checkValid()
    print "Valid : {}".format(valid)
    for _ in range(15):
        time.sleep(15)
        valid = s.checkValid()
        print "Valid : {}".format(valid)
    s.close()