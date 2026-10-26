import sys
from io import StringIO

# Add the folder containing attribute.py so Python can import it.
sys.path.append(
    "src/converter/schematic_converters/lib/PythonLib"
)

# Import the Attribute class that we want to test.
from attribute import Attribute


# ----------------------------------------------------------
# Test 1: Check whether the attribute name and value
# are parsed correctly from the input string.
#
# Input:
# PART=EPOLY
#
# Expected:
# name  -> PART
# value -> EPOLY
#
# This verifies the parsing logic inside Attribute.__init__().
# ----------------------------------------------------------
def test_attribute_name_and_value():
    attr = Attribute(
        "a 0 s 11 0 10 34 hln 100 PART=EPOLY"
    )

    assert attr.name == "PART"
    assert attr.value == "EPOLY"


# ----------------------------------------------------------
# Test 2: Check whether coordinates are multiplied by MULT.
#
# Input coordinates:
# x = 10
# y = 34
#
# In attribute.py:
# self.x = x0 * MULT
# self.y = y0 * MULT
#
# Since MULT = 10:
#
# x -> 100
# y -> 340
#
# This ensures coordinate scaling works correctly.
# ----------------------------------------------------------
def test_attribute_coordinates():
    attr = Attribute(
        "a 0 s 11 0 10 34 hln 100 PART=EPOLY"
    )

    assert attr.x == 0
    assert attr.y == 100


# ----------------------------------------------------------
# Test 3: Check whether orientation and text alignment
# are extracted correctly.
#
# Input:
# hln
#
# The constructor splits it into:
#
# h -> orient (horizontal)
# l -> hjust  (left justification)
# n -> vjust  (vertical alignment)
#
# This verifies that the string is correctly separated
# into three different properties.
# ----------------------------------------------------------
def test_attribute_orientation():
    attr = Attribute(
        "a 0 s 11 0 10 34 hln 100 PART=EPOLY"
    )

    assert attr.orient == "h"
    assert attr.hjust == "l"
    assert attr.vjust == "n"


# ----------------------------------------------------------
# Test 4: Check whether the attribute is marked as hidden.
#
# In attribute.py:
#
# if vis.find("13") == -1:
#     self.isHidden = True
#
# The visibility field in our input is:
#
# 0
#
# Since "13" is NOT present,
# isHidden should become True.
#
# This verifies the visibility detection logic.
# ----------------------------------------------------------
def test_attribute_hidden():
    attr = Attribute(
        "a 0 s 11 0 10 34 hln 100 PART=EPOLY"
    )

    assert attr.isHidden is True

# ----------------------------------------------------------
# Test 5: Check whether Attribute.print() writes the
# attribute value to the output stream.
#
# Input:
# PART=EPOLY
#
# The print() function writes:
#
# "EPOLY"
#
# into the KiCad output.
#
# This verifies that the attribute value is correctly
# written to the output stream.
# ----------------------------------------------------------
def test_attribute_print_value():
    attr = Attribute(
        "a 0 s 11 0 10 34 hln 100 PART=EPOLY"
    )

    output = StringIO()

    attr.print(output)

    result = output.getvalue()

    assert '"EPOLY"' in result


# ----------------------------------------------------------
# Test 6: Check whether the orientation is printed correctly.
#
# Input orientation:
# h
#
# Inside Attribute.print():
#
# self.orient.upper()
#
# converts it to:
#
# H
#
# This verifies that the orientation is converted to
# uppercase before being written to the output stream.
# ----------------------------------------------------------
def test_attribute_print_orientation():
    attr = Attribute(
        "a 0 s 11 0 10 34 hln 100 PART=EPOLY"
    )

    output = StringIO()

    attr.print(output)

    result = output.getvalue()

    assert "H" in result

# ----------------------------------------------------------
# Test 7: Check whether Attribute.print() writes the
# correct coordinates.
#
# According to the current implementation:
#
# x = 0
# y = 100
#
# These coordinates should appear in the generated
# KiCad output.
#
# This verifies that Attribute.print() correctly writes
# the stored coordinates.
# ----------------------------------------------------------
def test_attribute_print_coordinates():
    attr = Attribute(
        "a 0 s 11 0 10 34 hln 100 PART=EPOLY"
    )

    output = StringIO()

    attr.print(output)

    result = output.getvalue()

    assert "0 100" in result

# ----------------------------------------------------------
# Test 8: Check whether the hidden flag is printed.
#
# Since isHidden is True,
#
# int(True)
#
# becomes
#
# 1
#
# Therefore the generated output should contain:
#
# 0001
#
# This verifies that the visibility flag is correctly
# written into the KiCad output.
# ----------------------------------------------------------
def test_attribute_print_hidden_flag():
    attr = Attribute(
        "a 0 s 11 0 10 34 hln 100 PART=EPOLY"
    )

    output = StringIO()

    attr.print(output)

    result = output.getvalue()

    assert "0001" in result

# ----------------------------------------------------------
# Test 9: Check whether horizontal justification is
# converted to uppercase.
#
# Input:
#
# hln
#
# hjust = l
#
# Output should contain:
#
# L
#
# This verifies the formatting performed by
# Attribute.print().
# ----------------------------------------------------------
def test_attribute_print_hjust():
    attr = Attribute(
        "a 0 s 11 0 10 34 hln 100 PART=EPOLY"
    )

    output = StringIO()

    attr.print(output)

    result = output.getvalue()

    assert " L " in result

# ----------------------------------------------------------
# Test 10: Check whether vertical justification 'n'
# is converted to 'C'.
#
# The implementation maps:
#
# n -> C
#
# before writing the output.
#
# This verifies that special handling of vertical
# justification works correctly.
# ----------------------------------------------------------
def test_attribute_print_vertical_justification():
    attr = Attribute(
        "a 0 s 11 0 10 34 hln 100 PART=EPOLY"
    )

    output = StringIO()

    attr.print(output)

    result = output.getvalue()

    assert "CNN" in result