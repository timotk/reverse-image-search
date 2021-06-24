import itertools
import threading
import time


class Spinner:
    """
    Context manager that runs a spinner in a separate non-blocking thread.

    Args:
        delay: Time in seconds to indicate delay between changing spinners.
    """

    def __init__(self, delay: float = 0.1):
        self.delay = delay
        self.spinners = ["⢿", "⣻", "⣽", "⣾", "⣷", "⣯", "⣟", "⡿"]
        self.running = False
        self.thread = threading.Thread(target=self.spin, daemon=True)

    def spin(self):
        for c in itertools.cycle(self.spinners):
            if not self.running:
                print("\r", end="")
                break
            print("\r" + c, end="")
            time.sleep(self.delay)

    def __enter__(self):
        self.running = True
        self.thread.start()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.running = False
