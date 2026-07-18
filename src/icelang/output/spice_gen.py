import sys
sys.path.insert(0, '/home/princess/icelang')

from icelang_parser import CktBlock
from component_registry import lookup


def generate(ckt: CktBlock) -> str:
    lines = [f"* {ckt.name}", ""]

    counter = {}
    for comp in ckt.components:
        model  = lookup(comp.type)
        if not model:
            continue
        prefix = model.get("spice_prefix", comp.type[0].upper())
        counter[prefix] = counter.get(prefix, 0) + 1
        ref = f"{prefix}{counter[prefix]}"
        if len(comp.nodes) < 2:
            continue
        lines.append(f"{ref} {comp.nodes[0]} {comp.nodes[1]} {comp.value}")

    if ckt.port_in:
        lines.append("")
        lines.append(
            f"* test source auto-generated for port {ckt.port_in.name}"
        )
        lines.append(
            f"V_test {ckt.port_in.name} gnd PULSE(0 5 0 1n 1n 500u 1m)"
        )

    lines.extend(["", ".tran 1us 10ms", ".end"])
    return "\n".join(lines)


def write(ckt: CktBlock, path: str):
    content = generate(ckt)
    with open(path, "w") as f:
        f.write(content)
    print(f"spice written → {path}")


if __name__ == "__main__":
    from icelang_parser import Component, PortIn, PortOut

    ckt = CktBlock(
        name="rc_filter",
        port_in=PortIn(name="vin"),
        port_out=PortOut(name="vout", node="mc"),
        components=[
            Component(type="res", node1="vin", node2="mc",  value="10k"),
            Component(type="cap", node1="mc",  node2="gnd", value="10F"),
        ]
    )

    print(generate(ckt))
