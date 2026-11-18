#!/usr/bin/env python3
"""Plot the real ngspice transient output captured from the RC deck."""
import sys
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

src, out = sys.argv[1], sys.argv[2]
t, v = [], []
with open(src) as fh:
    for line in fh:
        parts = line.split()
        if len(parts) < 2:
            continue
        nums = []
        for p in parts:
            try:
                nums.append(float(p))
            except ValueError:
                nums = []
                break
        if len(nums) == 3:          # index time value
            _, tt, vv = nums
        elif len(nums) == 2:        # time value
            tt, vv = nums
        else:
            continue
        t.append(tt * 1e3)   # ms
        v.append(vv)

fig, ax = plt.subplots(figsize=(9, 4.5), dpi=140)
ax.plot(t, v, color="#1f77b4", linewidth=2)
ax.set_xlabel("time (ms)")
ax.set_ylabel("V(out) (V)")
ax.set_title("ngspice 44.2 transient simulation on Ubuntu 25.04\n"
             "RC low-pass, 1 kΩ / 1 µF, 5 V step input",
             fontsize=11)
ax.grid(True, alpha=0.3)
ax.set_ylim(-0.3, 5.3)
fig.tight_layout()
fig.savefig(out)
print(f"wrote {out} from {len(t)} ngspice sample points")
