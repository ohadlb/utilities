from functools import reduce
import operator
from typing import Iterable, Optional

__all__ = ['FunctionalDict', 'dmap', 'dzip', 'merge_dicts', 'rmerge_dicts']


def key_union(*ds) -> set:
    return reduce(operator.or_, map(set, ds), set())


def key_intersection(*ds) -> set:
    return reduce(operator.and_, map(set, ds))


class FunctionalDict(dict):
    def copy_subset(self,
                    whitelist: Optional[Iterable] = None,
                    blacklist: Optional[Iterable] = None) -> 'FunctionalDict':
        if whitelist is None:
            whitelist = self.keys()
        if blacklist is None:
            blacklist = set()

        return FunctionalDict((k, v) for k, v in self.items() if k in whitelist and k not in blacklist)

    def only_keys(self, keys: Iterable) -> 'FunctionalDict':
        return self.copy_subset(whitelist=keys)

    def without_keys(self, keys: Iterable) -> 'FunctionalDict':
        return self.copy_subset(blacklist=keys)

    @classmethod
    def zip(cls, *ds) -> 'FunctionalDict':
        return FunctionalDict((k, tuple(d[k] for d in ds))
                              for k in key_intersection(*ds))

    @classmethod
    def map(cls, func, *ds: dict, mapkeys: bool = True, mapvalues: bool = True) -> 'FunctionalDict':
        if not mapkeys and not mapvalues:
            raise ValueError('The function must operate on either the keys or the values!')
        elif not mapkeys:
            return cls.map(lambda k, *vs: (k, func(*vs)), *ds)
        elif not mapvalues:
            return cls.map(lambda k, *vs: (func(k), *vs), *ds)
        else:
            return FunctionalDict(func(k, *vs) for k, vs in cls.zip(*ds).items())

    @classmethod
    def _merge_single(cls, k, *ds: dict):
        vs = [d[k] for d in ds if k in d]
        if vs and all(vs[0] == v for v in vs[1:]):
            return vs[0]
        elif vs:
            raise ValueError(f'Found mismatched values for the key <<<{k}>>>')
        else:
            raise ValueError(f'Tried to merge on the missing key <<<{k}>>>')

    @classmethod
    def merge(cls, *ds: dict) -> 'FunctionalDict':
        return FunctionalDict((k, cls._merge_single(k, *ds))
                              for k in key_union(*ds))

    @classmethod
    def _rmerge_single(cls, k, *ds: dict, path: tuple):
        vs = [d[k] for d in ds if k in d]
        if vs:
            if all(isinstance(v, dict) for v in vs):
                return cls._rmerge(*vs, path=path + (k,))
            elif all(vs[0] == v for v in vs[1:]):
                return vs[0]
            else:
                raise ValueError(f'Found mismatched values in path {path + (k,)}')
        else:
            raise ValueError(f'Tried to merge at the vacant path {path + (k,)}')

    @classmethod
    def _rmerge(cls, *ds: dict, path: tuple) -> 'FunctionalDict':
        return FunctionalDict((k, cls._rmerge_single(k, *ds, path=path))
                              for k in key_union(*ds))

    @classmethod
    def rmerge(cls, *ds: dict) -> 'FunctionalDict':
        return cls._rmerge(*ds, path=())


def dmap(func, *ds: dict, mapkeys: bool = True, mapvalues: bool = True) -> dict:
    return FunctionalDict.map(func, *ds, mapkeys=mapkeys, mapvalues=mapvalues)


def dzip(*ds: dict) -> dict:
    return dict(FunctionalDict.zip(*ds))


def merge_dicts(*ds: dict) -> dict:
    return dict(FunctionalDict.merge(*ds))


def rmerge_dicts(*ds: dict) -> dict:
    return dict(FunctionalDict.rmerge(*ds))
