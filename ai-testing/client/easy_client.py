from SimpleWebSocketServer import SimpleWebSocketServer, WebSocket
import json

class EasyAIPlayer(WebSocket):

    self.clients = []

    def handleMessage(self):
        # self.sendMessage(self.data)
        print self.data

    def handleConnected(self):
        self.clients.append({str(self.address): [TicTacToe([Human_Player(), AI_Player])]})
        print self.address, 'connected'

    def handleClose(self):
        print self.address, 'closed'

server = SimpleWebSocketServer('', 8000, EasyAIPlayer)
server.serveforever()
