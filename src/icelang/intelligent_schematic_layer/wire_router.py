import heapq
from collections import Counter

GRID_SCALE = 4
SHEET_W_MM = 297
SHEET_H_MM = 210
GRID_W = SHEET_W_MM * GRID_SCALE
GRID_H = SHEET_H_MM * GRID_SCALE


def world_to_grid(x, y):
    col = int(round(x * GRID_SCALE))
    row = int(round(y * GRID_SCALE))
    col = max(0, min(GRID_W - 1, col))
    row = max(0, min(GRID_H - 1, row))
    return col, row


def grid_to_world(col, row):
    return round(col / GRID_SCALE, 4), round(row / GRID_SCALE, 4)


def astar(grid, start, goal):
    if start == goal:
        return [start]

    def heuristic(a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    open_set = []
    heapq.heappush(open_set, (0, start))
    came_from = {}
    g_score = {start: 0}

    while open_set:
        _, current = heapq.heappop(open_set)
        if current == goal:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.append(start)
            return list(reversed(path))

        col, row = current
        for dc, dr in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nb = (col + dc, row + dr)
            nc, nr = nb
            if not (0 <= nc < GRID_W and 0 <= nr < GRID_H):
                continue
            if grid.get(nb):
                continue
            new_g = g_score[current] + 1
            if new_g < g_score.get(nb, float("inf")):
                came_from[nb] = current
                g_score[nb] = new_g
                f = new_g + heuristic(nb, goal)
                heapq.heappush(open_set, (f, nb))

    return []


def path_to_segments(path):
    if len(path) < 2:
        return []
    segments = []
    seg_start = grid_to_world(*path[0])
    for i in range(1, len(path)):
        if i == len(path) - 1:
            segments.append((seg_start, grid_to_world(*path[i])))
        else:
            prev_dir = (path[i][0]-path[i-1][0], path[i][1]-path[i-1][1])
            next_dir = (path[i+1][0]-path[i][0], path[i+1][1]-path[i][1])
            if prev_dir != next_dir:
                segments.append((seg_start, grid_to_world(*path[i])))
                seg_start = grid_to_world(*path[i])
    return segments


def find_junctions(all_paths):
    pts = []
    for p in all_paths:
        pts.extend(p)
    counts = Counter(pts)
    return [pt for pt, c in counts.items() if c >= 3]


def route_nets(net_pins):
    """
    net_pins: { net_name: [(x_mm, y_mm), ...] }  KiCad mm coordinates
    routes as star topology from first pin to all others per net.
    returns: { "wires": [((x1,y1),(x2,y2)), ...], "junctions": [(x,y), ...] }
    """
    grid     = {}
    all_segs = []
    all_paths = []

    for net, pins in net_pins.items():
        if len(pins) < 2:
            continue

        # star anchor
        anchor = pins[0]
        anchor_cell = world_to_grid(*anchor)

        for p in pins[1:]:
            if p == anchor:
                continue
            goal = world_to_grid(*p)
            path = astar(grid, anchor_cell, goal)
            if not path:
                continue
            for pt in path[1:-1]:
                grid[pt] = True
            segs = path_to_segments(path)
            all_segs.extend(segs)
            all_paths.append([grid_to_world(*pt) for pt in path])

    # deduplicate segments
    seen = set()
    unique = []
    for seg in all_segs:
        (x1,y1),(x2,y2) = seg
        key = (round(x1,2),round(y1,2),round(x2,2),round(y2,2))
        rev = (key[2],key[3],key[0],key[1])
        if key not in seen and rev not in seen:
            seen.add(key)
            unique.append(seg)

    junctions = find_junctions(all_paths)
    return {"wires": unique, "junctions": junctions}


# for backward compatibility
def route(placed, edges):
    net_pins = {}
    for node, pos in placed.items():
        net_pins[node] = [pos]
    return route_nets(net_pins)
