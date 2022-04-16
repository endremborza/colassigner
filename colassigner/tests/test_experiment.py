import pandas as pd

from colassigner import ColAssigner, measure_effect


class Cols(ColAssigner):
    def col_a(self, df):
        return range(df.shape[0])

    def col_b(self, df):
        return df[Cols.col_a] * 2

    def col_c(self, df):
        return df[Cols.col_a] * 0.5

    def col_d(self, df):
        return df[Cols.col_b] - df[Cols.col_c]


def test_effect():
    cass = Cols()
    df = pd.DataFrame(index=range(10)).pipe(cass)
    assert measure_effect(cass, df, Cols.col_a, Cols.col_d, seed=742) == 1.5
