import pandas as pd

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
