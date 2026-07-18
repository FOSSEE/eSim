import re
import os

KICAD_SYM_PATHS = [
    "/usr/share/kicad/symbols",
    "/usr/local/share/kicad/symbols",
    os.path.expanduser("~/.local/share/kicad/9.0/symbols"),
]

_cache = {}


def find_lib(lib_name: str) -> str:
    for base in KICAD_SYM_PATHS:
        path = os.path.join(base, f"{lib_name}.kicad_sym")
        if os.path.exists(path):
            return path
    return None


def _extract_sym_block(content: str, sym_name: str) -> str:
    target = f'(symbol "{sym_name}"'
    start  = content.find(target)
    if start == -1:
        return None
    depth = 0
    i     = start
    while i < len(content):
        if content[i] == "(":
            depth += 1
        elif content[i] == ")":
            depth -= 1
            if depth == 0:
                return content[start:i+1]
        i += 1
    return None


def get_pin_offsets(kicad_symbol: str) -> dict:
    if kicad_symbol in _cache:
        return _cache[kicad_symbol]

    if ":" not in kicad_symbol:
        _cache[kicad_symbol] = {}
        return {}

    lib_name, sym_name = kicad_symbol.split(":", 1)
    lib_path = find_lib(lib_name)
    if not lib_path:
        _cache[kicad_symbol] = {}
        return {}

    with open(lib_path) as f:
        content = f.read()

    sym_block = _extract_sym_block(content, sym_name)
    if not sym_block:
        _cache[kicad_symbol] = {}
        return {}

    pins = re.findall(
        r'\(pin\s+\w+\s+\w+\s+\(at\s+([-\d.]+)\s+([-\d.]+)\s+\d+\)'
        r'.*?\(name\s+"([^"]+)"',
        sym_block, re.DOTALL
    )

    result = {}
    for x, y, name in pins:
        clean = name.strip("~")
        if clean and clean not in result:
            result[clean] = (float(x), float(y))

    if not result and pins:
        for i, (x, y, _) in enumerate(pins):
            result[str(i+1)] = (float(x), float(y))

    _cache[kicad_symbol] = result
    return result


def get_pin_offset_by_index(kicad_symbol: str, index: int) -> tuple:
    from component_registry import lookup
    entry   = lookup(kicad_symbol.split(":")[-1]) or {}
    offsets = get_pin_offsets(kicad_symbol)
    pin_names = entry.get("pin_names", list(offsets.keys()))
    if index < len(pin_names):
        name = pin_names[index]
        return offsets.get(name, (0, 0))
    return (0, 0)


if __name__ == "__main__":
    from component_registry import load
    reg  = load()
    seen = set()
    for name, entry in reg.items():
        sym = entry.get("kicad_symbol", "")
        if sym in seen or not sym:
            continue
        seen.add(sym)
        offsets = get_pin_offsets(sym)
        status  = "ok" if offsets else "no pins"
        print(f"  {sym:45} {status}: {offsets}")
