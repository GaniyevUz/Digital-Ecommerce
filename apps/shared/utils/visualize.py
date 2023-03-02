from itertools import cycle
from shutil import get_terminal_size
from threading import Thread
from time import sleep


class Loader:
    def __init__(self, func: callable, count: int, obj: str, *args, **kwargs):
        """
        A loader-like context manager

        Args:
            func (callable, required): Function for loading.
            count (int, required): Count of objects.
            obj (str, required): Object Name.
        """

        self.create = 'Creating {} {} object...'
        self.created = '\033[34m{}\033[00m {} object successfully \033[92mCreated!\033[00m'
        self.timeout = 0.05

        self.count = count
        self.obj = obj
        self.func = func

        self._thread = Thread(target=self._animate, daemon=True)
        self.steps = ["⢿", "⣻", "⣽", "⣾", "⣷", "⣯", "⣟", "⡿"]
        self.done = False
        self.run(func, *args, **kwargs)

    def start(self):
        self._thread.start()
        return self

    def _animate(self):
        for c in cycle(self.steps):
            if self.done:
                break
            print(f"\r\033[34m{c}\033[00m   {self.create.format(self.count, self.obj)}", flush=True, end="")
            sleep(self.timeout)

    def __enter__(self):
        self.start()

    def stop(self):
        self.done = True
        cols = get_terminal_size((80, 20)).columns
        print("\r" + " " * cols, end="", flush=True)
        print(f"\r{self.created.format(self.count, self.obj)}", flush=True)

    def __exit__(self, exc_type, exc_value, tb):
        self.stop()

    def run(self, func, *args, **kwargs):
        self.start()
        if func:
            func(*args, **kwargs)
        self.stop()
