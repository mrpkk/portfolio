#!/usr/bin/env python3
"""Generate AI covers for portfolio projects using Pollinations AI (flux model)."""
import urllib.parse
import urllib.request
import os
import time

OUT = "/home/iamthat/portfolio/images"
os.makedirs(OUT, exist_ok=True)

PROMPTS = {
    "onchain-agent": {
        "prompt": "futuristic cyberpunk digital artwork, autonomous AI robot agent on blockchain network, glowing blue neural network connections, Ethereum logo embedded in circuit board, dark background with neon cyan and purple accents, professional tech banner, ultra detailed, 4k render",
        "w": 1200, "h": 630, "seed": 42
    },
    "telegram-bot": {
        "prompt": "modern AI chatbot interface on smartphone screen, Telegram messenger UI with floating document icons, glowing brain neural network above phone, purple and blue gradient background, clean minimalist design, tech product visualization, 4k render",
        "w": 1200, "h": 630, "seed": 88
    },
    "rag-corp-bot": {
        "prompt": "abstract data visualization, flowing streams of documents transforming into intelligent search results, glowing magnifying glass over corporate documents, blue and teal color scheme, dark background, modern tech aesthetic, 4k render",
        "w": 1200, "h": 630, "seed": 33
    },
    "nivritti": {
        "prompt": "mystical golden mandala with Sanskrit Om symbol, Vedic astrology chart overlay, stars and cosmic energy, warm gold and deep purple colors, spiritual digital art, ornate sacred geometry patterns, ethereal glow, 4k render",
        "w": 1200, "h": 630, "seed": 77
    },
    "pravritti": {
        "prompt": "futuristic news data streams flowing across holographic displays, multiple news source icons converging into unified feed, world map with glowing connections, blue and orange accent colors, dark tech background, 4k render",
        "w": 1200, "h": 630, "seed": 55
    },
    "artha": {
        "prompt": "crypto trading dashboard with candlestick charts, Bitcoin and Ethereum symbols, holographic financial data overlay, green and red market indicators, dark futuristic background, professional fintech visualization, 4k render",
        "w": 1200, "h": 630, "seed": 99
    },
    "hero": {
        "prompt": "epic digital landscape, AI developer workspace, multiple holographic screens showing code, blockchain network visualization, robot hand typing on keyboard, dark cinematic atmosphere with blue and purple neon lighting, ultra wide composition, 4k render",
        "w": 1200, "h": 630, "seed": 11
    }
}

def generate(name, cfg):
    prompt_encoded = urllib.parse.quote(cfg["prompt"])
    url = f"https://image.pollinations.ai/prompt/{prompt_encoded}?width={cfg['w']}&height={cfg['h']}&nologo=true&seed={cfg['seed']}&model=flux"

    outfile = os.path.join(OUT, f"{name}.png")

    print(f"Generating {name}...", end=" ", flush=True)
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=120) as resp:
            data = resp.read()
            if len(data) > 1000:
                with open(outfile, "wb") as f:
                    f.write(data)
                print(f"OK ({len(data)//1024}KB)")
            else:
                print(f"FAILED (too small: {len(data)} bytes)")
    except Exception as e:
        print(f"ERROR: {e}")

for name, cfg in PROMPTS.items():
    generate(name, cfg)
    time.sleep(2)

print("\nDone!")
