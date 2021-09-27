from colassigner import ColAccessor, allcols


def test_accessor():
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

    assert TestCols.SubCol.a == "subc__a"
    assert TestCols.SubCol.SubSubCol.x == "subc__ss1__x"
    assert TestCols.SubCol.SubSubCol2.y == "subc__ss2__y"
    assert allcols(TestCols) == [
        "subc__ss1__x",
        "subc__ss1__y",
        "subc__ss2__x",
        "subc__ss2__y",
        "subc__a",
        "subc__b",
        "fing",
    ]


def test_accessor_id_cols():
    class IdCols(ColAccessor):

        fing_id = int
        other_id = str

    class TableCols(ColAccessor):

        foreign_key = IdCols.fing_id

    assert TableCols.foreign_key == "foreign_key"
