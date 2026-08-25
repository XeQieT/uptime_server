import time
import signal
import datetime
from src.database import Database
from src.ping import ping_host
from src.stats import print_stats

class Monitor:
    def __init__(self, host, interval, db_path):
        self.host = host
        self.interval = interval
        self.db = Database(db_path)
        self.running = True
        self.check_counter = 0
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)

    def signal_handler(self, sig, frame):
        self.running = False

    def run(self):
        print(f"Monitoring {self.host} started. Interval: {self.interval} sec.")
        print("Press Ctrl+C to stop.\n")
        while self.running:
            self.check_counter += 1
            latency = ping_host(self.host)
            success = latency is not None
            self.db.record_ping(success, latency)

            if self.check_counter % 10 == 0:
                uptime_1h = self.db.get_uptime(1)
                uptime_24h = self.db.get_uptime(24)
                last = self.db.get_last()
                print_stats(self.host, last, uptime_1h, uptime_24h)
            else:
                status = 'OK' if success else 'FAIL'
                latency_str = f"{latency} ms" if success else '---'
                print(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] {status} {self.host} -- {latency_str}")

            for _ in range(self.interval):
                if not self.running:
                    break
                time.sleep(1)

        self.db.close()
        print("Data saved. Exit.")