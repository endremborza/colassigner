import ast
from importlib import import_module
from itertools import chain
from pathlib import Path
from typing import List, Type

from .core import ColAssigner


class MethodDef:
    def __init__(self, stmt: ast.FunctionDef, bases):
        self.name = stmt.name
        self.bases = set(bases)
        self.uses = set()
        for inner in stmt.body:
            self._add(inner)

    def _add(self, elem: ast.AST):
        if isinstance(elem, (ast.Assign, ast.Return, ast.keyword, ast.Index)):
            return self._add(elem.value)
        if isinstance(elem, ast.ExtSlice):
            return [*map(self._add, elem.dims)]
        if isinstance(elem, ast.Slice):
            return self._add(elem.lower), self._add(elem.upper)
        if isinstance(elem, ast.Attribute):
            base = elem.value
            if isinstance(base, ast.Name) and (base.id in [*self.bases, "self"]):
                return self.uses.add(elem.attr)
            return self._add(base)
        if isinstance(elem, ast.Call):
            [*map(self._add, elem.args + elem.keywords)]
            return self._add(elem.func)
        if isinstance(elem, ast.BinOp):
            return self._add(elem.left), self._add(elem.right)
        if isinstance(elem, ast.Subscript):
            return self._add(elem.value), self._add(elem.slice)
        if isinstance(elem, (ast.Constant, ast.Name)) or elem is None:
            return
        ast.ExtSlice

        raise ValueError(f"unrecognized expression {type(elem)}: {elem}")


class ClsParser:
    def __init__(self, stmt: ast.ClassDef) -> None:
        self.name = stmt.name
        self._resolvers = {}
        self._mds: List[MethodDef] = []
        for fundef in stmt.body:
            md = MethodDef(fundef, [self.name])
            if md.name.startswith("_"):
                self._resolvers[md.name] = md.uses
            else:
                self._mds.append(md)

    def get_edges(self):
        return chain(*map(self._iter_mc, self._mds))

    def _iter_mc(self, md: MethodDef):
        for source in md.uses:
            if source.startswith("_"):
                for sub in self._resolve(source):
                    yield (sub, md.name)
            else:
                yield (source, md.name)

    def _resolve(self, source, resolved=()):
        for sub in self._resolvers.get(source, []):
            if sub in resolved:
                continue
            resolved = (sub, *resolved)
            if sub.startswith("_"):
                for ssub in self._resolve(sub, resolved):
                    yield ssub
            else:
                yield sub


def get_dag(cls: Type[ColAssigner]):
    """generates a dag of the reliances of columns
    based on the ast of a colassigner

    Parameters
    ----------
    cls : Type[ColAssigner]

    Returns
    -------
    list of edges of a dag

    BETA! - WIP

    rules:
    - explicitly access columns within other functions
    - no external function referencing column (only method of assigner class)
    - no common source in as attributes
    - self should always be named self
    """
    fp = import_module(cls.__module__).__file__
    asm = ast.parse(Path(fp).read_text(), filename=fp)
    for stmt in asm.body:
        if isinstance(stmt, ast.ClassDef) and stmt.name == cls.__name__:
            return [*ClsParser(stmt).get_edges()]
