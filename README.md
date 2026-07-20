# Connect

A real-time messaging backend built from scratch — JWT refresh rotation with theft detection, WebSocket chat with persisted history, Google OAuth2, and async background jobs. No boilerplate templates, no auth-as-a-service SDKs — every piece of the auth and real-time layer is hand-built and understood end-to-end.

**[Live demo click here →](https://snazzy-begonia-cbabf5.netlify.app/)** · Backend: FastAPI on Render · DB: Postgres on Neon

---

## Why this exists

Most portfolio chat apps wrap Firebase or Supabase and call it a backend project. This one doesn't. I wanted to actually understand what happens between "user hits login" and "message shows up on someone else's screen in real time" — token lifecycle, connection state, message durability — so I built each layer myself and broke it a few times along the way.

## Features

- **JWT access + refresh token rotation with theft detection** — refresh tokens are single-use; reuse of an already-rotated token invalidates the whole session chain, not just the request. Sessions are server-side source of truth, so logout actually revokes access instead of just deleting a client-side token.
- **Google OAuth2** via Authlib, with account linking against existing email-based accounts.
- **Real-time WebSocket chat** — deterministic SHA256-hashed room IDs (same two users always resolve to the same room, no duplicate room creation race), live delivery, and a connection manager handling multiple concurrent sockets per user.
- **Persisted message history** — every message is written to Postgres on send, independent of who's online. Offline users see full history on next login; no messages are lost to a dropped connection.
- **Password hashing with Argon2** (not bcrypt — chosen for its resistance to GPU-based cracking).
- **Async background tasks via Celery + Redis** for outbound email (verification, notifications), decoupled from the request/response cycle.
- **Schema migrations via Alembic** — 9 tracked migrations reflecting real iterative schema changes, not a single upfront "perfect" schema.
- **Dark, real-time-status-aware frontend** — connection state (connecting/connected/offline) is visible live, not assumed.

## Architecture

```
app/
├── api/            # route handlers — thin, delegate to services
├── services/        # business logic
├── repositories/     # DB access layer, isolated from route/service logic
├── models/           # SQLAlchemy models
├── schemas/           # Pydantic request/response contracts
├── core/               # security (JWT, hashing), error types, Celery config
├── ws/                  # WebSocket connection manager
├── tasks/               # Celery background tasks
├── db/                   # connection pooling
└── alembic/               # migrations
```

Layered on purpose: routes never touch the database directly, services never know about HTTP, repositories never contain business rules. This makes each layer independently testable and means a bug in, say, token rotation logic is isolated to one file instead of scattered across route handlers.

## Tech stack

| Layer | Choice |
|---|---|
| API framework | FastAPI (async, `asyncpg` connection pooling) |
| Database | PostgreSQL (Neon, managed) |
| ORM / migrations | SQLAlchemy 2.0 + Alembic |
| Auth | Custom JWT (python-jose) + Argon2 hashing + Google OAuth2 (Authlib) |
| Real-time | Native WebSockets (`websockets` lib), custom connection manager |
| Background jobs | Celery + Redis |
| Containerization | Docker + Docker Compose (local dev) |
| Deployment | Render (API + worker), Netlify (frontend), Neon (Postgres) |

## Running locally

**1. Clone and configure**
```bash
git clone https://github.com/hithuyeager/connect-with-friends.git
cd connect-with-friends/app
cp .env.example .env   # fill in the values below
```

**2. Required environment variables** (`.env`)
```
DATABASE_URL=postgresql://app_user:strongpassword@postgres:5432/fast_api
DATABASE_URL_FOR_RAW_SQL=postgresql://app_user:strongpassword@postgres:5432/fast_api
REDIS_URL=redis://redis:6379/0
ALGORITHM=HS256
SECRET_KEY=your-secret-key
ACCESS_TOKEN_EXPIRE=900
REFRESH_TOKEN_EXPIRE=604800
GOOGLE_CLIENT_ID=your-google-client-id
GOOGLE_CLIENT_SECRET=your-google-client-secret
GOOGLE_SECRET_KEY=your-session-secret
MY_EMAIL=your-sender-email
MY_EMAIL_PASSWORD=your-app-password
FRONTEND_URL=http://localhost:5500
```

**3. Run with Docker Compose**
```bash
docker-compose up --build
```
This starts Postgres, Redis, the FastAPI app, and the Celery worker together.

**4. Run migrations**
```bash
docker-compose exec fastapi alembic upgrade head
```

API is now live at `http://localhost:8000`. Open the frontend `index.html` (served via any static server, e.g. VS Code Live Server on port 5500) and it will connect automatically.

## API overview

| Endpoint | Method | Purpose |
|---|---|---|
| `/app/signup` | POST | Create account (email + password) |
| `/app/signin` | POST | Authenticate, returns access + refresh token |
| `/app/rotate` | POST | Rotate refresh token, issue new access token |
| `/app/logout` | POST | Revoke session server-side |
| `/google/login` | GET | Begin Google OAuth flow |
| `/google/callback` | GET | OAuth callback, redirects to frontend with tokens |
| `/ws/room/direct` | POST | Get/create deterministic room ID for two users |
| `/ws/chat/{room_id}` | WS | Real-time message socket |
| `/ws/get/{room_id}` | GET | Paginated message history |
| `/ws/users/search` | GET | Search users to start a conversation |

## What I'd build next

- Push notifications for offline message delivery (currently: message persists, user sees it on next login — correct MVP behavior, not yet real-time-pushed to offline devices)
- Read receipts and typing indicators (connection manager already tracks per-user socket state, this is a natural extension)
- Redis Pub/Sub for horizontal scaling across multiple WebSocket server instances

## Try it

A demo account is available on the live app if you'd rather explore than sign up — look for "Try demo account" on the login screen.

---

Built solo, self-taught, as part of an active job search. Feedback and issues welcome.
