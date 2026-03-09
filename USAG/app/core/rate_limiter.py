import time
from collections import defaultdict, deque
from threading import Lock


class RateLimiter:
    def __init__(self, max_requests: int, window_seconds: int = 60):
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.requests = defaultdict(deque)
        self.lock = Lock()

    def is_allowed(self, client_id: str) -> bool:
        current_time = time.time()

        with self.lock:
            queue = self.requests[client_id]

            while queue and current_time - queue[0] > self.window_seconds:
                queue.popleft()

            if len(queue) >= self.max_requests:
                return False

            queue.append(current_time)
            return True

    def get_remaining_requests(self, client_id: str) -> int:
        current_time = time.time()

        with self.lock:
            queue = self.requests[client_id]

            while queue and current_time - queue[0] > self.window_seconds:
                queue.popleft()

            return max(self.max_requests - len(queue), 0)
