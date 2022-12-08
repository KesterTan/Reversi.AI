# CITATION OF CLIENTS, SERVERS, SOCKET AND THREADING: https://www.youtube.com/watch?v=-3B1v-K1oXE&ab_channel=TechWithTim
import socket
from _thread import *
import sys
import threading
import threaded as threaded
# setting up server connection
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# setting up server and port
server = ''
port = 5555

server_ip = socket.gethostbyname(server)

# binding server connection (use try catch to output any errors)
try:
    s.bind((server, port))

except socket.error as e:
    print(str(e))

# listening for a connection to the server
# maximum of 2 connections
s.listen(3)
print("Connecting...")

currentId = "0"
# starts a new thread
def threaded(conn):
    global currentId
    connection.send(str.encode(currentId))
    reply = ''
    while True:
        try:
            data = conn.recv(2048)
            reply = data.decode('utf-8')
            if not data:
                conn.send(str.encode("Goodbye"))
                break
            else:
                print(f"Received {reply}")
                conn.sendall(str.encode(reply))
        except:
            print("An error occurred")
            break

# get all different connections
while True:
    # establish connection with client
    connection, address = s.accept()
    print(f"Connection found: {address}")

    start_new_thread(threaded, (connection, ))










