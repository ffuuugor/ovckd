import logging
from websocket_server import WebsocketServer
import json
from game import Game

game = Game()
clients = []

def new_client(client, server):
    clients.append(client)
    game.add_player(client["id"])
    if game.ready:
        game.start()

def message_received(client, server, message):
    pass

server = WebsocketServer(12345, host='0.0.0.0')
server.set_fn_new_client(new_client)
server.run_forever()