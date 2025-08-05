from threading import Thread
from typing import Any

class result_thread(Thread):
    result: Any
    
    def __init__(self, target, args):
        super().__init__()
        self._target = target
        self._args = args
        self.result = None

    def run(self):
        self.result = self._target(self._args[0])
        self._args[1](self.result)