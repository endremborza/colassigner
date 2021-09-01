import pandas as pd
from pytest import raises

from colassigner import ColAssigner, __version__, allcols


def test_import():
    assert isinstance(__version__, str)


def test_assigner():
    class Cols1(ColAssigner):
        def var1(self, df):
            return df.iloc[:, 0].mean()

    _df = pd.DataFrame({"a": [1, 2, 3]}).assign(**Cols1())

    assert (_df.loc[:, "var1"] == 2).all()
    assert (_df.loc[:, Cols1.var1] == 2).all()
    assert len(Cols1()) == 1
    assert allcols(Cols1) == ["var1"]


def test_wrong_colname():
    with raises(ValueError):

        class ColW(ColAssigner):
            def mro(self, df):
                return 4  # pragma: nocover


def test_subassigner():
    class Cols(ColAssigner):
        def var1(self, df):
            return 1

        class SubCol(ColAssigner):
            _prefix = "subc"

            def fing(self, df):
                return df.sum(axis=1)

            class SubSubCol(ColAssigner):
                _prefix = "ss1"

                def subvar(self, df):
                    return 0

                def subvar2(self, df):
                    return self._prefix + df[Cols.var1].astype(str)

            class SubSubCol2(SubSubCol):
                _prefix = "ss2"

    df1 = pd.DataFrame({"a": [1, 2, 3]})

    _df = df1.assign(**Cols())

    assert Cols.SubCol.fing == "subc__fing"
    assert Cols.SubCol.SubSubCol.subvar == "subc__ss1__subvar"
    assert Cols.SubCol.SubSubCol2.subvar2 == "subc__ss2__subvar2"
    assert allcols(Cols) == [
        "subc__ss1__subvar",
        "subc__ss1__subvar2",
        "subc__ss2__subvar",
        "subc__ss2__subvar2",
        "subc__fing",
        "var1",
    ]
    assert (_df.loc[:, Cols.SubCol.fing] == (_df["a"] + _df[Cols.var1])).all()
    assert (_df[Cols.SubCol.SubSubCol2.subvar2] == "ss21").all()
