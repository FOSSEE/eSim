import sys
from io import StringIO

sys.path.append(
    "src/converter/schematic_converters/lib/PythonLib"
)

from component_instance import ComponentInstance


def test_component_instance_basic_properties():
    stream = StringIO(
        "c 1 RES 10 20 h\n"
        "@\n"
    )

    comp = ComponentInstance(stream)

    assert comp.type_ == "RES"
    assert comp.x == 100
    assert comp.y == 200
    assert comp.orient == "h"

def test_component_instance_default_pkgref():
    stream = StringIO(
        "c 1 RES 10 20 h\n"
        "@\n"
    )

    comp = ComponentInstance(stream)

    assert comp.attrs[0].name == "PKGREF"
    assert comp.attrs[0].value == "RES"

def test_component_instance_default_value():
    stream = StringIO(
        "c 1 RES 10 20 h\n"
        "@\n"
    )

    comp = ComponentInstance(stream)

    assert comp.attrs[1].value == "RES"

def test_component_instance_pkgref_attribute():
    stream = StringIO(
        "c 1 RES 10 20 h\n"
        "a 0 s 11 0 10 34 hln 100 PKGREF=R1\n"
        "@\n"
    )

    comp = ComponentInstance(stream)

    assert comp.attrs[0].name == "PKGREF"
    assert comp.attrs[0].value == "R1"

def test_component_instance_value_attribute():
    stream = StringIO(
        "c 1 RES 10 20 h\n"
        "a 0 s 11 0 10 34 hln 100 VALUE=100\n"
        "@\n"
    )

    comp = ComponentInstance(stream)

    assert comp.attrs[1].name == "VALUE"
    assert comp.attrs[1].value == "100"

def test_component_instance_dc_attribute():
    stream = StringIO(
        "c 1 VDC 10 20 h\n"
        "a 0 s 11 0 10 34 hln 100 DC=5\n"
        "@\n"
    )

    comp = ComponentInstance(stream)

    assert comp.attrs[1].name == "DC"
    assert comp.attrs[1].value == "5"

def test_component_instance_gain_attribute():
    stream = StringIO(
        "c 1 AMP 10 20 h\n"
        "a 0 s 11 0 10 34 hln 100 GAIN=10\n"
        "@\n"
    )

    comp = ComponentInstance(stream)

    assert comp.attrs[1].name == "GAIN"
    assert comp.attrs[1].value == "10"

def test_component_instance_print_contains_component_block():
    stream = StringIO(
        "c 1 RES 10 20 h\n"
        "a 0 s 11 0 10 34 hln 100 PKGREF=R1\n"
        "a 0 s 11 0 10 34 hln 100 VALUE=100\n"
        "@\n"
    )

    comp = ComponentInstance(stream)

    output = StringIO()

    comp.print(output)

    result = output.getvalue()

    assert "$Comp" in result
    assert "$EndComp" in result

def test_component_instance_print_component_name():
    stream = StringIO(
        "c 1 RES 10 20 h\n"
        "a 0 s 11 0 10 34 hln 100 PKGREF=R1\n"
        "a 0 s 11 0 10 34 hln 100 VALUE=100\n"
        "@\n"
    )

    comp = ComponentInstance(stream)

    output = StringIO()

    comp.print(output)

    result = output.getvalue()

    assert "L RES R1" in result

def test_component_instance_print_coordinates():
    stream = StringIO(
        "c 1 RES 10 20 h\n"
        "a 0 s 11 0 10 34 hln 100 PKGREF=R1\n"
        "a 0 s 11 0 10 34 hln 100 VALUE=100\n"
        "@\n"
    )

    comp = ComponentInstance(stream)

    output = StringIO()

    comp.print(output)

    result = output.getvalue()

    assert "P 100 200" in result

def test_component_instance_print_horizontal_orientation():
    stream = StringIO(
        "c 1 RES 10 20 h\n"
        "a 0 s 11 0 10 34 hln 100 PKGREF=R1\n"
        "a 0 s 11 0 10 34 hln 100 VALUE=100\n"
        "@\n"
    )

    comp = ComponentInstance(stream)

    output = StringIO()

    comp.print(output)

    result = output.getvalue()

    assert "1    0    0    -1" in result

def test_component_instance_print_vertical_orientation():
    stream = StringIO(
        "c 1 RES 10 20 v\n"
        "a 0 s 11 0 10 34 hln 100 PKGREF=R1\n"
        "a 0 s 11 0 10 34 hln 100 VALUE=100\n"
        "@\n"
    )

    comp = ComponentInstance(stream)

    output = StringIO()

    comp.print(output)

    result = output.getvalue()

    assert "0    -1    -1    0" in result

def test_component_instance_print_H_orientation():
    stream = StringIO(
        "c 1 RES 10 20 H\n"
        "a 0 s 11 0 10 34 hln 100 PKGREF=R1\n"
        "a 0 s 11 0 10 34 hln 100 VALUE=100\n"
        "@\n"
    )

    comp = ComponentInstance(stream)

    output = StringIO()

    comp.print(output)

    result = output.getvalue()

    assert "-1    0    0    -1" in result

def test_component_instance_print_V_orientation():
    stream = StringIO(
        "c 1 RES 10 20 V\n"
        "a 0 s 11 0 10 34 hln 100 PKGREF=R1\n"
        "a 0 s 11 0 10 34 hln 100 VALUE=100\n"
        "@\n"
    )

    comp = ComponentInstance(stream)

    output = StringIO()

    comp.print(output)

    result = output.getvalue()

    assert "0    1    -1    0" in result

def test_component_instance_print_u_orientation():
    stream = StringIO(
        "c 1 RES 10 20 u\n"
        "a 0 s 11 0 10 34 hln 100 PKGREF=R1\n"
        "a 0 s 11 0 10 34 hln 100 VALUE=100\n"
        "@\n"
    )

    comp = ComponentInstance(stream)

    output = StringIO()

    comp.print(output)

    result = output.getvalue()

    assert "-1    0    0    1" in result


def test_component_instance_print_U_orientation():
    stream = StringIO(
        "c 1 RES 10 20 U\n"
        "a 0 s 11 0 10 34 hln 100 PKGREF=R1\n"
        "a 0 s 11 0 10 34 hln 100 VALUE=100\n"
        "@\n"
    )

    comp = ComponentInstance(stream)

    output = StringIO()

    comp.print(output)

    result = output.getvalue()

    assert "1    0    0    1" in result


def test_component_instance_print_d_orientation():
    stream = StringIO(
        "c 1 RES 10 20 d\n"
        "a 0 s 11 0 10 34 hln 100 PKGREF=R1\n"
        "a 0 s 11 0 10 34 hln 100 VALUE=100\n"
        "@\n"
    )

    comp = ComponentInstance(stream)

    output = StringIO()

    comp.print(output)

    result = output.getvalue()

    assert "0    1    1    0" in result


def test_component_instance_print_D_orientation():
    stream = StringIO(
        "c 1 RES 10 20 D\n"
        "a 0 s 11 0 10 34 hln 100 PKGREF=R1\n"
        "a 0 s 11 0 10 34 hln 100 VALUE=100\n"
        "@\n"
    )

    comp = ComponentInstance(stream)

    output = StringIO()

    comp.print(output)

    result = output.getvalue()

    assert "0    -1    1    0" in result

def test_component_instance_print_field_headers():
    stream = StringIO(
        "c 1 RES 10 20 h\n"
        "a 0 s 11 0 10 34 hln 100 PKGREF=R1\n"
        "a 0 s 11 0 10 34 hln 100 VALUE=100\n"
        "@\n"
    )

    comp = ComponentInstance(stream)

    output = StringIO()

    comp.print(output)

    result = output.getvalue()

    assert "F 0" in result
    assert "F 1" in result

def test_component_instance_print_reference_and_value():
    stream = StringIO(
        "c 1 RES 10 20 h\n"
        "a 0 s 11 0 10 34 hln 100 PKGREF=R1\n"
        "a 0 s 11 0 10 34 hln 100 VALUE=100\n"
        "@\n"
    )

    comp = ComponentInstance(stream)

    output = StringIO()

    comp.print(output)

    result = output.getvalue()

    assert '"R1"' in result
    assert '"100"' in result

def test_component_instance_print_unit_line():
    stream = StringIO(
        "c 1 RES 10 20 h\n"
        "a 0 s 11 0 10 34 hln 100 PKGREF=R1\n"
        "a 0 s 11 0 10 34 hln 100 VALUE=100\n"
        "@\n"
    )

    comp = ComponentInstance(stream)

    output = StringIO()

    comp.print(output)

    result = output.getvalue()

    assert "U 1 1" in result