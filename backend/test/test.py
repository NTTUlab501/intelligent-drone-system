import socket
import threading
import csv
s = socket.socket()                                         
s.bind(('192.168.1.124',8080))                                    
s.listen(5)
def handle(client,addr):
    while True:
        try:
            text = client.recv(1024)
            if not text:
                client.close()
            client.send(text)
            print(addr[0],'>>',text.decode())
            ans=text.decode()
            if ans[0]=='r':
                print("resp123")
                with open("respeaker.text",'w')as s:
                    s.write(ans+"\n")
            if ans[3]=='1':
                if ans[4]=='x':
                    print("Car123")
                    with open("Car1_x.text",'w') as s:
                        s.write(ans+"\n")
            if ans[3]=='1':
                if ans[4]=='y':
                    print("Car456")
                    with open("Car1_y.text",'w') as s:
                        s.write(ans+"\n")
            if ans[3]=='2':
                if ans[4]=='x':
                    print("Car789")
                    with open("Car2_x.text",'w') as s:
                        s.write(ans+"\n")
            if ans[3]=='2':
                if ans[4]=='y':
                    print("Car000")
                    with open("Car2_y.text",'w') as s:
                        s.write(ans+"\n") 
        except:
            print(addr[0],addr[1],'>>say goodby')
            break
    
while True:
    client,addr=s.accept()                                   #4、接受客戶端連線
    threading._start_new_thread(handle,(client,addr))        #5、多執行緒處理客戶端訊息