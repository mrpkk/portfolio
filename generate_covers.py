#!/usr/bin/env python3
"""Generate project covers for portfolio."""
from PIL import Image, ImageDraw, ImageFont
import os

OUT = "/home/iamthat/portfolio/images"
os.makedirs(OUT, exist_ok=True)

W, H = 1200, 630

def get_font(size):
    for p in ["/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
              "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"]:
        if os.path.exists(p):
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()

def draw_rounded_rect(draw, xy, radius, fill):
    x0, y0, x1, y1 = xy
    draw.rectangle([x0+radius, y0, x1-radius, y1], fill=fill)
    draw.rectangle([x0, y0+radius, x1, y1-radius], fill=fill)
    draw.pieslice([x0, y0, x0+2*radius, y0+2*radius], 180, 270, fill=fill)
    draw.pieslice([x1-2*radius, y0, x1, y0+2*radius], 270, 360, fill=fill)
    draw.pieslice([x0, y1-2*radius, x0+2*radius, y1], 90, 180, fill=fill)
    draw.pieslice([x1-2*radius, y1-2*radius, x1, y1], 0, 90, fill=fill)

def gradient_bg(colors, w, h):
    img = Image.new("RGB", (w, h))
    r1, g1, b1 = colors[0]
    r2, g2, b2 = colors[1]
    for y in range(h):
        r = int(r1 + (r2 - r1) * y / h)
        g = int(g1 + (g2 - g1) * y / h)
        b = int(b1 + (b2 - b1) * y / h)
        for x in range(w):
            img.putpixel((x, y), (r, g, b))
    return img

def make_cover(filename, title, subtitle, tags, colors, icon_text):
    img = gradient_bg(colors, W, H)
    draw = ImageDraw.Draw(img)

    # Icon circle
    cx, cy, cr = 160, 200, 60
    draw.ellipse([cx-cr, cy-cr, cx+cr, cy+cr], fill=(255,255,255,40))
    font_icon = get_font(40)
    bbox = draw.textbbox((0,0), icon_text, font=font_icon)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    draw.text((cx - tw//2, cy - th//2 - 5), icon_text, fill="white", font=font_icon)

    # Title
    font_title = get_font(52)
    draw.text((80, 310), title, fill="white", font=font_title)

    # Subtitle
    font_sub = get_font(24)
    draw.text((80, 380), subtitle, fill=(200,200,200), font=font_sub)

    # Tags
    font_tag = get_font(18)
    x = 80
    for tag in tags:
        bbox = draw.textbbox((0,0), tag, font=font_tag)
        tw = bbox[2] - bbox[0]
        draw_rounded_rect(draw, (x, 440, x+tw+24, 472), 8, (255,255,255,30))
        draw.text((x+12, 444), tag, fill=(180,200,255), font=font_tag)
        x += tw + 36

    # GitHub link
    font_link = get_font(20)
    draw.text((80, 540), "github.com/mrpkk", fill=(100,150,255), font=font_link)

    # Decorative dots
    for i in range(20):
        import random
        random.seed(i + hash(filename))
        dx = random.randint(900, 1150)
        dy = random.randint(50, 580)
        dr = random.randint(2, 6)
        draw.ellipse([dx-dr, dy-dr, dx+dr, dy+dr], fill=(255,255,255,20))

    img.save(os.path.join(OUT, filename), quality=95)
    print(f"Created: {filename}")

# 1. On-Chain AI Agent
make_cover(
    "onchain-agent.png",
    "On-Chain AI Agent",
    "Autonomous blockchain agents with AI reasoning",
    ["Solidity", "Python", "Web3.py", "Mistral AI", "Docker"],
    [(15, 23, 42), (30, 58, 95)],
    "Bot"
)

# 2. Telegram AI Bot
make_cover(
    "telegram-bot.png",
    "Telegram AI Bot",
    "RAG-powered document Q&A with admin panel",
    ["RAG", "Mistral AI", "ChromaDB", "Streamlit", "FastAPI"],
    [(20, 20, 40), (40, 30, 80)],
    "TG"
)

# 3. RAG Corp Bot
make_cover(
    "rag-corp-bot.png",
    "RAG Corp Bot",
    "Lightweight corporate document Q&A bot",
    ["LangChain", "ChromaDB", "Mistral AI", "Python"],
    [(15, 25, 35), (25, 50, 65)],
    "RAG"
)

# 4. Nivritti
make_cover(
    "nivritti.png",
    "Nivritti",
    "Autonomous Vedic media system - 5 TG channels",
    ["Muhurta", "Swisseph", "Mistral AI", "FastAPI"],
    [(40, 15, 30), (80, 25, 50)],
    "Om"
)

# 5. Pravritti
make_cover(
    "pravritti.png",
    "Pravritti",
    "AI news pipeline - 7 TG + 5 VK + Dzen",
    ["8 Sources", "7 Personas", "Multi-platform", "Pollinations"],
    [(15, 30, 15), (25, 60, 30)],
    "News"
)

# 6. Artha
make_cover(
    "artha.png",
    "Artha",
    "Crypto automation - 7 autonomous scripts",
    ["Signal Bot", "Airdrop Farmer", "Arbitrage", "Mistral AI"],
    [(40, 25, 10), (80, 50, 20)],
    "$"
)

# 7. Portfolio hero
make_cover(
    "hero.png",
    "mrpkk",
    "AI Agent & Blockchain Developer",
    ["Python", "Solidity", "FastAPI", "Web3.py", "Mistral AI", "Docker"],
    [(10, 10, 30), (20, 40, 80)],
    "Dev"
)

print("All covers created!")
