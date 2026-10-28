#!/usr/bin/env python3
"""
Plots for the SRAM testbench. Every signal group is its own axes, stacked
vertically (never overlaid), saved as PNG and (if a display exists) shown.

Inputs (written by sram_tb.spice via wrdata, same folder):
  tran_data.txt                      time + 11 signals (see TRAN_SIGS)
  snm_{hold,read,write}_{compact,pcell}.txt
Outputs: sram_transient.png, sram_butterfly_{hold,read,write}.png
"""
import os,sys
import numpy as np
import matplotlib
if not os.environ.get("DISPLAY") and os.name != "nt" and "darwin" not in sys.platform:
    matplotlib.use("Agg")
import matplotlib.pyplot as plt
from snm_calc import load, lobes

VDD = 1.8
TRAN_SIGS = ["wl_tr", "we", "pre_n",
             "q_c", "qb_c", "bl_c", "blb_c",
             "q_p", "qb_p", "bl_p", "blb_p"]

def load_tran(fn="tran_data.txt"):
    d = np.loadtxt(fn)
    n = len(TRAN_SIGS)
    if d.shape[1] == 1 + n:                 # wr_singlescale
        t, cols = d[:, 0], d[:, 1:]
    else:                                    # scale repeated per vector
        t, cols = d[:, 0], d[:, 1::2][:, :n]
    return t * 1e9, {k: cols[:, i] for i, k in enumerate(TRAN_SIGS)}

def transient():
    if not os.path.exists("tran_data.txt"):
        print("tran_data.txt missing - skipping transient plot"); return
    t, s = load_tran()
    panels = [
        ("Word line / write enable",  [("wl_tr", "WL"), ("we", "WE")]),
        ("Precharge (active low)",    [("pre_n", "PRE_N")]),
        ("sram_compact: Q / QB",      [("q_c", "Q"), ("qb_c", "QB")]),
        ("sram_p (PCell): Q / QB",    [("q_p", "Q"), ("qb_p", "QB")]),
        ("sram_compact: BL / BLB",    [("bl_c", "BL"), ("blb_c", "BLB")]),
        ("sram_p (PCell): BL / BLB",  [("bl_p", "BL"), ("blb_p", "BLB")]),
    ]
    fig, axs = plt.subplots(len(panels), 1, sharex=True, figsize=(11, 2.0 * len(panels)))
    for ax, (title, sigs) in zip(axs, panels):
        for key, lab in sigs:
            ax.plot(t, s[key], label=lab, lw=1.3)
        ax.set_title(title, fontsize=9, loc="left")
        ax.set_ylabel("V"); ax.set_ylim(-0.1, VDD + 0.2)
        ax.grid(alpha=0.3); ax.legend(loc="center right", fontsize=7, ncol=2)
        for tt in (10, 20, 30, 40, 50):
            ax.axvline(tt, color="gray", ls=":", lw=0.8)
    for x, lab in ((5, "Write 1"), (15, "Hold 1"), (25, "Read 1"),
                   (35, "Write 0"), (45, "Hold 0"), (55, "Read 0")):
        axs[0].text(x, VDD + 0.25, lab, ha="center", fontsize=8)
    axs[-1].set_xlabel("time (ns)")
    fig.tight_layout()
    fig.savefig("sram_transient.png", dpi=150)
    print("saved sram_transient.png")

def butterfly(mode, title):
    figs = []
    cells = [("compact", "sram_compact"), ("pcell", "sram_p")]
    fig, axs = plt.subplots(2, 1, figsize=(5.8, 11))
    ok = False
    for ax, (c, name) in zip(axs, cells):
        fn = f"snm_{mode}_{c}.txt"
        if not os.path.exists(fn):
            ax.set_title(f"{name}: {fn} missing"); continue
        ok = True
        swp, qb1, q2 = load(fn)
        ax.plot(swp, qb1, label="QB = f(Q)  (cell 1)", lw=1.6)
        ax.plot(q2, swp, label="Q = f(QB)  (cell 2, mirrored)", lw=1.6)
        ax.plot([0, VDD], [0, VDD], "k:", lw=0.7)
        l1, l2 = lobes(swp, qb1, q2)
        ax.set_title(f"{title} - {name}   (lobes {l1*1e3:.0f} / {l2*1e3:.0f} mV, "
                     f"min {min(l1,l2)*1e3:.0f} mV)", fontsize=9)
        ax.set_xlabel("Q (V)"); ax.set_ylabel("QB (V)")
        ax.set_xlim(0, VDD); ax.set_ylim(0, VDD); ax.set_aspect("equal")
        ax.grid(alpha=0.3); ax.legend(fontsize=7, loc="upper right")
    if ok:
        fig.tight_layout()
        fig.savefig(f"sram_butterfly_{mode}.png", dpi=150)
        print(f"saved sram_butterfly_{mode}.png")

if __name__ == "__main__":
    transient()
    butterfly("hold", "Hold butterfly")
    butterfly("read", "Read butterfly")
    butterfly("write", "Write butterfly (BL=0)")
    if matplotlib.get_backend().lower() != "agg":
        plt.show()