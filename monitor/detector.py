import time
import logging
from monitor.config import SYN_RATE_THRESHOLD, DURATION_THRESHOLD

class DetectionLogic:
    def __init__(self):
        self.consecutive_alerts = 0
        self.mitigation_active = False
        self.logger = logging.getLogger("Detector")
        
    def analyze(self, current_syn_rate):
        """
        Returns True if mitigation should be triggered.
        """
        if current_syn_rate > SYN_RATE_THRESHOLD:
            self.consecutive_alerts += 1
            self.logger.warning(f"Suspicious SYN rate: {current_syn_rate}/s (Alerts: {self.consecutive_alerts}/{DURATION_THRESHOLD})")
        else:
            if self.consecutive_alerts > 0:
                self.logger.info(f"SYN rate normalized: {current_syn_rate}/s")
            self.consecutive_alerts = 0
            
        if self.consecutive_alerts >= DURATION_THRESHOLD and not self.mitigation_active:
            return True
        
        return False

    def should_recover(self, current_syn_rate):
        """
        Returns True if traffic has been normal for a while and mitigation can be removed.
        """
        if self.mitigation_active and current_syn_rate < (SYN_RATE_THRESHOLD / 2):
            # For simplicity, if it's below half the threshold, consider it recovered
            return True
        return False
