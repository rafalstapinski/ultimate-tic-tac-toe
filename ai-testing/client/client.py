import easyAI.TwoPlayersGame
from SimpleWebSocketServer import SimpleWebSocketServer, WebSocket

class AIPlayer(WebSocket):

    def handleMessage(self):
        self.sendMessage(self.data)

    def handleConnected(self):
        print self.address, 'connected'

    def handleClose(self):
        print self.address, 'closed'
