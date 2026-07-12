"""
Compare 归档 4 (1-11, no-paren) vs 归档 5 (22-32 unique images)
via pixel-level statistics. NO vision — only math.
"""
import os, sys, hashlib
from pathlib import Path
from collections import defaultdict

try:
    from PIL import Image
    import numpy as np
except ImportError:
    print("Need pillow + numpy. pip install pillow numpy")
    sys.exit(1)

A4 = Path(r"D:\Users\Administrator\Downloads\归档 4")
A5 = Path(r"D:\Users\Administrator\Downloads\归档 5")

def load_images(folder):
    """Load all PNGs, return dict {index: PIL.Image} sorted by numeric index in filename."""
    out = {}
    for p in sorted(folder.glob("*.png")):
        # Parse index from filename: "...(12).png" or "...(1).png" or "....png" (root)
        stem = p.stem
        if "(" in stem:
            idx = int(stem.split("(")[-1].rstrip(")"))
        else:
            idx = 0  # no-paren
        out[idx] = Image.open(p).convert("RGB")
    return out

def img_stats(img):
    """Return (W,H, mean RGB, std RGB, colorfulness) as numpy."""
    a = np.asarray(img, dtype=np.float32)
    h, w, _ = a.shape
    mean = a.reshape(-1, 3).mean(axis=0)
    std  = a.reshape(-1, 3).std(axis=0)
    # colorfulness (Hasler-Süsstrunk simplified)
    rg = a[...,0] - a[...,1]
    yb = (a[...,0] + a[...,1])/2 - a[...,2]
    colorfulness = float(np.sqrt(rg.std()**2 + yb.std()**2) + 0.3*np.sqrt(rg.mean()**2 + yb.mean()**2))
    return dict(W=w, H=h, mean=mean, std=std, colorfulness=colorfulness)

def pixel_diff(a_img, b_img):
    """Normalize to same size, return mean abs diff in [0..255] + per-channel."""
    a = np.asarray(a_img.convert("RGB").resize((512,512)), dtype=np.float32)
    b = np.asarray(b_img.convert("RGB").resize((512,512)), dtype=np.float32)
    diff = np.abs(a - b)
    return {
        "mean_abs_diff": float(diff.mean()),
        "max_abs_diff":  float(diff.max()),
        "pct_pixels_changed": float((diff.mean(axis=2) > 8).mean() * 100),  # >8/255 = visible
        "channel_diff_R": float(diff[...,0].mean()),
        "channel_diff_G": float(diff[...,1].mean()),
        "channel_diff_B": float(diff[...,2].mean()),
    }

a4 = load_images(A4)
a5 = load_images(A5)
print(f"归档 4 loaded: {sorted(a4.keys())}")
print(f"归档 5 loaded: {sorted(a5.keys())}")
print()

# Dedup 归档 5 by hash, keep lowest index
def hash_img(img):
    return hashlib.md5(np.asarray(img.resize((64,64)), dtype=np.uint8).tobytes()).hexdigest()[:10]

seen = {}
for k in sorted(a5.keys()):
    h = hash_img(a5[k])
    if h not in seen:
        seen[h] = k
a5_unique = {k: a5[k] for k in seen.values()}
print(f"归档 5 dedup to {len(a5_unique)} unique images, indices: {sorted(a5_unique.keys())}")
print()

# Stats per image
print("="*100)
print("PER-IMAGE STATS")
print("="*100)
print(f"{'idx':>4} | {'source':>6} | {'WxH':>9} | {'mean R/G/B':>17} | {'std R/G/B':>17} | {'colorful':>8}")
print("-"*100)
for idx in sorted(a4.keys()):
    s = img_stats(a4[idx])
    print(f"{idx:>4} | A4     | {s['W']}x{s['H']:>3} | {s['mean'][0]:5.1f}/{s['mean'][1]:5.1f}/{s['mean'][2]:5.1f} | {s['std'][0]:5.1f}/{s['std'][1]:5.1f}/{s['std'][2]:5.1f} | {s['colorfulness']:7.2f}")
for idx in sorted(a5_unique.keys()):
    s = img_stats(a5_unique[idx])
    print(f"{idx:>4} | A5     | {s['W']}x{s['H']:>3} | {s['mean'][0]:5.1f}/{s['mean'][1]:5.1f}/{s['mean'][2]:5.1f} | {s['std'][0]:5.1f}/{s['std'][1]:5.1f}/{s['std'][2]:5.1f} | {s['colorfulness']:7.2f}")

# Pairwise: each A4 image vs each A5 unique image — find closest match
print()
print("="*100)
print("BEST-MATCH MAPPING (A4 idx -> A5 idx) by lowest mean abs diff")
print("="*100)
mapping = []
for i4 in sorted(a4.keys()):
    best = None
    best_diff = float("inf")
    for i5 in sorted(a5_unique.keys()):
        d = pixel_diff(a4[i4], a5_unique[i5])
        if d["mean_abs_diff"] < best_diff:
            best_diff = d["mean_abs_diff"]
            best = (i5, d)
    mapping.append((i4, best[0], best[1]))

print(f"{'A4 idx':>6} -> {'A5 idx':>6} | {'mean_abs':>9} | {'pct_changed':>11} | {'max_diff':>8}")
print("-"*60)
for i4, i5, d in mapping:
    print(f"{i4:>6} -> {i5:>6} | {d['mean_abs_diff']:9.2f} | {d['pct_pixels_changed']:10.1f}% | {d['max_abs_diff']:8.0f}")

# Verdict heuristics
print()
print("="*100)
print("VERDICT HEURISTICS")
print("="*100)
for i4, i5, d in mapping:
    md = d["mean_abs_diff"]
    if md < 3:
        verdict = "几乎一样 (no-op)"
    elif md < 8:
        verdict = "轻微变化 (调色/HDR/微调)"
    elif md < 20:
        verdict = "明显变化 (姿态/构图/换图)"
    else:
        verdict = "完全不同的图"
    print(f"  A4#{i4:>3} vs A5#{i5:>3}  mean_abs={md:5.1f}  →  {verdict}")
