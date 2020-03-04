import socket
def send_file_2_cliend(new_client_socket,socket_addr):
    # 接收客户端需要下载的文件名
    file_name=new_client_socket.recv(1024).decode('gbk')
    print('客户端(%s)需要下载的文件是:%s' % (socket_addr,file_name))
    file_content= None
    # 打开这个文件读取数据
    try:
        f = open(file_name,'rb')
        file_content=f.read()
        f.close()
    except Exception as e:
        print('没有下载的文件：%s' % (file_name))
    if file_content:
        # 发送数据到客户端
        new_client_socket.send(file_content)

def main():

    # 创建套接字
    tcp_socket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)

    # 绑定端口
    tcp_socket.bind(("",8088))

    # 让默认的套接字 有主动变为被动
    tcp_socket.listen(128)

    while True:

        # 等待客户端的连接
        new_client_socket,socket_addr=tcp_socket.accept()

        send_file_2_cliend(new_client_socket,socket_addr)

        # 关闭套接字
        new_client_socket.close()

    tcp_socket.close()

if __name__=="__main__":
    main()
