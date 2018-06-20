import socket
import threading


def receive_msg(udp_socket):
    while True:
        receive_data = udp_socket.recvfrom(1024)
        print(receive_data[1], receive_data[0].decode('gbk'))


def send_msg(udp_socket, dest_ip, dest_port):
    while True:
        send_data = input('请输入要发送的数据:')
        udp_socket.sendto(send_data.encode('utf-8'), (dest_ip, dest_port))


def main():
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_socket.bind(('', 7890))

    dest_ip = input('请输入对方的ip:')
    dest_port = int(input('请输入对方的port:'))

    receive_threading = threading.Thread(
        target=receive_msg, args=(udp_socket,))
    send_threading = threading.Thread(
        target=send_msg, args=(udp_socket, dest_ip, dest_port))

    receive_threading.start()
    send_threading.start()


if __name__ == '__main__':
    main()
