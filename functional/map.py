from multiprocessing.pool import Pool
from typing import Callable, Iterable, Optional, Tuple, TypeVar

from .base import compose

__all__ = ['dist_map', 'timeout_map', 'tqdm_map_func']

S = TypeVar('S')
T = TypeVar('T')
TMap = Callable[[Callable[[S], T], Tuple[Iterable[S], ...]], Iterable[T]]


def dist_map(nprocs: int, ordered: bool) -> TMap:
    # NOT creating the pool as a context, to avoid having it terminated upon `return`
    pool = Pool(processes=nprocs)

    return pool.imap if ordered else pool.imap_unordered


def timeout_map(timeout: Optional[float]) -> TMap:
    import timeout_decorator

    def map_(func: Callable[[S], T], *iterables: Iterable[S]) -> Iterable[T]:
        for xs in zip(iterables):
            try:
                yield timeout_decorator.timeout(timeout)(func)(*xs)
            except timeout_decorator.TimeoutError:
                continue

    return map_


def tqdm_map_func(map_: TMap, **tqdm_kwargs) -> TMap:
    from functools import partial
    import tqdm

    return compose(partial(tqdm.tqdm, **tqdm_kwargs), map_)
