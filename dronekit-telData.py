

# Import DroneKit-Python


from dronekit import connect, VehicleMode
from twisted.internet import reactor, protocol, task
from autobahn.twisted.websocket import WebSocketClientProtocol
from twisted.python import log
from twisted.internet.task import LoopingCall,deferLater
from autobahn.twisted.websocket import WebSocketClientFactory
import sys
import json
import uuid


#class
class Data:
    #update
    global v
    v = connect('/dev/ttyAMA0', baud=57600)
    def update(self):
        
        cur_data = {
                                "uas_telemetry":{
                                "heading": v.heading,
                                #"gps": v.gps_0,
                                #"battery": v.battery,
                                #"last_heartbeat": v.last_heartbeat,
                                #"is_armable": v.is_armable,
                                #"system_status": v.system_status.state,
                                #"mode": v.mode.name,
                                #"autopilot_firmware_versions": v.version,
                                #"autopilot_capabilities": v.capabilities.ftp,
                                #"global_location": v.location.global_frame,
                                #"global_location_relative_altitude": v.location.global_relative_frame,
                                #"local_location": v.location.local_frame,
                                #"attitude:": v.attitude,
                                #"velocity:": v.velocity,
                                #"gps": v.gps_0,
                                #"groundspeed": v.groundspeed,
                                #"airspeed": v.airspeed,
                                #"gimbal_status": v.gimbal,
                                #"battery": v.battery,
                                #"ekf_ok": v.ekf_ok,
                                #"last_heartbeat": v.last_heartbeat,
                                #"rangefinder": v.rangefinder,
                                #"rangefinder_distance": v.rangefinder_distance,
                                #"rangefinder_voltage": v.rangefinder_voltage,
                                #"heading": v.heading,
                                #"is_armable": v.is_armable,
                                #"system_status": v.system_status.state,
                                #"mode": v.mode.name,
                                #"armed": v.armed                      
                                }  
                    }
        return json.dumps(cur_data)


class ClientProtocol(WebSocketClientProtocol):
    def __init__(self):
        self.telData = Data()
    #What to do once the socket is open
    def onOpen(self):
        print 2
        #Send message to server with client identity and type
        self.sendMessage('[{"proto":{"identity":"'+str(uuid.uuid1())+'","type":"uav"}}]')
        LoopingCall(self.sendTelData).start(2)
    def sendTelData(self):
        self.sendMessage(self.telData.update())
        
    #What to do once the server is connected to the client
    def onConnect(self, response):
        print "Server Connected: {0}:".format(response.peer)
        

    
    #What to do if the server sends the client a message
#    def onMessage(self, payload, isBinary):
#        if isBinary:
#            print "Binary Message"
#        else:
#            self.digest(payload)
#
#    def digest(self, payload):
#        try:
#            payload = json.loads(payload)
#            if 'capture' in payload:
#                im = self.camera.sendImg()
#                self.sendMessage(im)
#            elif 'stream' in payload:
#                self.video.startStream()
#            else: print ["No implementation for this payload:y"]+payload.keys()
#        except Exception, e:
#            print "Payload not JSON formatted string"

        
        
   
    

 


factory = WebSocketClientFactory(u"ws://www.csuiteexperiment.com:9002")
factory.protocol = ClientProtocol
reactor.connectTCP("www.csuiteexperiment.com", 9002, factory)
reactor.run()

#translation layer that takes in json of some format
#on message, lookat the json, parse

# onMessage(self, payload)
    #try:
    #       payload = json.loads(payload)
    #except:
    #       pass
"""
    {"command":{"simple_goto":[lat, lon, alt]}}
               {"change_mode":0}
    }
    if "command" in payload:
        if "simple_goto" in payload.get("command"):
            (lat, lon, alt) = payload.get("command").get("simple_goto")
            mavproxy
"""
