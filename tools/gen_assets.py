"""Generates the profile SVGs in ../assets (header, toolkit). Run: python3 tools/gen_assets.py"""
import math, os, random

OUT = os.path.join(os.path.dirname(__file__), "..", "assets")
SANS = "-apple-system,BlinkMacSystemFont,'Segoe UI',Helvetica,Arial,sans-serif"
MONO = "ui-monospace,SFMono-Regular,'SF Mono',Menlo,Consolas,monospace"
BG, PANEL, EDGE, MUTED, TEXT = "#0d1117", "#161b22", "#30363d", "#8b949e", "#e6edf3"
G = ["#161b22", "#0e4429", "#006d32", "#26a641", "#39d353"]


def header():
    W, H = 1000, 300
    random.seed(21)
    cols, rows, cell, gap = 17, 7, 16, 5
    gx, gy = W - 40 - cols * (cell + gap) + gap, 70
    css, cells = [], []
    for c in range(cols):
        for r in range(rows):
            base = random.choices([0, 1, 2, 3, 4], [30, 30, 20, 12, 8])[0]
            x, y = gx + c * (cell + gap), gy + r * (cell + gap)
            delay = (c * 0.09 + r * 0.03)
            cells.append(f'<rect x="{x}" y="{y}" width="{cell}" height="{cell}" rx="3.5" fill="{G[base]}" '
                         f'class="w" style="animation-delay:{delay:.2f}s"/>')
    css.append("@keyframes wave{0%,100%{opacity:1}12%{opacity:1;fill:#39d353}24%{opacity:1}}"
               ".w{animation:wave 6s ease-in-out infinite}")
    # fade the grid into the left side so the text stays clean
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="Ganap Tewary — Computer Engineering PhD, Arizona State University">
<style>{"".join(css)}</style>
<defs>
  <linearGradient id="fade" x1="0" x2="1"><stop offset="0" stop-color="{BG}"/><stop offset=".6" stop-color="{BG}"/><stop offset=".72" stop-color="{BG}" stop-opacity="0"/></linearGradient>
  <linearGradient id="bar" x1="0" x2="1"><stop offset="0" stop-color="#39d353"/><stop offset="1" stop-color="#0e4429"/></linearGradient>
  <clipPath id="card"><rect width="{W}" height="{H}" rx="16"/></clipPath>
</defs>
<g clip-path="url(#card)">
  <rect width="{W}" height="{H}" fill="{BG}"/>
  {"".join(cells)}
  <rect width="{W}" height="{H}" fill="url(#fade)"/>
  <rect x="0" y="0" width="{W}" height="4" fill="url(#bar)"/>
</g>
<rect x=".5" y=".5" width="{W-1}" height="{H-1}" rx="16" fill="none" stroke="{EDGE}"/>
<text x="56" y="92" font-family="{MONO}" font-size="15" fill="#39d353" letter-spacing="1">~/ganap-tewary $</text>
<text x="54" y="152" font-family="{SANS}" font-size="56" font-weight="700" fill="{TEXT}" letter-spacing="-1">Ganap Tewary</text>
<text x="56" y="192" font-family="{SANS}" font-size="21" fill="{TEXT}">Computer Engineering PhD · Arizona State University</text>
<text x="56" y="226" font-family="{SANS}" font-size="17" fill="{MUTED}">Hardware–software co-design across the AI stack</text>
<g font-family="{MONO}" font-size="13">
  <rect x="56" y="248" width="196" height="28" rx="14" fill="#0e4429" stroke="#006d32"/>
  <text x="154" y="266.5" fill="#7ee787" text-anchor="middle">DAC 2026 · published</text>
  <rect x="264" y="248" width="150" height="28" rx="14" fill="{PANEL}" stroke="{EDGE}"/>
  <text x="339" y="266.5" fill="{MUTED}" text-anchor="middle">Tempe, Arizona</text>
</g>
</svg>'''


def toolkit():
    groups = [
        ("LANGUAGES", ["Python", "C++", "C", "CUDA", "Verilog", "TypeScript", "SQL"]),
        ("ML & SEARCH", ["PyTorch", "PyG / GNNs", "FAISS", "HNSW", "Hugging Face", "scikit-learn"]),
        ("SYSTEMS", ["Linux", "Slurm / HPC", "Docker", "AWS", "Node.js", "Git"]),
        ("HARDWARE", ["FPGA", "Vitis HLS", "STM32", "ARM Cortex-M", "chiplets", "GPU kernels"]),
    ]
    W, pad, rowh, top = 1000, 32, 62, 14
    H = top + len(groups) * rowh + 18
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="Toolkit">',
           f'<rect x=".5" y=".5" width="{W-1}" height="{H-1}" rx="16" fill="{BG}" stroke="{EDGE}"/>',
]
    shades = ["#39d353", "#26a641", "#26a641", "#39d353"]
    for i, (name, items) in enumerate(groups):
        y = top + i * rowh
        if i: out.append(f'<line x1="{pad}" y1="{y}" x2="{W-pad}" y2="{y}" stroke="#21262d"/>')
        out.append(f'<rect x="{pad}" y="{y+22}" width="4" height="18" rx="2" fill="{shades[i]}"/>')
        out.append(f'<text x="{pad+14}" y="{y+36}" font-family="{MONO}" font-size="12.5" fill="{MUTED}" letter-spacing="1.2">{name.replace("&", "&amp;")}</text>')
        x = 210
        for t in items:
            w = 28 + len(t) * 8.4
            out.append(f'<rect x="{x}" y="{y+17}" width="{w:.0f}" height="28" rx="14" fill="{PANEL}" stroke="{EDGE}"/>'
                       f'<text x="{x+w/2:.0f}" y="{y+36}" font-family="{SANS}" font-size="14" fill="{TEXT}" text-anchor="middle">{t}</text>')
            x += w + 10
    out.append("</svg>")
    return "\n".join(out)


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    for name, fn in [("header.svg", header), ("toolkit.svg", toolkit)]:
        open(os.path.join(OUT, name), "w").write(fn())
        print("wrote", name)
