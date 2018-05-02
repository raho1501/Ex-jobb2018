from coapthon.server.coap import CoAP
from coapthon.resources.resource import Resource
from numpy.random import random
import time
import threading
import paho.mqtt.client as mqtt
lock = threading.Lock()
resource_container = [];

class CoAPServer(CoAP):
    def __init__(self,host,port):
        CoAP.__init__(self,(host,port))
        self.add_resource('basic/', BasicResource())

class BasicResource(Resource):
    def __init__(self, name="BasicResource", coap_server=None):
        super(BasicResource, self).__init__(name, coap_server, visible=True,
                                            observable=True,
                                            allow_children=True)
        self.payload = str(20 + (5*random()))
        global resource_container 
    def render_GET(self, request):
        temp = str(20 + (5*random()))
        self.payload = temp[:5]
        return self

    def render_PUT(self, request):
        print "My recieved PAYLOAD is: " + self.payload
        
        lock.acquire()
        pos = request.payload.find(":")
        index = request.payload[:pos]
        resource_container[int(index)] = request.payload[pos+1:]
        self.payload = request.payload[pos+1:]
        ##print "\n\n"+index+"    "+request.payload[pos+1:]+"\n\n"
        lock.release()
        return self

    def render_POST(self, request):
        res = BasicResource()
        res.location_query = request.uri_query
        res.payload = request.payload
        return res

    def render_DELETE(self, request):
        return True
#----------------------------------------------------------------------------
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
        print "Got request from: "+msg.topic+" "+str(msg.payload)
        #print str(msg.payload[3:])
        collected_val = resource_container[msg.payload[3:]]
        
        self.mclient.publish("/home_result","Get for "+msg.payload[3:]+" resulted in:\n"+collected_val)
        

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
                self.mqclient.publish(self.topic_dir, ' : '.join(resource_container ))
                print "Published msg!"
                lock.release()
                time.sleep(10)
            #self.mclient.loop_forever()
        else:
            print "Waiting for request..."
            self.mqclient.loop_forever()
                


#----------------------------------------------------------------------------

def main():
    container_size = 300
    for i in range(0,container_size):
        resource_container.append("0")
        
    thread_mqtt = mqtt_part(mqtt.Client(),"/home",str(301))
    thread_mqtt.start()
    server = CoAPServer("127.0.0.1", 5683)
    print "starting server..."
    try:
        server.listen(1)
        print "RUNNING"
        
    except KeyboardInterrupt:
        print "\n server shutting down..."
        server.close()
        print "\n Server is off now. "

if __name__ == '__main__':
    main()
