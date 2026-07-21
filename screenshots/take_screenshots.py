#!/usr/bin/env python3
"""Скриншоты коммерческих проектов для Contra"""
from playwright.sync_api import sync_playwright
import os

OUT = "/home/iamthat/portfolio/screenshots"
os.makedirs(OUT, exist_ok=True)

SCREENSHOTS = [
    # Demo-страницы
    ("portfolio-main", "file:///home/iamthat/portfolio/index.html"),
    ("agent-dashboard", "file:///home/iamthat/portfolio/agent-dashboard.html"),
    ("telegram-bot-demo", "file:///home/iamthat/portfolio/telegram-bot.html"),
    # GitHub-страницы проектов
    ("github-onchain", "https://github.com/mrpkk/onchain-ai-agent"),
    ("github-telegram", "https://github.com/mrpkk/telegram-ai-bot"),
    ("github-rag", "https://github.com/mrpkk/rag-corp-bot"),
    ("github-solidity", "https://github.com/mrpkk/solidity-portfolio"),
    ("github-artha", "https://github.com/mrpkk/artha"),
    ("github-defi-pilot", "https://github.com/mrpkk/defi-pilot"),
    ("github-crypto-mcp", "https://github.com/mrpkk/crypto-mcp-server"),
    ("github-portfolio", "https://github.com/mrpkk/portfolio"),
    # GitHub Pages
    ("gh-pages-portfolio", "https://mrpkk.github.io/portfolio/"),
    ("gh-pages-agent", "https://mrpkk.github.io/portfolio/agent-dashboard.html"),
    ("gh-pages-bot", "https://mrpkk.github.io/portfolio/telegram-bot.html"),
]

with sync_playwright() as p:
    browser = p.chromium.launch(
        headless=True,
        executable_path="/usr/bin/google-chrome"
    )
    ctx = browser.new_context(
        viewport={"width": 1280, "height": 720},
        device_scale_factor=2,
    )

    for name, url in SCREENSHOTS:
        print(f"  {name}...", end=" ", flush=True)
        try:
            page = ctx.new_page()
            page.goto(url, wait_until="networkidle", timeout=30000)
            page.wait_for_timeout(2000)
            path = os.path.join(OUT, f"{name}.png")
            page.screenshot(path=path, full_page=False)
            page.close()
            print("OK")
        except Exception as e:
            print(f"ERROR: {e}")

    browser.close()

print("\nDone!")
