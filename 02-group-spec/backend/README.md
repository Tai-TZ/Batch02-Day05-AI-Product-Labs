# Backend — VinWonders Chat Agent (FastAPI)

Sườn backend cho demo nhóm **Batch02 Day 05–06**, tham khảo:

- **Day 04** (`Day04-C401-...`): tool loop YAML + OpenRouter provider
- **Day 03** (`C2-Team-040-AI-Chat-Bot`): SSE `/api/chat/stream`, destinations, prices

## Cấu trúc

```
backend/
├── app/
│   ├── main.py          # FastAPI routes
│   ├── chat/agent.py    # Agent + SSE events
│   ├── providers/       # OpenRouter
│   ├── tools/           # Tool registry + tools.yaml
│   └── vinwonders/      # destinations.json + prices (mock/live)
├── artifacts/
│   ├── system_prompt.md
│   └── tools.yaml
├── data/destinations.json
├── run.py
└── scripts/
```

## API (khớp frontend)

| Method | Path | Mô tả |
|--------|------|--------|
| GET | `/api/health` | Health + LLM config |
| POST | `/api/chat/stream` | SSE chat (UI chính) |
| POST | `/api/chat` | JSON chat hoặc legacy `{message, mode}` |
| GET | `/api/destinations` | Danh sách điểm đến |
| GET | `/api/prices?code=&date=` | Giá vé (mock mặc định) |

## Chạy local

```powershell
cd "...\02-group-spec\backend"
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
# Sửa OPENROUTER_API_KEY hoặc DEMO_MODE=true
python run.py
```

Frontend (terminal khác):

```powershell
cd "...\02-group-spec\frontend"
npm run dev
```

Mở http://localhost:8080 — Vite proxy `/api` → `127.0.0.1:8000`.

## Demo không cần API key

Trong `.env`:

```
DEMO_MODE=true
```

Agent trả lời mẫu + mock giá vé, vẫn stream SSE và cập nhật dashboard.

## Cloudflare Tunnel (demo công khai)

**Terminal 1** — backend:

```powershell
.\scripts\start.ps1
```

**Terminal 2** — tunnel:

```powershell
.\scripts\tunnel-cloudflare.ps1
```

Copy URL `https://....trycloudflare.com` từ terminal tunnel.

**Frontend** — nếu build/deploy tách backend, set:

```
VITE_VINWONDERS_API=https://xxxx.trycloudflare.com
```

CORS đã cho phép `*.trycloudflare.com`.

## Mở rộng (nhóm)

1. Chỉnh `artifacts/system_prompt.md` và `artifacts/tools.yaml`
2. Thêm tool trong `app/tools/registry.py`
3. `PRICES_MODE=live` để gọi API VinWonders thật (cần mạng ổn định)
4. Nâng ReAct / bootstrap từ Day 03 vào `app/chat/agent.py`
