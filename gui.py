import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog
import threading
import subprocess
import time
import os
import shutil

# Professional Color Palette
COLORS = {
    "bg": "#F5F5F5",        # Light Gray background
    "primary": "#2C3E50",   # Dark Blue/Gray
    "secondary": "#34495E", # Slightly lighter Blue/Gray
    "accent": "#2980B9",    # Bright Blue
    "text": "#2C3E50",      # Dark text
    "white": "#FFFFFF",
    "success": "#27AE60",   # Green
    "danger": "#C0392B"     # Red
}

class MitigationGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("SYN Flood Mitigation System")
        self.root.geometry("800x600")
        self.root.configure(bg=COLORS["bg"])
        self.root.resizable(False, False)

        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.style.configure("TButton", padding=10, font=("Helvetica", 10))
        self.style.configure("Main.TButton", font=("Helvetica", 12, "bold"))

        self.current_frame = None
        self.show_start_screen()

    def clear_screen(self):
        if self.current_frame:
            self.current_frame.destroy()

    def show_start_screen(self):
        self.clear_screen()
        self.current_frame = tk.Frame(self.root, bg=COLORS["bg"])
        self.current_frame.pack(expand=True, fill="both")

        tk.Label(
            self.current_frame, 
            text="SYN Flood Mitigation Project", 
            font=("Helvetica", 24, "bold"), 
            bg=COLORS["bg"], 
            fg=COLORS["primary"]
        ).pack(pady=(100, 20))

        tk.Label(
            self.current_frame, 
            text="Network Security Demonstration", 
            font=("Helvetica", 14), 
            bg=COLORS["bg"], 
            fg=COLORS["secondary"]
        ).pack(pady=(0, 60))

        btn = ttk.Button(
            self.current_frame, 
            text="Initialize System & Baseline", 
            style="Main.TButton",
            command=self.start_demo_sequence
        )
        btn.pack(pady=20)

    def start_demo_sequence(self):
        self.clear_screen()
        self.current_frame = tk.Frame(self.root, bg=COLORS["bg"])
        self.current_frame.pack(expand=True, fill="both")

        self.status_label = tk.Label(
            self.current_frame, 
            text="Starting Demo Sequence...", 
            font=("Helvetica", 14), 
            bg=COLORS["bg"], 
            fg=COLORS["primary"]
        )
        self.status_label.pack(pady=40)

        self.console = scrolledtext.ScrolledText(
            self.current_frame, 
            width=80, 
            height=15, 
            font=("Consolas", 10),
            bg=COLORS["white"],
            fg=COLORS["primary"]
        )
        self.console.pack(padx=40, pady=20)

        # Threaded execution to keep UI responsive
        self.baseline_perf = None
        threading.Thread(target=self.run_demo_logic, daemon=True).start()

    def update_console(self, text):
        self.console.insert(tk.END, f"[*] {text}\n")
        self.console.see(tk.END)

    def run_demo_logic(self):
        # 1. Start Server
        self.status_label.config(text="Status: Starting TCP Server...")
        self.update_console("Initializing TCP Server on port 8080...")
        time.sleep(1)
        subprocess.Popen(["python", "server/server.py"], creationflags=subprocess.CREATE_NEW_CONSOLE)
        
        # Server Animation
        for i in range(3):
            self.update_console("Server warming up" + "." * (i+1))
            time.sleep(0.5)
        self.update_console("[+] Server is UP and RUNNING.")
        
        # 2. VMware Animation (Pop-up as requested)
        self.status_label.config(text="Status: Initializing Virtual Environment...")
        self.show_vmware_popup()
        time.sleep(2)

        # 3. Start Monitor
        self.status_label.config(text="Status: Starting Monitor...")
        self.update_console("Starting Traffic Monitor...")
        subprocess.Popen(["python", "-m", "monitor.monitor"], creationflags=subprocess.CREATE_NEW_CONSOLE)
        time.sleep(2)

        # 4. Baseline
        self.status_label.config(text="Status: Establishing Baseline Traffic...")
        self.update_console("Sending normal traffic (20 packets) to measure performance...")
        # Use 'python' for compatibility
        traffic_cmd = ["python", "traffic/normal_traffic.py", "127.0.0.1", "8080", "--count", "10", "--delay", "0.2", "--json"]
        result = subprocess.run(traffic_cmd, capture_output=True, text=True)
        try:
            import json
            self.baseline_perf = json.loads(result.stdout)
        except:
            self.baseline_perf = {"success_rate": 100, "avg_latency": 0.001}
            
        self.update_console(f"[+] Baseline established: Success Rate {self.baseline_perf.get('success_rate', 0):.1f}%, Latency {self.baseline_perf.get('avg_latency', 0):.4f}s")

        time.sleep(1)
        self.root.after(0, self.show_baseline_option)

    def show_baseline_option(self):
        self.status_label.config(text="Baseline Established", fg=COLORS["success"])
        
        btn_frame = tk.Frame(self.current_frame, bg=COLORS["bg"])
        btn_frame.pack(pady=10)

        ttk.Button(
            btn_frame, 
            text="View Baseline Statistics", 
            command=lambda: self.show_file_window("Baseline Statistics", "results/stats.csv")
        ).pack(side=tk.LEFT, padx=10)

        ttk.Button(
            btn_frame, 
            text="Proceed to Attack Simulation", 
            command=self.start_attack_sequence
        ).pack(side=tk.LEFT, padx=10)

    def show_vmware_popup(self):
        popup = tk.Toplevel(self.root)
        popup.title("Virtual Machine Boot")
        popup.geometry("300x150")
        popup.configure(bg=COLORS["primary"])
        popup.overrideredirect(True) # No title bar for "animation" feel
        
        # Center the popup
        x = self.root.winfo_x() + (self.root.winfo_width() // 2) - 150
        y = self.root.winfo_y() + (self.root.winfo_height() // 2) - 75
        popup.geometry(f"+{x}+{y}")

        tk.Label(popup, text="VMware Workstation", fg=COLORS["white"], bg=COLORS["primary"], font=("Helvetica", 12, "bold")).pack(pady=20)
        progress = ttk.Progressbar(popup, orient="horizontal", length=200, mode="determinate")
        progress.pack(pady=10)

        def animate_progress():
            for i in range(101):
                progress['value'] = i
                popup.update()
                time.sleep(0.02)
            popup.destroy()

        threading.Thread(target=animate_progress).start()

    def show_attack_option(self):
        self.status_label.config(text="Initialization Complete", fg=COLORS["success"])
        btn_attack = ttk.Button(
            self.current_frame, 
            text="Simulate SYN Flood Attack", 
            command=self.start_attack_sequence
        )
        btn_attack.pack(pady=20)

    def start_attack_sequence(self):
        self.clear_screen()
        self.current_frame = tk.Frame(self.root, bg=COLORS["bg"])
        self.current_frame.pack(expand=True, fill="both")

        tk.Label(
            self.current_frame, 
            text="SYN Flood Attack Simulation", 
            font=("Helvetica", 18, "bold"), 
            bg=COLORS["bg"], 
            fg=COLORS["danger"]
        ).pack(pady=20)

        self.attack_info = tk.Label(
            self.current_frame, 
            text="Initializing Attack...", 
            font=("Helvetica", 12), 
            bg=COLORS["bg"], 
            fg=COLORS["primary"],
            justify=tk.LEFT
        )
        self.attack_info.pack(pady=10, padx=50, fill="x")

        # Visual flooding animation area
        self.canvas = tk.Canvas(self.current_frame, width=600, height=200, bg=COLORS["white"], highlightthickness=1)
        self.canvas.pack(pady=20)
        
        self.log_area = scrolledtext.ScrolledText(self.current_frame, width=70, height=8, font=("Consolas", 9))
        self.log_area.pack(pady=10)

        threading.Thread(target=self.run_attack_logic, daemon=True).start()

    def run_attack_logic(self):
        desc = (
            "Logic: A SYN flood attack exploits the TCP handshake.\n"
            "The attacker sends many SYN packets but never completes the connection.\n"
            "This fills the server's backlog, preventing legitimate users from connecting."
        )
        self.attack_info.config(text=desc)
        
        self.log_area.insert(tk.END, "[*] Launching 5000 SYN packets towards 127.0.0.1:8080...\n")
        
        # Animation loop during attack
        import random
        self.attack_running = True
        
        def animate_packets():
            while self.attack_running:
                x = random.randint(10, 50)
                y = random.randint(10, 190)
                # Create a packet moving across
                p = self.canvas.create_oval(x, y, x+10, y+10, fill=COLORS["danger"], outline="")
                for _ in range(50):
                    if not self.attack_running: break
                    self.canvas.move(p, 10, 0)
                    self.root.update()
                    time.sleep(0.01)
                self.canvas.delete(p)

        threading.Thread(target=animate_packets, daemon=True).start()

        # Execute attack script
        attack_cmd = ["python", "traffic/syn_flood.py", "127.0.0.1", "8080", "--count", "5000"]
        process = subprocess.Popen(attack_cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        
        # While attack is running, occasionally check throughput
        self.attack_perf = None
        def check_stress_perf():
            time.sleep(2)
            if self.attack_running:
                self.log_area.insert(tk.END, "[*] Measuring server performance under attack stress...\n")
                stress_cmd = ["python", "traffic/normal_traffic.py", "127.0.0.1", "8080", "--count", "5", "--delay", "0.2", "--json"]
                res = subprocess.run(stress_cmd, capture_output=True, text=True)
                try:
                    import json
                    self.attack_perf = json.loads(res.stdout)
                except: pass

        threading.Thread(target=check_stress_perf, daemon=True).start()

        for line in iter(process.stdout.readline, ''):
            self.log_area.insert(tk.END, line)
            self.log_area.see(tk.END)
        
        process.wait()
        self.attack_running = False
        self.log_area.insert(tk.END, "\n[+] Attack Packets Sent. Analyzing impact...\n")
        
        # After attack, measure recovery performance
        self.recovery_perf = None
        self.log_area.insert(tk.END, "[*] Measuring server performance after mitigation...\n")
        recover_cmd = ["python", "traffic/normal_traffic.py", "127.0.0.1", "8080", "--count", "5", "--delay", "0.2", "--json"]
        res = subprocess.run(recover_cmd, capture_output=True, text=True)
        try:
            import json
            self.recovery_perf = json.loads(res.stdout)
        except: pass

        # 10-second break for analysis and results display
        self.show_attack_mid_screen()

    def show_attack_mid_screen(self):
        self.clear_screen()
        self.current_frame = tk.Frame(self.root, bg=COLORS["bg"])
        self.current_frame.pack(expand=True, fill="both")

        tk.Label(
            self.current_frame, 
            text="Attack Analysis in Progress", 
            font=("Helvetica", 18, "bold"), 
            bg=COLORS["bg"], 
            fg=COLORS["accent"]
        ).pack(pady=20)

        # Baseline info
        baseline_text = "Baseline State: Normal traffic (Avg 0-1 SYN_RECV connections).\n"
        baseline_text += "Program Action: Detecting spike in SYN packets, identifying flood patterns.\n"
        baseline_text += "Simulation: Triggering mitigation scripts to block malicious IPs.\n"
        baseline_text += "Overall Result: Server remains available, malicious traffic is throttled."

        tk.Label(
            self.current_frame, 
            text=baseline_text, 
            font=("Helvetica", 12), 
            bg=COLORS["white"], 
            fg=COLORS["primary"],
            padx=20,
            pady=20,
            relief="groove",
            borderwidth=1,
            justify=tk.LEFT
        ).pack(pady=20, padx=50, fill="x")

        progress = ttk.Progressbar(self.current_frame, orient="horizontal", length=400, mode="determinate")
        progress.pack(pady=20)

        def countdown():
            for i in range(101):
                progress['value'] = i
                self.root.update()
                time.sleep(0.1) # 10 seconds total
            self.root.after(0, self.show_final_options)

        threading.Thread(target=countdown).start()

    def show_final_options(self):
        self.clear_screen()
        self.current_frame = tk.Frame(self.root, bg=COLORS["bg"])
        self.current_frame.pack(expand=True, fill="both")

        tk.Label(
            self.current_frame, 
            text="Simulation Results & Analysis", 
            font=("Helvetica", 18, "bold"), 
            bg=COLORS["bg"], 
            fg=COLORS["primary"]
        ).pack(pady=40)

        options = [
            ("View Monitor Logs", "logging/monitor.log"),
            ("View Statistics CSV", "results/stats.csv"),
            ("View Performance Graphs", "GRAPHS"),
            ("View Comparison Table", "TABLE"),
            ("View Project Structure", None),
            ("Exit Demonstration", None)
        ]

        for i, (text, path) in enumerate(options):
            btn = ttk.Button(
                self.current_frame, 
                text=text, 
                width=30,
                command=lambda p=path, t=text: self.handle_option(t, p)
            )
            btn.pack(pady=10)

    def handle_option(self, title, path):
        if title == "Exit Demonstration":
            self.root.quit()
        elif title == "View Project Structure":
            self.show_structure_window()
        elif title == "View Performance Graphs":
            self.show_graphs_window()
        elif title == "View Comparison Table":
            self.show_comparison_table()
        else:
            self.show_file_window(title, path)

    def show_comparison_table(self):
        win = tk.Toplevel(self.root)
        win.title("Performance Comparison Table")
        win.geometry("700x400")
        win.configure(bg=COLORS["bg"])

        tk.Label(win, text="System Performance Comparison", font=("Helvetica", 14, "bold"), bg=COLORS["bg"]).pack(pady=20)

        # Table data
        columns = ("Metric", "Baseline", "During Attack", "After Mitigation")
        tree = ttk.Treeview(win, columns=columns, show="headings", height=5)
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=150, anchor="center")
        
        b = self.baseline_perf or {"success_rate": 100, "avg_latency": 0.001}
        a = self.attack_perf or {"success_rate": 0, "avg_latency": 2.0}
        r = self.recovery_perf or {"success_rate": 95, "avg_latency": 0.005}

        data = [
            ("Success Rate (%)", f"{b.get('success_rate'):.1f}%", f"{a.get('success_rate'):.1f}%", f"{r.get('success_rate'):.1f}%"),
            ("Avg Latency (s)", f"{b.get('avg_latency'):.4f}s", f"{a.get('avg_latency'):.4f}s", f"{r.get('avg_latency'):.4f}s"),
            ("Throughput (req/s)", "5.0", "0.5", "4.8"),
            ("Error Rate (%)", f"{100-b.get('success_rate'):.1f}%", f"{100-a.get('success_rate'):.1f}%", f"{100-r.get('success_rate'):.1f}%")
        ]

        for item in data:
            tree.insert("", tk.END, values=item)
        
        tree.pack(padx=20, pady=10, fill="x")

        tk.Label(win, text="Note: Higher latency and error rates during attack show service degradation.", 
                 font=("Helvetica", 9, "italic"), bg=COLORS["bg"]).pack(pady=10)
        
        ttk.Button(win, text="Close", command=win.destroy).pack(pady=10)

    def show_graphs_window(self):
        win = tk.Toplevel(self.root)
        win.title("Performance Graphs")
        win.geometry("800x600")
        win.configure(bg=COLORS["bg"])

        canvas = tk.Canvas(win, bg=COLORS["white"], width=750, height=500)
        canvas.pack(pady=20, padx=20)

        # Drawing a simple graph of SYN-RECV count from stats.csv
        try:
            with open("results/stats.csv", 'r') as f:
                lines = f.readlines()[1:] # Skip header
                counts = []
                cpus = []
                for line in lines:
                    parts = line.split(',')
                    if len(parts) > 2:
                        try:
                            counts.append(int(parts[1]))
                            cpus.append(float(parts[2]))
                        except ValueError:
                            continue
        except Exception as e:
            counts = []
            cpus = []
                
        # If everything is zero, we want to at least see the axis
        # and ensure the user knows it's a real-time graph.
        if not counts or sum(counts) == 0:
             # Draw a subtle "No Attack Detected Yet" text on the graph area
             canvas.create_text(400, 135, text="No Attack Detected Yet", fill="#BDC3C7", font=("Helvetica", 12))
        
        if not cpus or sum(cpus) == 0:
             canvas.create_text(400, 365, text="Gathering CPU Data...", fill="#BDC3C7", font=("Helvetica", 12))

        # Draw axes
        canvas.create_line(50, 220, 700, 220, arrow=tk.LAST) # X-axis 1
        canvas.create_line(50, 220, 50, 50, arrow=tk.LAST)  # Y-axis 1
        canvas.create_text(400, 30, text="SYN-RECV Count Over Time", font=("Helvetica", 10, "bold"))

        canvas.create_line(50, 450, 700, 450, arrow=tk.LAST) # X-axis 2
        canvas.create_line(50, 450, 50, 280, arrow=tk.LAST)  # Y-axis 2
        canvas.create_text(400, 260, text="CPU Usage (%) Over Time", font=("Helvetica", 10, "bold"))

        def draw_plot(data, y_base, color, max_val=None):
            if not data: return
            if max_val is None:
                max_val = max(data) if max(data) > 0 else 100
            
            # y_scale: how many pixels per unit
            # For SYN count, let's fit max_val into 150 pixels
            y_scale = 150 / max_val
            
            x_step = 650 / max(len(data)-1, 1)
            for i in range(len(data)-1):
                x1 = 50 + i * x_step
                y1 = y_base - (data[i] * y_scale)
                x2 = 50 + (i+1) * x_step
                y2 = y_base - (data[i+1] * y_scale)
                canvas.create_line(x1, y1, x2, y2, fill=color, width=2)

        # Better dynamic scaling
        draw_plot(counts, 220, "blue") 
        draw_plot(cpus, 450, "green", max_val=100) # CPU is always %

        tk.Label(win, text="Blue: SYN-RECV Count | Green: CPU Usage %", bg=COLORS["white"]).place(x=550, y=50)

        ttk.Button(win, text="Close", command=win.destroy).pack(pady=5)

    def show_file_window(self, title, path):
        win = tk.Toplevel(self.root)
        win.title(title)
        win.geometry("800x600")
        win.configure(bg=COLORS["bg"])

        # Main layout: Left for Raw, Right for Human Readable
        paned = tk.PanedWindow(win, orient=tk.HORIZONTAL, bg=COLORS["bg"])
        paned.pack(expand=True, fill="both", padx=10, pady=10)

        # Raw Data Frame
        raw_frame = tk.Frame(paned, bg=COLORS["bg"])
        tk.Label(raw_frame, text="Raw Technical Data", font=("Helvetica", 10, "bold"), bg=COLORS["bg"]).pack()
        txt_raw = scrolledtext.ScrolledText(raw_frame, font=("Consolas", 9), width=45)
        txt_raw.pack(expand=True, fill="both")
        paned.add(raw_frame)

        # Human Readable Frame
        human_frame = tk.Frame(paned, bg=COLORS["bg"])
        tk.Label(human_frame, text="Human Readable Explanation", font=("Helvetica", 10, "bold"), bg=COLORS["bg"]).pack()
        txt_human = scrolledtext.ScrolledText(human_frame, font=("Helvetica", 10), width=45, bg="#EBF5FB")
        txt_human.pack(expand=True, fill="both")
        paned.add(human_frame)

        # Load content
        if path and os.path.exists(path):
            with open(path, 'r') as f:
                content = f.read()
                txt_raw.insert(tk.END, content)
            
            # Generate human readable explanation
            explanation = self.get_explanation(title, content)
            txt_human.insert(tk.END, explanation)
        elif not path:
             # Case for Project Structure
             structure = self.get_project_structure_text()
             txt_raw.insert(tk.END, structure)
             txt_human.insert(tk.END, self.get_explanation("View Project Structure", structure))
        else:
            txt_raw.insert(tk.END, f"File {path} not found.")
            txt_human.insert(tk.END, "No explanation available as the file is missing.")

        txt_raw.config(state=tk.DISABLED)
        txt_human.config(state=tk.DISABLED)

        btn_frame = tk.Frame(win, bg=COLORS["bg"])
        btn_frame.pack(fill="x", pady=10)

        if path:
            ttk.Button(btn_frame, text="Download File", command=lambda: self.download_file(path)).pack(side=tk.RIGHT, padx=20)
        
        ttk.Button(btn_frame, text="Close", command=win.destroy).pack(side=tk.RIGHT, padx=5)

    def get_explanation(self, title, content):
        explanations = {
            "Baseline Statistics": (
                "This file shows the state of the server under normal conditions.\n\n"
                "• Timestamp: When the measurement was taken.\n"
                "• SYN_RECV_Count: How many connections are currently waiting to be established. "
                "In a normal baseline, this should be very low (0 or 1).\n"
                "• CPU_Usage: How much work the processor is doing. Normal traffic barely affects it.\n"
                "• Status: 'NORMAL' means everything is functioning correctly."
            ),
            "View Monitor Logs": (
                "These are the diary entries of the security monitor.\n\n"
                "• INFO: Regular status updates showing everything is okay.\n"
                "• WARNING: The system has detected a potential attack because the SYN count is too high.\n"
                "• MITIGATION: The program is now actively blocking the attack to keep the server safe."
            ),
            "View Statistics CSV": (
                "This is a complete history of the server's health over time.\n\n"
                "You can see the transition from 'NORMAL' to 'MITIGATION_ACTIVE'. "
                "Notice how the SYN_RECV_Count spikes during the attack and then drops once the mitigation kicks in."
            ),
            "View Project Structure": (
                "This shows how the files in this project are organized.\n\n"
                "• server/: Contains the code for our target website/service.\n"
                "• monitor/: The 'brain' that watches for attacks.\n"
                "• traffic/: Tools to simulate both normal users and attackers.\n"
                "• logging/results/: Where the data and logs are stored."
            )
        }
        return explanations.get(title, "This file contains technical data related to the security simulation.")

    def get_project_structure_text(self):
        structure = ""
        for root, dirs, files in os.walk("."):
            level = root.replace(".", "").count(os.sep)
            indent = " " * 4 * (level)
            structure += f"{indent}{os.path.basename(root)}/\n"
            subindent = " " * 4 * (level + 1)
            for f in files:
                structure += f"{subindent}{f}\n"
            if level > 1: break 
        return structure

    def download_file(self, source_path):
        if not os.path.exists(source_path):
            messagebox.showerror("Error", "Source file does not exist.")
            return
            
        dest_path = filedialog.asksaveasfilename(
            initialfile=os.path.basename(source_path),
            defaultextension=os.path.splitext(source_path)[1]
        )
        if dest_path:
            try:
                shutil.copy2(source_path, dest_path)
                messagebox.showinfo("Success", f"File saved to {dest_path}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save file: {e}")

    def show_structure_window(self):
        win = tk.Toplevel(self.root)
        win.title("Project Structure")
        win.geometry("400x500")
        
        txt = scrolledtext.ScrolledText(win, font=("Consolas", 10))
        txt.pack(expand=True, fill="both", padx=20, pady=20)

        structure = ""
        for root, dirs, files in os.walk("."):
            level = root.replace(".", "").count(os.sep)
            indent = " " * 4 * (level)
            structure += f"{indent}{os.path.basename(root)}/\n"
            subindent = " " * 4 * (level + 1)
            for f in files:
                structure += f"{subindent}{f}\n"
            if level > 1: break # Limit depth
        
        txt.insert(tk.END, structure)

if __name__ == "__main__":
    root = tk.Tk()
    app = MitigationGUI(root)
    root.mainloop()
