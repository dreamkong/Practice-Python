import socket


def main():
    # 1 创建套接字
    tcp_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # 2 绑定本地信息
    tcp_server_socket.bind(('', 7788))

    # 3 让默认的套接字由主动变为被动 listen
    tcp_server_socket.listen(128)

    while True:
        # 4 等待客户端的连接 accept
        print('等待新的客户端连接...')
        client_socket, client_ip = tcp_server_socket.accept()
        print('客户端的ip:', client_ip)

        while True:
            # 接收客户端发送过来的请求
            receice_content = client_socket.recv(1024)
            print(receice_content.decode('gbk'))

            # 回复客户端
            # 如果recv解堵塞有2种情况
            # 1 客户端发送数据过来
            # 2 客户端调用close导致关闭
            if receice_content:
                client_socket.send('已收到消息'.encode('utf-8'))
            else:
                client_socket.send('断开连接'.encode('utf-8'))
                break

        # 关闭套接字
        client_socket.close()

    tcp_server_socket.close()


if __name__ == '__main__':
    main()
