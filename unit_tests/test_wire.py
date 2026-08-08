import sys
from io import StringIO

sys.path.append(
    "src/converter/schematic_converters/lib/PythonLib"
)

import wire


def test_wire_constructor():
    w = wire.Wire(1, 2, 3, 4)

    assert w.x1 == 1
    assert w.y1 == 2
    assert w.x2 == 3
    assert w.y2 == 4


def test_connector_constructor():
    c = wire.Connector(5, 6)

    assert c.x == 5
    assert c.y == 6


def test_parse_wire():
    wires = []

    stream = StringIO(
        "s 1 2 3 4 0\n"
        "@\n"
    )

    wire.parseWire(stream, wires)

    assert len(wires) == 1

    w = wires[0]

    assert w.x1 == 10
    assert w.y1 == 20
    assert w.x2 == 30
    assert w.y2 == 40


def test_parse_conn():
    conns = []

    stream = StringIO(
        "j 7 8\n"
        "@\n"
    )

    wire.parseConn(stream, conns)

    assert len(conns) == 1

    c = conns[0]

    assert c.x == 70
    assert c.y == 80