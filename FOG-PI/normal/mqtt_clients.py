from coapthon.server.coap import CoAP
from coapthon.resources.resource import Resource
from numpy.random import random
import time
import threading
import paho.mqtt.client as mqtt
lock = threading.Lock()
resource_container = [];
mqtt_container = [];

class mqtt_part(threading.Thread):
    def __init__(self,client, topic_dir,thread_id):
        threading.Thread.__init__(self)
        self.mqclient = client
        self.topic_dir = topic_dir
        self.thread_id = thread_id
        global lock
        global resource_container 
    # The callback for when the client receives a CONNACK response from the server.
    def on_connect(self,client, userdata, flags, rc):
        print("Connected with result code "+str(rc))

        # Subscribing in on_connect() means that if we lose the connection and
        # reconnect then subscriptions will be renewed.
        self.mqclient.subscribe(self.topic_dir)

    # The callback for when a PUBLISH message is received from the server.
    def on_message(self,client, userdata, msg):
        print "Got request from: "+msg.topic+" "+str(msg.payload[3:])
        #print str(msg.payload[3:])
        collected_val = str(20 + (5*random())) #resource_container[msg.payload[3:]]
        
        self.mqclient.publish("/home_result","Get for "+msg.payload[3:]+" resulted in:\n"+resource_container[int(msg.payload[3:])])
        

    def run(self):
        
        self.mqclient.on_connect = self.on_connect
        self.mqclient.on_message = self.on_message
        self.mqclient.connect("10.14.1.199", 1883, 300)

        # Blocking call that processes network traffic, dispatches callbacks and
        # handles reconnecting.
        # Other loop*() functions are available that give a threaded interface and a
        # manual interface.
        if(self.topic_dir == "/home"):
            #self.mclient.loop_forever()
            while(True):
                lock.acquire()
                temp = str(20 + (5*random()))
                self.mqclient.publish(self.topic_dir, temp[:5])
                print "Published msg! " +  self.thread_id
                resource_container[int(self.thread_id)] = temp[:5]
                lock.release()
                time.sleep(.25)
            #self.mclient.loop_forever()
        else:
            print "Waiting for request..."
            self.mqclient.loop_forever()
                

def main():
    size = 150
    for i in range(0,size):
        resource_container.append("0")
    for i in range(0,size):
        thread_mqtt = mqtt_part(mqtt.Client(),"/home",str(i))
        mqtt_container.append(thread_mqtt)
    read_thread = mqtt_part(mqtt.Client(),"/home_req",str(301))
    print "Threads created \n"

    for th in mqtt_container:
        th.start()
    read_thread.start()
    print "Threads running \n"

if __name__ == '__main__':
    main()
