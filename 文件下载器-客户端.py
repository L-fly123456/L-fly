import socket

# 创建套接字
tcp_socket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)

# 输入服务器的ip和port
dest_ip=input('请输入服务器的ip:')
dest_port=int(input('请输入服务器的port:'))

# 链接服务器
tcp_socket.connect((dest_ip,dest_port))

# 输入需要下载的文件名
file_name=input('请输入需要下载的文件名：')
tcp_socket.send(file_name.encode('gbk'))

# 接收对方发过来的文件数据最大1M
resv_data=tcp_socket.recv(1024*1024)
# print(resv_data.decode('gbk'))

if resv_data:
    with open('[新]'+file_name,'wb') as f:
        f.write(resv_data)
        
# 关闭套接字
tcp_socket.close()


