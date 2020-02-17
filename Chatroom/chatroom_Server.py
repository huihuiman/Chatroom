#!/usr/bin/env python3
#coding=utf-8

from socket import * 
import os,sys 

#登錄判斷
def do_login(s,user,name,addr):
    if (name in user)  or  name == '管理员':
        s.sendto("該用戶已存在".encode(),addr) 
        return
    s.sendto(b'OK',addr)

    #通知其他人
    msg = "\n歡迎 %s 進入聊天室"%name 
    for i in user:
        s.sendto(msg.encode(),user[i])
    #保存用戶狀態
    user[name] = addr 

#轉發聊天消息
def do_chat(s,user,name,text):
    msg = "\n%s 說:%s"%(name,text)
    for i in user:
        if i != name:
            s.sendto(msg.encode(),user[i])

#退出聊天室
def do_quit(s,user,name):
    msg = '\n' + name + "退出了聊天室"
    for i in user:
        if i == name:
            s.sendto(b'EXIT',user[i])
        else:
            s.sendto(msg.encode(),user[i])
    #從字典刪除用戶
    del user[name]


# 接收客户端请求
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

# 管理員說話
def do_child(s,addr):
    while True:
        msg = input("管理員消息:")
        msg = 'C 管理員 ' + msg 
        s.sendto(msg.encode(),addr)

#創建網絡,創建進程,調用功能函数
def main():
    #server address 
    ADDR = ('0.0.0.0',8888)

    # 創建套接字，udp連線
    s = socket(AF_INET,SOCK_DGRAM)
    s.setsockopt(SOL_SOCKET,SO_REUSEADDR,1)
    s.bind(ADDR)

    #創建進程讓管理員發廣播
    pid = os.fork()
    if pid < 0:
        sys.exit("創建進程失敗")
    elif pid == 0:
        do_child(s,ADDR)
    else:
        do_parent(s)

if __name__ == "__main__":
    main()