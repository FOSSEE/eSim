import networkx as nx
import matplotlib.pyplot as plt
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from icelang_parser import CktBlock, Component


def build(ckt: CktBlock) -> nx.Graph:
    G = nx.Graph()

    for comp in ckt.components:
        if len(comp.nodes) < 2:
            continue
        G.add_node(
            comp.nodes[0],
            node_type="signal" if comp.nodes[0] == "vin" else "internal"
        )
        G.add_node(
            comp.nodes[1],
            node_type="ground" if comp.nodes[1] == "gnd" else "internal"
        )
        G.add_edge(
            comp.nodes[0],
            comp.nodes[1],
            component=comp.type,
            value=comp.value,
            ref=f"{comp.type}_{comp.nodes[0]}_{comp.nodes[1]}"
        )

    if ckt.port_in:
        if ckt.port_in.name in G.nodes:
            G.nodes[ckt.port_in.name]["node_type"] = "port_in"

    if ckt.port_out and ckt.port_out.node:
        if ckt.port_out.node in G.nodes:
            G.nodes[ckt.port_out.node]["node_type"] = "port_out"

    return G


def visualise(G: nx.Graph, title: str = "Circuit Graph", save_path: str = None):
    color_map = {
        "port_in":  "#4CAF50",
        "port_out": "#2196F3",
        "ground":   "#F44336",
        "internal": "#9E9E9E",
        "signal":   "#4CAF50"
    }

    colors = [
        color_map.get(G.nodes[n].get("node_type", "internal"), "#9E9E9E")
        for n in G.nodes
    ]

    edge_labels = {
        (u, v): f"{d['component']}\n{d['value']}"
        for u, v, d in G.edges(data=True)
    }

    pos = nx.spring_layout(G, seed=42)

    plt.figure(figsize=(8, 5))
    nx.draw(G, pos,
            with_labels=True,
            node_color=colors,
            node_size=1800,
            font_size=10,
            font_weight="bold",
            edge_color="#555555",
            width=2)
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=8)
    plt.title(title)

    if save_path:
        plt.savefig(save_path, dpi=150, bbox_inches="tight")
        print(f"graph saved → {save_path}")
    else:
        plt.show()

    plt.close()


if __name__ == "__main__":
    from icelang_parser import (
        CktBlock, Component, PortIn, PortOut
    )

    ckt = CktBlock(
        name="rc_filter",
        port_in=PortIn(name="vin"),
        port_out=PortOut(name="vout", node="mc"),
        components=[
            Component(type="res", node1="vin", node2="mc", value="10k"),
            Component(type="cap", node1="mc",  node2="gnd", value="10F"),
        ]
    )

    G = build(ckt)

    print("------> Graph Nodes")
    for node, data in G.nodes(data=True):
        print(f"  {node:10} → {data}")

    print("------>Graph Edges")
    for u, v, data in G.edges(data=True):
        print(f"  {u} ── {v}  [{data['component']} {data['value']}]")

    print(f" nodes : {G.number_of_nodes()}")
    print(f"  edges : {G.number_of_edges()}")

    import pathlib
    output_path = pathlib.Path(__file__).parent.parent / "intelligent_schematic_layer" / "rc_filter_graph.png"
    visualise(G, title="rc_filter", save_path=str(output_path))
