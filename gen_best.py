#!/usr/bin/env python3
"""Generate best quality covers with optimized prompts."""
import urllib.parse, urllib.request, os, time

OUT = "/home/iamthat/portfolio/images"
os.makedirs(OUT, exist_ok=True)

# Optimized prompts for each image
IMAGES = {
    "hero-banner": (
        "professional freelance profile banner, dark navy blue and deep purple gradient, "
        "abstract glowing AI neural network sphere made of luminous cyan nodes and connections, "
        "floating transparent glass cube with internal glow on right side, "
        "futuristic cyberpunk aesthetic, 3D octane render, glossy reflections, "
        "volumetric lighting, lens flare, clean minimalist composition, "
        "subtle text AI Web3 Automation in corner, cinematic, 8k quality"
    ),
    "architecture": (
        "isometric 3D technical diagram, central glowing cloud server with neural brain inside, "
        "surrounded by floating icons Telegram bot blue, crypto wallet gold, database cylinder, "
        "AI brain pink, all connected by bright neon blue data streams, "
        "dark matte navy background, blueprint grid lines, futuristic circuit board aesthetic, "
        "clean professional, high detail, 4k render"
    ),
    "dashboard-ui": (
        "cinematic close-up of MacBook Pro screen showing futuristic glassmorphism dashboard, "
        "dark UI with neon green and cyan data visualizations, agent status cards with green active badges, "
        "line charts showing crypto portfolio growth, chat panel with AI responses, "
        "purple ambient glow, blurred bokeh city lights background, "
        "product photography style, shallow depth of field, 4k"
    ),
    "ai-blockchain": (
        "epic digital art, left side holographic AI brain made of spinning cyan gears and particles, "
        "right side golden Bitcoin and Ethereum coins floating in transparent glass vault, "
        "glowing smart contract document with digital seal between them, "
        "streaming binary data particles connecting both sides, "
        "dark cyberpunk background with orange and blue neon accents, cinematic, 8k"
    ),
    "onchain-agent": (
        "futuristic robot hand signing a glowing holographic smart contract, "
        "floating wallet balances showing ETH USDC tokens, green transaction confirmations, "
        "Ethereum network visualization in background, dark blue tech interface panels, "
        "neon cyan accents, professional product visualization, cinematic lighting, 4k"
    ),
    "telegram-bot": (
        "sleek smartphone showing Telegram chat with AI assistant, user bubble blue asking question, "
        "bot response bubble with document icon and source reference, "
        "floating PDF documents and brain neural network above phone, "
        "purple and blue gradient background, clean SaaS product shot, 4k"
    ),
    "rag-corp-bot": (
        "abstract visualization of document intelligence, stack of PDF files on left, "
        "glowing magnifying glass in center transforming documents into knowledge, "
        "brain neural network on right processing information, "
        "flowing data particles, dark teal background, professional tech aesthetic, 4k"
    ),
    "nivritti": (
        "stunning golden Om mandala with intricate sacred geometry patterns, "
        "cosmic purple nebula background with stars, five glowing orbs around mandala "
        "representing five wisdom channels, ancient Vedic symbols, "
        "ethereal golden light rays, spiritual digital art, 8k, cinematic"
    ),
    "pravritti": (
        "futuristic news command center, multiple holographic screens showing different news sources, "
        "AI processing brain in center analyzing incoming data streams, "
        "output feeds flowing to social media icons, blue and orange color scheme, "
        "dark tech background, data visualization, professional, 4k"
    ),
    "artha": (
        "professional crypto trading terminal with multiple monitors, candlestick charts BTC ETH, "
        "green buy signal indicator glowing, airdrop opportunity scanner panel, "
        "funding rate dashboard, dark fintech theme with green and red accents, "
        "bokeh lights, cinematic product shot, 4k"
    ),
}

for name, prompt in IMAGES.items():
    # Generate with flux (best quality)
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
                    print(f"small...", end=" ", flush=True)
        except Exception as e:
            print(f"retry...", end=" ", flush=True)
        time.sleep(3)
    else:
        print("FAILED")
    time.sleep(2)

print("\nAll done!")
