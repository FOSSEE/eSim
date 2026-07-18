import networkx as nx

GRID           = 2.54
SERIES_SPACING = 5.08    # world units between series nodes  (~25mm KiCad)
SHUNT_DEPTH    = -6.35   # world units below signal path     (~32mm KiCad)
SHUNT_X_GAP    = 5.08    # world units between parallel shunts
DRIVER_OFFSET  = -7.62   # world units LEFT of VIN for voltage/current sources
POWER_NODES    = {"gnd", "vcc", "vdd", "vdd3v3", "vdd5v"}

DRIVER_TYPES = {"vsource", "isource", "vdc", "vac", "vpulse", "idc",
                "voltage_source", "current_source", "v", "i"}


def _classify(ckt):
    series  = []
    shunts  = {}
    drivers = []

    for i, comp in enumerate(ckt.components):
        if len(comp.nodes) < 2:
            continue

        if comp.type.lower() in DRIVER_TYPES:
            drivers.append(i)
            continue

        n1, n2 = comp.nodes[0], comp.nodes[1]
        p1 = n1 in POWER_NODES
        p2 = n2 in POWER_NODES

        if p1 and p2:
            shunts.setdefault(n1, []).append(i)
        elif p1:
            shunts.setdefault(n2, []).append(i)
        elif p2:
            shunts.setdefault(n1, []).append(i)
        else:
            series.append(i)

    return series, shunts, drivers


def _trace_signal_path(ckt, series_indices):
    port_in = ckt.port_in.name if ckt.port_in else None

    adj = {}
    for i in series_indices:
        comp = ckt.components[i]
        if len(comp.nodes) < 2:
            continue
        n1, n2 = comp.nodes[0], comp.nodes[1]
        adj.setdefault(n1, []).append(n2)
        adj.setdefault(n2, []).append(n1)

    if not port_in or port_in not in adj:
        nodes = []
        for i in series_indices:
            comp = ckt.components[i]
            for n in comp.nodes:
                if n not in nodes and n not in POWER_NODES:
                    nodes.append(n)
        return nodes

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
    series, shunts, drivers = _classify(ckt)
    path = _trace_signal_path(ckt, series)

    placed = {}

    for idx, node in enumerate(path):
        placed[node] = (idx * SERIES_SPACING, 0.0)

    for i in series:
        comp = ckt.components[i]
        for n in comp.nodes:
            if n not in placed and n not in POWER_NODES:
                placed[n] = (len(placed) * SERIES_SPACING, 0.0)

    for sig_node, comp_indices in shunts.items():
        if sig_node not in placed:
            placed[sig_node] = (0.0, 0.0)
        sx, sy = placed[sig_node]
        n_shunts = len(comp_indices)

        for k, ci in enumerate(comp_indices):
            comp       = ckt.components[ci]
            n1, n2     = comp.nodes[0], comp.nodes[1]
            power_node = n1 if n1 in POWER_NODES else n2

            x_off   = (k - (n_shunts - 1) / 2.0) * SHUNT_X_GAP
            pwr_pos = (round(sx + x_off, 4), round(sy + SHUNT_DEPTH, 4))

            unique_key = f"{power_node}_shunt_{ci}"
            placed[unique_key] = pwr_pos

            if power_node not in placed:
                placed[power_node] = pwr_pos

    vin_x = placed.get(path[0], (0.0, 0.0))[0] if path else 0.0

    for k, ci in enumerate(drivers):
        comp   = ckt.components[ci]
        n1, n2 = comp.nodes[0], comp.nodes[1]

        drv_x = vin_x + DRIVER_OFFSET - k * SHUNT_X_GAP

        if n2 in POWER_NODES:
            pos_node, neg_node = n1, n2
        elif n1 in POWER_NODES:
            pos_node, neg_node = n2, n1
        else:
            pos_node, neg_node = n1, n2

        placed[pos_node] = (vin_x, 0.0)

        neg_key = f"{neg_node}_driver_{ci}"
        placed[neg_key] = (drv_x, SHUNT_DEPTH)
        if neg_node not in placed:
            placed[neg_node] = (drv_x, SHUNT_DEPTH)

    snapped = {}
    for node, (x, y) in placed.items():
        gx = round(x / GRID) * GRID
        gy = round(y / GRID) * GRID
        snapped[node] = (round(gx, 4), round(gy, 4))

    return snapped


def place_components(ckt):
    from intelligent_schematic_layer.graph_builder import build
    G      = build(ckt)
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
