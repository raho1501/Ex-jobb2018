from coapthon.server.coap import CoAP
from coapthon.resources.resource import Resource
from numpy.random import random
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

    def render_GET(self, request):
        temp = str(20 + (5*random()))
        self.payload = temp[:5]
        return self

    def render_PUT(self, request):
        print "My recieved PAYLOAD is: " + self.payload
        self.payload = request.payload
        return self

    def render_POST(self, request):
        res = BasicResource()
        res.location_query = request.uri_query
        res.payload = request.payload
        return res

    def render_DELETE(self, request):
        return True


def main():
    server = CoAPServer("10.14.1.216", 5683)
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
