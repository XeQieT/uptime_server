from src.monitor import Monitor
import config

if __name__ == '__main__':
    monitor = Monitor(config.HOST, config.INTERVAL, config.DB_PATH)
    monitor.run()