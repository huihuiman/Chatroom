#!/usr/bin/env python3
#coding=utf-8

from  socket import * 
import sys,os 

#發送消息
def send_msg(s,name,addr):
    while True:
        text = input("發言:")
        #如果输入quit表示退出
        if text.strip() == 'quit':
            msg = 'Q ' + name
            s.sendto(msg.encode(),addr)
            sys.exit("退出聊天室") 
                      
        msg = 'C %s %s'%(name,text)
        s.sendto(msg.encode(),addr)

#接收消息
def recv_msg(s):
    while True:
        data,addr = s.recvfrom(2048)
        if data.decode() == 'EXIT':
            sys.exit(0)
        print(data.decode() + "\n發言:",end="") 

#創建套接字,登錄,創建子進程
def main():
    # 輸入IP與端口
    if len(sys.argv) < 3:
        print("argv is error")
        return
    HOST = sys.argv[1]
    PORT = int(sys.argv[2])
    ADDR = (HOST,PORT)

    #創建套接字，udp連線
    s = socket(AF_INET,SOCK_DGRAM)

    while True:
        name = input("請輸入姓名:")
        msg = "L " + name 
        #發送登錄請求
        s.sendto(msg.encode(),ADDR)
        #等待伺服器回應
        data,addr = s.recvfrom(1024)
        if data.decode() == 'OK':
            print("您已進入聊天室")
            break 
        else:
            #不成功之伺服器回復不允許登錄原因
            print(data.decode())

    #創建父子進程來實現多人連線(收發功能)
    pid = os.fork()
    if pid < 0:
        sys.exit("創建子進程失败")
    elif pid == 0:
        send_msg(s,name,ADDR)
    else:
        recv_msg(s)


if __name__ == "__main__":
    main()