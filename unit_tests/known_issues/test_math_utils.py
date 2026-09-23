import sys
import os
import unittest
import importlib.util

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "src"))

import numpy as np


def _load_module_from_file(module_name, filename):
    path = os.path.join(
        os.path.dirname(__file__), "..", "..", "src", "ngspiceSimulation", filename
    )
    spec = importlib.util.spec_from_file_location(module_name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


_math_utils = _load_module_from_file("math_utils", "math_utils.py")

_format_measurement = _math_utils._format_measurement
_format_frequency = _math_utils._format_frequency
_canonical_expr = _math_utils._canonical_expr
_safe_eval = _math_utils._safe_eval


class KnownIssueFormatMeasurement(unittest.TestCase):
    """
    Characterisation tests for _format_measurement input sanitation.

    Each test pins the CURRENT (buggy) behaviour. When a dev fixes the
    underlying issue the assertion will fail, signalling that the test
    should move into unit_tests/test_math_utils.py with the corrected
    expectation.
    """

    def test_unknown_unit_falls_through_to_volts(self):
        self.assertEqual(_format_measurement(5.0, "W"), "5 V")

    def test_lowercase_unit_uses_volts_branch(self):
        self.assertEqual(_format_measurement(5.0, "a"), "5 V")

    def test_none_unit_returns_volts(self):
        self.assertEqual(_format_measurement(5.0, None), "5 V")

    def test_nan_value_returns_nan_string(self):
        self.assertEqual(_format_measurement(float("nan"), "V"), "nan V")

    def test_inf_value_returns_inf_string(self):
        self.assertEqual(_format_measurement(float("inf"), "A"), "inf A")


class KnownIssueFormatFrequency(unittest.TestCase):
    def test_negative_frequency_propagates(self):
        self.assertEqual(_format_frequency(-500), "-500 Hz")

    def test_non_numeric_input_raises_typeerror(self):
        with self.assertRaises(TypeError):
            _format_frequency("1e3")


class KnownIssueCanonicalExpr(unittest.TestCase):
    def test_attribute_syntax_leaks_ast_repr(self):
        result = _canonical_expr("a.b")
        self.assertNotEqual(result, "a.b")
        self.assertIn("Attribute", result)


class KnownIssueSafeEval(unittest.TestCase):
    def test_empty_function_args_raise_typeerror(self):
        with self.assertRaises(TypeError):
            _safe_eval("sin()", {})

    def test_division_by_zero_returns_inf(self):
        np.testing.assert_array_equal(
            _safe_eval("a/0", {"a": np.array([1.0])}), [np.inf]
        )

    def test_bool_literal_is_coerced_to_one(self):
        np.testing.assert_array_equal(
            _safe_eval("a+True", {"a": np.array([1.0])}), [2.0]
        )

    def test_list_input_concatenates(self):
        np.testing.assert_array_equal(
            _safe_eval("a+a", {"a": [1, 2]}), [1.0, 2.0, 1.0, 2.0]
        )


if __name__ == "__main__":
    unittest.main()
