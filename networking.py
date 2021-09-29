from CONSTANTS import *

def send(msg, sender):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    sender.send(send_length)
    sender.send(message)


def recieve(reciever):
    msg_length = reciever.recv(HEADER).decode(FORMAT)
    if msg_length:
        msg_length = int(msg_length)
        msg = reciever.recv(msg_length).decode(FORMAT)
        return msg