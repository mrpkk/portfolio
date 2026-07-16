#!/usr/bin/env python3
"""Generate informative project covers — each tells the story of the product."""
import urllib.parse, urllib.request, os, time

OUT = "/home/iamthat/portfolio/images"
os.makedirs(OUT, exist_ok=True)

PROMPTS = {
    "onchain-agent": (
        "professional tech product screenshot mockup, dark UI dashboard showing "
        "autonomous AI agent managing cryptocurrency wallet, blockchain transaction "
        "history panel on left, real-time Ethereum price chart in center, agent "
        "decision log on right with green checkmarks, spending limits bar, kill "
        "switch button, multiple wallet balances showing ETH and USDC, dark blue "
        "and cyan color scheme, clean modern UI design, product marketing banner "
        "style, high quality digital rendering"
    ),
    "telegram-bot": (
        "professional product mockup showing Telegram chat interface on smartphone, "
        "user asking question about company policy, AI bot responding with detailed "
        "answer from knowledge base, chat bubbles visible, admin analytics dashboard "
        "floating beside phone showing documents uploaded 23, queries today 847, "
        "accuracy rate 94 percent, FAQ entries 156, clean white and blue color scheme, "
        "modern SaaS product visualization, professional marketing style"
    ),
    "rag-corp-bot": (
        "clean product visualization showing document upload interface, PDF files "
        "flowing into intelligent search system, chat window with instant answers, "
        "brain icon connecting documents to responses, corporate blue color scheme, "
        "simple minimalist design showing upload analyze answer workflow, professional "
        "SaaS product marketing style"
    ),
    "nivritti": (
        "beautiful Telegram channel interface showing Vedic spiritual content, "
        "golden Sanskrit text on dark background, five channel icons arranged in "
        "circle representing five content niches, muhurta clock showing auspicious "
        "time indicator, cosmic background with stars, warm gold and deep purple "
        "colors, spiritual yet modern tech aesthetic, channel preview mockup"
    ),
    "pravritti": (
        "news aggregation dashboard showing seven different Telegram channels, "
        "each with unique persona avatar and name, content streams from multiple "
        "tech news sources flowing into AI processing pipeline, HackerNews ArsTechnica "
        "BleepingComputer logos, output feeds going to Telegram VK Dzen, dark "
        "professional interface with orange and blue accents, data visualization style"
    ),
    "artha": (
        "crypto monitoring dashboard with multiple panels, Bitcoin price chart "
        "with green up arrows, airdrop opportunity scanner showing new tokens, "
        "arbitrage spread indicator between exchanges, funding rate monitor, "
        "signal bot notification showing buy recommendation, professional trading "
        "terminal dark theme with red green candles, fintech product visualization"
    ),
    "hero": (
        "epic wide cinematic shot of futuristic developer workstation, multiple "
        "holographic screens showing code blockchain networks and AI models, robot "
        "arm writing smart contracts, floating Ethereum and Bitcoin symbols, neural "
        "network visualization in background, dramatic blue and purple lighting, "
        "professional tech portfolio hero banner, ultra wide composition"
    )
}

for name, prompt in PROMPTS.items():
    encoded = urllib.parse.quote(prompt)
    url = f"https://image.pollinations.ai/prompt/{encoded}?width=1200&height=630&nologo=true&seed={hash(name) % 9999}&model=flux"
    outfile = os.path.join(OUT, f"{name}.png")

    print(f"  {name}...", end=" ", flush=True)
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=120) as resp:
            data = resp.read()
            if len(data) > 1000:
                with open(outfile, "wb") as f:
                    f.write(data)
                print(f"OK ({len(data)//1024}KB)")
            else:
                print(f"TOO SMALL")
    except Exception as e:
        print(f"ERROR: {e}")
    time.sleep(3)

print("\nAll covers generated!")
