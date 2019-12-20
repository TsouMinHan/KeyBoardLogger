import socket
import my_protocol

def send_msg():
    # (IP4, TCP)
    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # return tuple (server IP, port)
    serverSocket.bind((socket.gethostname(), 1234,))
    serverSocket.listen(5)

    while True:
        conn, addr = serverSocket.accept()
        while True:
            data, _ = my_protocol.nbyte_to_data(conn)
            
            print(data)
            if not data:
                break
        # conn.send(data)
        conn.close()
        if not data:
            break

    print('close')

    serverSocket.close()

def send_file():
    flag = False

    # (IP4, TCP)
    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # return tuple (server IP, port)
    serverSocket.bind((socket.gethostname(), 1234,))
    serverSocket.listen(5)

    while True:
        print(1)
        conn, addr = serverSocket.accept()
        print('connect from', addr)

        while True:
            data = conn.recv(2048)
            print(data)
            if not data:
                flag = True
                break

        # conn.send(data)
        conn.close()

        if not flag:
            break

    print('close')


if __name__ == "__main__":
    send_msg()

    # send_file()