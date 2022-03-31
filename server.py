# server code
import socket
import threading
import time
import argparse

# parser that checks if necessary arguments are provided
argParser = argparse.ArgumentParser(description="Start the chat server and listen for incoming connections. for.Example: python3 server.py 4444 \n"
                                                "\n To connect to one of the chat rooms. type: client.py localhost 4444 (host or bots name)")
argParser.add_argument("port", type=int, help="The server is running on 'Integers datatyp'")
args = argParser.parse_args()
port = args.port

#It returns a socket object which has the following main methods: bind(), listen()
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#this object is used to associate the socket with local address
serverSocket.bind(("localhost", port))
# this is for listen for connections
serverSocket.listen()
clientNames = []  # ths is  list of the client names
clients = []  # list of clients



# function. which sends message from one client to other clients
def clientMessages(message, client):
    # looping through the client connection
    for host in clients:
        # sends only to other clinets
        if host is not client:
            host.send(message)


#client controller receives the message from the clients and sends it to other clients.
# If the client ends the connection or there are other errors,
# it will remove them from the server and send a message to other connected clients that the client has left the chat.
def clientController(client):
    while True:
        try:
            # Receive message from clients
            message = client.recv(1024)
            # Decode the message to text
            hostmsg = message.decode().split(": ")

            if (hostmsg[1] == "exit"):
                time.sleep(1)
                print("The clients are disconnected")
                for host in clients:
                    host.close()
                print("The server stopped listening ...")
                exit()

            else:
                # send messages to all bots
                time.sleep(0.5)
                clientMessages(message, client)

        except:
            # Get the index from the client connection.
            index = clients.index(client)
            clients.remove(client)
            # used to mark the socket as closed
            client.close()
            name = clientNames[index]
            clientMessages(f"{name} has disconnected from the chat room!".encode("utf-8"), client)
            print(f"{name} disconnected from the chat room")
            # Remove clientname from the list.
            clientNames.remove(name)
            break


# set server status and connect incoming clients to the server(chat room)
def start():
    print("\nThe server is listening to connections...\n"
          "to connect to one of the chat rooms. type: client.py localhost 4444 (host or bots name)\n"
          "you can use one of the bots(Alice, Bob, Tor, Bob)\n"
          "For the host you can use different name")
    while True:
        # to accept the connection and add to a new clients.
        client, address = serverSocket.accept()

        client.send("name?".encode("utf-8"))
        name = client.recv(1024).decode("utf-8")
        # Append the clientname to the server
        clientNames.append(name)
        # Append the request to the bot list
        clients.append(client)
        print(f"Successfully connection with {name} {str(address)}")
        clientMessages(f"{name} is now successfully connected to the chat room".encode("utf-8"), client)
        client.send("You are now connected to the chat room!".encode("utf-8"))
        # Start a new thread to check the new client connection
        thread = threading.Thread(target=clientController, args=(client,))
        thread.start()


start()


