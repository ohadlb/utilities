from typing import Callable, TypeVar

__all__ = ['compose']

R = TypeVar('R')
S = TypeVar('S')
T = TypeVar('T')


def compose(f: Callable[[S], T], g: Callable[[R], S]) -> Callable[[R], T]:
    def comp(*args, **kwargs):
        return f(g(*args, **kwargs))

    return comp
