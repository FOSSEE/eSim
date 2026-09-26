import os
import sys
import types
import unittest
import importlib.util
from unittest.mock import mock_open, patch
from xml.etree import ElementTree as ET

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "src"))


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
        os.path.dirname(__file__), "..", "..", "src", "kicadtoNgspice", "Convert.py"
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


class KnownIssueConverttosciform(unittest.TestCase):
    """
    Characterisation tests for converttosciform input sanitation.

    Each test pins the CURRENT (buggy) behaviour. When a dev fixes the
    underlying issue the assertion will fail, signalling that the test
    should move into unit_tests/test_convert.py with the corrected
    expectation.
    """

    def setUp(self):
        self.convert = Convert([], {}, [], "/f/c.cir")

    def test_mega_misread_as_milli(self):
        self.assertEqual(self.convert.converttosciform("meg"), "e-03")

    def test_kilo_unsupported(self):
        self.assertEqual(self.convert.converttosciform("k"), "e-00")

    def test_capital_mega_unsupported(self):
        self.assertEqual(self.convert.converttosciform("M"), "e-00")

    def test_none_falls_back_to_default(self):
        self.assertEqual(self.convert.converttosciform(None), "e-00")

    def test_non_string_raises_type_error(self):
        with self.assertRaises(TypeError):
            self.convert.converttosciform(123)


class KnownIssueDefaultvalue(unittest.TestCase):
    def setUp(self):
        self.convert = Convert([], {}, [], "/f/c.cir")

    def test_none_passes_through(self):
        self.assertEqual(self.convert.defaultvalue(None), None)


class KnownIssueAddSourceParameter(unittest.TestCase):
    def test_ac_substring_in_node_name_garbles_line(self):
        convert = Convert(
            [[0, "ac", 0, 1]],
            _entries([(0, "1"), (1, "0")]),
            ["vac1 1 0 ac"],
            "/f/c.cir",
        )
        self.assertEqual(convert.addSourceParameter(), ["v ac 1 0"])

    def test_out_of_range_index_raises(self):
        convert = Convert(
            [[5, "dc", 0, 0]],
            _entries([(0, "5")]),
            ["v1 1 0 dc 0"],
            "/f/c.cir",
        )
        with self.assertRaises(IndexError):
            convert.addSourceParameter()

    def test_missing_entry_key_is_silently_ignored(self):
        convert = Convert(
            [[0, "dc", 0, 0]],
            {},
            ["v1 1 0 dc 0"],
            "/f/c.cir",
        )
        self.assertEqual(convert.addSourceParameter(), ["v1 1 0 dc 0"])


class KnownIssueAnalysisInsertor(unittest.TestCase):
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

    def test_dc_empty_source_name_not_defaulted(self):
        self.assertEqual(
            self._content(
                "DC",
                dcv=_entries(
                    [(0, ""), (1, "0"), (2, "0.1"), (3, "5"), (4, ""),
                     (5, ""), (6, ""), (7, "")]
                ),
                dcp={0: "V", 1: "V", 2: "V"},
            ),
            ".dc  0e-00 5e-00 0.1e-00",
        )

    def test_ac_empty_type_double_space(self):
        self.assertEqual(
            self._content(
                "AC",
                acv=_entries([(0, "1"), (1, "1e6"), (2, "100")]),
                acp={0: "Hz", 1: "Meg"},
                ac_type="",
            ),
            ".ac  100 1Hz 1e6Meg",
        )


class KnownIssueGetReferenceName(unittest.TestCase):
    def test_missing_ref_model_raises_unbound_local(self):
        tree = ET.fromstring("<lib><model>X</model></lib>")
        with patch("kicadtoNgspice.Convert.ET.parse", return_value=tree):
            with self.assertRaises(UnboundLocalError):
                Convert([], {}, [], "/f/c.cir").getReferenceName(
                    "2n2222.lib", "/libs"
                )


if __name__ == "__main__":
    unittest.main()
