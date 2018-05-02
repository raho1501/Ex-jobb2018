from coapthon.client.helperclient import HelperClient
import time
import threading
import paho.mqtt.client as mqtt


host = "10.14.1.216"
port = 5683
path ="basic"
lock = threading.Lock()
sensor_pool = []
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
            self.response = self.client.get(self.path)
            id_print = "\nID: "+self.thread_id+"\n-----\n\n"
            #print id_print+ self.response.payload
            sensor_pool[int(self.thread_id)] = self.response.payload
            self.text = self.response.payload
            #print "set val from: " + self.thread_id 
            lock.release()
            #print "i release " + self.thread_id
            #time.sleep(.25)
    def collectOne(self):
        self.response = self.client.get(self.path)
        id_print = "\nID: "+self.thread_id+"\n-----\n\n"
        return self.response.payload
         


#-----------------------------------------------------------------------
class mqtt_part(threading.Thread):
    def __init__(self,client, topic_dir,thread_id):
        threading.Thread.__init__(self)
        self.mclient = client
        self.topic_dir = topic_dir
        self.thread_id = thread_id
        global lock
    # The callback for when the client receives a CONNACK response from the server.
    def on_connect(self,client, userdata, flags, rc):
        print("Connected with result code "+str(rc))

        # Subscribing in on_connect() means that if we lose the connection and
        # reconnect then subscriptions will be renewed.
        self.mclient.subscribe(self.topic_dir)

    # The callback for when a PUBLISH message is received from the server.
    def on_message(self,client, userdata, msg):
        print "Got request from: "+msg.topic+" "+str(msg.payload)
        #print str(msg.payload[3:])
        client = HelperClient(server=(host, port))
        result_to_ret = Sensorrequester(client,path, str(msg.payload[3:]))
        collected_val = result_to_ret.collectOne()
        
        self.mclient.publish("/home_result","Get for "+msg.payload[3:]+" resulted in:\n"+collected_val)
        
    def run(self):
        
        self.mclient.on_connect = self.on_connect
        self.mclient.on_message = self.on_message
        self.mclient.connect("10.14.1.215", 1883, 300)

        # Blocking call that processes network traffic, dispatches callbacks and
        # handles reconnecting.
        # Other loop*() functions are available that give a threaded interface and a
        # manual interface.
        if(self.topic_dir == "/home"):
            #self.mclient.loop_forever()
            while(True):
                lock.acquire()
                self.mclient.publish(self.topic_dir, ' : '.join(sensor_pool))
                print "Published msg!"
                lock.release()
                time.sleep(10)
            #self.mclient.loop_forever()
        else:
            print "Waiting for request..."
            self.mclient.loop_forever()
                

#-----------------------------------------------------------------------

def pool_print(self, m_client):
    lock.acquire()
    print "Values:\n-----------------"
    for i in sensor_pool:
        print str(i) + "\n"
    print "-----------------\n"
    m_client.publish(topic_dir, ' '.join(sensor_pool))
    lock.release()


def main():
    client = HelperClient(server=(host, port))
    #sensor = Sensorrequester(client,path, "thread_id")
    number_of_threads = 50
    for j in range(0,number_of_threads):
        sensor_pool.append("0")
    thread_pool = []
    for i in range(0,number_of_threads):
        thread = Sensorrequester(client,path, str(i))
        thread_pool.append(thread)
    thread_mqtt = mqtt_part(mqtt.Client(),"/home",str(301))
    request_thread = mqtt_part(mqtt.Client(),"/home_req", str(302))
    for th in thread_pool:
        th.start()
    
    thread_mqtt.start()
    request_thread.start()
    print "RUNNING"
        #pool_print()
##    while(True):
##        try:
##            #response = client.get(path) #.put(path,payload) .get(path)
##            #print response.pretty_print()
##            #time.sleep(5)
##            print "Working \n"
##        except KeyboardInterrupt:
##            print "\nstoping requests \n"
##            break

##    client.stop()
if __name__=='__main__':
    main()
