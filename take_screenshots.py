#!/usr/bin/env python3
"""Take screenshots of project pages using Playwright Python."""
from playwright.sync_api import sync_playwright
import os, time

OUT = "/home/iamthat/portfolio/images"
os.makedirs(OUT, exist_ok=True)

PAGES = [
    ("onchain-agent", "file:///home/iamthat/portfolio/agent-dashboard.html"),
    ("telegram-bot", "file:///home/iamthat/portfolio/telegram-bot.html"),
    ("rag-github", "https://github.com/mrpkk/rag-corp-bot"),
    ("nivritti-github", "https://github.com/mrpkk/nivritti"),
    ("artha-github", "https://github.com/mrpkk/artha"),
    ("portfolio", "file:///home/iamthat/portfolio/index.html"),
]

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True, executable_path="/usr/bin/google-chrome")
    ctx = browser.new_context(
        viewport={"width": 1280, "height": 720},
        device_scale_factor=2,
    )

    for name, url in PAGES:
        print(f"  {name}...", end=" ", flush=True)
        try:
            page = ctx.new_page()
            page.goto(url, wait_until="networkidle", timeout=30000)
            page.wait_for_timeout(2000)
            page.screenshot(path=os.path.join(OUT, f"{name}.png"), full_page=False)
            page.close()
            print("OK")
        except Exception as e:
            print(f"ERROR: {e}")

    browser.close()

print("\nDone!")
