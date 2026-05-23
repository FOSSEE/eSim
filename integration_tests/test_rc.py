import pytest

from utils.simulator import run_ngspice


circuits = [
    "rc.cir",
    "rl.cir",
    "rlc.cir"
]


@pytest.mark.parametrize("circuit", circuits)
def test_circuit_simulation(circuit):

    result = run_ngspice(f"testcases/{circuit}")

    assert result.returncode == 0

    assert "No. of Data Rows" in result.stdout

    assert "Simulation executed from .control section" in result.stdout