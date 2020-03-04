import socket
import threading

def send_msg(udp_socked,send_ip,send_port):
    while True:
        send_data = input('请填写要发送的数据：')
        udp_socked.sendto(send_data.encode('gbk'), (send_ip, send_port))

def resv_mag(udp_socked):
    while True:
        resv_data = udp_socked.recvfrom(1024)
        print('%s:%s' % (str(resv_data[1]),resv_data[0].decode('gbk')))

def main():
    # 创建套接字
    udp_socked=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    # 绑定端口
    udp_socked.bind(("",1234))
    send_ip = input('请输入对方电脑的ip:')
    send_port = int(input('请输入对方电脑的port：'))
    t_send=threading.Thread(target=send_msg,args=(udp_socked,send_ip,send_port))
    t_resv=threading.Thread(target=resv_mag,args=(udp_socked,))
    t_send.start()
    t_resv.start()

if __name__=="__main__":
    main()

