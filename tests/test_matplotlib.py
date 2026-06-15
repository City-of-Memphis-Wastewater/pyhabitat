def test_import_pyhabitat_does_not_import_matplotlib():
    import sys

    sys.modules.pop("matplotlib", None)
    sys.modules.pop("matplotlib.pyplot", None)

    import pyhabitat

    assert "matplotlib" not in sys.modules
    assert "matplotlib.pyplot" not in sys.modules
