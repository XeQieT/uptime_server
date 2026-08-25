import sqlite3
import datetime

class Database:
    def __init__(self, db_path):
        self.conn = sqlite3.connect(db_path, detect_types=sqlite3.PARSE_DECLTYPES)
        self.cursor = self.conn.cursor()
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS ping_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TIMESTAMP NOT NULL,
                success INTEGER NOT NULL,
                latency_ms REAL
            )
        ''')
        self.conn.commit()

    def record_ping(self, success, latency):
        now = datetime.datetime.now()
        self.cursor.execute(
            "INSERT INTO ping_log (timestamp, success, latency_ms) VALUES (?, ?, ?)",
            (now, 1 if success else 0, latency)
        )
        self.conn.commit()

    def get_uptime(self, hours=24):
        since = datetime.datetime.now() - datetime.timedelta(hours=hours)
        self.cursor.execute(
            "SELECT COUNT(*), SUM(success) FROM ping_log WHERE timestamp >= ?",
            (since,)
        )
        total, successes = self.cursor.fetchone()
        if total is None or total == 0:
            return None
        return (successes or 0) / total * 100.0

    def get_last(self):
        self.cursor.execute("SELECT timestamp, success, latency_ms FROM ping_log ORDER BY id DESC LIMIT 1")
        return self.cursor.fetchone()

    def close(self):
        self.conn.close()