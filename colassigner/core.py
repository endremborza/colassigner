from abc import ABCMeta
from collections.abc import Mapping
from dataclasses import dataclass
from functools import wraps
from typing import Optional

dic_methods = ["get", "keys", "items", "values"]
CALL_RECORDS = []
CURRENT_CALLER: Optional["CurrentCaller"] = None


@dataclass
class CurrentCaller:
    cls: str
    att: str


@dataclass
class CallRecord:
    caller_cls: str
    called_cls: str
    caller_att: str
    called_att: str

    @property
    def edge(self):
        return {
            "to": ".".join([self.caller_cls, self.caller_att]),
            "from": ".".join([self.called_cls, self.called_att]),
        }


class ColMeta(ABCMeta):
    def __new__(cls, name, bases, local):
        for attr in local:
            value = local[attr]
            if callable(value) and not attr.startswith("_"):
                local[attr] = decor_w_current(value, name, attr)
        return type.__new__(cls, name, bases, local)

    def __getattribute__(cls, attid):
        if attid.startswith("_") or (attid in dic_methods):
            return super().__getattribute__(attid)
        if CURRENT_CALLER is not None:
            CALL_RECORDS.append(
                CallRecord(
                    CURRENT_CALLER.cls, cls.__name__, CURRENT_CALLER.att, attid
                )
            )
        return attid


class ColAssigner(Mapping, metaclass=ColMeta):
    """define functions that create columns in a dataframe

    later the class atributes can be used to access the column"""

    def __init__(self):
        self._callables = {}
        self._add_callables()

    def __getitem__(self, key):
        return self._callables[key]

    def __iter__(self):
        for k in self._callables.keys():
            yield k

    def __len__(self):
        return len(self._callables)

    def _add_callables(self):
        for mid in self.__dir__():
            if mid.startswith("_") or (mid in dic_methods):
                continue
            m = getattr(self, mid)
            self._callables[mid] = m


def allcols(cls):
    return [c for c in cls.__dict__.keys() if not c.startswith("_")]


def decor_w_current(f, clsname, attr):
    @wraps(f)
    def wrapper(*args, **kwds):
        global CURRENT_CALLER
        CURRENT_CALLER = CurrentCaller(clsname, attr)
        out = f(*args, **kwds)
        CURRENT_CALLER = None
        return out

    return wrapper


def get_cr_graph():
    return [cr.edge for cr in CALL_RECORDS]
