#!/usr/bin/env python3
#coding=utf-8

from  socket import * 
import sys,os 

def send_msg(s,name,addr):
    while True:
        text = input("發言:")
        if text.strip() == 'quit':
            msg = 'Q ' + name
            s.sendto(msg.encode(),addr)
            sys.exit("退出聊天室") 
                      
        msg = 'C %s %s'%(name,text)
        s.sendto(msg.encode(),addr)

def recv_msg(s):
    while True:
        data,addr = s.recvfrom(2048)
        if data.decode() == 'EXIT':
            sys.exit(0)
        print(data.decode() + "\n發言:",end="") 

def main():
    if len(sys.argv) < 3:
        print("argv is error")
        return
    HOST = sys.argv[1]
    PORT = int(sys.argv[2])
    ADDR = (HOST,PORT)
    s = socket(AF_INET,SOCK_DGRAM)

    while True:
        name = input("請輸入姓名:")
        msg = "L " + name 
        s.sendto(msg.encode(),ADDR)
        data,addr = s.recvfrom(1024)
        if data.decode() == 'OK':
            print("您已進入聊天室")
            break 
        else:
            print(data.decode())

    pid = os.fork()
    if pid < 0:
        sys.exit("創建子進程失败")
    elif pid == 0:
        send_msg(s,name,ADDR)
    else:
        recv_msg(s)

if __name__ == "__main__":
    main()
