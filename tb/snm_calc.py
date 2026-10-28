"""
Butterfly-curve SNM post-processor for the SRAM testbench.

Reads the wrdata files written by sram_tb.spice:
    snm_<mode>_<cell>.txt   columns: sweep, v(qb1), v(q2)      (wr_singlescale)
    (5-column files, i.e. scale repeated per vector, are also accepted)

Curve A (cell 1, Q forced by the sweep):   points (x=swp, y=qb1)
Curve B (cell 2, QB forced by the sweep):  points (x=q2,  y=swp)

Seevinck method: rotate 45 deg,  p=(x+y)/sqrt2 , q=(y-x)/sqrt2.
Both curves are monotonically decreasing, so each is a single-valued p(q).
A square's diagonal lies along p (slope +1 in x-y plane), hence
    side = max |pA(q)-pB(q)| / sqrt2     (one value per lobe)
SNM = min(lobe1, lobe2).
"""
import sys, os
import numpy as np

S2 = np.sqrt(2.0)

def load(fn):
    d = np.loadtxt(fn)
    if d.shape[1] >= 5:           # scale repeated for every vector
        return d[:, 0], d[:, 1], d[:, 3]
    return d[:, 0], d[:, 1], d[:, 2]

def lobes(swp, qb1, q2, n=20001):
    # curve A: (swp, qb1)   curve B: (q2, swp)
    xa, ya = swp, qb1
    xb, yb = q2, swp
    out = []
    for x, y in ((xa, ya), (xb, yb)):
        p = (x + y) / S2
        q = (y - x) / S2
        i = np.argsort(q)
        out.append((q[i], p[i]))
    (qa, pa), (qb, pb) = out
    lo, hi = max(qa.min(), qb.min()), min(qa.max(), qb.max())
    qg = np.linspace(lo, hi, n)
    d = np.interp(qg, qa, pa) - np.interp(qg, qb, pb)
    return d.max() / S2, (-d).max() / S2

def report(tag, fn):
    if not os.path.exists(fn):
        return None
    l1, l2 = lobes(*load(fn))
    return l1, l2

if __name__ == "__main__":
    cells = [("compact", "sram_compact"), ("pcell", "sram_p")]
    print()
    print("---- 3. STATIC NOISE MARGINS (from butterfly curves) ----")
    print(f"{'':22s}{'lobe1 (V)':>10s}{'lobe2 (V)':>10s}{'SNM (V)':>10s}")
    for mode, label in (("hold", "Hold SNM"), ("read", "Read SNM")):
        for c, name in cells:
            r = report(c, f"snm_{mode}_{c}.txt")
            if r is None:
                print(f"{label+' '+name:22s}  (missing file)")
            else:
                print(f"{label+' '+name:22s}{r[0]:10.4f}{r[1]:10.4f}{min(r):10.4f}")
    print()
    print("---- 4. WRITABILITY (butterfly with BL=0, BLB=VDD, WL=VDD) ----")
    for c, name in cells:
        r = report(c, f"snm_write_{c}.txt")
        if r is None:
            print(f"{name:22s}  (missing file)"); continue
        m = min(r)
        ok = m < 0.005   # one lobe collapsed -> only one stable state left
        print(f"{name:22s}remaining lobe = {m:7.4f} V  ->  "
              f"{'WRITABLE (monostable)' if ok else 'NOT writable (still bistable)'}")