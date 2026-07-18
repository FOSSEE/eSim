import json
import os

REGISTRY_PATH = os.path.join(os.path.dirname(__file__), "registry.json")

_registry = None


def load() -> dict:
    global _registry
    if _registry is None:
        with open(REGISTRY_PATH) as f:
            data = json.load(f)

        _registry = {}
        for canonical_name, entry in data.items():
            _registry[canonical_name.lower()] = entry
            for alias in entry.get("aliases", []):
                _registry[alias.lower()] = entry

    return _registry


def lookup(name: str) -> dict:
    reg = load()
    result = reg.get(name.lower())
    return result


def register(name: str, kicad_symbol: str,
             spice_prefix: str, pin_count: int,
             pin_names: list, aliases: list = None,
             signal_pin: str = None):
    reg = load()
    entry = {
        "kicad_symbol": kicad_symbol,
        "spice_prefix":  spice_prefix,
        "pin_count":     pin_count,
        "pin_names":     pin_names,
        "aliases":       aliases or []
    }
    if signal_pin:
        entry["signal_pin"] = signal_pin
    reg[name.lower()] = entry
    for alias in (aliases or []):
        reg[alias.lower()] = entry

    with open(REGISTRY_PATH) as f:
        data = json.load(f)
    data[name] = entry
    with open(REGISTRY_PATH, "w") as f:
        json.dump(data, f, indent=2)

    print(f"registered {name} → {kicad_symbol}")


if __name__ == "__main__":
    reg = load()
    print(f"registry has {len(set(e['kicad_symbol'] for e in reg.values()))} unique components")
    print(f"total names + aliases: {len(reg)}")
    for name, entry in sorted(reg.items()):
        print(f"  {name:20} → {entry['kicad_symbol']}")
