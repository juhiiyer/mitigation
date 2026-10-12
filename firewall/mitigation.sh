#!/bin/bash
PORT=$1
if [ -z "$PORT" ]; then
    PORT=8080
fi

echo "[*] Applying firewall mitigation on port $PORT..."

# 1. Rate limit SYN packets: Accept 1 per second with a burst of 5
sudo iptables -A INPUT -p tcp --syn --dport $PORT -m limit --limit 1/s --limit-burst 5 -j ACCEPT

# 2. Drop all other SYN packets for this port
sudo iptables -A INPUT -p tcp --syn --dport $PORT -j DROP

echo "[+] Mitigation rules applied."
