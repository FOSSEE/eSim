import sys
import os
import uuid
sys.path.insert(0, '/home/princess/icelang')

from icelang_parser import CktBlock
from component_registry import lookup as _reg_lookup
from pin_reader import get_pin_offsets as _get_pin_offsets

SHEET_CENTRE_X = 150.0
SHEET_CENTRE_Y = 100.0
SCALE          = 5.0
SHEET_UUID     = str(uuid.uuid4())
PIN_HALF       = 3.81

KICAD_SYM_PATHS = [
    "/usr/share/kicad/symbols",
    "/usr/local/share/kicad/symbols",
    os.path.expanduser("~/.local/share/kicad/9.0/symbols"),
    os.path.expanduser("~/.local/share/kicad/symbols"),
]

THREE_TERMINAL = {"bjt_npn", "bjt_pnp", "jfet_n", "jfet_p"}
FOUR_TERMINAL  = {"nmos", "pmos"}

DRIVER_TYPES = {"vsource", "isource", "vdc", "vac", "vpulse", "idc",
                "voltage_source", "current_source", "v", "i"}
POWER_NODES  = {"gnd", "vcc", "vdd", "vdd3v3", "vdd5v"}


def _uid():
    return str(uuid.uuid4())


def _scale(x, y):
    sx = round(SHEET_CENTRE_X + x * SCALE, 4)
    sy = round(SHEET_CENTRE_Y - y * SCALE, 4)
    return sx, sy


def find_kicad_lib(lib_name):
    for base in KICAD_SYM_PATHS:
        path = os.path.join(base, f"{lib_name}.kicad_sym")
        if os.path.exists(path):
            return path
    return None


def extract_symbol(lib_name, sym_name):
    path = find_kicad_lib(lib_name)
    if not path:
        print(f"  WARNING: library {lib_name} not found")
        return None
    with open(path) as f:
        content = f.read()
    target = f'(symbol "{sym_name}"'
    start  = content.find(target)
    if start == -1:
        print(f"  WARNING: {sym_name} not found in {lib_name}")
        return None
    depth = 0
    i     = start
    while i < len(content):
        if content[i] == "(":
            depth += 1
        elif content[i] == ")":
            depth -= 1
            if depth == 0:
                sym       = content[start:i+1]
                full_name = f"{lib_name}:{sym_name}"
                sym = sym.replace(
                    f'(symbol "{sym_name}"',
                    f'(symbol "{full_name}"',
                    1
                )
                return "\n".join("    " + l for l in sym.splitlines())
        i += 1
    return None


def build_lib_symbols(comp_types, needs_gnd):
    parts = []
    seen  = set()
    for ct in comp_types:
        if ct in seen:
            continue
        entry = _reg_lookup(ct)
        if not entry:
            continue
        lib_id = entry.get("kicad_symbol", "")
        if ":" not in lib_id:
            continue
        lib, sym = lib_id.split(":", 1)
        s = extract_symbol(lib, sym)
        if s:
            parts.append(s)
            seen.add(ct)
            print(f"  embedded {lib}:{sym}")
    if needs_gnd:
        s = extract_symbol("power", "GND")
        if s:
            parts.append(s)
            print("  embedded power:GND")
    if not parts:
        return "  (lib_symbols)"
    return "  (lib_symbols\n" + "\n".join(parts) + "\n  )"


def pin_positions(kx, ky, rotation):
    if rotation == 0:
        return (kx, ky - PIN_HALF), (kx, ky + PIN_HALF)
    else:
        return (kx - PIN_HALF, ky), (kx + PIN_HALF, ky)


def closer_pin(n_kx, n_ky, pin_a, pin_b):
    da = (pin_a[0]-n_kx)**2 + (pin_a[1]-n_ky)**2
    db = (pin_b[0]-n_kx)**2 + (pin_b[1]-n_ky)**2
    return (pin_a, pin_b) if da <= db else (pin_b, pin_a)


def manhattan_wires(x1, y1, x2, y2):
    segs = []
    if abs(x1-x2) < 0.01 and abs(y1-y2) < 0.01:
        return segs
    if abs(x1-x2) < 0.01:
        segs.append((x1, y1, x2, y2))
    elif abs(y1-y2) < 0.01:
        segs.append((x1, y1, x2, y2))
    else:
        segs.append((x1, y1, x2, y1))
        segs.append((x2, y1, x2, y2))
    return segs


def _wire(x1, y1, x2, y2):
    return f"""  (wire
    (pts (xy {x1} {y1}) (xy {x2} {y2}))
    (stroke (width 0) (type default))
    (uuid "{_uid()}")
  )"""


def _junction(x, y):
    return (f'  (junction (at {x} {y}) '
            f'(diameter 0) (color 0 0 0 0) (uuid "{_uid()}"))')


def _placed_symbol(lib_id, ref, x, y, value, rotation=0):
    return f"""  (symbol
    (lib_id "{lib_id}")
    (at {x} {y} {rotation})
    (unit 1)
    (in_bom yes)
    (on_board yes)
    (uuid "{_uid()}")
    (property "Reference" "{ref}"
      (at {round(x+2.032,4)} {round(y-1.0,4)} 0)
      (effects (font (size 1.27 1.27)))
    )
    (property "Value" "{value}"
      (at {round(x-2.032,4)} {round(y-1.0,4)} 0)
      (effects (font (size 1.27 1.27)))
    )
    (property "Footprint" "" (at 0 0 0)
      (effects (font (size 1.27 1.27)) hide)
    )
    (property "Datasheet" "~" (at 0 0 0)
      (effects (font (size 1.27 1.27)) hide)
    )
    (instances
      (project "schematic"
        (path "/{SHEET_UUID}"
          (reference "{ref}")
          (unit 1)
        )
      )
    )
  )"""


def _gnd_symbol(ref, x, y):
    return f"""  (symbol
    (lib_id "power:GND")
    (at {x} {y} 0)
    (unit 1)
    (in_bom yes)
    (on_board yes)
    (uuid "{_uid()}")
    (property "Reference" "{ref}"
      (at {x} {round(y+6.35,4)} 0)
      (effects (font (size 1.27 1.27)) hide)
    )
    (property "Value" "GND"
      (at {x} {round(y+3.81,4)} 0)
      (effects (font (size 1.27 1.27)))
    )
    (property "Footprint" "" (at 0 0 0)
      (effects (font (size 1.27 1.27)) hide)
    )
    (property "Datasheet" "" (at 0 0 0)
      (effects (font (size 1.27 1.27)) hide)
    )
    (instances
      (project "schematic"
        (path "/{SHEET_UUID}"
          (reference "{ref}")
          (unit 1)
        )
      )
    )
  )"""


def _net_label(name, x, y):
    return f"""  (label "{name}"
    (at {x} {y} 0)
    (fields_autoplaced yes)
    (effects (font (size 1.27 1.27)) (justify left))
    (uuid "{_uid()}")
  )"""


def _place_two_terminal(comp, comp_idx, placed, lib_id, ref, blocks, wire_segs):
    node1 = comp.nodes[0] if len(comp.nodes) > 0 else "vin"
    node2 = comp.nodes[1] if len(comp.nodes) > 1 else "gnd"

    is_driver = comp.type.lower() in DRIVER_TYPES

    if is_driver:
        if node2 in POWER_NODES:
            pos_node, neg_node = node1, node2
        elif node1 in POWER_NODES:
            pos_node, neg_node = node2, node1
        else:
            pos_node, neg_node = node1, node2

        neg_key = f"{neg_node}_driver_{comp_idx}"
        raw_x1, raw_y1 = placed.get(pos_node, (0.0, 0.0))
        raw_x2, raw_y2 = placed.get(neg_key, placed.get(neg_node, (0.0, -6.35)))
    else:
        shunt_key1 = f"{node1}_shunt_{comp_idx}"
        shunt_key2 = f"{node2}_shunt_{comp_idx}"
        n1_lookup  = shunt_key1 if shunt_key1 in placed else node1
        n2_lookup  = shunt_key2 if shunt_key2 in placed else node2
        raw_x1, raw_y1 = placed.get(n1_lookup, (0.0, 0.0))
        raw_x2, raw_y2 = placed.get(n2_lookup, (0.0, 0.0))

    mid_x = (raw_x1 + raw_x2) / 2
    mid_y = (raw_y1 + raw_y2) / 2
    kx, ky   = _scale(mid_x, mid_y)
    dx = abs(raw_x2 - raw_x1)
    dy = abs(raw_y2 - raw_y1)
    rotation = 90 if dx > dy else 0

    pa, pb = pin_positions(kx, ky, rotation)
    n1_kx, n1_ky = _scale(raw_x1, raw_y1)
    n2_kx, n2_ky = _scale(raw_x2, raw_y2)
    node1_pin, node2_pin = closer_pin(n1_kx, n1_ky, pa, pb)

    blocks.append(_placed_symbol(lib_id, ref, kx, ky, comp.value, rotation))

    for seg in manhattan_wires(n1_kx, n1_ky, node1_pin[0], node1_pin[1]):
        wire_segs.append(seg)
    for seg in manhattan_wires(n2_kx, n2_ky, node2_pin[0], node2_pin[1]):
        wire_segs.append(seg)


def generate(ckt: CktBlock, placed: dict, routing: dict) -> str:
    from intelligent_schematic_layer.graph_builder import build
    from intelligent_schematic_layer.placement_engine import place
    from intelligent_schematic_layer.wire_router import route

    G      = build(ckt)
    placed = place(G, ckt)
    edges  = [(u, v, f"{d['component']}_{u}_{v}")
              for u, v, d in G.edges(data=True)]
    routing = route(placed, edges)

    blocks     = []
    wire_segs  = []
    comp_types = [c.type for c in ckt.components]

    needs_gnd = any(
        k == "gnd" or k.startswith("gnd_shunt_") or k.startswith("gnd_driver_")
        for k in placed
    )

    blocks.append('(kicad_sch')
    blocks.append('  (version 20240101)')
    blocks.append('  (generator "icelang")')
    blocks.append('  (generator_version "1.0")')
    blocks.append('  (paper "A4")')
    blocks.append(f'  (title_block (title "{ckt.name}"))')
    blocks.append(build_lib_symbols(comp_types, needs_gnd))

    counter = {}

    for comp in ckt.components:
        entry  = _reg_lookup(comp.type)
        if not entry:
            continue
        lib_id = entry.get("kicad_symbol", "")
        if not lib_id:
            continue
        prefix = entry.get("spice_prefix", comp.type[0].upper())
        counter[prefix] = counter.get(prefix, 0) + 1
        ref      = f"{prefix}{counter[prefix]}"
        comp_idx = ckt.components.index(comp)

        if comp.type in THREE_TERMINAL or comp.type in FOUR_TERMINAL:
            offsets        = _get_pin_offsets(lib_id)
            pin_names      = entry.get("pin_names", [])
            node_positions = [placed.get(n, (0.0, 0.0)) for n in comp.nodes]
            mid_x = sum(p[0] for p in node_positions) / len(node_positions)
            mid_y = sum(p[1] for p in node_positions) / len(node_positions)
            kx, ky = _scale(mid_x, mid_y)
            blocks.append(_placed_symbol(lib_id, ref, kx, ky, comp.value, 0))
            for i, node in enumerate(comp.nodes):
                if i >= len(pin_names):
                    break
                pname      = pin_names[i]
                off        = offsets.get(pname, (0, 0))
                pin_kx     = round(kx + off[0], 4)
                pin_ky     = round(ky + off[1], 4)
                n_kx, n_ky = _scale(*placed.get(node, (0.0, 0.0)))
                for seg in manhattan_wires(n_kx, n_ky, pin_kx, pin_ky):
                    wire_segs.append(seg)
        else:
            _place_two_terminal(comp, comp_idx, placed, lib_id, ref,
                                blocks, wire_segs)

    gnd_counter          = 0
    placed_gnd_positions = set()

    for key, (raw_x, raw_y) in placed.items():
        is_gnd_key = (
            key == "gnd"
            or key.startswith("gnd_shunt_")
            or key.startswith("gnd_driver_")
        )
        if is_gnd_key:
            kx, ky  = _scale(raw_x, raw_y)
            pos_key = (round(kx, 1), round(ky, 1))
            if pos_key not in placed_gnd_positions:
                placed_gnd_positions.add(pos_key)
                gnd_counter += 1
                blocks.append(_gnd_symbol(f"#PWR0{gnd_counter}", kx, ky))

    print(f"port_in node: {ckt.port_in.name}, placed at: {placed.get(ckt.port_in.name)}")
    print(f"port_out node: {ckt.port_out.node}, placed at: {placed.get(ckt.port_out.node)}")
    print(f"full placed dict: {placed}")

    if ckt.port_in:
        node = ckt.port_in.name
        if node in placed:
            raw_x, raw_y = placed[node]
            kx, ky = _scale(raw_x, raw_y)
            blocks.append(_net_label("VIN", kx, ky))

    if ckt.port_out and ckt.port_out.node:
        node = ckt.port_out.node
        if node in placed:
            raw_x, raw_y = placed[node]
            kx, ky = _scale(raw_x, raw_y)
            blocks.append(_net_label("VOUT", kx, ky))

    seen_segs = set()
    for seg in wire_segs:
        key = (round(seg[0], 2), round(seg[1], 2),
               round(seg[2], 2), round(seg[3], 2))
        rev = (key[2], key[3], key[0], key[1])
        if key not in seen_segs and rev not in seen_segs:
            seen_segs.add(key)
            blocks.append(_wire(*seg))

    blocks.append("""  (sheet_instances
    (path "/"
      (page "1")
    )
  )""")
    blocks.append(')')
    return '\n\n'.join(blocks)


def write(ckt, placed, routing, path):
    content = generate(ckt, placed, routing)
    with open(path, "w") as f:
        f.write(content)
    print(f"kicad schematic written -> {path}")
