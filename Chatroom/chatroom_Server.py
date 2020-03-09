#!/usr/bin/env python3
#coding=utf-8

from socket import * 
import os,sys 

def do_login(s,user,name,addr):
    if (name in user)  or  name == '管理员':
        s.sendto("該用戶已存在".encode(),addr) 
        return
    s.sendto(b'OK',addr)

    msg = "\n歡迎 %s 進入聊天室"%name 
    for i in user:
        s.sendto(msg.encode(),user[i])
    user[name] = addr 

def do_chat(s,user,name,text):
    msg = "\n%s 說:%s"%(name,text)
    for i in user:
        if i != name:
            s.sendto(msg.encode(),user[i])

def do_quit(s,user,name):
    msg = '\n' + name + "退出了聊天室"
    for i in user:
        if i == name:
            s.sendto(b'EXIT',user[i])
        else:
            s.sendto(msg.encode(),user[i])
    del user[name]

def do_parent(s):
    #儲存數據 {'某某某':('127.0.0.1',9999)}
    user = {}

    while True:
        msg,addr = s.recvfrom(1024)
        msgList = msg.decode().split(' ')
        
        #設定請求類型並響應執行該函數
        if msgList[0] == 'L':
            do_login(s,user,msgList[1],addr)
        elif msgList[0] == 'C':
            do_chat(s,user,msgList[1],' '.join(msgList[2:]))
        elif msgList[0] == 'Q':
            do_quit(s,user,msgList[1])

def do_child(s,addr):
    while True:
        msg = input("管理員消息:")
        msg = 'C 管理員 ' + msg 
        s.sendto(msg.encode(),addr)

def main():
    #server address 
    ADDR = ('0.0.0.0',8000)
    s = socket(AF_INET,SOCK_DGRAM)
    s.setsockopt(SOL_SOCKET,SO_REUSEADDR,1)
    s.bind(ADDR)

    pid = os.fork()
    if pid < 0:
        sys.exit("創建進程失敗")
    elif pid == 0:
        do_child(s,ADDR)
    else:
        do_parent(s)

if __name__ == "__main__":
    main()
