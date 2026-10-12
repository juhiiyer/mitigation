#!/bin/bash
PORT=$1
if [ -z "$PORT" ]; then
    PORT=8080
fi

echo "[*] Cleaning up firewall rules for port $PORT..."

sudo iptables -D INPUT -p tcp --syn --dport $PORT -m limit --limit 1/s --limit-burst 5 -j ACCEPT 2>/dev/null
sudo iptables -D INPUT -p tcp --syn --dport $PORT -j DROP 2>/dev/null

echo "[+] Cleanup complete."
