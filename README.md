# SYN Flood Mitigation System

Automated mitigation of TCP SYN Flood attacks using firewall rule automation and real-time monitoring.

## Overview
This project demonstrates a security system designed to detect and mitigate SYN Flood attacks. It features a TCP server, a traffic monitor that detects anomalies, and automated firewall rule application (using `iptables` on Linux) to maintain service availability during an attack.

A professional GUI is provided to walk users through the initialization, baseline establishment, attack simulation, and results analysis.

## Project Structure
- `gui.py`: The main entry point. A professional Tkinter-based interface for the entire demonstration.
- `server/server.py`: Target TCP server listening on port `8080`.
- `monitor/`:
    - `monitor.py`: Main monitoring loop.
    - `detector.py`: Detection logic and threshold management.
    - `config.py`: System thresholds and configuration.
- `firewall/`:
    - `mitigation.sh`: Bash script to apply `iptables` rules.
    - `cleanup.sh`: Bash script to remove firewall rules.
- `traffic/`:
    - `syn_flood.py`: Attack simulator using Scapy.
    - `normal_traffic.py`: Client simulator for baseline and verification.
- `results/`:
    - `stats.csv`: Log of SYN-RECV counts, CPU usage, and mitigation status.
    - `generate_plots.py`: Performance visualization tool.
- `logging/`: Contains `monitor.log` for detailed system events.

## Features
- **Professional GUI**: Easy-to-use interface with animations and progress tracking.
- **Real-time Monitoring**: Tracks `SYN_RECV` states and CPU usage.
- **Automated Mitigation**: Automatically triggers firewall rules when thresholds are exceeded.
- **Advanced Analytics**: Generates performance comparison tables and live-drawn graphs (SYN-RECV count, CPU usage, Throughput, Error rates) for academic presentation.
- **Human-Readable Analysis**: Provides side-by-side technical data and simplified explanations for non-technical users.
- **Data Export**: Ability to view and download logs and statistics directly from the UI.

## How to Run

### Prerequisites
- Python 3.x
- `scapy` library (for attack simulation)
- `tkinter` (usually included with Python)
- Administrative/Root privileges (required for Scapy and firewall modifications)
- **Windows Support**: Works on Windows 10/11 using `netsh` and `netstat`.
- **Linux Support**: Works on Linux using `iptables` and `ss`.

### Steps
1. **Launch the GUI** (Run as Administrator/Sudo):
   ```bash
   python gui.py
   ```
2. **Initialize System**: Click the "Initialize System & Baseline" button. This will start the server and monitor, and establish a normal traffic baseline.
3. **View Baseline**: Review the baseline statistics to understand the server's normal state.
4. **Simulate Attack**: Click "Proceed to Attack Simulation". The GUI will simulate a SYN Flood and show the mitigation logic in progress.
5. **Analyze Results**: After the simulation, use the final menu to view monitor logs, statistics, and project structure with human-readable explanations.

## Technical Details
- **Threshold Detection**: Uses a sliding window and configurable thresholds to minimize false positives.
- **Mitigation Strategy**: Throttles or blocks malicious IP patterns identified during the flood.
- **Performance Tracking**: Records high-resolution metrics for academic or forensic analysis.

---
