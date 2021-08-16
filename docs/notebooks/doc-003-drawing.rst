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

    df_base = pd.DataFrame(
        {
            RawCols.icol1: [1, 1, 2, 3, 0, 1, 2, 3, 5, 4],
            RawCols.fcol1: [0.4, 0.2, 1.2, 3.1, 3.0, 0.1, 0.9, 4.1, 9.0, 3.2],
        }
    )

.. code:: ipython3

    df_base




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
          <th>icol1</th>
          <th>fcol1</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <th>0</th>
          <td>1</td>
          <td>0.4</td>
        </tr>
        <tr>
          <th>1</th>
          <td>1</td>
          <td>0.2</td>
        </tr>
        <tr>
          <th>2</th>
          <td>2</td>
          <td>1.2</td>
        </tr>
        <tr>
          <th>3</th>
          <td>3</td>
          <td>3.1</td>
        </tr>
        <tr>
          <th>4</th>
          <td>0</td>
          <td>3.0</td>
        </tr>
        <tr>
          <th>5</th>
          <td>1</td>
          <td>0.1</td>
        </tr>
        <tr>
          <th>6</th>
          <td>2</td>
          <td>0.9</td>
        </tr>
        <tr>
          <th>7</th>
          <td>3</td>
          <td>4.1</td>
        </tr>
        <tr>
          <th>8</th>
          <td>5</td>
          <td>9.0</td>
        </tr>
        <tr>
          <th>9</th>
          <td>4</td>
          <td>3.2</td>
        </tr>
      </tbody>
    </table>
    </div>



.. code:: ipython3

    df = df_base.assign(**CalcedCols())

.. code:: ipython3

    df




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
          <th>icol1</th>
          <th>fcol1</th>
          <th>compcol1</th>
          <th>modcol1</th>
          <th>compcol2</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <th>0</th>
          <td>1</td>
          <td>0.4</td>
          <td>1.4</td>
          <td>0.20</td>
          <td>0.20</td>
        </tr>
        <tr>
          <th>1</th>
          <td>1</td>
          <td>0.2</td>
          <td>1.2</td>
          <td>0.10</td>
          <td>0.10</td>
        </tr>
        <tr>
          <th>2</th>
          <td>2</td>
          <td>1.2</td>
          <td>3.2</td>
          <td>0.60</td>
          <td>1.20</td>
        </tr>
        <tr>
          <th>3</th>
          <td>3</td>
          <td>3.1</td>
          <td>6.1</td>
          <td>1.55</td>
          <td>4.65</td>
        </tr>
        <tr>
          <th>4</th>
          <td>0</td>
          <td>3.0</td>
          <td>3.0</td>
          <td>1.50</td>
          <td>0.00</td>
        </tr>
        <tr>
          <th>5</th>
          <td>1</td>
          <td>0.1</td>
          <td>1.1</td>
          <td>0.05</td>
          <td>0.05</td>
        </tr>
        <tr>
          <th>6</th>
          <td>2</td>
          <td>0.9</td>
          <td>2.9</td>
          <td>0.45</td>
          <td>0.90</td>
        </tr>
        <tr>
          <th>7</th>
          <td>3</td>
          <td>4.1</td>
          <td>7.1</td>
          <td>2.05</td>
          <td>6.15</td>
        </tr>
        <tr>
          <th>8</th>
          <td>5</td>
          <td>9.0</td>
          <td>14.0</td>
          <td>4.50</td>
          <td>22.50</td>
        </tr>
        <tr>
          <th>9</th>
          <td>4</td>
          <td>3.2</td>
          <td>7.2</td>
          <td>1.60</td>
          <td>6.40</td>
        </tr>
      </tbody>
    </table>
    </div>



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


