#!/usr/bin/env python3
"""make.fun bounty: Sum up 19 November's world news in one image.

Writes one deterministic 1024x1024 PNG to /output/entry.png (or ./entry.png
when run locally). No network, stdlib + Pillow only. The image is a
front-page summary of Thursday 19 November 2026, drawn from that day's
public reporting. Same input -> same bytes on every run.
"""
import os
from PIL import Image, ImageDraw, ImageFont

W = H = 1024
BG = (247, 243, 234)
INK = (18, 18, 18)
RED = (178, 34, 34)
DARK = (24, 32, 48)
GREY = (90, 86, 78)
LINE = (200, 192, 176)


def font(name, size, bold=False):
    if name == "serif":
        p = "/usr/share/fonts/truetype/liberation/LiberationSerif" + ("-Bold.ttf" if bold else "-Regular.ttf")
    else:
        p = "/usr/share/fonts/truetype/dejavu/DejaVuSans" + ("-Bold.ttf" if bold else ".ttf")
    if os.path.exists(p):
        return ImageFont.truetype(p, size)
    return ImageFont.load_default()


def wrap(draw, text, fnt, max_w):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if draw.textlength(t, font=fnt) <= max_w:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def para(draw, x, y, max_w, text, fnt, fill=INK, lh=None):
    lh = lh or (fnt.size + 4)
    for ln in wrap(draw, text, fnt, max_w):
        draw.text((x, y), ln, font=fnt, fill=fill)
        y += lh
    return y


def head(draw, x, y, max_w, text, size, fill=INK, lh=None, serif=True):
    f = font("serif" if serif else "sans", size, bold=True)
    lh = lh or (size + 2)
    for ln in wrap(draw, text, f, max_w):
        draw.text((x, y), ln, font=f, fill=fill)
        y += lh
    return y


def rule(draw, x, y, w, fill=INK, h=2):
    draw.rectangle([x, y, x + w, y + h], fill=fill)


img = Image.new("RGB", (W, H), BG)
d = ImageDraw.Draw(img)
M = 34
CW = W - 2 * M

# ---- masthead ----
lab = "15 STORIES  •  ONE PAGE"
f_lab = font("sans", 20, True)
d.text((M, 20), "THURSDAY 19 NOVEMBER 2026", font=f_lab, fill=RED)
d.text((W - M - d.textlength(lab, font=f_lab), 20), lab, font=f_lab, fill=GREY)
y = head(d, M, 44, CW, "THE WORLD IN ONE DAY", 66, lh=68)
rule(d, M, y + 4, CW, h=4)
rule(d, M, y + 12, CW, fill=RED, h=2)
y += 22

# ---- lead row: ICJ (left, wide) + summit (right) ----
col1_w, gap = 600, 24
col2_w = CW - col1_w - gap
x2 = M + col1_w + gap
top = y
y = head(d, M, top, col1_w, "WORLD COURT: MYANMAR COMMITTED GENOCIDE", 36, lh=38)
y = para(d, M, y + 4, col1_w,
         "The Hague — the International Court of Justice rules Myanmar "
         "committed genocide against the Rohingya in 2017, in Gambia v. "
         "Myanmar. A 9–6 vote, watched live from the refugee camps.",
         font("sans", 17), lh=22)
lead_end = y
y2 = head(d, x2, top, col2_w, "TRUMP, XI, PUTIN: NO TO NUCLEAR WAR", 27, lh=29, fill=RED)
y2 = para(d, x2, y2 + 4, col2_w,
          "Shenzhen — the three leaders end their historic summit with a "
          "four-point Declaration toward Peace and a joint denunciation "
          "of nuclear war. No major deal, but dialogue opens.",
          font("sans", 16), lh=21)
y = max(lead_end, y2) + 8
rule(d, M, y, CW, fill=LINE, h=2)
y += 10

# ---- Anthropic IPO row ----
y = head(d, M, y, CW, "ANTHROPIC'S $81BN IPO SOARS 34% ON DEBUT", 34, lh=36)
y = para(d, M, y + 4, CW,
         "Wall Street — the AI lab prices at $83 a share, the biggest IPO on record, "
         "and jumps toward a $2 trillion valuation on day one — even as US stocks slide.",
         font("sans", 17), lh=22)
y += 8

# ---- GTA VI banner ----
bh = 58
d.rectangle([M, y, W - M, y + bh], fill=DARK)
d.text((M + 16, y + 6), "GTA VI IS OUT TODAY", font=font("sans", 28, True), fill=(255, 214, 90))
d.text((M + 16, y + 36), "Leonida opens on PS5 and Xbox — launch day, 19 November",
       font=font("sans", 16), fill=(235, 235, 235))
y += bh + 10
rule(d, M, y, CW, fill=LINE, h=2)
y += 8

# ---- markets strip ----
y = head(d, M, y, CW, "MARKETS: GOLD UNDER $3,700  •  WALMART $188.8BN  •  YEN WATCH", 22, lh=24, fill=RED)
y = para(d, M, y + 2, CW,
         "Gold falls below $3,700, down $170 on the week. Walmart revenue rises 5.2%. "
         "Japan inflation hits 2.2% as the Bank of Japan eyes another hike.",
         font("sans", 16), lh=21)
y += 6
rule(d, M, y, CW, fill=LINE, h=2)
y += 8

# ---- briefs grid: 2 cols x 4 rows ----
briefs = [
    ("DENMARK 109–0", "Parliament approves the Greenland–US security pact, unanimously."),
    ("COP31 OUTCRY", "Fossil-fuel phase-out is cut from the draft UN climate deal."),
    ("APEC SHENZHEN", "Leaders adopt the Shenzhen Outlook on trade, data and AI risks."),
    ("US SENATE 51–48", "Iran war-powers resolution rejected; three Republicans back it."),
    ("GAZA", "Israel ends its Nuseirat raid after a day; four killed across Gaza."),
    ("AUSTRALIA", "Jobless rate jumps to its highest since 2021 as confidence sags."),
    ("UK + NORWAY", "£100m-plus joint programme: two naval craft for Ukraine."),
    ("CRYPTO", "Binance hit by a $6.5bn Abu Dhabi freeze order; miners sell $3.4bn of bitcoin."),
]
bw = (CW - 24) // 2
bx = [M, M + bw + 24]
row_y = y
for i, (h, t) in enumerate(briefs):
    col = i % 2
    ry = row_y + (i // 2) * 78
    x = bx[col]
    d.text((x, ry), h, font=font("sans", 18, True), fill=RED)
    para(d, x, ry + 23, bw, t, font("sans", 16), lh=20)

# ---- footer ----
fy = H - 40
rule(d, M, fy - 8, CW, fill=LINE, h=2)
d.text((M, fy), "Compiled from public reporting of 19 November 2026  •  make.fun news-image-20261119",
       font=font("sans", 15), fill=GREY)

out = os.environ.get("OUTPUT", "/output/entry.png")
os.makedirs(os.path.dirname(out) or ".", exist_ok=True)
img.save(out, "PNG", optimize=True)
print("wrote", out, os.path.getsize(out), "bytes")
