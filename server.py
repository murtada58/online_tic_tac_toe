import socket
import threading
from networking import send, recieve
from CONSTANTS import *

PORT = 5050
SERVER =  "" #socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

data = {"messages": {}, "players": set()}

def handle_client_send(conn, addr, player_id):
    connected = True
    while connected:
        if player_id in data["messages"]:
            if data["messages"][player_id] == DISCONNECT_MESSAGE:
                connected = False
                del data["messages"][player_id]
                print(f"[DISCONNECTED SENDER FOR {player_id}]")
        
            else:
                send(data["messages"][player_id], conn)
                print(f"[SENT] {data['messages'][player_id]} TO {player_id}")
                del data["messages"][player_id]

    conn.close()

def handle_client_recieve(conn, addr, player_id):
    print(f"[CONNECTED] {addr}")
    connected = True
    send(str(player_id), conn)
    while connected:
        msg = recieve(conn)
        print(f"[RECIEVED] {msg} FROM {player_id}")
        to_id, msg = msg.split("|")
        to_id = int(to_id)
        if msg == DISCONNECT_MESSAGE:
            connected = False
            data["players"].remove(player_id)
            data["messages"][player_id] = msg
            print(f"[DISCONNECTED RECIEVER FOR {player_id}]")
        else:
            data["messages"][to_id] = msg

    conn.close()



def start():
    server.listen()
    print(f"[LISTENING] ON {SERVER}")
    while True:
        conn, addr = server.accept()
        if 1 not in data["players"]:
            data["players"].add(1)
            player = 1
        elif 2 not in data["players"]:
            data["players"].add(2)
            player = 2
        else:
            print("[IGNORED EXTRA PLAYER]")
            continue
        thread = threading.Thread(target=handle_client_recieve, args=(conn, addr, player))
        thread.start()
        thread = threading.Thread(target=handle_client_send, args=(conn, addr, player))
        thread.start()
        print(f"[PLAYERS] {data['players']}")

print("[STARTING]")
start()