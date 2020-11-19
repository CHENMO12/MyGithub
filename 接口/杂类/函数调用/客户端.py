import socket
import sys

HOST = 'localhost'
PORT = 21567
BUFSIZ = 4096
ADDR = (HOST, PORT)

# 创建客户端TCP连接
tcpCliSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# 连接服务器
try:
    tcpCliSock.connect(ADDR)
except Exception as e:
    print("连接服务器失败:",e)
    sys.exit(-1)

while True:
    data = input('请输入： ')
    # if not data:
    #     break
    # 循环发送数据，直到没有数据发送退出
    tcpCliSock.send(bytes(data, encoding='utf-8'))
    # 接收服务端返回的消息，如果没有消息返回，也将退出循环
    data = tcpCliSock.recv(BUFSIZ)
    if not data:
        break
    print(data.decode('utf-8'))

tcpCliSock.close()