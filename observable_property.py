"""
https://rxpy.readthedocs.io/en/latest/operators.html
"""

import sys
import os
from pathlib import Path

import reactivex as rx
from reactivex import operators as ops
from typing import Any, Callable
import weakref 

class ObservableProperty[T](property):
    InstanceAny = Any 
    rx_sub: rx.Subject[bool]

    def __init__(
        self,
        fget: Callable[[InstanceAny], T] | None = ...,
        fset: Callable[[InstanceAny, T], None] | None = ...,
        fdel: Callable[[InstanceAny], None] | None = ...,
        doc: str | None = ...,
    ) -> None:
        super().__init__(fget, fset, fdel, doc)
        self._rx_subs_map = weakref.WeakKeyDictionary()

    def observable(self, instance: InstanceAny, /) -> rx.abc.ObservableBase:
        return self._get_rx_sub(instance)

    def _get_rx_sub(self, instance: InstanceAny, /) -> rx.Subject[T]:
        return self._rx_subs_map.setdefault(instance, rx.Subject[T]())

    def __delete__(self, instance: InstanceAny, /) -> None:
        super().__delete__(instance)
        self._get_rx_sub(instance).on_completed()

    def __set__(self, instance: Any, value: Any, /) -> None:
        super().__set__(instance, value)
        self._get_rx_sub(instance).on_next(value)

class Config:

    def __init__(self):
        self._x = False
        self._y = True
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
        # print(self.x)
        return self.sub
    
    def observable(self, property: ObservableProperty) -> rx.abc.ObservableBase:
        return property.observable(self)

    x: ObservableProperty[bool] = ObservableProperty[bool](_getx, _setx, _delx, "x property.")

    

def test_observable_property():
    t = Config
    config = Config()
    config2 = Config()

    # config.get_x_property().subscribe(lambda x: print(f'1: {x=}'))
    # config2.get_x_property().subscribe(lambda x: print(f'2: {x=}'))
    config.observable(Config.x).subscribe(lambda x: print(f'3: {x=}'))
    config2.observable(Config.x).subscribe(lambda x: print(f'4: {x=}'))

    print('config.x = True')
    config.x = True
    print('config2.x = True')
    config2.x = True
    print('config2.x = False')
    config2.x = False
    del config
    config2.x = True

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