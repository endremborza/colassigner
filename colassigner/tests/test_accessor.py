from colassigner import ColAccessor, allcols


def test_accessor():
    class TestCols(ColAccessor):

        fing = "fing"

        class SubCol(ColAccessor):
            _prefix = "subc"
            a = "a"
            b = "b"

            class SubSubCol(ColAccessor):
                _prefix = "ss1"
                x = "x"
                y = "y"

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
