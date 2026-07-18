import networkx as nx

GRID           = 2.54
SERIES_SPACING = 5.08   # world units between series nodes  (~25mm KiCad)
SHUNT_DEPTH    = -6.35  # world units below signal path     (~32mm KiCad)
SHUNT_X_GAP    = 5.08   # world units between parallel shunts
POWER_NODES    = {"gnd", "vcc", "vdd", "vdd3v3", "vdd5v"}


def _classify(ckt):
    series = []
    shunts = {}   # signal_node -> [comp_index, ...]

    for i, comp in enumerate(ckt.components):
        if len(comp.nodes) < 2:
            continue
        n1, n2 = comp.nodes[0], comp.nodes[1]
        p1 = n1 in POWER_NODES
        p2 = n2 in POWER_NODES

        if p1 and p2:
            # vol Vcc gnd ... -- both power nodes, treat as shunt at n1
            shunts.setdefault(n1, []).append(i)
        elif p1:
            shunts.setdefault(n2, []).append(i)
        elif p2:
            shunts.setdefault(n1, []).append(i)
        else:
            series.append(i)

    return series, shunts


def _trace_signal_path(ckt, series_indices):
    port_in = ckt.port_in.name if ckt.port_in else None
    if not port_in:
        nodes = []
        for i in series_indices:
            comp = ckt.components[i]
            for n in comp.nodes:
                if n not in nodes:
                    nodes.append(n)
        return nodes

    # build adjacency from series components only
    adj = {}
    for i in series_indices:
        comp = ckt.components[i]
        if len(comp.nodes) < 2:
            continue
        n1, n2 = comp.nodes[0], comp.nodes[1]
        adj.setdefault(n1, []).append(n2)
        adj.setdefault(n2, []).append(n1)

    # BFS from port_in
    path    = [port_in]
    visited = {port_in}
    current = port_in
    while True:
        neighbors = [n for n in adj.get(current, [])
                     if n not in visited and n not in POWER_NODES]
        if not neighbors:
            break
        nxt = neighbors[0]
        path.append(nxt)
        visited.add(nxt)
        current = nxt

    return path


def place(G, ckt) -> dict:
    series, shunts = _classify(ckt)
    path = _trace_signal_path(ckt, series)

    placed = {}

    # place signal path nodes horizontally
    for idx, node in enumerate(path):
        placed[node] = (idx * SERIES_SPACING, 0.0)

    # any series nodes not on the traced path
    for i in series:
        comp = ckt.components[i]
        for n in comp.nodes:
            if n not in placed and n not in POWER_NODES:
                placed[n] = (len(placed) * SERIES_SPACING, 0.0)

    # place shunt components below their signal node
    for sig_node, comp_indices in shunts.items():
        if sig_node not in placed:
            placed[sig_node] = (0.0, 0.0)
        sx, sy = placed[sig_node]
        n_shunts = len(comp_indices)

        for k, ci in enumerate(comp_indices):
            comp = ckt.components[ci]
            n1, n2 = comp.nodes[0], comp.nodes[1]
            power_node = n1 if n1 in POWER_NODES else n2

            # space parallel shunts symmetrically around signal node
            x_off = (k - (n_shunts - 1) / 2.0) * SHUNT_X_GAP
            gnd_pos = (round(sx + x_off, 4), round(sy + SHUNT_DEPTH, 4))

            # use a unique key if multiple shunts share the same power node
            unique_key = f"{power_node}_shunt_{ci}"
            placed[unique_key] = gnd_pos

            # also keep the canonical power node at average position
            if power_node not in placed:
                placed[power_node] = gnd_pos

    # snap to grid
    snapped = {}
    for node, (x, y) in placed.items():
        sx = round(x / GRID) * GRID
        sy = round(y / GRID) * GRID
        snapped[node] = (round(sx, 4), round(sy, 4))

    return snapped


def place_components(ckt):
    from intelligent_schematic_layer.graph_builder import build
    G = build(ckt)
    placed = place(G, ckt)
    positions = {}
    for i, comp in enumerate(ckt.components):
        if comp.nodes:
            positions[i] = placed.get(comp.nodes[0], (0.0, 0.0))
    net_map = {}
    for i, comp in enumerate(ckt.components):
        for node in comp.nodes:
            net_map.setdefault(node, []).append(i)
    return positions, net_map
