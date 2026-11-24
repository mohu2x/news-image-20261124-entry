from functools import cache
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


SIZE = 1024
SCALE = 4
LEFT, RIGHT = 52, 972
FONT_DIR = Path("/usr/share/fonts/truetype/noto")
SERIF = "NotoSerifDisplay-Black.ttf"
REGULAR = "NotoSans-Regular.ttf"
SEMIBOLD = "NotoSans-SemiBold.ttf"
BOLD = "NotoSans-Bold.ttf"

PAPER = "#f9f5eb"
INK = "#171612"
BODY = "#38352e"
ACCENT = "#8d3029"
RULE = "#b7ad9a"
TICKER = "#24221d"
TICKER_ACCENT = "#f3c1a8"

BRIEFS = (
    (
        "CYBER · DEALS",
        ("CrowdStrike snaps up", "Zscaler in $44bn deal"),
        (
            "The takeover, one of the largest ever in cybersecurity,",
            "comes as AI-driven threats mount.",
        ),
    ),
    (
        "AI · COURTS",
        ("States sue Musk firms", "over Grok images"),
        (
            "US states say the chatbot generated a flood of",
            "sexualized images; they want the companies held to account.",
        ),
    ),
    (
        "WAR · UKRAINE",
        ("Leaked data puts", "Russia's toll near 500,000"),
        (
            "The hacked figures emerged as Russian strikes",
            "on the Kyiv region killed at least 14 people.",
        ),
    ),
    (
        "ASIA · CHINA",
        ("China sentences official", "to death for spying"),
        (
            "A former official was convicted of leaking national secrets,",
            "in one of the harshest espionage sentences in years.",
        ),
    ),
)

TICKER_ROWS = (
    (
        'Moscow accuses Estonia of acts "on the verge of open war"',
        "Drones hit homes and a UN building in Sudan's capital",
    ),
    (
        "UN chief demands an AI risk framework within a year",
        "Thousands evacuated from UK concert after unknown substance released",
    ),
    (
        "Japan presses Russia over detained reporter",
        "Storms threaten messy Thanksgiving travel",
    ),
)


@cache
def font(face, size):
    return ImageFont.truetype(str(FONT_DIR / face), round(size * SCALE))


def line(draw, words, x, y, face, size, color=INK, *, tracking=0, align="left"):
    """Draw a line with y aligned to the top of a capital H."""
    typeface = font(face, size)
    baseline = y * SCALE - typeface.getbbox("H", anchor="ls")[1]
    position = x * SCALE
    if tracking:
        advances = [typeface.getlength(char) + tracking * SCALE for char in words]
        width = sum(advances) - tracking * SCALE
    else:
        width = typeface.getlength(words)
    if align == "center":
        position -= width / 2
    elif align == "right":
        position -= width
    if tracking:
        for char, advance in zip(words, advances):
            draw.text((round(position), baseline), char, font=typeface, fill=color, anchor="ls")
            position += advance
    else:
        draw.text((round(position), baseline), words, font=typeface, fill=color, anchor="ls")


def lines(draw, copy, x, y, step, face, size, color=INK):
    for index, words in enumerate(copy):
        line(draw, words, x, y + index * step, face, size, color)


def rule(draw, x1, y1, x2, y2, color=RULE, width=1):
    draw.line(tuple(value * SCALE for value in (x1, y1, x2, y2)), fill=color, width=width * SCALE)


def kicker(draw, words, x, y):
    line(draw, words, x, y, BOLD, 13, ACCENT, tracking=1.25)


def render():
    page = Image.new("RGB", (SIZE * SCALE, SIZE * SCALE), PAPER)
    draw = ImageDraw.Draw(page)

    line(draw, "THE WORLD IN ONE IMAGE", LEFT, 32, BOLD, 12, tracking=1.75)
    line(draw, "TUESDAY · 24 NOVEMBER 2026", RIGHT, 32, BOLD, 12, tracking=1.75, align="right")
    rule(draw, LEFT, 54, RIGHT, 54)
    line(draw, "The Day the Market Roared Back", SIZE / 2, 69, BOLD, 23, tracking=2.8, align="center")
    rule(draw, LEFT, 105, RIGHT, 105, INK, 2)

    kicker(draw, "MARKETS · WALL STREET", LEFT, 129)
    lines(draw, ("Wall Street roars back: Nvidia", "leaps 31% as Huang returns"), LEFT, 158, 62, SERIF, 58)
    lines(
        draw,
        (
            "The Nasdaq surged 6.5% and the S&P 500 4.7% in the biggest one-day rebound",
            "on record, snapping the longest losing streak since April 2024 — a day after",
            'Trump brokered Jensen Huang\'s return to Nvidia, declaring "I made the deal."',
        ),
        LEFT, 300, 29, REGULAR, 22, BODY,
    )
    rule(draw, LEFT, 401, RIGHT, 401, INK)

    kicker(draw, "SPACE · NATO", LEFT, 421)
    lines(
        draw,
        ("NATO vows space defence as", "Russia readies a nuclear satellite"),
        LEFT, 453, 37, SERIF, 33,
    )
    rule(draw, 643, 438, 643, 534)
    lines(
        draw,
        (
            "Allies say Moscow could launch",
            "a nuclear anti-satellite weapon",
            "within weeks; German reports say",
            "the launch would give Russia the",
            "ability to destroy satellites in orbit.",
        ),
        666, 439, 20, REGULAR, 17, BODY,
    )
    rule(draw, LEFT, 550, RIGHT, 550, INK)

    rule(draw, 512, 568, 512, 880)
    rule(draw, LEFT, 720, RIGHT, 720)
    for (x, y), (section, headline, body) in zip(
        ((LEFT, 571), (536, 571), (LEFT, 741), (536, 741)), BRIEFS, strict=True
    ):
        kicker(draw, section, x, y)
        lines(draw, headline, x, y + 25, 33, SERIF, 29)
        lines(draw, body, x, y + 98, 20, REGULAR, 15, BODY)

    draw.rectangle((LEFT * SCALE, 896 * SCALE, RIGHT * SCALE, 992 * SCALE), fill=TICKER)
    ticker_left = 71
    line(draw, "ALSO ON TUESDAY", ticker_left, 909, SEMIBOLD, 12, TICKER_ACCENT, tracking=1.5)
    ticker_copy = tuple("  ·  ".join(stories) for stories in TICKER_ROWS)
    lines(draw, ticker_copy, ticker_left, 931, 19.5, REGULAR, 14, PAPER)

    return page.resize((SIZE, SIZE), Image.Resampling.LANCZOS)


if __name__ == "__main__":
    render().save(Path(__file__).with_name("asset.png"), optimize=True)
