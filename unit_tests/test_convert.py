import os
import sys
import types
import unittest
import importlib.util
from unittest.mock import mock_open, patch
from xml.etree import ElementTree as ET

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))


def _load_convert():
    sys.modules["PyQt6"] = types.ModuleType("PyQt6")
    qtw = types.ModuleType("PyQt6.QtWidgets")
    qtw.QErrorMessage = type("QErrorMessage", (), {})
    qtw.QWidget = type("QWidget", (), {})
    sys.modules["PyQt6.QtWidgets"] = qtw
    tw = types.ModuleType("kicadtoNgspice.TrackWidget")
    tw.TrackWidget = type("TrackWidget", (), {})
    sys.modules["kicadtoNgspice.TrackWidget"] = tw
    path = os.path.join(
        os.path.dirname(__file__), "..", "src", "kicadtoNgspice", "Convert.py"
    )
    spec = importlib.util.spec_from_file_location("kicadtoNgspice.Convert", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    sys.modules["kicadtoNgspice.Convert"] = module
    return module


_convert = _load_convert()
Convert = _convert.Convert


class _MockEntry:
    def __init__(self, text):
        self._text = text

    def text(self):
        return self._text


def _entries(pairs):
    return dict((index, _MockEntry(text)) for index, text in pairs)


class TestConverttosciform(unittest.TestCase):
    def setUp(self):
        self.convert = Convert([], {}, [], "/f/c.cir")

    def test_milli(self):
        self.assertEqual(self.convert.converttosciform("m"), "e-03")

    def test_micro(self):
        self.assertEqual(self.convert.converttosciform("u"), "e-06")

    def test_nano(self):
        self.assertEqual(self.convert.converttosciform("n"), "e-09")

    def test_pico(self):
        self.assertEqual(self.convert.converttosciform("p"), "e-12")

    def test_empty(self):
        self.assertEqual(self.convert.converttosciform(""), "e-00")

    def test_unrecognised_unit_uses_default(self):
        self.assertEqual(self.convert.converttosciform("V"), "e-00")


class TestDefaultvalue(unittest.TestCase):
    def setUp(self):
        self.convert = Convert([], {}, [], "/f/c.cir")

    def test_empty_string_defaults_to_zero(self):
        self.assertEqual(self.convert.defaultvalue(""), 0)

    def test_value_passthrough(self):
        self.assertEqual(self.convert.defaultvalue("100"), "100")

    def test_zero_passthrough(self):
        self.assertEqual(self.convert.defaultvalue(0), 0)


class TestAddSourceParameter(unittest.TestCase):
    def _convert(self, track, entries, schematic):
        return Convert(track, entries, schematic, "/f/c.cir")

    def test_sine(self):
        convert = self._convert(
            [[0, "sine", 0, 4]],
            _entries([(0, "1"), (1, "5"), (2, "1k"), (3, "0"), (4, "0")]),
            ["v1 1 0 sine(0 0 0 0 0)"],
        )
        self.assertEqual(convert.addSourceParameter(), ["v1 1 0 sine(1 5 1k 0 0)"])

    def test_sine_empty_entries_use_zero(self):
        convert = self._convert(
            [[0, "sine", 0, 4]],
            _entries([(0, ""), (1, ""), (2, ""), (3, ""), (4, "")]),
            ["v1 1 0 sine(0 0 0 0 0)"],
        )
        self.assertEqual(convert.addSourceParameter(), ["v1 1 0 sine(0 0 0 0 0)"])

    def test_pulse(self):
        convert = self._convert(
            [[0, "pulse", 0, 6]],
            _entries(
                [(0, "0"), (1, "5"), (2, "1m"), (3, "1u"), (4, "1u"), (5, "5m"),
                 (6, "10m")]
            ),
            ["v1 1 0 pulse(0 0 0 0 0 0 0)"],
        )
        self.assertEqual(
            convert.addSourceParameter(), ["v1 1 0 pulse(0 5 1m 1u 1u 5m 10m)"]
        )

    def test_pwl(self):
        convert = self._convert(
            [[0, "pwl", 0, 0]],
            _entries([(0, "0 0 1m 5 2m 0")]),
            ["v1 1 0 pwl(0 0)"],
        )
        self.assertEqual(convert.addSourceParameter(), ["v1 1 0 pwl(0 0 1m 5 2m 0)"])

    def test_pwl_empty_uses_default(self):
        convert = self._convert(
            [[0, "pwl", 0, 0]],
            _entries([(0, "")]),
            ["v1 1 0 pwl(0 0)"],
        )
        self.assertEqual(convert.addSourceParameter(), ["v1 1 0 pwl(0 0)"])

    def test_ac(self):
        convert = self._convert(
            [[0, "ac", 0, 1]],
            _entries([(0, "1"), (1, "0")]),
            ["v1 1 0 ac"],
        )
        self.assertEqual(convert.addSourceParameter(), ["v1 1 0  ac 1 0"])

    def test_dc(self):
        convert = self._convert(
            [[0, "dc", 0, 0]],
            _entries([(0, "5")]),
            ["v1 1 0 dc 0"],
        )
        self.assertEqual(convert.addSourceParameter(), ["v1 1 0  dc 5"])

    def test_exp(self):
        convert = self._convert(
            [[0, "exp", 0, 5]],
            _entries([(0, "0"), (1, "5"), (2, "1m"), (3, "1u"), (4, "1m"), (5, "1u")]),
            ["v1 1 0 exp(0 0 0 0 0 0)"],
        )
        self.assertEqual(
            convert.addSourceParameter(), ["v1 1 0 exp(0 5 1m 1u 1m 1u)"]
        )

    def test_multiple_sources_replaced_in_order(self):
        convert = self._convert(
            [[0, "sine", 0, 4], [1, "dc", 5, 5]],
            _entries([(0, "1"), (1, "0"), (2, "1k"), (3, "0"), (4, "0"), (5, "5")]),
            ["v1 1 0 sine(0 0 0 0 0)", "v2 2 0 dc 0"],
        )
        self.assertEqual(
            convert.addSourceParameter(),
            ["v1 1 0 sine(1 0 1k 0 0)", "v2 2 0  dc 5"],
        )


class TestAnalysisInsertor(unittest.TestCase):
    def _content(self, variable, acv=None, dcv=None, trv=None, acp=None,
                 dcp=None, trp=None, ac_type="", op=None):
        convert = Convert([], {}, [], "/fake/circuit.cir")
        m = mock_open()
        with patch("builtins.open", m):
            convert.analysisInsertor(
                acv or {},
                dcv or {},
                trv or {},
                variable,
                acp or {},
                dcp or {},
                trp or {},
                ac_type,
                op or [0],
            )
        return "".join(call.args[0] for call in m().write.call_args_list)

    def test_ac_dec(self):
        self.assertEqual(
            self._content(
                "AC",
                acv=_entries([(0, "1"), (1, "1e6"), (2, "100")]),
                acp={0: "Hz", 1: "Meg"},
                ac_type="dec",
            ),
            ".ac dec 100 1Hz 1e6Meg",
        )

    def test_ac_lin(self):
        self.assertEqual(
            self._content(
                "AC",
                acv=_entries([(0, "1"), (1, "1e6"), (2, "1")]),
                acp={0: "Hz", 1: "Meg"},
                ac_type="lin",
            ),
            ".ac lin 1 1Hz 1e6Meg",
        )

    def test_ac_empty_entries_default_to_zero(self):
        self.assertEqual(
            self._content(
                "AC",
                acv=_entries([(0, ""), (1, ""), (2, "")]),
                acp={0: "Hz", 1: "Meg"},
                ac_type="dec",
            ),
            ".ac dec 0 0Hz 0Meg",
        )

    def test_tran(self):
        self.assertEqual(
            self._content(
                "TRAN",
                trv=_entries([(0, "0"), (1, "0.01"), (2, "1")]),
                trp={0: "sec", 1: "sec", 2: "sec"},
            ),
            ".tran 0.01e-00 1e-00 0e-00",
        )

    def test_dc(self):
        self.assertEqual(
            self._content(
                "DC",
                dcv=_entries(
                    [(0, "V1"), (1, "0"), (2, "0.1"), (3, "5"), (4, ""),
                     (5, ""), (6, ""), (7, "")]
                ),
                dcp={0: "V", 1: "V", 2: "V"},
            ),
            ".dc V1 0e-00 5e-00 0.1e-00",
        )

    def test_dc_two_sources(self):
        self.assertEqual(
            self._content(
                "DC",
                dcv=_entries(
                    [(0, "V1"), (1, "0"), (2, "0.1"), (3, "5"), (4, "V2"),
                     (5, "0"), (6, "1"), (7, "10")]
                ),
                dcp={0: "V", 1: "V", 2: "V", 3: "V", 4: "V", 5: "V"},
            ),
            ".dc V1 0e-00 5e-00 0.1e-00 V2 0e-00 10e-00 1e-00",
        )

    def test_op(self):
        self.assertEqual(
            self._content("DC", dcv=_entries([(0, "V1"), (1, ""), (2, ""),
                                              (3, ""), (4, ""), (5, ""),
                                              (6, ""), (7, "")]), op=[1]),
            ".op",
        )

    def test_unknown_variable_writes_nothing(self):
        self.assertEqual(self._content("NONE"), "")


class TestGetReferenceName(unittest.TestCase):
    def test_returns_ref_model_text(self):
        tree = ET.fromstring("<lib><ref_model>2N2222</ref_model></lib>")
        with patch("kicadtoNgspice.Convert.ET.parse", return_value=tree) as parse:
            result = Convert([], {}, [], "/f/c.cir").getReferenceName(
                "2n2222.lib", "/libs"
            )
        self.assertEqual(result, "2N2222")
        parse.assert_called_once_with(os.path.join("/libs", "2n2222.xml"))


if __name__ == "__main__":
    unittest.main()
