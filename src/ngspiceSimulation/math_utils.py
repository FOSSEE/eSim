from typing import Optional
import numpy as np


def _safe_eval(expr: str, data_map: dict) -> "np.ndarray":
    """Evaluate a sanitized expression over pre-resolved trace arrays.

    Caller must run _resolve_expr() first — trace names are replaced with
    _trace_N_ identifiers before this function sees the expression, so the
    AST parser never encounters NGSpice names like v(net1) or i(r1).

    Allowed: trace identifiers (keys of data_map), numeric literals,
    +  -  *  /  ** (unary - and +), abs sqrt log log10 exp sin cos tan.
    Arrays of mismatched length are trimmed to the shorter one before ops.
    Raises ValueError for unknown names, disallowed constructs, or syntax errors.
    """
    import ast
    import operator as op

    _NUMPY_FNS: dict = {
        'abs': np.abs, 'sqrt': np.sqrt,
        'log': np.log, 'log10': np.log10, 'exp': np.exp,
        'sin': np.sin, 'cos': np.cos, 'tan': np.tan,
    }
    _BINOPS: dict = {
        ast.Add: op.add, ast.Sub: op.sub,
        ast.Mult: op.mul, ast.Div: op.truediv,
        ast.Pow: op.pow,
    }
    _UNOPS: dict = {
        ast.USub: op.neg,
        ast.UAdd: lambda x: x,
    }

    def _align(a, b):
        if hasattr(a, '__len__') and hasattr(b, '__len__') and len(a) != len(b):
            n = min(len(a), len(b))
            return a[:n], b[:n]
        return a, b

    def _eval(node):
        if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
            return np.float64(node.value)
        if isinstance(node, ast.Name):
            if node.id in data_map:
                return data_map[node.id]
            raise ValueError(f"Unknown identifier '{node.id}' — "
                             "trace names are substituted before evaluation, "
                             "so this indicates a typo or unsupported construct.")
        if isinstance(node, ast.BinOp):
            fn = _BINOPS.get(type(node.op))
            if fn is None:
                raise ValueError(f"Unsupported operator: {type(node.op).__name__}")
            l, r = _align(_eval(node.left), _eval(node.right))
            return fn(l, r)
        if isinstance(node, ast.UnaryOp):
            fn = _UNOPS.get(type(node.op))
            if fn is None:
                raise ValueError(f"Unsupported unary operator: {type(node.op).__name__}")
            return fn(_eval(node.operand))
        if isinstance(node, ast.Call):
            if not isinstance(node.func, ast.Name):
                raise ValueError(
                    "Attribute calls (e.g. np.sin) are not allowed. "
                    "Use the bare function name instead: sin(…)")
            fn = _NUMPY_FNS.get(node.func.id)
            if fn is None:
                raise ValueError(
                    f"Unknown function '{node.func.id}'. "
                    f"Allowed: {', '.join(sorted(_NUMPY_FNS))}")
            if node.keywords:
                raise ValueError("Keyword arguments are not allowed in function calls.")
            args = [_eval(a) for a in node.args]
            return fn(*args)
        raise ValueError(
            f"Unsupported expression node '{type(node).__name__}'. "
            "Only arithmetic operators and whitelisted functions are allowed.")

    try:
        tree = ast.parse(expr, mode='eval')
    except SyntaxError as exc:
        raise ValueError(f"Syntax error: {exc.msg}") from exc
    return np.asarray(_eval(tree.body), dtype=float)


def _canonical_expr(sanitized: str) -> str:
    """Return canonical form of a sanitized expression for duplicate detection.

    Commutative operators (+, *) flatten their operand chains and sort them,
    so 'a+b+c' and 'c+a+b' produce the same string.  Non-commutative ops
    (-, /, **) keep original order, so 'a-b' and 'b-a' remain distinct.
    Falls back to whitespace-stripped input on parse error.
    """
    import ast

    def _collect(node, op_type: type, results: list) -> None:
        if isinstance(node, ast.BinOp) and isinstance(node.op, op_type):
            _collect(node.left, op_type, results)
            _collect(node.right, op_type, results)
        else:
            results.append(_norm(node))

    def _norm(node) -> str:
        if isinstance(node, ast.BinOp):
            if isinstance(node.op, (ast.Add, ast.Mult)):
                sym = '+' if isinstance(node.op, ast.Add) else '*'
                parts: list = []
                _collect(node, type(node.op), parts)
                parts.sort()
                result = parts[0]
                for p in parts[1:]:
                    result = f'({result}{sym}{p})'
                return result
            left, right = _norm(node.left), _norm(node.right)
            sym = {ast.Sub: '-', ast.Div: '/', ast.Pow: '**'}.get(type(node.op), '?')
            return f'({left}{sym}{right})'
        if isinstance(node, ast.UnaryOp):
            sym = '-' if isinstance(node.op, ast.USub) else '+'
            return f'({sym}{_norm(node.operand)})'
        if isinstance(node, ast.Call):
            func = node.func.id if isinstance(node.func, ast.Name) else repr(node.func)
            return f'{func}({",".join(_norm(a) for a in node.args)})'
        if isinstance(node, ast.Name):
            return node.id
        if isinstance(node, ast.Constant):
            return str(node.value)
        return repr(node)

    try:
        return _norm(ast.parse(sanitized, mode='eval').body)
    except Exception:
        return sanitized.replace(' ', '')


def _format_measurement(value: float, unit: str) -> str:
    """Format a voltage or current with SI prefix. Covers pA/nV to handle
    very small signals without silently returning '0'."""
    abs_val = abs(value)
    if unit == "A":
        if abs_val >= 1:       return f"{value:.3g} A"
        if abs_val >= 1e-3:    return f"{value * 1e3:.3g} mA"
        if abs_val >= 1e-6:    return f"{value * 1e6:.3g} µA"
        if abs_val >= 1e-9:    return f"{value * 1e9:.3g} nA"
        if abs_val >= 1e-12:   return f"{value * 1e12:.3g} pA"
        return f"{value:.3g} A"
    else:
        if abs_val >= 1:       return f"{value:.3g} V"
        if abs_val >= 1e-3:    return f"{value * 1e3:.3g} mV"
        if abs_val >= 1e-6:    return f"{value * 1e6:.3g} µV"
        if abs_val >= 1e-9:    return f"{value * 1e9:.3g} nV"
        if abs_val >= 1e-12:   return f"{value * 1e12:.3g} pV"
        return f"{value:.3g} V"


def _format_frequency(freq_hz: float) -> str:
    """Format a frequency in Hz with an appropriate SI prefix."""
    if freq_hz >= 1e9:   return f"{freq_hz / 1e9:.3g} GHz"
    if freq_hz >= 1e6:   return f"{freq_hz / 1e6:.3g} MHz"
    if freq_hz >= 1e3:   return f"{freq_hz / 1e3:.3g} kHz"
    return                      f"{freq_hz:.3g} Hz"


# numpy 2.0 renamed trapz → trapezoid
_trapz = getattr(np, 'trapezoid', None) or np.trapz


def _detect_frequency(time_data: "np.ndarray",
                      logic_normalized: "np.ndarray") -> "Optional[float]":
    """Return signal frequency in Hz if periodic, else None.

    Uses rising-edge timing with linear interpolation for sub-sample accuracy.
    Requires ≥2 complete cycles and CV < 10% to reject non-periodic signals.
    """
    transitions = np.diff(logic_normalized.astype(np.int8))
    rising_idx = np.where(transitions == 1)[0]
    if len(rising_idx) < 3:
        return None
    # Interpolate crossing time: edge is between sample i and i+1, midpoint
    # gives sub-sample accuracy for non-uniform (adaptive-step) time grids.
    edge_times = (time_data[rising_idx] + time_data[rising_idx + 1]) / 2.0
    periods = np.diff(edge_times)
    if len(periods) == 0:
        return None
    mean_p = float(np.mean(periods))
    if mean_p <= 0:
        return None
    if len(periods) > 1 and float(np.std(periods)) / mean_p > 0.10:
        return None
    return 1.0 / mean_p

