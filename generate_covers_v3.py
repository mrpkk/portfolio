#!/usr/bin/env python3
"""Generate informative project covers — Pillow style with text, icons, architecture."""
from PIL import Image, ImageDraw, ImageFont
import os, math

OUT = "/home/iamthat/portfolio/images"
os.makedirs(OUT, exist_ok=True)

W, H = 1200, 630

def font(size, bold=True):
    names = ["DejaVuSans-Bold.ttf", "LiberationSans-Bold.ttf", "DejaVuSans.ttf"]
    if not bold:
        names = ["DejaVuSans.ttf", "LiberationSans-Regular.ttf"]
    for n in names:
        for p in [f"/usr/share/fonts/truetype/dejavu/{n}",
                  f"/usr/share/fonts/truetype/liberation/{n}"]:
            if os.path.exists(p):
                return ImageFont.truetype(p, size)
    return ImageFont.load_default()

def gradient_bg(c1, c2, w=W, h=H):
    img = Image.new("RGB", (w, h))
    for y in range(h):
        t = y / h
        r = int(c1[0] + (c2[0]-c1[0])*t)
        g = int(c1[1] + (c2[1]-c1[1])*t)
        b = int(c1[2] + (c2[2]-c1[2])*t)
        for x in range(w):
            img.putpixel((x,y), (r,g,b))
    return img

def draw_gradient_text(draw, xy, text, f, colors):
    x, y = xy
    for i, ch in enumerate(text):
        t = i / max(len(text)-1, 1)
        r = int(colors[0][0] + (colors[1][0]-colors[0][0])*t)
        g = int(colors[0][1] + (colors[1][1]-colors[0][1])*t)
        b = int(colors[0][2] + (colors[1][2]-colors[0][2])*t)
        draw.text((x, y), ch, fill=(r,g,b), font=f)
        bbox = f.getbbox(ch)
        x += bbox[2] - bbox[0] + 1

def text_width(draw, text, f):
    bbox = f.getbbox(text)
    return bbox[2] - bbox[0]

def icon_circle(draw, cx, cy, r, color, icon_char, icon_font):
    draw.ellipse([cx-r, cy-r, cx+r, cy+r], fill=color)
    bbox = icon_font.getbbox(icon_char)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    draw.text((cx - tw//2, cy - th//2 - 2), icon_char, fill="white", font=icon_font)

def stat_block(draw, x, y, value, label, color):
    vf = font(36)
    lf = font(16, bold=False)
    draw_gradient_text(draw, (x, y), value, vf, [color, (255,255,255)])
    draw.text((x, y+45), label, fill=(120,130,150), font=lf)

def phone_frame(img, x, y, w, h):
    draw = ImageDraw.Draw(img)
    r = 20
    draw.rounded_rectangle([x, y, x+w, y+h], radius=r, fill=(20,25,35), outline=(50,60,80), width=2)
    draw.rounded_rectangle([x+10, y+10, x+w-10, y+30], radius=8, fill=(30,35,50))
    return draw

def chat_bubble(draw, x, y, w, text_lines, is_user=False, bg=(30,40,60)):
    line_h = 22
    h = len(text_lines) * line_h + 16
    if is_user:
        bx = x + w - w
        draw.rounded_rectangle([bx, y, bx+w, y+h], radius=12, fill=(0, 120, 200))
    else:
        draw.rounded_rectangle([x, y, x+w, y+h], radius=12, fill=bg)
    f = font(14, bold=False)
    for i, line in enumerate(text_lines):
        tx = x + 12 if not is_user else bx + 12
        draw.text((tx, y + 8 + i*line_h), line, fill="white", font=f)
    return h

def arch_box(draw, x, y, w, h, icon, title, subtitle, highlight=False):
    color = (0, 180, 120) if highlight else (40, 50, 70)
    outline = (0, 200, 140) if highlight else (60, 70, 90)
    draw.rounded_rectangle([x, y, x+w, y+h], radius=10, fill=color, outline=outline, width=2)
    icon_f = font(28)
    title_f = font(14)
    sub_f = font(11, bold=False)
    draw.text((x + w//2 - 8, y + 10), icon, fill="white", font=icon_f)
    tw = text_width(draw, title, title_f)
    draw.text((x + w//2 - tw//2, y + 48), title, fill="white", font=title_f)
    tw2 = text_width(draw, subtitle, sub_f)
    draw.text((x + w//2 - tw2//2, y + 68), subtitle, fill=(140,150,170), font=sub_f)

def arrow(draw, x1, y1, x2, y2, color=(80,90,110)):
    draw.line([x1, y1, x2, y2], fill=color, width=2)
    angle = math.atan2(y2-y1, x2-x1)
    al = 8
    draw.line([x2, y2, int(x2-al*math.cos(angle-0.4)), int(y2-al*math.sin(angle-0.4))], fill=color, width=2)
    draw.line([x2, y2, int(x2-al*math.cos(angle+0.4)), int(y2-al*math.sin(angle+0.4))], fill=color, width=2)


# ══════════════════════════════════════════════════════════════
# 1. On-Chain AI Agent
# ══════════════════════════════════════════════════════════════
img = gradient_bg((10, 15, 30), (15, 25, 50))
d = ImageDraw.Draw(img)

# Title
draw_gradient_text(d, (60, 40), "On-Chain AI Agent", font(48), [(0,200,255), (100,120,255)])
d.text((60, 100), "Автономный AI-агент для блокчейна", fill=(150,160,180), font=font(22, False))

# Stats
stat_block(d, 60, 160, "24/7", "Без остановки", (0,200,255))
stat_block(d, 250, 160, "3", "Сети (ETH,BSC,POL)", (0,200,180))
stat_block(d, 520, 160, "0 MB", "Локальных моделей", (100,120,255))

# Architecture
d.text((60, 260), "Архитектура", fill=(200,210,230), font=font(24))
boxes = [
    (60, 310, "Web3", "Восприятие", "Блокчейн"),
    (230, 310, "AI", "Рассуждение", "Mistral"),
    (400, 310, "Plan", "Планирование", "Цели"),
    (570, 310, "Exec", "Исполнение", "Транзакции"),
]
for bx, by, icon, title, sub in boxes:
    arch_box(d, bx, by, 140, 90, icon, title, sub)
for i in range(3):
    arrow(d, 60+140+i*170+140, 355, 60+170*(i+1), 355)

# Safety boxes
d.text((60, 430), "Безопасность", fill=(200,210,230), font=font(18))
safe_items = ["Лимиты расходов", "Kill Switch", "Симуляция", "Аудит логов"]
for i, item in enumerate(safe_items):
    sx = 60 + i * 170
    d.rounded_rectangle([sx, 460, sx+155, 495], radius=8, fill=(20,35,20), outline=(0,120,80))
    d.text((sx+10, 468), f"✓ {item}", fill=(0,200,120), font=font(13, False))

# Phone mockup (agent dashboard)
px, py = 780, 30
phone_frame(img, px, py, 350, 560)
d = ImageDraw.Draw(img)
d.text((px+20, py+40), "Agent Dashboard", fill=(0,200,255), font=font(16))
# Balance
d.text((px+20, py+80), "Баланс:", fill=(120,130,150), font=font(13, False))
d.text((px+20, py+100), "2.45 ETH", fill="white", font=font(22))
# Status
d.rounded_rectangle([px+20, py+140, px+130, py+165], radius=8, fill=(0,40,20))
d.text((px+30, py+144), "● RUNNING", fill=(0,255,120), font=font(13))
# Progress
d.text((px+20, py+185), "Yield: 8.2% APY", fill=(120,130,150), font=font(12, False))
d.rounded_rectangle([px+20, py+210, px+330, py+225], radius=4, fill=(30,40,60))
d.rounded_rectangle([px+20, py+210, px+250, py+225], radius=4, fill=(0,150,200))
# TX history
d.text((px+20, py+250), "Последние транзакции:", fill=(120,130,150), font=font(12, False))
txs = [
    ("Deposit 0.5 ETH → Aave", "✓"),
    ("Swap 100 USDC → ETH", "✓"),
    ("Bridge 0.2 → Polygon", "✓"),
]
for i, (tx, status) in enumerate(txs):
    ty = py + 275 + i * 28
    d.text((px+20, ty), f"{status} {tx}", fill=(180,200,220), font=font(11, False))

# AI Decision Log
d.text((px+20, py+370), "AI Решение:", fill=(120,130,150), font=font(12, False))
d.rounded_rectangle([px+20, py+395, px+330, py+455], radius=8, fill=(15,25,15))
d.text((px+30, py+405), "Aave APY 8.2%, Gas 12 gwei", fill=(0,200,120), font=font(11, False))
d.text((px+30, py+425), "→ DEPOSIT 0.5 ETH", fill=(0,255,120), font=font(13))
d.text((px+30, py+445), "confidence: 0.94", fill=(100,120,100), font=font(10, False))

# GitHub
d.text((px+20, py+480), "github.com/mrpkk", fill=(0,150,255), font=font(14))

img.save(os.path.join(OUT, "onchain-agent.png"), quality=95)
print("onchain-agent.png OK")


# ══════════════════════════════════════════════════════════════
# 2. Telegram AI Bot
# ══════════════════════════════════════════════════════════════
img = gradient_bg((12, 12, 28), (20, 15, 40))
d = ImageDraw.Draw(img)

draw_gradient_text(d, (60, 40), "AI Telegram-бот", font(48), [(0,180,255), (130,80,255)])
d.text((60, 100), "для вашего бизнеса", fill=(130,80,255), font=font(28))
d.text((60, 140), "Отвечает на вопросы клиентов 24/7", fill=(150,160,180), font=font(18, False))
d.text((60, 168), "на основе ваших документов", fill=(150,160,180), font=font(18, False))

# Format tags
tags = [("PDF, DOCX, TXT", (0,150,200)), ("Mistral AI", (180,80,200)), ("Админ-панель", (0,180,120))]
tx = 60
for tag_text, color in tags:
    tw = text_width(d, tag_text, font(14))
    d.rounded_rectangle([tx, 210, tx+tw+20, 238], radius=8, fill=(color[0]//4, color[1]//4, color[2]//4))
    d.text((tx+10, 215), tag_text, fill=color, font=font(14))
    tx += tw + 35

# Phone mockup — chat
px, py = 720, 20
phone_frame(img, px, py, 420, 580)
d = ImageDraw.Draw(img)

# Bot header
d.ellipse([px+15, py+40, px+45, py+70], fill=(0,120,200))
d.text((px+55, py+45), "AI-ассистент", fill="white", font=font(16))
d.text((px+55, py+65), "● online", fill=(0,200,120), font=font(12, False))

# User question
chat_bubble(d, px+80, py+100, 300, ["Как оформить возврат?"], is_user=True)

# Bot answer
chat_bubble(d, px+20, py+145, 360, [
    "Возврат товара возможен",
    "в течение 14 дней.",
    "Нужен чек и сохраненный",
    "товарный вид."
], is_user=False, bg=(30,45,55))

# Source indicator
d.rounded_rectangle([px+20, py+260, px+200, py+280], radius=4, fill=(20,30,40))
d.text((px+30, py+263), "📄 policy_return.pdf", fill=(0,180,220), font=font(11, False))

# Second question
chat_bubble(d, px+120, py+300, 260, ["Как связаться с поддержкой?"], is_user=True)

# Bot answer 2
chat_bubble(d, px+20, py+345, 360, [
    "📞 +7 (900) 123-45-67",
    "📧 support@company.com"
], is_user=False, bg=(30,45,55))

d.rounded_rectangle([px+20, py+415, px+200, py+435], radius=4, fill=(20,30,40))
d.text((px+30, py+418), "📄 contacts.pdf", fill=(0,180,220), font=font(11, False))

# Stats on left
d.text((60, 290), "Результат для бизнеса", fill=(200,210,230), font=font(20))
stats = [
    ("847", "Вопросов в день"),
    ("94%", "Точность ответов"),
    ("1.2с", "Среднее время"),
    ("$0", "Стоимость AI"),
]
for i, (val, label) in enumerate(stats):
    sx = 60 + (i % 2) * 250
    sy = 340 + (i // 2) * 90
    d.rounded_rectangle([sx, sy, sx+220, sy+75], radius=10, fill=(20,25,40))
    d.text((sx+15, sy+10), val, fill=(0,200,255), font=font(28))
    d.text((sx+15, sy+48), label, fill=(120,130,150), font=font(13, False))

d.text((60, 540), "github.com/mrpkk", fill=(0,150,255), font=font(14))

img.save(os.path.join(OUT, "telegram-bot.png"), quality=95)
print("telegram-bot.png OK")


# ══════════════════════════════════════════════════════════════
# 3. RAG Corp Bot
# ══════════════════════════════════════════════════════════════
img = gradient_bg((10, 15, 30), (12, 20, 40))
d = ImageDraw.Draw(img)

draw_gradient_text(d, (60, 50), "RAG-ассистент", font(48), [(0,180,255), (0,220,180)])
d.text((60, 110), "по документам", fill=(0,220,180), font=font(36))
d.text((60, 165), "Telegram-бот, который отвечает на вопросы", fill=(150,160,180), font=font(18, False))
d.text((60, 192), "по корпоративным PDF-документам с указанием источника", fill=(150,160,180), font=font(18, False))

# Stats
stat_block(d, 60, 250, "100%", "Бесплатный API", (0,200,255))
stat_block(d, 280, 250, "0 MB", "Локальных моделей", (0,200,180))
stat_block(d, 480, 250, "3", "Документа в демо", (100,120,255))

# Architecture
d.text((60, 340), "Архитектура", fill=(200,210,230), font=font(24))
arch_boxes = [
    (60, 390, "👤", "Пользователь", "Telegram"),
    (230, 390, "🤖", "Telegram Bot", "python-telegram-bot"),
    (400, 390, "🔗", "LangChain", "Оркестрация RAG"),
    (570, 390, "🔍", "ChromaDB", "Векторный поиск"),
]
for bx, by, icon, title, sub in arch_boxes:
    arch_box(d, bx, by, 150, 90, icon, title, sub)
for i in range(3):
    arrow(d, 60+150+i*170+150, 435, 60+170*(i+1), 435)

# Second row
arch_box(d, 180, 510, 170, 80, "🧠", "Mistral AI", "LLM + Эмбеддинги", highlight=True)
arch_box(d, 420, 510, 170, 80, "📄", "PDF Документы", "Политики компании")

d.text((780, 540), "github.com/mrpkk", fill=(0,150,255), font=font(14))

img.save(os.path.join(OUT, "rag-corp-bot.png"), quality=95)
print("rag-corp-bot.png OK")


# ══════════════════════════════════════════════════════════════
# 4. Nivritti
# ══════════════════════════════════════════════════════════════
img = gradient_bg((25, 10, 30), (40, 15, 50))
d = ImageDraw.Draw(img)

draw_gradient_text(d, (60, 40), "Nivritti", font(52), [(255,200,50), (255,120,50)])
d.text((60, 105), "Автономная ведическая медиа-система", fill=(180,160,200), font=font(20, False))

# 5 channels
channels = [
    ("Advaita", "Адвайта-веданта"),
    ("Vedas", "Веды"),
    ("Yoga", "Йога"),
    ("Mantras", "Мантры"),
    ("Muhurtas", "Мухурты"),
]
d.text((60, 160), "5 Telegram-каналов", fill=(200,180,220), font=font(20))
for i, (name, desc) in enumerate(channels):
    cx = 60 + i * 140
    d.rounded_rectangle([cx, 195, cx+125, 260], radius=12, fill=(40,20,50), outline=(100,60,120))
    d.text((cx+10, 205), name, fill=(255,200,50), font=font(16))
    d.text((cx+10, 228), desc, fill=(140,120,160), font=font(11, False))

# Muhurta clock
d.text((60, 300), "Muhurta Scheduler", fill=(200,180,220), font=font(20))
d.rounded_rectangle([60, 340, 350, 450], radius=12, fill=(20,10,25))
# Clock face
cx, cy, cr = 205, 395, 45
d.ellipse([cx-cr, cy-cr, cx+cr, cy+cr], outline=(100,60,120), width=2)
d.text((cx-30, cy+50), "Благоприятная мухурта", fill=(0,200,120), font=font(11, False))
# Clock hands
d.line([cx, cy, cx+25, cy-20], fill=(255,200,50), width=3)
d.line([cx, cy, cx-15, cy+30], fill=(200,120,255), width=2)
d.text((cx-5, cy-35), "▲", fill=(0,200,120), font=font(14))

# AI Content
d.text((400, 300), "AI-контент", fill=(200,180,220), font=font(20))
items = [
    "Mistral AI генерирует посты",
    "Каждая рубрика — уникальный стиль",
    "Публикация в благоприятные мухурты",
    "6 постов в день автоматически",
]
for i, item in enumerate(items):
    d.text((400, 340 + i*28), f"✓ {item}", fill=(180,180,200), font=font(14, False))

# Stats
d.text((400, 470), "5 каналов  •  6 постов/день  •  24/7", fill=(120,130,150), font=font(14, False))

d.text((60, 560), "github.com/mrpkk", fill=(200,150,255), font=font(14))

img.save(os.path.join(OUT, "nivritti.png"), quality=95)
print("nivritti.png OK")


# ══════════════════════════════════════════════════════════════
# 5. Pravritti
# ══════════════════════════════════════════════════════════════
img = gradient_bg((10, 20, 15), (15, 30, 20))
d = ImageDraw.Draw(img)

draw_gradient_text(d, (60, 40), "Pravritti", font(48), [(0,200,100), (255,180,0)])
d.text((60, 100), "AI-новости для 7 каналов + 5 VK + Dzen", fill=(150,170,150), font=font(20, False))

# 8 Sources
d.text((60, 155), "8 источников", fill=(200,220,200), font=font(18))
sources = ["HN", "Ars", "Bleep", "TC", "Wired", "Habr", "ExploitDB", "Reddit"]
for i, src in enumerate(sources):
    sx = 60 + i * 80
    d.rounded_rectangle([sx, 185, sx+70, 215], radius=6, fill=(20,35,25))
    d.text((sx+8, 192), src, fill=(0,200,100), font=font(13))

# Pipeline
d.text((60, 250), "Pipeline", fill=(200,220,200), font=font(20))
pipe = [
    (60, "📰", "Источники"),
    (210, "🤖", "AI (7 personas)"),
    (380, "✏️", "Контент"),
    (530, "📢", "Публикация"),
]
for px, icon, label in pipe:
    arch_box(d, px, 290, 140, 80, icon, label, "")
for i in range(3):
    arrow(d, 60+140+i*170+140, 330, 60+170*(i+1), 330)

# 7 Personas
d.text((60, 400), "7 уникальных персон", fill=(200,220,200), font=font(18))
personas = ["Stratechery", "Военкор", "Кибер-разведчик", "CTO", "DevOps", "Crypto", "Economist"]
for i, p in enumerate(personas):
    px = 60 + i * 80
    d.rounded_rectangle([px, 430, px+72, 460], radius=6, fill=(30,25,15))
    d.text((px+5, 437), p, fill=(200,180,100), font=font(10, False))

# Platforms
d.text((60, 490), "Платформы", fill=(200,220,200), font=font(18))
platforms = [("7 TG", (0,150,255)), ("5 VK", (0,100,200)), ("Dzen RSS", (200,50,50))]
px = 60
for label, color in platforms:
    tw = text_width(d, label, font(16))
    d.rounded_rectangle([px, 520, px+tw+20, 550], radius=8, fill=(color[0]//4, color[1]//4, color[2]//4))
    d.text((px+10, 525), label, fill=color, font=font(16))
    px += tw + 35

d.text((780, 560), "github.com/mrpkk", fill=(0,150,255), font=font(14))

img.save(os.path.join(OUT, "pravritti.png"), quality=95)
print("pravritti.png OK")


# ══════════════════════════════════════════════════════════════
# 6. Artha
# ══════════════════════════════════════════════════════════════
img = gradient_bg((15, 12, 8), (25, 20, 10))
d = ImageDraw.Draw(img)

draw_gradient_text(d, (60, 40), "Artha", font(52), [(255,180,0), (255,100,0)])
d.text((60, 105), "Крипто-автоматизация — 7 скриптов", fill=(180,160,120), font=font(20, False))

# 7 scripts as cards
scripts = [
    ("Signal Bot", "AI-сигналы", (0,180,100)),
    ("Airdrop Farmer", "Сканер аирдропов", (0,150,200)),
    ("Arbitrage", "Межбиржевой спред", (200,150,0)),
    ("Funding Monitor", "Фьючерсы", (200,80,80)),
    ("Liquidation", "Ликвидации", (200,50,50)),
    ("Income Engine", "Доход через AI", (100,200,0)),
    ("Report", "Ежедневный отчёт", (150,100,200)),
]
for i, (name, desc, color) in enumerate(scripts):
    row = i // 4
    col = i % 4
    sx = 60 + col * 165
    sy = 155 + row * 100
    d.rounded_rectangle([sx, sy, sx+150, sy+85], radius=10, fill=(20,18,12), outline=(color[0]//3, color[1]//3, color[2]//3))
    d.text((sx+10, sy+10), name, fill=color, font=font(14))
    d.text((sx+10, sy+35), desc, fill=(120,110,100), font=font(12, False))
    # Mini chart
    for j in range(5):
        bar_h = 10 + (j*7 + i*3) % 20
        d.rectangle([sx+10+j*25, sy+75-bar_h, sx+20+j*25, sy+75], fill=(color[0]//2, color[1]//2, color[2]//2))

# Phone — signal notification
px, py = 720, 150
phone_frame(img, px, py, 400, 450)
d = ImageDraw.Draw(img)
d.text((px+20, py+40), "Crypto Signal Bot", fill=(255,180,0), font=font(16))
d.text((px+20, py+65), "🤖 AI-сигналы в Telegram", fill=(120,130,150), font=font(12, False))

# Signal card
d.rounded_rectangle([px+20, py+100, px+380, py+220], radius=10, fill=(15,25,15))
d.text((px+30, py+110), "🟢 BTC/USDT", fill=(0,255,120), font=font(18))
d.text((px+30, py+140), "Цена: $67,450", fill="white", font=font(14))
d.text((px+30, py+165), "Signal: BUY", fill=(0,255,120), font=font(16))
d.text((px+30, py+195), "Confidence: 87%", fill=(100,120,100), font=font(12, False))

# Airdrop card
d.rounded_rectangle([px+20, py+240, px+380, py+330], radius=10, fill=(15,20,30))
d.text((px+30, py+250), "🪂 Новый airdrop", fill=(0,180,255), font=font(16))
d.text((px+30, py+275), "Protocol: EigenLayer", fill="white", font=font(14))
d.text((px+30, py+300), "Reward: ~$50-200", fill=(100,200,100), font=font(13, False))

# Funding rate
d.rounded_rectangle([px+20, py+350, px+380, py+420], radius=10, fill=(25,15,15))
d.text((px+30, py+360), "📊 Funding Rate", fill=(200,100,100), font=font(16))
d.text((px+30, py+385), "ETH: -0.012% (short pays)", fill="white", font=font(13))
d.text((px+30, py+405), "SOL: +0.008% (long pays)", fill="white", font=font(13))

d.text((px+20, py+440), "github.com/mrpkk", fill=(0,150,255), font=font(14))

img.save(os.path.join(OUT, "artha.png"), quality=95)
print("artha.png OK")


# ══════════════════════════════════════════════════════════════
# 7. Hero
# ══════════════════════════════════════════════════════════════
img = gradient_bg((8, 10, 25), (12, 15, 35))
d = ImageDraw.Draw(img)

draw_gradient_text(d, (60, 60), "mrpkk", font(64), [(0,180,255), (130,80,255)])
d.text((60, 140), "AI Agent & Blockchain Developer", fill=(150,160,180), font=font(24, False))

# 3 project cards
cards = [
    ("🤖", "AI-агенты", "Автономные боты\nдля блокчейна", (0,200,255)),
    ("💬", "Telegram AI", "RAG-системы\nдля бизнеса", (130,80,255)),
    ("⛓️", "Смарт-контракты", "Solidity\nHardhat", (0,200,150)),
]
for i, (icon, title, desc, color) in enumerate(cards):
    cx = 60 + i * 220
    d.rounded_rectangle([cx, 210, cx+200, 340], radius=12, fill=(15,18,30), outline=(color[0]//3, color[1]//3, color[2]//3))
    d.text((cx+15, 225), icon, fill=color, font=font(32))
    d.text((cx+15, 270), title, fill=color, font=font(18))
    for j, line in enumerate(desc.split("\n")):
        d.text((cx+15, 300 + j*20), line, fill=(120,130,150), font=font(13, False))

# Tech stack
d.text((60, 380), "Стек", fill=(200,210,230), font=font(20))
stack = ["Python", "Solidity", "FastAPI", "Web3.py", "Mistral AI", "Docker"]
tx = 60
for s in stack:
    tw = text_width(d, s, font(14))
    d.rounded_rectangle([tx, 410, tx+tw+16, 438], radius=8, fill=(20,25,40), outline=(50,60,80))
    d.text((tx+8, 415), s, fill=(100,180,255), font=font(14))
    tx += tw + 28

# Stats
d.text((60, 480), "Проекты", fill=(200,210,230), font=font(20))
stat_block(d, 60, 520, "6", "Проектов", (0,200,255))
stat_block(d, 200, 520, "24/7", "Автономность", (0,200,180))
stat_block(d, 400, 520, "100%", "API (бесплатно)", (130,80,255))

d.text((780, 560), "github.com/mrpkk", fill=(0,150,255), font=font(16))

img.save(os.path.join(OUT, "hero.png"), quality=95)
print("hero.png OK")


print("\nAll v3 covers done!")
