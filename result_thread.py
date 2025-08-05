from threading import Thread
from typing import Any

class result_thread(Thread):
    """ 
    idea being that we want to capture the image and extract the information 
    in an isolated thread, so as not to interfere with the camera operation.

    So far this does the trick, so long as you are interacting with the second camera... kinda weird behavior
    """
    result: Any
    
    def __init__(self, target, args):
        super().__init__()
        self._target = target
        self._args = args
        self.result = None

    def run(self):
        self.result = self._target(self._args[0])
        self._args[1](self.result)