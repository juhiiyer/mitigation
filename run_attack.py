import subprocess
import time
import os
import sys

def run_command(command, description):
    print(f"[*] {description}...")
    try:
        # Standardize python command
        command = [c if c != "python3" else "python" for c in command]
        # Run in a new console so it doesn't block this script if it's long-running
        process = subprocess.Popen(command, creationflags=subprocess.CREATE_NEW_CONSOLE)
        return process
    except Exception as e:
        print(f"[-] Failed to {description}: {e}")
        return None

def view_file(filepath):
    if os.path.exists(filepath):
        print(f"\n--- Content of {filepath} ---")
        try:
            with open(filepath, 'r') as f:
                # Print last 20 lines for brevity if it's a log
                lines = f.readlines()
                for line in lines[-20:]:
                    print(line.strip())
        except Exception as e:
            print(f"Could not read file: {e}")
    else:
        print(f"File {filepath} not found.")

def main():
    print("=== SYN Flood Mitigation: Part 2 - Attack & Results ===")
    
    target_ip = "127.0.0.1" # Change to VM IP if running remotely
    print(f"\n[!] Target IP is set to {target_ip}. Make sure the server is running.")

    # 1. Launch SYN Flood Attack
    # Note: Scapy on Windows requires Npcap/WinPcap and often Admin privileges.
    print("[*] Launching SYN Flood Attack (5000 packets)...")
    attack_cmd = ["python", "traffic/syn_flood.py", target_ip, "8080", "--count", "5000"]
    attack_proc = subprocess.run(attack_cmd)
    
    print("\n[*] Attack simulation finished.")
    print("[*] Waiting for monitor to process and apply rules (if applicable)...")
    time.sleep(5)

    # 2. Verify Mitigation / Cleanup
    # In a real scenario, we might run cleanup.sh here if on Linux.
    # On Windows, we'll just indicate the demonstration is nearing end.
    
    # 3. Interactive File Viewing
    while True:
        print("\n" + "="*40)
        print("What would you like to view?")
        print("1. Monitor Log (logging/monitor.log)")
        print("2. Statistics CSV (results/stats.csv)")
        print("3. View project structure")
        print("4. Exit")
        
        choice = input("Enter choice (1-4): ")
        
        if choice == '1':
            view_file("logging/monitor.log")
        elif choice == '2':
            view_file("results/stats.csv")
        elif choice == '3':
            print("\nProject Structure:")
            for root, dirs, files in os.walk("."):
                level = root.replace(".", "").count(os.sep)
                indent = " " * 4 * (level)
                print(f"{indent}{os.path.basename(root)}/")
                subindent = " " * 4 * (level + 1)
                for f in files:
                    print(f"{subindent}{f}")
                if level > 1: break # Limit depth
        elif choice == '4':
            break
        else:
            print("Invalid choice.")

    print("\n[+] Demonstration finished. Cleanup recommended.")
    print("If you applied firewall rules on Linux, run 'sudo bash firewall/cleanup.sh'.")
    input("Press Enter to close...")

if __name__ == "__main__":
    main()
