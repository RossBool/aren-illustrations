"""
Build a side-by-side comparison HTML for 归档 4 vs 归档 5.

Outputs (all under workspace/):
  imgs/a4/<idx>.png         copies of 归档 4 images (resized to 512)
  imgs/a5/<idx>.png         copies of 归档 5 unique images (resized to 512)
  imgs/diff/<a4>_<a5>.png   diff heatmap (red = changed, blue = unchanged)
  compare.html              the page
"""
import os, sys, hashlib, shutil
from pathlib import Path
from PIL import Image, ImageDraw
import numpy as np

A4_DIR = Path(r"D:\Users\Administrator\Downloads\归档 4")
A5_DIR = Path(r"D:\Users\Administrator\Downloads\归档 5")
OUT    = Path(r"D:\Users\Administrator\.mavis\sessions\mvs_c0f3eb77482b409d86b44f7cfd26f2a9\workspace")

# 1. Re-run the load + dedup + best-match logic from compare_batches.py
def load_images(folder):
    out = {}
    for p in sorted(folder.glob("*.png")):
        stem = p.stem
        if "(" in stem:
            idx = int(stem.split("(")[-1].rstrip(")"))
        else:
            idx = 0
        out[idx] = (p, Image.open(p).convert("RGB"))
    return out

def hash_img(img):
    return hashlib.md5(np.asarray(img.resize((64,64)), dtype=np.uint8).tobytes()).hexdigest()[:10]

a4 = load_images(A4_DIR)
a5 = load_images(A5_DIR)

seen = {}
for k in sorted(a5.keys()):
    h = hash_img(a5[k][1])
    if h not in seen:
        seen[h] = k
a5_unique = {k: a5[k] for k in seen.values()}

def pixel_diff_stats(a_img, b_img):
    a = np.asarray(a_img.convert("RGB").resize((512,512)), dtype=np.float32)
    b = np.asarray(b_img.convert("RGB").resize((512,512)), dtype=np.float32)
    diff = np.abs(a - b)
    return {
        "mean_abs": float(diff.mean()),
        "pct": float((diff.mean(axis=2) > 8).mean() * 100),
    }

# Best-match mapping
mapping = []
for i4 in sorted(a4.keys()):
    best = (None, float("inf"), None)
    for i5 in sorted(a5_unique.keys()):
        d = pixel_diff_stats(a4[i4][1], a5_unique[i5][1])
        if d["mean_abs"] < best[1]:
            best = (i5, d["mean_abs"], d["pct"])
    mapping.append((i4, best[0], best[1], best[2]))

# Sort by mean_abs desc (biggest diff first — more interesting at top)
mapping.sort(key=lambda x: -x[2])

# 2. Prepare output dirs
img_a4  = OUT / "imgs" / "a4"
img_a5  = OUT / "imgs" / "a5"
img_dif = OUT / "imgs" / "diff"
for d in (img_a4, img_a5, img_dif):
    d.mkdir(parents=True, exist_ok=True)

# 3. Copy A4 + A5 unique images as 512px PNGs
def save_resized(src_img, dst_path, size=512):
    im = src_img.convert("RGB")
    im.thumbnail((size, size), Image.LANCZOS)
    im.save(dst_path, "PNG", optimize=True)

for i4 in a4:
    save_resized(a4[i4][1], img_a4 / f"{i4:02d}.png")
for i5 in a5_unique:
    save_resized(a5_unique[i5][1], img_a5 / f"{i5:02d}.png")

# 4. Generate diff heatmaps
def make_diff_heatmap(a_img, b_img, out_path):
    SIZE = 512
    a = np.asarray(a_img.convert("RGB").resize((SIZE,SIZE)), dtype=np.float32)
    b = np.asarray(b_img.convert("RGB").resize((SIZE,SIZE)), dtype=np.float32)
    diff = np.abs(a - b).mean(axis=2)  # [0..255]
    # Normalize to 0..1
    diff_n = np.clip(diff / 60.0, 0, 1)  # 60 = visual threshold
    # Build RGBA: red intensity proportional to diff, dark bg
    rgba = np.zeros((SIZE, SIZE, 3), dtype=np.uint8)
    # Base: dark gray to show structure
    base = (a.mean(axis=2) * 0.25).astype(np.uint8)
    rgba[..., 0] = base
    rgba[..., 1] = base
    rgba[..., 2] = base
    # Overlay: red channel boosted by diff
    rgba[..., 0] = np.clip(rgba[..., 0].astype(np.int32) + (diff_n * 255).astype(np.int32), 0, 255).astype(np.uint8)
    rgba[..., 1] = np.clip(rgba[..., 1].astype(np.int32) - (diff_n * 80).astype(np.int32), 0, 255).astype(np.uint8)
    rgba[..., 2] = np.clip(rgba[..., 2].astype(np.int32) - (diff_n * 80).astype(np.int32), 0, 255).astype(np.uint8)
    Image.fromarray(rgba, "RGB").save(out_path, "PNG", optimize=True)

for i4, i5, _, _ in mapping:
    make_diff_heatmap(a4[i4][1], a5_unique[i5][1], img_dif / f"{i4:02d}_vs_{i5:02d}.png")

# 5. Generate HTML
def verdict(md):
    if md < 3:   return ("几乎一样", "#888")
    if md < 8:   return ("轻微变化", "#3498db")
    if md < 20:  return ("明显变化", "#f39c12")
    return ("完全不同的图", "#e74c3c")

rows = []
for i4, i5, md, pct in mapping:
    label, color = verdict(md)
    rows.append(f"""
    <div class="card" data-mean="{md:.2f}">
      <div class="card-head">
        <span class="pair">A4 #{i4:02d} <span class="arrow">→</span> A5 #{i5:02d}</span>
        <span class="verdict" style="background:{color}">{label}</span>
        <span class="stats">mean_abs = <b>{md:.1f}</b> · 变化像素 = <b>{pct:.1f}%</b></span>
      </div>
      <div class="card-body">
        <div class="col"><div class="col-label">归档 4</div><img src="imgs/a4/{i4:02d}.png" /></div>
        <div class="col"><div class="col-label">归档 5</div><img src="imgs/a5/{i5:02d}.png" /></div>
        <div class="col"><div class="col-label">差异热力图</div><img src="imgs/diff/{i4:02d}_vs_{i5:02d}.png" /></div>
      </div>
    </div>""")

html = f"""<!doctype html>
<html lang="zh-CN">
<head>
<meta charset="utf-8" />
<title>归档 4 vs 归档 5 — 像素对比</title>
<style>
  :root {{
    --bg:#0f1115; --panel:#181b22; --text:#e6e6e6; --muted:#8a8f99; --line:#262a33;
  }}
  * {{ box-sizing: border-box; }}
  body {{ margin: 0; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "PingFang SC", "Microsoft YaHei", sans-serif; background: var(--bg); color: var(--text); }}
  header {{ padding: 20px 28px; border-bottom: 1px solid var(--line); background: #14171d; position: sticky; top: 0; z-index: 10; }}
  h1 {{ margin: 0 0 6px 0; font-size: 18px; font-weight: 600; }}
  .sub {{ color: var(--muted); font-size: 13px; }}
  .controls {{ margin-top: 12px; display: flex; gap: 16px; align-items: center; flex-wrap: wrap; }}
  .controls label {{ font-size: 13px; color: var(--muted); }}
  input[type=range] {{ width: 200px; vertical-align: middle; }}
  .legend {{ display: inline-flex; gap: 6px; align-items: center; }}
  .legend .dot {{ width: 10px; height: 10px; border-radius: 2px; display: inline-block; }}
  main {{ padding: 20px 28px; max-width: 1400px; margin: 0 auto; }}
  .card {{ background: var(--panel); border: 1px solid var(--line); border-radius: 8px; margin-bottom: 16px; overflow: hidden; }}
  .card-head {{ display: flex; align-items: center; gap: 14px; padding: 10px 16px; border-bottom: 1px solid var(--line); background: #1d2029; }}
  .pair {{ font-weight: 600; font-size: 14px; }}
  .arrow {{ color: var(--muted); margin: 0 4px; }}
  .verdict {{ font-size: 11px; padding: 3px 8px; border-radius: 4px; color: white; font-weight: 500; }}
  .stats {{ font-size: 12px; color: var(--muted); margin-left: auto; }}
  .stats b {{ color: var(--text); font-weight: 600; }}
  .card-body {{ display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 1px; background: var(--line); }}
  .col {{ background: var(--panel); padding: 10px; }}
  .col-label {{ font-size: 11px; color: var(--muted); text-transform: uppercase; letter-spacing: 1px; margin-bottom: 8px; }}
  .col img {{ width: 100%; height: auto; display: block; border-radius: 4px; background: #000; }}
  .card.hidden {{ display: none; }}
  .summary {{ background: var(--panel); border: 1px solid var(--line); border-radius: 8px; padding: 14px 18px; margin-bottom: 18px; font-size: 13px; line-height: 1.7; }}
  .summary code {{ background: #0a0c10; padding: 1px 6px; border-radius: 3px; font-size: 12px; }}
</style>
</head>
<body>
<header>
  <h1>归档 4 vs 归档 5 — 12 对像素对比</h1>
  <div class="sub">按 mean_abs 差异降序 · 归档 5 是去重后的 12 张唯一图 · 全部为 2048×2048 同源生成</div>
  <div class="controls">
    <label>最小 mean_abs 阈值: <span id="thr-val">0</span></label>
    <input type="range" id="thr" min="0" max="40" step="0.5" value="0" />
    <span class="legend"><span class="dot" style="background:#888"></span> 几乎一样 &lt;3</span>
    <span class="legend"><span class="dot" style="background:#3498db"></span> 轻微变化 &lt;8</span>
    <span class="legend"><span class="dot" style="background:#f39c12"></span> 明显变化 &lt;20</span>
    <span class="legend"><span class="dot" style="background:#e74c3c"></span> 完全不同 ≥20</span>
  </div>
</header>
<main>
  <div class="summary">
    <b>关键结论</b>：12 对里 <b>0 对</b> "几乎一样" · <b>1 对</b> 轻微变化（A4#5↔A5#23, 6.1）· <b>10 对</b> 明显变化 · <b>1 对</b> 完全不同（A4#4↔A5#24, 38.0）。归档 5 是真新批，不是调色版。
    <br/><br/>
    <b>怎么读热力图</b>：暗色 = 与归档 4 一致的区域 · 红色 = 与归档 4 不同的区域（diff &gt; 60/255）。看红色聚集在头部区域 = 发型/头型变化；集中在背景 = 构图/取景变化。
  </div>
  {''.join(rows)}
</main>
<script>
  const thr = document.getElementById('thr');
  const thrVal = document.getElementById('thr-val');
  const cards = document.querySelectorAll('.card');
  thr.addEventListener('input', () => {{
    thrVal.textContent = thr.value;
    const t = parseFloat(thr.value);
    cards.forEach(c => {{
      const m = parseFloat(c.dataset.mean);
      c.classList.toggle('hidden', m < t);
    }});
  }});
</script>
</body>
</html>"""

(OUT / "compare.html").write_text(html, encoding="utf-8")

# Print summary
print(f"HTML:  {OUT / 'compare.html'}")
print(f"卡片数: {len(rows)}")
print(f"按 mean_abs 降序前 5:")
for r in mapping[:5]:
    print(f"  A4#{r[0]:02d} → A5#{r[1]:02d}  mean_abs={r[2]:5.1f}  变化像素={r[3]:.1f}%")
print(f"最小 mean_abs: {mapping[-1][2]:.2f}  A4#{mapping[-1][0]} → A5#{mapping[-1][1]}")
print(f"最大 mean_abs: {mapping[0][2]:.2f}  A4#{mapping[0][0]} → A5#{mapping[0][1]}")
