import easyAI.TwoPlayersGame
from SimpleWebSocketServer import SimpleWebSocketServer, WebSocket
import json

class AIPlayer(WebSocket):

    def handleMessage(self):
        # self.sendMessage(self.data)
        print self.data

    def handleConnected(self):
        print self.address, 'connected'

    def handleClose(self):
        print self.address, 'closed'

server = SimpleWebSocketServer('', 8000, AIPlayer)
server.serveforever()
