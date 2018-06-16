import socket


def send_msg(udp_socket):
    dest_ip = input('请输入对方的ip:')
    dest_port = int(input('请输入对方的端口:'))
    send_content = input('请输入要发送的内容:')
    udp_socket.sendto(send_content.encode('utf-8'), (dest_ip, dest_port))


def receive_msg(udp_socket):
    receive_data = udp_socket.recvfrom(1024)
    print('{}{}'.format(receive_data[1], receive_data[0].decode('gbk')))
    print('{}{}'.format(type(receive_data[1]), type(receive_data[0])))


def main():

    # 创建套接字
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # 绑定信息
    udp_socket.bind(('', 7787))

    # 循环处理事情
    while True:
        print('请选择要进行的操作:')
        print('-'*50)
        print('0 发送消息')
        print('1 接收消息')
        print('q 退出')

        operation = input()
        if operation == '0':
            # 发送
            send_msg(udp_socket)
        elif operation == '1':
            # 接收并显示
            receive_msg(udp_socket)
        elif operation == 'q':
            break
        else:
            continue

    # 关闭套接字
    udp_socket.close()


if __name__ == '__main__':
    main()