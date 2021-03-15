Quickstart
==========

.. code:: ipython3

    import pandas as pd

.. code:: ipython3

    from colassigner import ColAssigner

.. code:: ipython3

    class Cols1(ColAssigner):    
        
        def var1(self, df):
            return df.iloc[:,0].mean()
        
        def var2(self, df):
            return "added-another"

.. code:: ipython3

    df = pd.DataFrame({"a": [1,2,3]}).assign(**Cols1())

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
          <th>a</th>
          <th>var1</th>
          <th>var2</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <th>0</th>
          <td>1</td>
          <td>2.0</td>
          <td>added-another</td>
        </tr>
        <tr>
          <th>1</th>
          <td>2</td>
          <td>2.0</td>
          <td>added-another</td>
        </tr>
        <tr>
          <th>2</th>
          <td>3</td>
          <td>2.0</td>
          <td>added-another</td>
        </tr>
      </tbody>
    </table>
    </div>


