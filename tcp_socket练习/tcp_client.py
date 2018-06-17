import socket


def main():
    # 1 创建tcp套接字
    tcp_client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # 2 连接服务器
    server_ip = input('请输入要连接的服务器的ip:')
    server_port = input('请输入要连接的服务器的port:')
    tcp_client_socket.connect((server_ip, int(server_port)))

    # 3 收发数据
    send_content = input('请输入要发送的内容:')
    tcp_client_socket.send(send_content.encode('gbk'))

    receive_content = tcp_client_socket.recv(1024)
    print('接收到的数据为:', receive_content.decode('gbk'))

    # 4 关闭tcp套接字
    tcp_client_socket.close()


if __name__ == '__main__':
    main()
