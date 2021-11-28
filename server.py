import socket
import asyncore
import random
import pickle

BUFFERSIZE = 512

outgoing = []

class Player:
    def __init__(self, ownerid):
        self.ownerid = ownerid

playermap = {}

def updateWorld(message):
    arr = pickle.loads(message)
    print(str(arr))
    playerid = arr[1]

    if playerid == 0: return

    remove = []

    for i in outgoing:
        update = ['player locations']

        for key, value in playermap.items():
            update.append([value.ownerid])
    
        try:
            i.send(pickle.dumps(update))
        except Exception:
            remove.append(i)
            continue
    
        print('sent update data')

        for r in remove:
            outgoing.remove(r)

class MainServer(asyncore.dispatcher):
    def __init__(self, port):
        asyncore.dispatcher.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.bind(('', port))
        print(f"Listening on port {port}")
        self.listen(10)
    def handle_accept(self):
        conn, addr = self.accept()
        print(f'Connection address: {addr[0]} {str(addr[1])}')
        outgoing.append(conn)
        playerid = random.randint(1000, 1000000)
        player = Player(playerid)
        playermap[playerid] = player
        conn.send(pickle.dumps(['id update', playerid]))
        SecondaryServer(conn)

class SecondaryServer(asyncore.dispatcher_with_send):
  def handle_read(self):
    recievedData = self.recv(BUFFERSIZE)
    if recievedData:
        updateWorld(recievedData)
    else:
        self.close()

MainServer(4321)
asyncore.loop()