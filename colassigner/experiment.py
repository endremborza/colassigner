import numpy as np

_T_COL = "__treatment"


def experiment(assigner_inst, base_df, col_to_treat, treat_rate=0.5, seed=742):
    treat_arr = np.random.RandomState(seed).rand(base_df.shape[0]) < treat_rate
    orig_fun = getattr(assigner_inst, col_to_treat)

    def f(df, *args, **kwargs):
        out = orig_fun(df, *args, **kwargs)
        return out + treat_arr.astype(int)

    f.__name__ = col_to_treat
    setattr(assigner_inst, col_to_treat, f)
    out = base_df.assign(**{_T_COL: treat_arr}).pipe(assigner_inst)
    setattr(assigner_inst, col_to_treat, orig_fun)
    return out


def measure_effect(assigner, base_df, cause_col, effect_col, treat_rate=0.5, seed=742):
    _cols = [_T_COL, effect_col]
    exp_df = experiment(assigner, base_df, cause_col, treat_rate, seed).loc[:, _cols]
    treat_ser = exp_df[_T_COL]
    return (
        exp_df.loc[treat_ser, effect_col].mean()
        - base_df.loc[treat_ser, effect_col].mean()
    )
