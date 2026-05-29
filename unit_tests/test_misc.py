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