import socket
from time import ctime

HOST = 'localhost'
PORT = 21567
BUFSIZ = 4096
ADDR = (HOST, PORT)

# 创建TCP套接字
tcpSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# 创建UDP套接字
# udpSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
tcpSock.bind(ADDR)  # 将地址绑定到套接字上
tcpSock.listen(5)  # 设置并启动TCP监听器

while True:
    print("waiting for connection....")
    tcpCliSock, addr = tcpSock.accept()  # 被动接收TCP客户端连接，一直等待直到连接到达（阻塞）
    print("... connected from", addr)

    while True:
        data = tcpCliSock.recv(BUFSIZ)  # 接收TCP消息
        # print(type(data))
        print(data)
        # 如果有数据加上时间戳后返回给客户端，因为只接受字节数据，所以把数据使用bytes函数转换

        # tcpCliSock.send(bytes('[%s] %s' % (ctime(), data.decode('utf-8')), 'utf-8'))
        if data.decode('utf-8') == "1":
            tcpCliSock.send(bytes("Welcome".encode('utf-8')))
        elif data.decode('utf-8') == "2":
            tcpCliSock.send(bytes("Bryant".encode('utf-8')))
        else:
            break

    tcpCliSock.close()
