import pandas as pd
import matplotlib.pyplot as plt
import os

def generate_graphs(csv_file='results/stats.csv'):
    if not os.path.exists(csv_file):
        print(f"[-] Error: {csv_file} not found.")
        return

    df = pd.read_csv(csv_file)
    df['Timestamp'] = pd.to_datetime(df['Timestamp'])

    plt.figure(figsize=(12, 6))

    # SYN-RECV Plot
    plt.subplot(2, 1, 1)
    plt.plot(df['Timestamp'], df['SYN_RECV_Count'], label='SYN-RECV Connections', color='blue')
    plt.ylabel('Count')
    plt.title('TCP SYN Flood Detection and Mitigation')
    plt.grid(True)
    
    # Highlight Mitigation Periods
    mitigation_active = df[df['Status'] == 'MITIGATION_ACTIVE']
    if not mitigation_active.empty:
        plt.scatter(mitigation_active['Timestamp'], mitigation_active['SYN_RECV_Count'], color='red', label='Mitigation Active', s=10)

    plt.legend()

    # CPU Usage Plot
    plt.subplot(2, 1, 2)
    plt.plot(df['Timestamp'], df['CPU_Usage'], label='CPU Usage (%)', color='green')
    plt.ylabel('Percentage')
    plt.xlabel('Time')
    plt.grid(True)
    plt.legend()

    plt.tight_layout()
    plt.savefig('results/performance_graph.png')
    print("[+] Graph saved to results/performance_graph.png")

if __name__ == "__main__":
    generate_graphs()
