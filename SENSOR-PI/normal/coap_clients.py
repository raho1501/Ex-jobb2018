from coapthon.client.helperclient import HelperClient
import time
import threading
from numpy.random import random

host = "10.14.1.176"
port = 5683
path ="basic"
lock = threading.Lock()
class Sensorrequester(threading.Thread):
    def __init__(self,client, path,thread_id):
        threading.Thread.__init__(self)
        self.client = client
        self.path = path
        self.thread_id = thread_id
        self.response = ""
        self.text = ""
        global lock
    def run(self):
        while(True):
            lock.acquire()
            temp = str(20 + (5*random()))
            temp_ret = self.thread_id+":"+temp[:5]
            self.response = self.client.put(self.path,temp_ret)
            print self.response
            lock.release()
    def collectOne(self):
        self.response = self.client.get(self.path)
        id_print = "\nID: "+self.thread_id+"\n-----\n\n"
        return self.response.payload
         


def main():
    client = HelperClient(server=(host, port))
    number_of_threads = 300
    thread_pool = []
    for i in range(0,number_of_threads):
        thread = Sensorrequester(client,path, str(i))
        thread_pool.append(thread)
    for th in thread_pool:
        th.start()

    print "RUNNING"

if __name__=='__main__':
    main()
