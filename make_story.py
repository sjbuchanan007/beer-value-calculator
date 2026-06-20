"""England match-day graphic + portrait Story (1080x1920) versions."""
from PIL import Image, ImageDraw, ImageFilter
from make_wc import font, football, make_mark, lerp, GOLD, GOLD_SOFT, CREAM, MUTED, GREEN

RED = (206, 17, 38)        # England red
BG_TOP = (46, 33, 23)
BG_BOT = (20, 15, 11)


def grad(img, w, h):
    d = ImageDraw.Draw(img)
    for y in range(h):
        d.line([(0, y), (w, y)], fill=lerp(BG_TOP, BG_BOT, y / h))


def glow(img, w, h, cx, cy, rx, ry, s=70, blur=100):
    g = Image.new("L", (w, h), 0)
    ImageDraw.Draw(g).ellipse([cx - rx, cy - ry, cx + rx, cy + ry], fill=s)
    g = g.filter(ImageFilter.GaussianBlur(blur))
    img.paste(Image.new("RGB", (w, h), GOLD), (0, 0), g)


def ctext(d, w, cy, text, fnt, fill):
    tw = d.textlength(text, font=fnt)
    d.text(((w - tw) / 2, cy), text, font=fnt, fill=fill)


def flag(d, cx, cy, w, h):
    x0, y0 = cx - w / 2, cy - h / 2
    d.rounded_rectangle([x0, y0, x0 + w, y0 + h], radius=12, fill=(245, 245, 245))
    bar = h * 0.17
    d.rectangle([x0, cy - bar / 2, x0 + w, cy + bar / 2], fill=RED)
    d.rectangle([cx - bar / 2, y0, cx + bar / 2, y0 + h], fill=RED)


def url_pill(d, w, cy, text="thevaluator.app", size=40):
    f = font("LiberationSans-Bold.ttf", size)
    tw = d.textlength(text, font=f)
    pw, ph = tw + 88, 76
    px = (w - pw) / 2
    d.rounded_rectangle([px, cy, px + pw, cy + ph], radius=ph / 2, fill=GOLD)
    d.text(((w - tw) / 2, cy + (ph - size) / 2 - 4), text, font=f, fill=(28, 20, 16))


def draw_row(d, name, detail, ppint, best, badge, y, rh, w=1080):
    d.rounded_rectangle([60, y, w - 60, y + rh - 18], radius=18,
                        fill=(44, 58, 37) if best else (42, 31, 23))
    d.text((96, y + 22), name, font=font("LiberationSans-Bold.ttf", 42), fill=CREAM)
    d.text((96, y + 70), detail, font=font("LiberationSans-Regular.ttf", 27), fill=MUTED)
    vf = font("LiberationSans-Bold.ttf", 48)
    val = "£%.2f/pint" % ppint
    vw = d.textlength(val, font=vf)
    d.text((w - 92 - vw, y + 36), val, font=vf, fill=GOLD if best else GOLD_SOFT)
    if badge:
        bf = font("LiberationSans-Bold.ttf", 22)
        lw = d.textlength(name, font=font("LiberationSans-Bold.ttf", 42))
        bx = 96 + lw + 18
        bw = d.textlength(badge, font=bf) + 24
        d.rounded_rectangle([bx, y + 26, bx + bw, y + 60], radius=17, fill=GREEN)
        d.text((bx + 12, y + 30), badge, font=bf, fill=(12, 28, 12))


# ---------------- England match-day (square 1080) ----------------
def england_square():
    W = H = 1080
    img = Image.new("RGB", (W, H), BG_BOT); grad(img, W, H)
    glow(img, W, H, W / 2, 430, 280, 240)
    d = ImageDraw.Draw(img)
    flag(d, W / 2, 200, 210, 138)
    ctext(d, W, 360, "MATCH DAY", font("LiberationSans-Bold.ttf", 96), CREAM)
    ctext(d, W, 490, "England are playing — sort the fridge for less",
          font("LiberationSans-Regular.ttf", 36), GOLD_SOFT)
    ctext(d, W, 560, "Best value beer, down to the pence per pint",
          font("LiberationSans-Regular.ttf", 30), MUTED)
    football(d, 250, 760, 46)
    football(d, 830, 760, 46)
    url_pill(d, W, 720)
    ctext(d, W, 980, "Enjoy responsibly · 18+", font("LiberationSans-Regular.ttf", 24), (150, 134, 108))
    img.save("england-matchday.png"); print("wrote england-matchday.png")


# ---------------- Story helpers (portrait 1080x1920) ----------------
PW, PH = 1080, 1920


def story_base(title, sub):
    img = Image.new("RGB", (PW, PH), BG_BOT); grad(img, PW, PH)
    d = ImageDraw.Draw(img)
    img.paste(make_mark(120), (int(PW / 2 - 60), 300), make_mark(120))
    d = ImageDraw.Draw(img)
    ctext(d, PW, 450, title, font("LiberationSans-Bold.ttf", 60), CREAM)
    ctext(d, PW, 540, sub, font("LiberationSans-Regular.ttf", 30), MUTED)
    return img, d


def story_ranked(fname, title, sub, rows, punch=None):
    img, d = story_base(title, sub)
    top, rh = 660, 150
    for i, (name, detail, ppint, best, badge) in enumerate(rows):
        draw_row(d, name, detail, ppint, best, badge, top + i * rh, rh)
    if punch:
        ctext(d, PW, top + len(rows) * rh + 30, punch,
              font("LiberationSans-Bold.ttf", 36), GOLD_SOFT)
    url_pill(d, PW, 1560)
    ctext(d, PW, 1670, "Spotted at Tesco · prices vary · 18+",
          font("LiberationSans-Regular.ttf", 24), (150, 134, 108))
    img.save(fname); print("wrote", fname)


def story_hero(fname, big, line1, line2):
    img = Image.new("RGB", (PW, PH), BG_BOT); grad(img, PW, PH)
    glow(img, PW, PH, PW / 2, 900, 320, 300)
    d = ImageDraw.Draw(img)
    img.paste(make_mark(120), (int(PW / 2 - 60), 360), make_mark(120))
    d = ImageDraw.Draw(img)
    ctext(d, PW, 760, big, font("LiberationSans-Bold.ttf", 200), GOLD)
    ctext(d, PW, 1020, line1, font("LiberationSans-Bold.ttf", 52), CREAM)
    ctext(d, PW, 1120, line2, font("LiberationSans-Regular.ttf", 34), MUTED)
    url_pill(d, PW, 1560)
    ctext(d, PW, 1670, "Spotted at Tesco · prices vary · 18+",
          font("LiberationSans-Regular.ttf", 24), (150, 134, 108))
    img.save(fname); print("wrote", fname)


def england_story():
    img = Image.new("RGB", (PW, PH), BG_BOT); grad(img, PW, PH)
    glow(img, PW, PH, PW / 2, 850, 320, 320)
    d = ImageDraw.Draw(img)
    flag(d, PW / 2, 560, 240, 158)
    ctext(d, PW, 760, "MATCH DAY", font("LiberationSans-Bold.ttf", 110), CREAM)
    ctext(d, PW, 920, "England are playing —", font("LiberationSans-Regular.ttf", 40), GOLD_SOFT)
    ctext(d, PW, 980, "sort the fridge for less", font("LiberationSans-Regular.ttf", 40), GOLD_SOFT)
    ctext(d, PW, 1080, "Best value beer, down to the pence per pint",
          font("LiberationSans-Regular.ttf", 32), MUTED)
    football(d, 270, 1260, 50)
    football(d, 810, 1260, 50)
    url_pill(d, PW, 1500)
    ctext(d, PW, 1620, "Enjoy responsibly · 18+", font("LiberationSans-Regular.ttf", 24), (150, 134, 108))
    img.save("england-matchday-story.png"); print("wrote england-matchday-story.png")


BEST = [
    ("Heineken", "15 × 440 ml  ·  £13.00", 1.12, True, "CHEAPEST"),
    ("Carling", "18 × 440 ml  ·  £15.99", 1.15, False, ""),
    ("Stella", "18 × 440 ml  ·  £17.89", 1.28, False, ""),
    ("Madri", "15 × 440 ml  ·  £15.00", 1.29, False, ""),
    ("San Miguel", "10 × 440 ml  ·  £10.00", 1.29, False, ""),
]
TRAP = [
    ("18 × 330 ml", "Birra Moretti · £18 Clubcard", 1.72, True, "6 MORE BOTTLES"),
    ("12 × 330 ml", "Birra Moretti · £18.25", 2.62, False, "SAME £, LESS BEER"),
]

if __name__ == "__main__":
    england_square()
    england_story()
    story_ranked("tesco-best-story.png", "MATCH-DAY BEST VALUE",
                 "Tesco · best price per pint", BEST)
    story_ranked("tesco-trap-story.png", "SAME BEER, MIND THE PACK",
                 "Birra Moretti at Tesco", TRAP,
                 punch="Same price — 6 more bottles. Always check.")
    story_hero("tesco-pint-story.png", "£1.12", "to £3.23 a pint",
               "The same lagers — that's why it pays to check")
