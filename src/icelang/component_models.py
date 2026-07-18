MODELS = {
    "res": {
        "kicad_symbol": "Device:R",
        "pins": {"1": "node1", "2": "node2"},
        "spice_prefix": "R"
    },
    "cap": {
        "kicad_symbol": "Device:C",
        "pins": {"1": "node1", "2": "node2"},
        "spice_prefix": "C"
    },
    "ind": {
        "kicad_symbol": "Device:L",
        "pins": {"1": "node1", "2": "node2"},
        "spice_prefix": "L"
    },
    "diode": {
        "kicad_symbol": "Device:D",
        "pins": {"A": "node1", "K": "node2"},
        "spice_prefix": "D"
    },
    "bjt": {
        "kicad_symbol": "Device:Q_NPN_BCE",
        "pins": {"B": "node1", "C": "node2", "E": "node3"},
        "spice_prefix": "Q"
    },
    "mos": {
        "kicad_symbol": "Device:NMOS",
        "pins": {"G": "node1", "D": "node2", "S": "node3", "B": "node3"},
        "spice_prefix": "M"
    },
    "vol": {
        "kicad_symbol": "Device:Battery",
        "pins": {"+": "node1", "-": "node2"},
        "spice_prefix": "V"
    },
}


def get(comp_type: str) -> dict:
    model = MODELS.get(comp_type.lower())
    if not model:
        raise ValueError(f"unknown component type: {comp_type}")
    return model
