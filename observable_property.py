"""
https://rxpy.readthedocs.io/en/latest/operators.html
"""

import sys
import os
from pathlib import Path

import reactivex as rx
from reactivex import operators as ops

class Config:

    def __init__(self):
        self._x = False
        self.sub = rx.Subject[bool]()

    def _getx(self) -> bool:
        return self._x

    def _setx(self, value: bool):
        if self._x != value:
            self.sub.on_next(value)
            self._x = value

    def _delx(self):
        self.sub.on_completed()
        del self._x

    def get_x_property(self) -> rx.abc.ObservableBase[bool]:
        return self.sub

    x = property(_getx, _setx, _delx, "I'm the 'x' property.")


def test_observable_property():
    config = Config()

    print(config.get_x_property().subscribe(lambda x: print(f'{x=}')))

    config.x = True
    config.x = False
    config.x = False
    config.x = True
    config.x = False
    config.x = True

def simple_subject_test():
    test = rx.Subject[str]()
    test.subscribe(
        on_next = lambda i: print("Received {0}".format(i)),
        on_error = lambda e: print("Error Occurred: {0}".format(e)),
        on_completed = lambda: print("Done!"),
    )
    test.on_next("foo")
    test.on_next("bar")
    test.on_completed()



if __name__ == '__main__':
    test_observable_property()