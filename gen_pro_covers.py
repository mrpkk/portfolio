#!/usr/bin/env python3
"""Generate professional covers using Pollinations AI flux model."""
import urllib.parse, urllib.request, os, time

OUT = "/home/iamthat/portfolio/images"
os.makedirs(OUT, exist_ok=True)

IMAGES = {
    # === HERO BANNER ===
    "hero-banner": (
        "Professional freelance profile banner, dark blue and purple gradient background, "
        "abstract glowing AI neural network made of interconnected nodes and digital lines, "
        "floating transparent glass geometric shapes cube and sphere on the right side, "
        "futuristic cyberpunk style, 3D render, octane render, glossy gradients, "
        "minimalist tech design, small text AI Web3 Automation in the corner, "
        "clean composition, 4k, ultra detailed, cinematic lighting, no watermark"
    ),

    # === ARCHITECTURE DIAGRAM ===
    "architecture": (
        "Isometric technical infrastructure diagram of AI bot and blockchain smart contract, "
        "central 3D cloud server with arrows connecting to Telegram icon, crypto wallet "
        "Ethereum icon, database cylinder, and glowing brain icon for AI, neon blue "
        "connecting lines, dark matte background, futuristic blueprint style, highly detailed, "
        "4k, professional tech architecture, no watermark, clean composition"
    ),

    # === DASHBOARD UI ===
    "dashboard-ui": (
        "Close-up of modern glassmorphism UI dashboard on a MacBook screen, displaying "
        "AI agent management and crypto transaction analytics, colorful neon graphs "
        "green and cyan, green Active status indicators, chat interface with automated "
        "bot replies, purple and cyan neon glow, blurred city night background, "
        "high-tech look, 4k, professional product shot, no watermark"
    ),

    # === AI + BLOCKCHAIN INTEGRATION ===
    "ai-blockchain": (
        "Dynamic visualization of AI and blockchain integration, left side holographic "
        "spinning gears and brain particles, right side transparent glass structure with "
        "floating golden bitcoins and a glowing smart contract scroll with digital seal, "
        "data particles 0 and 1 flowing between them, cyberpunk high-tech style, "
        "action shot, premium case cover, 4k, cinematic lighting, no watermark"
    ),

    # === PROJECT COVERS ===
    "onchain-agent": (
        "Autonomous AI agent operating on Ethereum blockchain, robot hand signing "
        "smart contract on holographic screen, multiple wallet balances floating around, "
        "green checkmark transactions, dark blue cyberpunk background, neon cyan accents, "
        "professional tech product visualization, 4k, no watermark"
    ),

    "telegram-bot": (
        "Modern AI chatbot interface on smartphone, Telegram messenger with floating "
        "document icons and brain neural network above, user asking question bot "
        "responding with answer from knowledge base, purple and blue gradient, "
        "clean SaaS product visualization, 4k, no watermark"
    ),

    "rag-corp-bot": (
        "Corporate document intelligence system, PDF files transforming into searchable "
        "knowledge, magnifying glass over documents with AI brain processing, "
        "blue and teal color scheme, dark background, professional tech aesthetic, "
        "4k, no watermark"
    ),

    "nivritti": (
        "Vedic spiritual content system, golden mandala with Om symbol, five Telegram "
        "channel icons in circle, muhurta clock showing auspicious time, cosmic "
        "background with stars, warm gold and deep purple, spiritual digital art, "
        "4k, no watermark"
    ),

    "pravritti": (
        "News aggregation AI pipeline, multiple news source icons HackerNews TechCrunch "
        "ArsTechnica flowing into AI processing brain, output feeds going to Telegram "
        "and social media, data visualization, blue and orange accents, dark background, "
        "professional, 4k, no watermark"
    ),

    "artha": (
        "Crypto trading automation dashboard, candlestick charts Bitcoin Ethereum symbols, "
        "signal bot notification showing buy recommendation, airdrop scanner panel, "
        "funding rate monitor, dark fintech terminal theme, green red market indicators, "
        "professional, 4k, no watermark"
    ),
}

for name, prompt in IMAGES.items():
    encoded = urllib.parse.quote(prompt)
    url = f"https://image.pollinations.ai/prompt/{encoded}?width=1200&height=630&nologo=true&seed={abs(hash(name)) % 99999}&model=flux"
    outfile = os.path.join(OUT, f"{name}.png")

    print(f"  {name}...", end=" ", flush=True)
    for attempt in range(3):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=120) as resp:
                data = resp.read()
                if len(data) > 1000:
                    with open(outfile, "wb") as f:
                        f.write(data)
                    print(f"OK ({len(data)//1024}KB)")
                    break
                else:
                    print(f"retry...", end=" ", flush=True)
        except Exception as e:
            print(f"retry({e})...", end=" ", flush=True)
        time.sleep(3)
    else:
        print("FAILED")
    time.sleep(2)

print("\nAll professional covers generated!")
