from colassigner import ColAccessor, get_col_type


def test_type_retention():
    class TestCols(ColAccessor):

        fing = int

        class SubCol(ColAccessor):
            _prefix = "subc"
            a = int
            b = float

            class SubSubCol(ColAccessor):
                _prefix = "ss1"
                x = str
                y = str

            class SubSubCol2(SubSubCol):
                _prefix = "ss2"

    assert get_col_type(TestCols, TestCols.fing) == int
    assert get_col_type(TestCols.SubCol, TestCols.SubCol.b) == float
    assert (
        get_col_type(TestCols.SubCol.SubSubCol2, TestCols.SubCol.SubSubCol2.x)
        == str
    )
