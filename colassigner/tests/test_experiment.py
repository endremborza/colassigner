import numpy as np
import pandas as pd

from colassigner import ColAssigner, experiment, measure_effect
from colassigner.experiment import _T_COL


class Cols(ColAssigner):
    def __init__(self) -> None:
        self._rng = None

    def col_a(self, df):
        self._rng = np.random.RandomState(123)
        return self._rng.random(df.shape[0])

    def col_b(self, df):
        return df[Cols.col_a] * 2

    def col_c(self, df):
        return df[Cols.col_a] * 0.5

    def col_d(self, df):
        return df[Cols.col_b] - df[Cols.col_c]


def test_effect():
    cass = Cols()
    df = pd.DataFrame(index=range(1000)).pipe(cass)
    eff = measure_effect(cass, df, Cols.col_a, Cols.col_d)
    assert round(eff, 1) == 1.5


def test_experiment():
    cass = Cols()
    edf = experiment(cass, pd.DataFrame(index=range(500)), Cols.col_b, 0.3)
    treat_means = edf.groupby(_T_COL).mean().round(1).loc[True, :].tolist()
    assert treat_means == [0.5, 2.0, 0.2, 1.7]
