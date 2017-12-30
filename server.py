import logging
from websocket_server import WebsocketServer
import json
from game import Game
from food import *

game = Game()
clients = {}


def new_client(client, server):
    print "hi", client


def message_received(client, server, message):

    msg = json.loads(message)
    if msg["type"] == "login":
        print "login", message

        if msg["playerName"] not in list(clients.itervalues()):
            game.add_player(msg["playerName"])
            server.send_message_to_all(game.to_json())
            if game.ready:
                game.start()
        clients[client["id"]] = msg["playerName"]

    if msg["type"] == "move":
        game.move(clients[client["id"]], msg["args"]["direction"])
    elif msg["type"] == "start-cut":
        game.start_cut(clients[client["id"]])
    elif msg["type"] == "take-drop":
        game.take_or_drop(clients[client["id"]])

    server.send_message_to_all(game.to_json())


server = WebsocketServer(12345, host='0.0.0.0')
server.set_fn_new_client(new_client)
server.set_fn_message_received(message_received)
server.run_forever()