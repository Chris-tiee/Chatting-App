# Chatting-App
Set up a simple peer-to-peer chatting application using Python. Ensured reliability of the messages in an unreliable network simulated by a network emulator (netem)
The project was done in pair.

To explain the code briefly: for each host we have two functions that are running in parallel constantly.
- The first function called receive() specifies the local IP and local port of the host and then 
creates a socket which we will bind using the local IP and local port. This socket is always 
checking the buffer associated with the host so whenever it receives a message it fetches it and 
decodes it to then display it on the screen.
- The second function called send() specifies the IP address and port number of the person it 
wants to send the message to and then also creates a socket which we will bind using the local 
IP and local port. Whenever the user inputs a message in the screen, this message will be 
encoded and sent using the socket. 
So far, the two hosts can easily communicate with each other, but in an unreliable environment 
messages will be lost. To fix this we wrote a code that will make sure to tell the sender that the message 
has been correctly received.
To ensure the messages were well received we simply needed to send back an ACK but since we needed 
to account for the time delay, we needed to keep track of which ACK belongs to which message sent 
otherwise messages would be ACKed wrongfully. We simply needed to keep track of the sequence 
number of the message we are sending and the corresponding ACK that we are receiving to avoid 
duplicates and to do that we used a global variable called SEQ . 
Following the code step by step in an ideal situation: 
- Whenever a host inputs a message to send, a “1” would get concatenated to the beginning of 
the message before encoding and sending it. This “1” would serve as an indicator to the second 
host that the message received is a message to be displayed.
- Once the message is sent the function “time.sleep(0.5)” would stall the sending code for 0.5 
seconds to give the message enough time to arrive to the receiver and an ACK to come back.
This function serves as a timeout essentially.
- During this time, the message would be received by the second host, which thanks to the “1” at 
the beginning of the message knows that it is to be displayed on the screen. 
- The receiving host then automatically sends a message “2ACK” with the “2” serving as an 
indicator to the initial host that this message is not to be printed.
- Once the initial sending host receives this “2ACK” it will flip the SEQ variable from 0 to 1 or vice 
versa.
- If all of this was done before the 0.5s timeout, then the if condition after the stalling function 
will check that the SEQ was changed and so no need to resend the message.
Concerning the corruption part, the best option would be to compute the checksum, but seeing that we 
are sending this over UDP, there is already a checksum being calculated in a different layer so there is 
no need to recompute it again.
After writing a code that ensures reliability we tested it using netem to cause corruption, duplicates, 
time delay and packet loss

Now other than the two functions discussed previously, we have two other functions that are 
also running in parallel which will allow users to transfer txt files using TCP while still being able to chat 
using UDP
- The first is sendfile() in which a buffer size is specified. This buffer size will eventually affect the 
speed with which the files are gonna be downloaded and uploaded seeing that it limits the size 
of the parts that are divided from the original message causing the code to divide into more 
parts. Next, we await the message containing the txt file name. We then create a new socket 
and use it to establish a connection with the other user. We indicate to the sender that the 
connection has been established and start encoding the file and sending it while updating the 
progress bar accordingly. When the txt file is fully sent, the connection closes.
- The second is receivefile() in which a buffer is also specified with the same purpose. We open a 
socket which will allow the receiver to await a connection. Once a connection is established, the 
txt file will start downloading and the process bar will be updated accordingly. Once the file is 
fully downloaded, the connection will be closed. 
At the end of this process, the receiving user will have the file with the same name and content as the 
one sent by the sending user
