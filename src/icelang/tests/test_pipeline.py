"""
ICELang test suite
==================
Covers the full pipeline from parser to KiCad output, plus the plugin
runner adapter. Does not test the KiCad/PyQt5 UI layer (requires a
running KiCad session — out of scope for CI).

Run with:
    cd /home/princess/icelang
    python -m pytest tests/test_pipeline.py -v
"""

import os
import sys
import json
import shutil
import subprocess
import pytest
from pathlib import Path

ROOT = Path(__file__).parent.parent.resolve()
sys.path.insert(0, str(ROOT))

from icelang_parser import parser, ICELangTransformer, analyse, CktBlock
from intelligent_schematic_layer.graph_builder import build
from intelligent_schematic_layer.placement_engine import place


# ---------------------------------------------------------------------------
# Source fixtures
# ---------------------------------------------------------------------------

RC_FILTER = """
ckt rc_filter:
    port_in: Vin
    port_out: Vout mid
    res Vin mid 1k
    cap mid gnd 220n
done
"""

VOLTAGE_DIVIDER = """
ckt voltage_divider:
    port_in: Vin
    port_out: Vout mid
    vol Vin gnd 9V
    res Vin mid 10k
    res mid gnd 10k
done
"""

SIGNAL_CONDITIONER = """
ckt signal_conditioner:
    define filter_cap kicad="Device:C" spice=C pins=2
    define pull_down  kicad="Device:R" spice=R pins=2
    define series_res kicad="Device:R" spice=R pins=2
    port_in: Vin
    port_out: Vout mid
    series_res Vin mid 1k
    filter_cap mid gnd 220n
    pull_down  mid gnd 100k
done
"""

ZENER_CLAMP = """
ckt zener_clamp:
    ncomp zen: D_Zener
    port_in: Vin
    port_out: Vout mid
    res Vin mid 1k
    zen mid gnd 5V1
done
"""


def _parse(src: str) -> CktBlock:
    tree   = parser.parse(src.strip())
    result = ICELangTransformer().transform(tree)
    blocks = result if isinstance(result, list) else [result]
    ckts   = [b for b in blocks if isinstance(b, CktBlock)]
    assert ckts, "No CktBlock found"
    return ckts[-1]


# ---------------------------------------------------------------------------
# 1. Parser round-trip tests
# ---------------------------------------------------------------------------

class TestParser:

    def test_rc_filter_component_count(self):
        ckt = _parse(RC_FILTER)
        assert ckt.name == "rc_filter"
        assert len(ckt.components) == 2

    def test_rc_filter_node_names(self):
        ckt  = _parse(RC_FILTER)
        nodes = {n for c in ckt.components for n in c.nodes}
        assert "vin" in nodes
        assert "mid" in nodes
        assert "gnd" in nodes

    def test_rc_filter_port_in(self):
        ckt = _parse(RC_FILTER)
        assert ckt.port_in is not None
        assert ckt.port_in.name == "vin"

    def test_rc_filter_port_out(self):
        ckt = _parse(RC_FILTER)
        assert ckt.port_out is not None
        assert ckt.port_out.node == "mid"

    def test_rc_filter_component_types(self):
        ckt   = _parse(RC_FILTER)
        types = [c.type for c in ckt.components]
        assert "res" in types
        assert "cap" in types

    def test_rc_filter_values(self):
        ckt    = _parse(RC_FILTER)
        values = {c.type: c.value for c in ckt.components}
        assert values["res"] == "1k"
        assert values["cap"] == "220n"

    def test_signal_conditioner_component_count(self):
        ckt = _parse(SIGNAL_CONDITIONER)
        assert len(ckt.components) == 3

    def test_signal_conditioner_define_types(self):
        ckt   = _parse(SIGNAL_CONDITIONER)
        types = {c.type for c in ckt.components}
        assert "series_res" in types or "res" in types
        assert "filter_cap" in types or "cap" in types
        assert "pull_down"  in types or "res" in types

    def test_voltage_divider_driver_present(self):
        ckt   = _parse(VOLTAGE_DIVIDER)
        types = [c.type for c in ckt.components]
        assert "vol" in types

    def test_semantic_analysis_passes_rc_filter(self):
        ckt    = _parse(RC_FILTER)
        errors = analyse(ckt)
        assert errors == [], f"Unexpected semantic errors: {errors}"

    def test_semantic_analysis_passes_voltage_divider(self):
        ckt    = _parse(VOLTAGE_DIVIDER)
        errors = analyse(ckt)
        assert errors == [], f"Unexpected semantic errors: {errors}"


# ---------------------------------------------------------------------------
# 2. ncomp registration tests
# ---------------------------------------------------------------------------

class TestNcomp:

    def test_ncomp_parses_without_error(self):
        ckt = _parse(ZENER_CLAMP)
        assert ckt.name == "zener_clamp"

    def test_ncomp_registers_in_registry(self):
        _parse(ZENER_CLAMP)
        from component_registry import lookup
        entry = lookup("zen")
        assert entry is not None
        assert entry["kicad_symbol"] == "Device:D_Zener"

    def test_ncomp_pin_count_enforced(self):
        from component_registry import lookup
        entry = lookup("zen")
        assert entry["pin_count"] == 2

    def test_ncomp_signal_pin_inferred(self):
        _parse(ZENER_CLAMP)
        from component_registry import lookup
        entry = lookup("zen")
        assert entry.get("signal_pin") == "K"

    def test_ncomp_component_has_two_nodes(self):
        ckt = _parse(ZENER_CLAMP)
        zen = next(c for c in ckt.components if c.type == "zen")
        assert len(zen.nodes) == 2
        assert "mid" in zen.nodes
        assert "gnd" in zen.nodes

    def test_ncomp_rejects_three_terminal(self, tmp_path):
        src = """
ckt bad_circuit:
    ncomp q: Q_NPN_BCE
    port_in: Vin
    port_out: Vout mid
    res Vin mid 1k
    q mid gnd 0
done
"""
        with pytest.raises(Exception, match="two-terminal|pins|not found"):
            _parse(src)

    def test_ncomp_rejects_nonexistent_symbol(self):
        src = """
ckt bad_circuit:
    ncomp fake: NonExistentSymbol_XYZ123
    port_in: Vin
    port_out: Vout mid
    res Vin mid 1k
done
"""
        with pytest.raises(Exception, match="not found"):
            _parse(src)


# ---------------------------------------------------------------------------
# 3. Placement engine tests
# ---------------------------------------------------------------------------

class TestPlacement:

    def test_series_nodes_at_y_zero(self):
        ckt    = _parse(RC_FILTER)
        G      = build(ckt)
        placed = place(G, ckt)
        for node in ("vin", "mid"):
            assert node in placed, f"{node} not in placed"
            _, y = placed[node]
            assert abs(y) < 0.01, f"{node} y={y}, expected 0"

    def test_series_nodes_left_to_right(self):
        ckt    = _parse(RC_FILTER)
        G      = build(ckt)
        placed = place(G, ckt)
        vin_x, _ = placed["vin"]
        mid_x, _ = placed["mid"]
        assert mid_x > vin_x, f"mid ({mid_x}) should be right of vin ({vin_x})"

    def test_shunt_node_below_signal_path(self):
        ckt    = _parse(RC_FILTER)
        G      = build(ckt)
        placed = place(G, ckt)
        gnd_keys = [k for k in placed if k == "gnd" or k.startswith("gnd_shunt_")]
        assert gnd_keys, "No GND position in placed dict"
        for k in gnd_keys:
            _, y = placed[k]
            assert y < 0, f"GND key {k} has y={y}, expected negative"

    def test_voltage_divider_three_nodes(self):
        ckt    = _parse(VOLTAGE_DIVIDER)
        G      = build(ckt)
        placed = place(G, ckt)
        assert "vin" in placed
        assert "mid" in placed
        vin_x, _ = placed["vin"]
        mid_x, _ = placed["mid"]
        assert mid_x > vin_x

    def test_parallel_shunts_spread_horizontally(self):
        ckt    = _parse(SIGNAL_CONDITIONER)
        G      = build(ckt)
        placed = place(G, ckt)
        gnd_shunt_keys = [k for k in placed if k.startswith("gnd_shunt_")]
        assert len(gnd_shunt_keys) >= 2, "Expected at least 2 shunt GND positions"
        xs = [placed[k][0] for k in gnd_shunt_keys]
        assert len(set(xs)) > 1, "Parallel shunts should have different x coordinates"

    def test_driver_placed_left_of_vin(self):
        ckt    = _parse(VOLTAGE_DIVIDER)
        G      = build(ckt)
        placed = place(G, ckt)
        vin_x, _ = placed["vin"]
        driver_keys = [k for k in placed if k.startswith("gnd_driver_")]
        if driver_keys:
            for k in driver_keys:
                drv_x, _ = placed[k]
                assert drv_x < vin_x, f"Driver at x={drv_x} should be left of VIN x={vin_x}"

    def test_grid_snapping(self):
        ckt    = _parse(RC_FILTER)
        G      = build(ckt)
        placed = place(G, ckt)
        grid   = 2.54
        for node, (x, y) in placed.items():
            assert abs(x % grid) < 0.01 or abs(x % grid - grid) < 0.01, \
                f"{node} x={x} is not on 2.54mm grid"
            assert abs(y % grid) < 0.01 or abs(y % grid - grid) < 0.01, \
                f"{node} y={y} is not on 2.54mm grid"


# ---------------------------------------------------------------------------
# 4. KiCad output validity tests
# ---------------------------------------------------------------------------

class TestKiCadOutput:

    def _run_compiler(self, ilang_path: Path, output_dir: Path) -> Path:
        result = subprocess.run(
            [sys.executable, str(ROOT / "main.py"),
             str(ilang_path), str(output_dir)],
            capture_output=True, text=True, cwd=str(ROOT)
        )
        assert result.returncode == 0, (
            f"Compiler failed\nstdout: {result.stdout}\nstderr: {result.stderr}"
        )
        return output_dir / f"{ilang_path.stem}.kicad_sch"

    def test_rc_filter_output_exists(self, tmp_path):
        src = ROOT / "test_circuits" / "rc_filter.ilang"
        if not src.exists():
            pytest.skip("test_circuits/rc_filter.ilang not found")
        sch = self._run_compiler(src, tmp_path)
        assert sch.exists(), f"{sch} was not created"

    def test_kicad_sch_starts_correctly(self, tmp_path):
        src = ROOT / "test_circuits" / "rc_filter.ilang"
        if not src.exists():
            pytest.skip("test_circuits/rc_filter.ilang not found")
        sch     = self._run_compiler(src, tmp_path)
        content = sch.read_text()
        assert content.strip().startswith("(kicad_sch"), \
            "Output does not start with (kicad_sch"

    def test_output_contains_symbols(self, tmp_path):
        src = ROOT / "test_circuits" / "rc_filter.ilang"
        if not src.exists():
            pytest.skip("test_circuits/rc_filter.ilang not found")
        content = self._run_compiler(src, tmp_path).read_text()
        assert "(symbol" in content

    def test_output_contains_wires(self, tmp_path):
        src = ROOT / "test_circuits" / "rc_filter.ilang"
        if not src.exists():
            pytest.skip("test_circuits/rc_filter.ilang not found")
        content = self._run_compiler(src, tmp_path).read_text()
        assert "(wire" in content

    def test_output_contains_vin_vout(self, tmp_path):
        src = ROOT / "test_circuits" / "rc_filter.ilang"
        if not src.exists():
            pytest.skip("test_circuits/rc_filter.ilang not found")
        content = self._run_compiler(src, tmp_path).read_text()
        assert "VIN"  in content
        assert "VOUT" in content

    def test_output_contains_gnd(self, tmp_path):
        src = ROOT / "test_circuits" / "rc_filter.ilang"
        if not src.exists():
            pytest.skip("test_circuits/rc_filter.ilang not found")
        content = self._run_compiler(src, tmp_path).read_text()
        assert "GND" in content

    def test_voltage_divider_output_valid(self, tmp_path):
        src = ROOT / "test_circuits" / "voltage_divider.ilang"
        if not src.exists():
            pytest.skip("test_circuits/voltage_divider.ilang not found")
        content = self._run_compiler(src, tmp_path).read_text()
        assert content.strip().startswith("(kicad_sch")
        assert "(wire" in content

    def test_zener_clamp_output_valid(self, tmp_path):
        src = ROOT / "test_circuits" / "zener_clamp.ilang"
        if not src.exists():
            pytest.skip("test_circuits/zener_clamp.ilang not found")
        content = self._run_compiler(src, tmp_path).read_text()
        assert content.strip().startswith("(kicad_sch")
        assert "(wire" in content


# ---------------------------------------------------------------------------
# 5. Plugin runner tests (no KiCad/PyQt5 required)
# ---------------------------------------------------------------------------

class TestPluginRunner:

    def _plugin_root(self) -> Path:
        plugin = ROOT.parent / "icelang_plugin"
        if not plugin.exists():
            pytest.skip("icelang_plugin/ not found alongside icelang/")
        return plugin

    def test_runner_importable(self):
        plugin = self._plugin_root()
        sys.path.insert(0, str(plugin.parent))
        try:
            from icelang_plugin import runner
            assert hasattr(runner, "run")
            assert hasattr(runner, "RunnerError")
        finally:
            sys.path.pop(0)

    def test_runner_finds_compiler(self):
        plugin = self._plugin_root()
        sys.path.insert(0, str(plugin.parent))
        try:
            from icelang_plugin.runner import _find_compiler_root, RunnerError
            os.environ["ICELANG_ROOT"] = str(ROOT)
            found = _find_compiler_root()
            assert found == ROOT
        finally:
            del os.environ["ICELANG_ROOT"]
            sys.path.pop(0)

    def test_runner_rejects_missing_file(self, tmp_path):
        plugin = self._plugin_root()
        sys.path.insert(0, str(plugin.parent))
        try:
            from icelang_plugin.runner import run, RunnerError
            os.environ["ICELANG_ROOT"] = str(ROOT)
            with pytest.raises(RunnerError, match="not found"):
                run(str(tmp_path / "nonexistent.ilang"), str(tmp_path))
        finally:
            del os.environ["ICELANG_ROOT"]
            sys.path.pop(0)

    def test_runner_rejects_wrong_extension(self, tmp_path):
        plugin = self._plugin_root()
        sys.path.insert(0, str(plugin.parent))
        bad_file = tmp_path / "circuit.txt"
        bad_file.write_text("not a circuit")
        try:
            from icelang_plugin.runner import run, RunnerError
            os.environ["ICELANG_ROOT"] = str(ROOT)
            with pytest.raises(RunnerError, match=".ilang"):
                run(str(bad_file), str(tmp_path))
        finally:
            del os.environ["ICELANG_ROOT"]
            sys.path.pop(0)

    def test_runner_compiles_rc_filter(self, tmp_path):
        plugin = self._plugin_root()
        src    = ROOT / "test_circuits" / "rc_filter.ilang"
        if not src.exists():
            pytest.skip("test_circuits/rc_filter.ilang not found")
        sys.path.insert(0, str(plugin.parent))
        try:
            from icelang_plugin.runner import run, RunnerError
            os.environ["ICELANG_ROOT"] = str(ROOT)
            result = run(str(src), str(tmp_path))
            assert "kicad_sch" in result
            assert Path(result["kicad_sch"]).exists()
            assert result["circuit_name"] == "rc_filter"
        finally:
            del os.environ["ICELANG_ROOT"]
            sys.path.pop(0)

    def test_runner_returns_spice_path(self, tmp_path):
        plugin = self._plugin_root()
        src    = ROOT / "test_circuits" / "rc_filter.ilang"
        if not src.exists():
            pytest.skip("test_circuits/rc_filter.ilang not found")
        sys.path.insert(0, str(plugin.parent))
        try:
            from icelang_plugin.runner import run
            os.environ["ICELANG_ROOT"] = str(ROOT)
            result = run(str(src), str(tmp_path))
            assert result["spice_cir"] is not None
            assert Path(result["spice_cir"]).exists()
        finally:
            del os.environ["ICELANG_ROOT"]
            sys.path.pop(0)
