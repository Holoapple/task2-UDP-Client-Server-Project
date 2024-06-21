import socket
import time
import struct
import random
import statistics
import sys

TIMEOUT = 0.1  # 100ms超时
RETRIES = 2  # 重传次数

def create_message(seq_no, version, data):
    data_padded = data.encode().ljust(200, b'\x00')
    return struct.pack('!HB200s', seq_no, version, data_padded)

def parse_response(data):
    seq_no, version, data_padded = struct.unpack('!HB200s', data)
    server_time = data_padded.decode().strip('\x00')
    return seq_no, version, server_time

def main(server_ip, server_port):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    client_socket.settimeout(TIMEOUT)

    # 三次握手过程
    try:
        # 发送SYN
        client_socket.sendto(b'SYN', (server_ip, server_port))
        response, _ = client_socket.recvfrom(2048)
        if response == b'SYN-ACK':
            # 发送ACK
            client_socket.sendto(b'ACK', (server_ip, server_port))
            print("连接建立")
        else:
            print("未能建立连接")
            client_socket.close()
            return
    except socket.timeout:
        print("连接超时")
        client_socket.close()
        return

    seq_no = 1
    received_packets = 0
    rtt_list = []
    first_response_time = None
    last_response_time = None

    for i in range(12):
        message = create_message(seq_no, 2, "X" * 200)
        retries = 0
        while retries <= RETRIES:
            try:
                start_time = time.time()
                client_socket.sendto(message, (server_ip, server_port))
                response, _ = client_socket.recvfrom(2048)
                rtt = (time.time() - start_time) * 1000  # 转换为毫秒

                seq_no_resp, version, server_time = parse_response(response)
                if seq_no_resp == seq_no and version == 2:
                    received_packets += 1
                    rtt_list.append(rtt)
                    if first_response_time is None:
                        first_response_time = start_time
                    last_response_time = time.time()
                    print(f"sequence no: {seq_no}, serverIP:Port: {server_ip}:{server_port}, RTT: {rtt:.2f} ms")
                    break
            except socket.timeout:
                retries += 1
                if retries > RETRIES:
                    print(f"sequence no: {seq_no}, request time out")
                    break
        seq_no += 1

    # 发送FIN消息
    client_socket.sendto(b'FIN', (server_ip, server_port))
    try:
        response, _ = client_socket.recvfrom(2048)
        if response == b'FIN-ACK':
            print("接收到FIN-ACK，发送ACK")
            client_socket.sendto(b'ACK', (server_ip, server_port))
    except socket.timeout:
        print("FIN超时")

    client_socket.close()

    # 汇总信息
    total_packets = 12
    lost_packets = total_packets - received_packets
    lost_percentage = (lost_packets / total_packets) * 100
    max_rtt = max(rtt_list) if rtt_list else 0
    min_rtt = min(rtt_list) if rtt_list else 0
    avg_rtt = statistics.mean(rtt_list) if rtt_list else 0
    stddev_rtt = statistics.stdev(rtt_list) if len(rtt_list) > 1 else 0
    overall_response_time = (last_response_time - first_response_time) * 1000 if first_response_time and last_response_time else 0

    print("\n汇总信息:")
    print(f"接收到的udp packets数目: {received_packets}")
    print(f"丢包率: {lost_percentage:.2f}%")
    print(f"最大RTT: {max_rtt:.2f} ms")
    print(f"最小RTT: {min_rtt:.2f} ms")
    print(f"平均RTT: {avg_rtt:.2f} ms")
    print(f"RTT的标准差: {stddev_rtt:.2f} ms")
    print(f"server的整体响应时间: {overall_response_time:.2f} ms")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(f"用法: {sys.argv[0]} <server_ip> <server_port>")
        sys.exit(1)

    server_ip = sys.argv[1]
    server_port = int(sys.argv[2])
    main(server_ip, server_port)
