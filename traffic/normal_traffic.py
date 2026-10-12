import socket
import time
import argparse
import json
import sys

def send_legitimate_request(server_ip, server_port):
    start = time.time()
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(2)
        s.connect((server_ip, server_port))
        data = s.recv(1024)
        s.close()
        return True, time.time() - start
    except Exception as e:
        return False, time.time() - start

def main():
    parser = argparse.ArgumentParser(description="Normal TCP traffic generator")
    parser.add_argument("ip", help="Server IP address")
    parser.add_argument("port", type=int, help="Server port")
    parser.add_argument("--count", type=int, default=1, help="Number of requests to send")
    parser.add_argument("--delay", type=float, default=1.0, help="Delay between requests in seconds")
    parser.add_argument("--json", action="store_true", help="Output results in JSON format")
    
    args = parser.parse_args()
    
    successes = 0
    latencies = []
    
    for i in range(args.count):
        if not args.json:
            print(f"[*] Sending request {i+1}/{args.count}...")
        
        success, latency = send_legitimate_request(args.ip, args.port)
        if success:
            successes += 1
            latencies.append(latency)
        
        if not args.json:
            if success:
                print(f"[+] Success: {latency:.4f}s")
            else:
                print(f"[-] Failed")
        
        if i < args.count - 1:
            time.sleep(args.delay)
    
    avg_latency = sum(latencies) / len(latencies) if latencies else 0
    result = {
        "total": args.count,
        "success": successes,
        "failed": args.count - successes,
        "success_rate": (successes / args.count) * 100 if args.count > 0 else 0,
        "avg_latency": avg_latency
    }
    
    if args.json:
        print(json.dumps(result))
    else:
        print(f"\n--- Results ---")
        print(f"Success Rate: {result['success_rate']:.2f}%")
        print(f"Avg Latency: {result['avg_latency']:.4f}s")

if __name__ == "__main__":
    main()
