import networkx as nx
import os
import re
import logging
from typing import Dict, List, Any

logger = logging.getLogger(__name__)

class eSimGraphRAG:
    """Directed Knowledge Graph index for eSim component topologies and subcircuit dependencies."""
    
    def __init__(self):
        self.graph = nx.DiGraph()
        self._build_circuit_ontology()

    def _build_circuit_ontology(self):
        """Populates the initial knowledge graph with component rules and subcircuit linkages."""
        # 1. Analog Operational Amplifiers
        self.graph.add_node("LM741", type="OpAmp", pins=8, subcircuit="LM741.sub")
        self.graph.add_edge("LM741", "Dual_Power_Supply", relation="REQUIRES", note="+Vcc (Pin 7), -Vee (Pin 4)")
        self.graph.add_edge("LM741", "LM741.sub", relation="USES_SUBCIRCUIT")
        self.graph.add_edge("LM741", "Bypass_Capacitor", relation="RECOMMENDS", note="0.1uF decoupling on power rails")

        # 2. Timers & Logic ICs
        self.graph.add_node("555_Timer", type="Timer_IC", pins=8, subcircuit="timer555.sub")
        self.graph.add_edge("555_Timer", "timer555.sub", relation="USES_SUBCIRCUIT")
        self.graph.add_edge("555_Timer", "Reset_Pin", relation="REQUIRES", note="Pin 4 must be pulled high if unused")

        # 3. Transistors & Diodes
        self.graph.add_node("BC547", type="BJT_NPN", pins=3, model="QBC547")
        self.graph.add_edge("BC547", "Base_Resistor", relation="REQUIRES", note="Limit base current to prevent saturation damage")
        self.graph.add_edge("BC547", "Emitter_Ground", relation="CONNECTS_TO")

        self.graph.add_node("1N4148", type="Diode", pins=2, model="D1N4148")
        self.graph.add_edge("1N4148", "Flyback_Protection", relation="RECOMMENDS", note="Place anti-parallel across inductive loads")

    def get_topology_context(self, user_query: str) -> str:
        """
        Scans user prompt for component mentions and returns structured topological rules.
        """
        query_upper = user_query.upper()
        extracted_rules = []

        for node in self.graph.nodes():
            clean_node = node.replace("_", " ").upper()
            if node.upper() in query_upper or clean_node in query_upper:
                attrs = self.graph.nodes[node]
                node_type = attrs.get("type", "Component")
                
                rule_str = f"• Component [{node}] ({node_type}):"
                subckt = attrs.get("subcircuit") or attrs.get("model")
                if subckt:
                    rule_str += f" Model File: '{subckt}'."
                
                edges = []
                for _, target, data in self.graph.out_edges(node, data=True):
                    rel = data.get("relation", "CONNECTED")
                    note = data.get("note", "")
                    note_fmt = f" ({note})" if note else ""
                    edges.append(f"{rel} -> {target}{note_fmt}")
                
                if edges:
                    rule_str += " Relationships: " + "; ".join(edges)
                
                extracted_rules.append(rule_str)

        if not extracted_rules:
            return ""

        return "\n[GraphRAG Circuit Topology Context]:\n" + "\n".join(extracted_rules) + "\n"
