import sys

sys.path.append(
    "src/converter/schematic_converters/lib/PythonLib"
)

import misc


def test_strip_num_from_ref_resistor():
    assert misc.stripNumFromRef("R10") == "R"


def test_strip_num_from_ref_capacitor():
    assert misc.stripNumFromRef("C25") == "C"


def test_strip_num_from_ref_transistor():
    assert misc.stripNumFromRef("Q100") == "Q"

from io import StringIO

def test_skip_to_found():
    stream = StringIO(
        "abc\n"
        "def\n"
        "*symbol transistor\n"
        "xyz\n"
    )

    result = misc.skipTo(stream, "*symbol")

    assert result == "*symbol transistor"


def test_skip_to_not_found():
    stream = StringIO(
        "abc\n"
        "def\n"
        "xyz\n"
    )

    result = misc.skipTo(stream, "*symbol")

    assert result == "__ERROR__"