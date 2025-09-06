import threading
from queue import PriorityQueue
from app.notification import NotificationManager
from app.metrics import Metrics
import time


# Simple priority map so earlier timestamps are processed first
def _priority_from_timestamp(ts_str: str) -> float:
    try:
        # convert ISO-like timestamp to epoch for priority
        from datetime import datetime
        dt = datetime.fromisoformat(ts_str)
        return dt.timestamp()
    except Exception:
        return time.time()

# Shared metrics singleton so different LogProcessor instances update the same counters
_shared_metrics = Metrics()


class LogProcessor:
    def __init__(self):
        self.queues = {
            "CRITICAL": PriorityQueue(),
            "WARNING": PriorityQueue(),
            "INFO": PriorityQueue(),
        }

        # Helpers
        self.notification_manager = NotificationManager()
        # use shared metrics singleton
        self.metrics = _shared_metrics

        # in-memory storage of received logs
        self._storage = []
        self.running = True

        # Start consumer threads for each log level
        self._start_consumers()

    def _start_consumers(self):
        # Start a separate thread for each queue to consume logs
        self.consumer_threads = []
        for level in self.queues:
            thread = threading.Thread(target=self._consume_queue, args=(level,), daemon=True)
            thread.start()
            self.consumer_threads.append(thread)

    def _consume_queue(self, level):
        """ Continuously consumes logs from the queue for the given log level. """
        q = self.queues.get(level)
        while self.running:
            try:
                # block for a short time to allow graceful shutdown
                priority, log = q.get(timeout=0.5)
            except Exception:
                continue
            # process the log - for now we will call notification if level is CRITICAL/WARNING
            try:
                # send notification respecting cooldown
                now = time.time()
                last = self.notification_manager.last_notification_time.get(level)
                cooldown = self.notification_manager.cooldown.get(level, 0)
                if last is None or (now - last) >= cooldown:
                    self.notification_manager.last_notification_time[level] = now
                    self.notification_manager.send_notification(log)
                    self.metrics.increment("notifications_sent")
            finally:
                q.task_done()

    def process_log(self, log_data: dict):
        """Store the incoming log and enqueue it for processing by level.

        This method is safe to call from request handlers or tests.
        """
        # store original log
        self._storage.append(log_data)

        # increment processed metric immediately so /metrics reflects received logs
        try:
            self.metrics.increment("logs_processed")
        except Exception:
            pass

        # enqueue into appropriate priority queue
        level = log_data.get("level")
        if level not in self.queues:
            # unknown level, ignore enqueue but still count as received
            return

        priority = _priority_from_timestamp(log_data.get("timestamp", ""))
        self.queues[level].put((priority, log_data))

    def get_logs(self, level: str | None = None):
        """Return stored logs, optionally filtered by level."""
        if level:
            if level not in self.queues:
                return []
            return [l for l in self._storage if l.get("level") == level]
        return list(self._storage)


# Shared metrics singleton so different LogProcessor instances update the same counters
_shared_metrics = Metrics()

