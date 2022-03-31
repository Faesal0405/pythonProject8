# client code
import socket
import random
import threading
import sys
import time
import argparse



# parser who checks if the arguments are correct, ip, portnr and name.
argParser = argparse.ArgumentParser(description="to connect to one of the chat rooms. use for.Example: client.py localhost 4444 Tor")
argParser.add_argument("IP", type=str, help="IP address of server/client is connecting to.")
argParser.add_argument("port", type=int, help="The client is connecting to (Integers only).")
argParser.add_argument("name", type=str, help="name of the clients.(Alice, Tor, John and Bob)")
args = argParser.parse_args()
IP = args.IP
port = args.port
name = args.name



#It returns a socket object like 'sockets.connect()', this object is specific for client sockets.
#it immediately sends data to the server. Then it receives 1024 bytes back, closes the socket,
# and prints the received data.
# Starting a socket instance for the client.
clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Connect to the server with the local IP and port number that the user enter.
clientSocket.connect((IP, port))


# list of some keywords that you can choose to write in the chat
goodThings = ["play", "work", "write", "train", "eat"]
badThings = ["fight", "lie", "smash", "hit", "steal"]

#list of bots that are authorized
bots = ["alice", "tor", "john", "bob"]

# here are the bot functions that receive selected words from the chat and respond with appropriate answers.
#there are several alternative answers. some for good things and some for bad things.
#if a word other than that mentioned in the list is written, appropriate answers will also be sent
def alice(word):
    if word in goodThings:
        alternatives1 = [
            "{}: Did you say {}? I like it\n",
            "{}: I think {} will be nice!\n"
        ]
        return random.choice(alternatives1).format(name, word + "ing")

    elif word in badThings:
        alternatives2 = [
            "{}: {}? its will not end good\n",
            "{}: I'm not like {}, sorry.\n"
        ]
        return random.choice(alternatives2).format(name, word + "ing")

    else:
        return "{}: Sorry, this is not so interesting ..".format(name)

# chatbot function
def tor(word):
    if word in goodThings:
        alternatives3 = [
            "{}: {}...? You can't be serious..\n",
            "{}: I've better things to do than {}..\n"
        ]
        return random.choice(alternatives3).format(name, word + "ing")

    elif word in badThings:
        alternative4 = [
            "{}: Nope. Not doing that.\n",
            "{}: I don't want to do that.\n"
        ]
        return random.choice(alternative4).format(name, word + "ing")
    else:
        return "{}: Sorry, this is not so interesting ..".format(name)

# chatbot function
def john(word):
    if word in goodThings:
        alternatives5 = [
            "{}: {}?? Sure, why not, im with you:)?\n",
            "{}: {} hm, let me think about that.\n"
        ]
        return random.choice(alternatives5).format(name, word + "ing")

    elif word in badThings:
        alternatives6 = [
            "{}: Yeah I will not do things like {}...\n",
            "{}: What!{}? no..\n"
        ]
        return random.choice(alternatives6).format(name, word + "ing")

    else:
        return "{}: Sorry, this is not so interesting ..".format(name)

#chatbot function
def bob(word):
    if word in goodThings:
        alternatives7 = [
            "{}: That'd be col!\n",
            "{}: I think {} sounds great!\n"
        ]
        return random.choice(alternatives7).format(name, word + "ing")

    elif word in badThings:
        alternatives8 = [
            "{}: {}? You can't be serious.\n",
            "{}: Yeah I don't know about {}...\n"
        ]
        return random.choice(alternatives8).format(name, word + "ing")

    else:
        return "{}: Sorry, this is not so interesting ..".format(name)



# client receive is responsible for receiving the message from the server script and sending the name back.
# The while loop will run continuously and in the else if statement we take the message from the host and divide it up
# and search for the value in the word-list. If it is in the list, it will send the word to the chat-bot function,
# otherwise it will send a another text value.
def clientReceive():
    while True:
        # used to decode strings sendt like messages,
        message = clientSocket.recv(1024).decode('utf-8')

        if message == "name?":
            #Send data to the socket
            clientSocket.send(name.encode('utf-8'))

        else:
            if ":" in message:

                messageSplit = message.split(":")

                if messageSplit[0] not in bots:
                    w = ""
                    i = 0
                    #this loop that iterates through the word list and finds if the selected word exists
                    while i < len(badThings):
                        if badThings[i] in message.lower():
                            w = badThings[i]

                        if goodThings[i] in message.lower():
                            w = goodThings[i]
                        i = i + 1
                    #returns a copy of the string in which all case-based characters have been lowercased.
                    botmessage = ""
                    if name.lower() == "alice":
                        botmessage = alice(w)

                    elif name.lower() == "tor":
                        botmessage = tor(w)

                    elif name.lower() == "john":
                        botmessage = john(w)
                    elif name.lower() == "bob":
                        botmessage = bob(w)

                    #printer out messages
                    print(message)
                    clientSend(botmessage)

                else:
                    time.sleep(0.5)
                    print(message)

            else:
                print(message)


def clientSend(message):
    print(message)
    clientSocket.send(message.encode('utf-8'))


# checks client messages and send the messages to forward.
def clientMessager():
    while True:
        try:
            message = f'{name}: {input()}'
            # this breaks up a string at the specified separator and returns a string eks: name : (input)
            split = message.split(": ")
            if (split[1].isspace()):
                print("empty string. write to me!")
            elif (split[1] == ""):
                print("empty string. write to me!")
                continue
            else:
                time.sleep(0.4)
                print(message)
                clientSocket.send(message.encode('utf-8'))
        except:
            print("\nYou have disconnected from the chat room\n")
            sys.exit()
            break


receive_thread = threading.Thread(target=clientReceive)
receive_thread.start()

if name not in bots:
    send_thread = threading.Thread(target=clientMessager)
    send_thread.start()