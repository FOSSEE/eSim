import sys
sys.path.insert(0, '/home/princess/icelang')
sys.path.insert(0, '/home/princess/icelang/intelligent_schematic_layer')

from icelang_parser import CktBlock, Component, PortIn, PortOut
from graph_builder import build
from placement_engine import place
from wire_router import route

ckt = CktBlock(
    name="rc_filter",
    port_in=PortIn(name="vin"),
    port_out=PortOut(name="vout", node="mc"),
    components=[
        Component(type="res", node1="vin", node2="mc",  value="10k"),
        Component(type="cap", node1="mc",  node2="gnd", value="10F"),
    ]
)

G       = build(ckt)
placed  = place(G, ckt)
print("---------> Placed Positions")
for node, coords in placed.items():
    print(f"  {node:10} → {coords}")
edges   = [(u, v, f"{d['component']}_{u}_{v}") for u, v, d in G.edges(data=True)]
routing = route(placed, edges)

print("----------> Wire Segments")
for label, wire in routing["wires"].items():
    print(f" {label}")
    print(f"    {wire['from']} → {wire['to']}")
    if wire.get("error"):
        print(f"    ERROR: {wire['error']}")
    else:
        for seg in wire["segments"]:
            print(f"    {seg[0]} → {seg[1]}")

print("-------->Junctions")
if routing["junctions"]:
    for j in routing["junctions"]:
        print(f"  junction at {j}")
else:
    print("no junctions in this circuit")
