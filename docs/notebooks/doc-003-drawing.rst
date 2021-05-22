Generating Call Graph
=====================

.. code:: ipython3

    import pandas as pd
    
    from colassigner import ColAssigner, get_cr_graph

.. code:: ipython3

    class RawCols(ColAssigner):
    
        icol1 = int
        fcol1 = float

.. code:: ipython3

    class CalcedCols(ColAssigner):
        def compcol1(self, df):
            return df.loc[:, RawCols.fcol1] + df.loc[:, RawCols.icol1]
    
        def modcol1(self, df):
            return df.loc[:, RawCols.fcol1] / 2
    
        def compcol2(self, df):
            return df.loc[:, RawCols.icol1] * df.loc[:, CalcedCols.modcol1]

.. code:: ipython3

    df = pd.DataFrame(
        {
            RawCols.icol1: [1, 1, 2, 3, 0, 1, 2, 3, 5, 4],
            RawCols.fcol1: [0.4, 0.2, 1.2, 3.1, 3.0, 0.1, 0.9, 4.1, 9.0, 3.2],
        }
    ).assign(**CalcedCols())

.. code:: ipython3

    pd.DataFrame(get_cr_graph())




.. raw:: html

    <div>
    <style scoped>
        .dataframe tbody tr th:only-of-type {
            vertical-align: middle;
        }
    
        .dataframe tbody tr th {
            vertical-align: top;
        }
    
        .dataframe thead th {
            text-align: right;
        }
    </style>
    <table border="1" class="dataframe">
      <thead>
        <tr style="text-align: right;">
          <th></th>
          <th>to</th>
          <th>from</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <th>0</th>
          <td>CalcedCols.compcol1</td>
          <td>RawCols.fcol1</td>
        </tr>
        <tr>
          <th>1</th>
          <td>CalcedCols.compcol1</td>
          <td>RawCols.icol1</td>
        </tr>
        <tr>
          <th>2</th>
          <td>CalcedCols.modcol1</td>
          <td>RawCols.fcol1</td>
        </tr>
        <tr>
          <th>3</th>
          <td>CalcedCols.compcol2</td>
          <td>RawCols.icol1</td>
        </tr>
        <tr>
          <th>4</th>
          <td>CalcedCols.compcol2</td>
          <td>CalcedCols.modcol1</td>
        </tr>
      </tbody>
    </table>
    </div>


