import socket
import struct
import random
import time

SERVER_IP = '0.0.0.0'  # 监听所有网络接口
SERVER_PORT = 12345    # 服务器端口号
DROP_RATE = 0.2  # 丢包率设置为20%

# 创建响应报文
def create_response(seq_no, version):
    # 获取当前系统时间并填充到200字节
    server_time = time.strftime("%H-%M-%S", time.localtime()).encode().ljust(200, b'\x00')
    # 打包响应报文
    return struct.pack('!HB200s', seq_no, version, server_time)

def main():
    # 创建UDP套接字
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind((SERVER_IP, SERVER_PORT))  # 绑定服务器地址和端口

    print(f"服务器启动，监听 {SERVER_IP}:{SERVER_PORT}")

    connections = {}  # 维护客户端连接

    while True:
        message, client_address = server_socket.recvfrom(2048)  # 接收消息

        # 处理三次握手过程
        if client_address not in connections:
            if message == b'SYN':
                # 收到SYN，发送SYN-ACK
                server_socket.sendto(b'SYN-ACK', client_address)
                continue
            elif message == b'ACK':
                # 收到ACK，建立连接
                connections[client_address] = True
                print(f"与 {client_address} 的连接建立")
                continue

        # 处理四次挥手过程
        if message == b'FIN':
            # 收到FIN，发送FIN-ACK
            server_socket.sendto(b'FIN-ACK', client_address)
            response, _ = server_socket.recvfrom(2048)
            if response == b'ACK':
                # 收到ACK，关闭连接
                print(f"与 {client_address} 的连接关闭")
                del connections[client_address]
                continue

        # 确保消息长度正确
        if len(message) == 203:
            seq_no, version, data_padded = struct.unpack('!HB200s', message)  # 解包消息
            # 模拟丢包
            if random.random() > DROP_RATE:
                response = create_response(seq_no, version)  # 创建响应报文
                server_socket.sendto(response, client_address)  # 发送响应
                print(f"响应发送到 {client_address}, sequence no: {seq_no}")
            else:
                print(f"丢弃来自 {client_address} 的请求，sequence no: {seq_no}")

if __name__ == "__main__":
    main()
