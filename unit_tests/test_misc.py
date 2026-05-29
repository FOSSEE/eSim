import sys
class MockAttr:
    def __init__(self, value):
        self.value = value


class MockInst:
    def __init__(self, type_, attrs):
        self.type_ = type_
        self.attrs = attrs

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

def test_fix_inst_j_reference():
    inst = MockInst(
        "ANY",
        [MockAttr("J10")]
    )

    misc.fixInst(inst)

    assert inst.attrs[0].value == "J?"

def test_fix_inst_m_reference():
    inst = MockInst(
        "ANY",
        [MockAttr("M25")]
    )

    misc.fixInst(inst)

    assert inst.attrs[0].value == "M?"