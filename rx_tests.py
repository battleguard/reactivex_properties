"""
https://rxpy.readthedocs.io/en/latest/operators.html
"""

import sys
import os
from pathlib import Path

import reactivex as rx
from reactivex import operators as ops

def test_rx_on_path():
    sys_paths: rx.Observable[list[str]] = rx.from_iterable(os.environ['PATH'].split(os.pathsep))
    HOME_PATH: Path = Path.home()
    # user_paths = sys_paths.pipe(
    #     ops.map(lambda p: Path(p)),
    #     ops.filter(lambda p: p.is_relative_to(HOME_PATH)),
    #     ops.map(lambda p: p.relative_to(HOME_PATH))
    # )

    def path_query(p: str):
        if (path := Path(p)) and path.is_relative_to(HOME_PATH):
            yield path

    def filter(p: str):
        if (path := Path(p)) and path.is_relative_to(HOME_PATH):
            return rx.of(path.relative_to(HOME_PATH))
        return rx.empty()

    user_paths = sys_paths.pipe(
        ops.map(Path),
        ops.map(Path.as_uri),
        ops.map(len),
        ops.sum(),
        # ops.flat_map(filter),
        # ops.flat_map(lambda p: rx.of(p.relative_to(HOME_PATH)) \
        #              if (p := Path(p)) and p.is_relative_to(HOME_PATH) \
        #                 else rx.empty()),
        # ops.map(lambda p: Path(p).relative_to(HOME_PATH)),
        ops.distinct()
    )

    # sys_paths: rx.Observable[list[str]] = rx.from_iterable([1,2,3])
    user_paths.subscribe(lambda value: print(f"Received {value} {value.__class__}"),
                         on_error=lambda e: print(f'{e=}'),
                         on_completed=lambda: print(f'on_complete'))


def default_test():
    source = rx.of("Alpha", "Beta", "Gamma", "Delta", "Epsilon")
    composed = source.pipe(
        ops.map(lambda s: len(s)),
        ops.filter(lambda i: i >= 5)
    )
    composed.subscribe(lambda value: print("Received {0}".format(value)))

def test_lambda():
    (lambda x: (a:=x*2) + a)(3)
    func = lambda x: (x + 1) + 1
    print(func(5))
    

if __name__ == '__main__':
    test_lambda()
    # test_rx_on_path()



# how to open multiple windows?

# how to install package?
# pip installing required restart of idle
