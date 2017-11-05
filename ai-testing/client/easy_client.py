from SimpleWebSocketServer import SimpleWebSocketServer, WebSocket
import json

class EasyAIPlayer(WebSocket):

    self.clients = []

    def handleMessage(self):
        # self.sendMessage(self.data)
        print self.data

    def handleConnected(self):
        # self.clients.append(self.address, )
        print self.address, 'connected'

    def handleClose(self):
        print self.address, 'closed'

server = SimpleWebSocketServer('', 8000, EasyAIPlayer)
server.serveforever()
