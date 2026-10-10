# LaborX — опубликованные гиги (2026-08-06)

Все 3 гига созданы через автоматизацию (Playwright + headless, сессия в профиле worker).
Статус: в аккаунте (My Gigs), публичные URL могут быть недоступны до модерации.

| # | ID | Цена | Title | URL (public) |
|---|----|------|-------|--------------|
| 1 | 118301 | $400 | I will develop and deploy a Solidity smart contract (ERC-20, staking, vesting) | https://laborx.com/gigs/i-will-develop-and-deploy-a-solidity-smart-contract-erc-20-staking-vesting-118301 |
| 2 | 118302 | $850 | I will build a token presale / IDO dApp with vesting and claim portal (Solidity + React) | https://laborx.com/gigs/i-will-build-a-token-presale-ido-dapp-with-vesting-and-claim-portal-solidity-react-118302 |
| 3 | 118304 | $250 | I will review and optimize your Solidity smart contract (gas + security) | https://laborx.com/gigs/i-will-review-and-optimize-your-solidity-smart-contract-gas-security-118304 |

## Паттерн публикации (переиспользуемый)
1. `python3 /tmp/opencode/publish_gig.py "<title>" "<desc>" "<price>"` — заполняет форму и публикует.
2. Сессия: профиль `/home/iamthat/.playwright-profiles/worker` (accessToken в куках).
3. Обложка: клик Add cover → модалка → `set_input_files` на `input[type=file]` внутри `[class*=gig-banner-upload]` → Select.
4. Unsplash-мок: `**api.unsplash.com/search/photos*` — возвращает локальную картинку (http://127.0.0.1:8012/cover.png), чтобы модалка не ждала недоступный из РФ Unsplash.
5. Publish: `scroll_into_view_if_needed()` + `click(force=True)`.
6. Перед запуском: `rm -f ~/.playwright-profiles/worker/Singleton*`; локальный сервер: `python3 -m http.server 8012 --directory /tmp/opencode/cover_srv`.

## Важные уроки
- reCAPTCHA на логине — headless-автологин невозможен; вход только руками (сессия сохраняется в куках профиля).
- Сессия истекает при закрытии браузера (accessToken в памяти/sessionStorage + cookie) — если пропала, открыть окно и войти руками.
- Модалка обложки падала из-за web3-запросов к blockchain.googleapis.com (из РФ не отвечает) — не мешает загрузке файла, обходится через модалку Add cover.
## Статус: 2026-08-07 — МОДЕРАЦИЯ ПРОЙДЕНА, ГИГИ ПУБЛИЧНЫ
- Все 3 гига: статус **Visible** (одобрены модерацией)
- Публичные URL: HTTP 200 (проверено curl)
- Просмотры: gig 118301 (ERC-20, $400) = 7 views; gig 118304 (review, $250) = 4 views
- CodeHawks: аккаунт @iamthat активен, Unranked, $0; все конкурсы Ended — мониторить новые
- Ureed: брошен (шаг 2 заблокирован, Continue disabled при валидной форме)

## Гиги 4-6 (2026-08-07)
| # | ID | Цена | Title | URL (public) |
|---|----|------|-------|--------------|
| 4 | 118327 | $500 | AI Telegram-бот (Python + FastAPI + LLM) | https://laborx.com/gigs/i-will-build-an-ai-powered-telegram-bot-python-fastapi-llm-118327 |
| 5 | 118328 | $600 | RAG knowledge-base assistant | https://laborx.com/gigs/i-will-build-a-rag-knowledge-base-ai-assistant-vector-search-llm-118328 |
| 6 | 118329 | $700 | Web3 DeFi portfolio dashboard / onchain analytics | https://laborx.com/gigs/i-will-build-a-web3-defi-portfolio-dashboard-onchain-analytics-app-118329 |

## Гиги 7-10 (2026-08-07)
| # | ID | Цена | Title | URL |
|---|----|------|-------|-----|
| 7 | 118330 | $350 | Solidity security audit | https://laborx.com/gigs/i-will-audit-your-solidity-smart-contract-for-security-vulnerabilities-118330 |
| 8 | 118331 | $650 | NFT collection launch (ERC-721 + mint dApp) | https://laborx.com/gigs/i-will-launch-your-nft-collection-erc-721-mint-dapp-118331 |
| 9 | 118332 | $450 | Telegram crypto alerts bot | https://laborx.com/gigs/i-will-build-a-telegram-crypto-alerts-bot-prices-wallets-gas-118332 |
| 10 | 118333 | $600 | DeFi protocols integration | https://laborx.com/gigs/i-will-integrate-defi-protocols-staking-lending-swaps-into-your-app-118333 |

## Заявки на заказы (Applications) — 2026-08-07

| Дата | Заказ | Бюджет | Статус | URL |
|------|-------|--------|--------|-----|
| 07.08 06:49 | Senior Frontend Engineer with web3 experience (Bergevin Ricord) | $1,200 | ✅ Offer Sent | laborx.com/jobs/senior-frontend-engineer-with-web3-experience-103969 |
| 07.08 | smart contract for a web3 game (Pranay Gaurav) | $2,000 | ✅ Send clicked | laborx.com/jobs/smart-contract-for-a-web3-game-102398 |
| 07.08 | React & Electron Expert Needed for Crypto Wallet App (Jimmy/Stacklogic) | — | ✅ Send clicked | laborx.com/jobs/react-amp-electron-expert-needed-for-crypto-wallet-app-102286 |

Примечания:
- Заявки шлются через кнопку "Apply for this Job" → textarea (письмо ≤2000) + необязательные budget/deadline → Send.
- Заказ blockchain-dapp-developer-104134 ($1,500, 7 ч) — удалён клиентом (404 при прямом переходе), заявку не отправили.
- Клик "See details" в списке даёт 404 (JS-косяк) — заказы открываются прямым page.goto по URL из href.
- Новый процесс LaborX: Application → Customer responds → Offer → Start. Счётчик уведомлений 19, растёт.

## Kwork-отклики (2026-08-07, 7 шт.)
| ID | Проект | Бюджет | Моя цена | Статус |
|----|--------|--------|----------|--------|
| 3231707 | ИИ-Агент обзвон ATI | до 30 000 ₽ | 25 000 ₽ | ✅ Отправлен |
| 3230092 | Бот-магнит TG | до 30 000 ₽ | 8 000 ₽ | ✅ Отправлен |
| 3224472 | Перенос парсинга | 500 ₽ | 500 ₽ | ✅ Отправлен |
| 3228528 | WP импорт парсера | 500 ₽ | 500 ₽ | ✅ Отправлен |
| 3230182 | ТГ-бот лайки сторис | до 9 000 ₽ | 5 000 ₽ | ✅ Отправлен |
| 3115700 | Чат-бот обмена | 500 ₽ | 500 ₽ | ✅ Отправлен |
| 3222823 | Сайт-визитка недвижимость Испании | до 15 000 ₽ | 12 000 ₽ | ✅ Отправлен |

## Новые регистрации (2026-08-07)
- **BountyHub** (крипто-баунти): maxim-crypto-dev / wiggle.pkk@gmail.com — создан, ждёт верификации почты (24 ч)
