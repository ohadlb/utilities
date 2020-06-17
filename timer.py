import time
from typing import Callable, Union


class ExecutionTimer:
    def __init__(self, output: Union[None, str, Callable[[float], None]] = 'Execution completed in {:.2f}s'):
        """
        A simple reusable context for timing a section of code. The start and end of the exection are timestamped
        as the members `.start` and `.stop` for external use.

        The parameter `output` can be one of the following:
        1. None, and then the timer is silent, and only records the execution
        2. a string with one formattable position, which will be formatted with the total elapsed time
        3. a callback function accepting a single float argument, which will be called with the total elapsed time
        """
        self.output = output

    def __enter__(self):
        self.start = time.time()

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stop = time.time()
        self.interval = self.stop - self.start

        if self.output is None:
            # Do nothing
            pass
        elif isinstance(self.output, str):
            print(self.output.format(self.interval))
        else:
            self.output(self.interval)
