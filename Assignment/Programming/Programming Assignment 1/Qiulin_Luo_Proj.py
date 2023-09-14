# Description #
'''
As the communication is a TCP connection, a "three-way handshake" operation is required first.

After defining the target host and port, send an introMessage to perform "three-way handshakes".

Since more than one expression is sent back from the target host, I defined a loop.

Each loop receives an expression for processing, and the exit condition is when the client host receives
a message that is not an EXPR message, but a SUCC message.

In the processing of the EXPR message, I used regular expression matching to extract the expressions in
the message string and stored the operators and operands in two separate tuples.

The final result of the operation is obtained by string and number conversion and sent to the destination
host via socket, which gets a response and goes on to the next loop.

Finally, I get SUCC message and flag information after jumping out of the loop.
'''

# NU ID number #
'''
002191479
'''

# Secret flag #
'''
4a9e41cf99af26d31f1467fcd304a65ea93f6ff2860fefa2857c9bbc7aad1bbf
'''
from socket import *
import re

serverName = 'kopi.ece.neu.edu'
serverPort = 5203
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName, serverPort))

introMessage = 'EECE7374 INTR 002191479'
clientSocket.send(introMessage.encode())

while True:
    expMessage = clientSocket.recv(4096)

    dMessage = expMessage.decode()
    if dMessage[9] != 'E':
        break
    else:
        expString = expMessage.decode()[14:]
        number = re.findall(r"\d*\d", expString)
        opr = re.findall('[\+\-\*\/]',expString)

        if opr[0] == '+':
            result = int(number[0]) + int(number[1])
        elif opr[0] == '-':
            result = int(number[0]) - int(number[1])
        elif opr[0] == '*':
            result = int(number[0]) * int(number[1])
        elif opr[0] == '/':
            result = int(number[0]) / int(number[1])

        resultMessage = 'EECE7374 RSLT ' + str(result)
        clientSocket.send(resultMessage.encode())

print(dMessage)
print("The flag is:", dMessage[14:])

clientSocket.close()
