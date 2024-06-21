task2：UDP Client-Server Project

简介
这个项目实现了一个基于UDP协议的客户端-服务器通信系统，模拟了TCP连接的建立和释放过程，并且具有模拟丢包的功能。客户端可以发送请求报文，服务器接收并响应，同时记录RTT和丢包率。

运行环境
- 操作系统：Windows,  Linux
- Python 版本：Python 3.12（3.8及以上版本）


先决条件
- 安装 Python 3.12（3.8及以上版本）
- 安装 pip (Python 包管理工具)

安装步骤：
1. 克隆或下载项目到本地：

   git clone https://github.com/Holoapple/task2-UDP-Client-Server-Project
   cd udp-client-server

2. 安装依赖库：

   pip install numpy


使用方法：

运行服务器
1. 在本地os里打开终端或命令提示符。
2. 导航到项目目录。
3. 运行以下命令启动服务器：

   python udpserver.py

   服务器将监听所有网络接口上的端口 `12345`。

运行客户端
1. 打开虚拟机os里的终端。
2. 导航到项目目录。
3. 运行以下命令启动客户端：

   python udpclient.py <server_ip> <server_port>

   例如：

   python udpclient.py 192.168.1.100 12345

   替换 `<server_ip>` 为服务器的实际IP地址，`<server_port>` 为服务器端口（默认为 `12345`）。

配置选项

 服务器配置
`SERVER_IP`: 服务器监听的IP地址（默认为 `0.0.0.0`，监听所有网络接口）。
`SERVER_PORT`: 服务器监听的端口号（默认为 `12345`）。
`DROP_RATE`: 丢包率（默认为 `0.2`，即 20% 的丢包率）。

客户端配置
`TIMEOUT`: 客户端接收超时时间，单位为秒（默认为 `0.1` 秒）。
`RETRIES`: 客户端请求的重传次数（默认为 `2` 次）。

示例

运行示例
1. 启动服务器：

   python udpserver.py

2. 启动客户端并连接到服务器：

   python udpclient.py 192.168.1.100 12345


预期输出
在客户端：

连接建立
sequence no: 1, serverIP:Port: 192.168.1.100:12345, RTT: 10.24 ms
sequence no: 2, serverIP:Port: 192.168.1.100:12345, RTT: 12.34 ms
...
接收到的udp packets数目: 12
丢包率: 16.67%
最大RTT: 15.67 ms
最小RTT: 8.23 ms
平均RTT: 11.45 ms
RTT的标准差: 2.45 ms
server的整体响应时间: 123.45 ms


文件结构

udp-client-server/
│
├── udpserver.py       # 服务器代码
├── udpclient.py       # 客户端代码
├── README.txt         # 项目说明文件





