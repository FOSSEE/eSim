import sys
import os
import unittest
import importlib.util

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

import numpy as np


def _load_module_from_file(module_name, filename):
    path = os.path.join(
        os.path.dirname(__file__), "..", "src", "ngspiceSimulation", filename
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
_detect_frequency = _math_utils._detect_frequency


class TestFormatMeasurement(unittest.TestCase):
    def test_bare_volt(self):
        self.assertEqual(_format_measurement(5.0, "V"), "5 V")

    def test_milliamp(self):
        self.assertEqual(_format_measurement(0.0012, "A"), "1.2 mA")

    def test_microamp(self):
        self.assertEqual(_format_measurement(5e-6, "A"), "5 \u00b5A")

    def test_nanovolt(self):
        self.assertEqual(_format_measurement(3e-9, "V"), "3 nV")

    def test_picoamp(self):
        self.assertEqual(_format_measurement(1e-12, "A"), "1 pA")

    def test_below_pico_uses_scientific(self):
        self.assertEqual(_format_measurement(1e-15, "V"), "1e-15 V")

    def test_negative_value(self):
        self.assertEqual(_format_measurement(-0.0012, "A"), "-1.2 mA")


class TestFormatFrequency(unittest.TestCase):
    def test_hz(self):
        self.assertEqual(_format_frequency(50), "50 Hz")

    def test_khz(self):
        self.assertEqual(_format_frequency(1234), "1.23 kHz")

    def test_mhz(self):
        self.assertEqual(_format_frequency(1_230_000), "1.23 MHz")

    def test_ghz(self):
        self.assertEqual(_format_frequency(2_400_000_000), "2.4 GHz")

    def test_exact_threshold_khz(self):
        self.assertEqual(_format_frequency(1e3), "1 kHz")

    def test_exact_threshold_ghz(self):
        self.assertEqual(_format_frequency(1e9), "1 GHz")


class TestCanonicalExpr(unittest.TestCase):
    def test_add_commutative(self):
        self.assertEqual(_canonical_expr("a+b"), _canonical_expr("b+a"))

    def test_mul_commutative(self):
        self.assertEqual(_canonical_expr("a*b"), _canonical_expr("b*a"))

    def test_sub_not_commutative(self):
        self.assertNotEqual(_canonical_expr("a-b"), _canonical_expr("b-a"))

    def test_div_not_commutative(self):
        self.assertNotEqual(_canonical_expr("a/b"), _canonical_expr("b/a"))

    def test_pow_not_commutative(self):
        self.assertNotEqual(_canonical_expr("a**b"), _canonical_expr("b**a"))

    def test_mixed_expression_stability(self):
        self.assertEqual(_canonical_expr("(a+b)*c"), _canonical_expr("(b+a)*c"))


class TestSafeEval(unittest.TestCase):
    def test_simple_add(self):
        data = {"a": np.array([1.0, 2.0]), "b": np.array([3.0, 4.0])}
        np.testing.assert_array_equal(_safe_eval("a+b", data), [4.0, 6.0])

    def test_subtraction(self):
        data = {"a": np.array([5.0]), "b": np.array([2.0])}
        np.testing.assert_array_equal(_safe_eval("a-b", data), [3.0])

    def test_multiplication_and_division(self):
        data = {"a": np.array([6.0]), "b": np.array([3.0])}
        np.testing.assert_array_equal(_safe_eval("a*b/b", data), [6.0])

    def test_power(self):
        data = {"a": np.array([2.0])}
        np.testing.assert_array_equal(_safe_eval("a**3", data), [8.0])

    def test_unary_minus(self):
        data = {"a": np.array([2.0])}
        np.testing.assert_array_equal(_safe_eval("-a", data), [-2.0])

    def test_math_functions(self):
        data = {"x": np.array([0.0, np.pi / 2])}
        np.testing.assert_array_almost_equal(
            _safe_eval("sin(x)", data), [0.0, 1.0], decimal=5
        )

    def test_log_and_exp(self):
        data = {"x": np.array([1.0])}
        np.testing.assert_array_almost_equal(
            _safe_eval("exp(log(x))", data), [1.0], decimal=5
        )

    def test_numeric_literal_only(self):
        result = _safe_eval("2*3", {})
        np.testing.assert_array_equal(result, [6.0])

    def test_unknown_identifier_raises(self):
        with self.assertRaises(ValueError):
            _safe_eval("z", {"a": np.array([1.0])})

    def test_unknown_function_raises(self):
        with self.assertRaises(ValueError):
            _safe_eval("foo(x)", {"x": np.array([1.0])})

    def test_keyword_argument_raises(self):
        with self.assertRaises(ValueError):
            _safe_eval("sin(x, step=1)", {"x": np.array([1.0])})

    def test_syntax_error_raises(self):
        with self.assertRaises(ValueError):
            _safe_eval("a+", {"a": np.array([1.0])})

    def test_mismatched_lengths_trimmed(self):
        data = {"a": np.array([1.0, 2.0, 3.0]), "b": np.array([1.0, 2.0])}
        self.assertEqual(len(_safe_eval("a+b", data)), 2)


class TestDetectFrequency(unittest.TestCase):
    def test_periodic_signal(self):
        t = np.linspace(0, 1e-3, 1000)
        sig = np.where(np.sin(2 * np.pi * 1e4 * t) > 0, 1.0, 0.0)
        freq = _detect_frequency(t, sig)
        self.assertIsNotNone(freq)
        self.assertGreater(freq, 8000)
        self.assertLess(freq, 12000)

    def test_too_few_edges_returns_none(self):
        t = np.array([0.0, 1.0])
        sig = np.array([0.0, 1.0])
        self.assertIsNone(_detect_frequency(t, sig))

    def test_constant_signal_returns_none(self):
        t = np.linspace(0, 1e-3, 100)
        sig = np.ones_like(t)
        self.assertIsNone(_detect_frequency(t, sig))


if __name__ == "__main__":
    unittest.main()
