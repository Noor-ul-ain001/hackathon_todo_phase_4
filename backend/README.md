---
title: Todo Intelligence Platform API
emoji: ✅
colorFrom: blue
colorTo: purple
sdk: docker
pinned: false
app_port: 7860
---

# Todo Intelligence Platform API

FastAPI backend for the Todo Intelligence Platform.

## Environment Variables (set as Secrets in HF Space settings)

| Variable | Required | Description |
|---|---|---|
| `DATABASE_URL` | Yes | PostgreSQL connection string (e.g., Neon) |
| `JWT_SECRET_KEY` | Yes | Secret key for JWT token signing |
| `GROQ_API_KEY` | No | Groq API key for AI features |
| `ALLOWED_ORIGINS` | No | Comma-separated list of allowed CORS origins |

## API Endpoints

- `GET /` — API info
- `GET /health` — Health check
- `POST /api/auth/register` — Register
- `POST /api/auth/login` — Login
- `GET /api/auth/me` — Current user
- `GET /api/tasks` — List tasks
- `POST /api/chat` — AI chat
