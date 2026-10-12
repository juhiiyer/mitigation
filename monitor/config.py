# Configuration for SYN Flood Monitor

# Network settings
INTERFACE = "eth1"  # Host-only interface on the server
SERVER_PORT = 8080

# Thresholds
# SYN_RATE_THRESHOLD: number of SYN packets per interval
SYN_RATE_THRESHOLD = 50 
# INTERVAL: monitoring window in seconds
CHECK_INTERVAL = 5
# DURATION_THRESHOLD: how many consecutive intervals must exceed threshold to trigger mitigation
DURATION_THRESHOLD = 2

# Mitigation settings
MITIGATION_ENABLED = True
BLOCK_DURATION = 60 # seconds (optional auto-cleanup)

# Log settings
LOG_FILE = "logging/monitor.log"
STATS_FILE = "results/stats.csv"
