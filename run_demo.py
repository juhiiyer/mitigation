import subprocess
import time
import os
import sys

def run_command(command, description):
    print(f"[*] {description}...")
    try:
        # Use 'python' instead of 'python3' as requested
        command = [c if c != "python3" else "python" for c in command]
        process = subprocess.Popen(command, creationflags=subprocess.CREATE_NEW_CONSOLE)
        return process
    except Exception as e:
        print(f"[-] Failed to {description}: {e}")
        return None

def main():
    print("=== SYN Flood Mitigation: Part 1 - Initialization & Baseline ===")
    
    # 1. Start Server
    server_proc = run_command(["python", "server/server.py"], "Starting TCP Server")
    time.sleep(2)

    # 2. Start Monitor (Warning: requires Linux for full functionality)
    print("[!] Warning: Monitor requires Linux (iptables/ss) to function fully.")
    monitor_proc = run_command(["python", "-m", "monitor.monitor"], "Starting Monitor")
    time.sleep(2)

    # 3. Establish Baseline with Normal Traffic
    server_ip = "127.0.0.1" 
    print(f"[*] Establishing baseline with Normal Traffic against {server_ip}...")
    traffic_cmd = ["python", "traffic/normal_traffic.py", server_ip, "8080", "--count", "20"]
    subprocess.run(traffic_cmd)

    print("\n[+] Initialization and Baseline complete.")
    print("Keep this window and the server/monitor windows open.")
    print("Next, run 'run_attack.py' to simulate the attack.")
    input("Press Enter to exit this automator (processes will remain running if possible)...")

if __name__ == "__main__":
    main()
