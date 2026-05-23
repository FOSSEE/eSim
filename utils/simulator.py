import subprocess


def run_ngspice(netlist):

    result = subprocess.run(
        ["ngspice", "-b", netlist],
        capture_output=True,
        text=True
    )

    return result