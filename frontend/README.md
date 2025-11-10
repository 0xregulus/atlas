# Atlas Frontend

Next.js 15 (canary) dashboard that visualizes tenant usage, AI workflows, and observability signals.

## Getting Started
```bash
cd frontend
pnpm install # or npm install
pnpm dev
```

Set `NEXT_PUBLIC_CORE_API_URL` and `CORE_API_URL` to point at the FastAPI service (default `http://localhost:8000`). The first is used by browser fetches, the second powers Next.js server actions that call FastAPI securely.

## Structure
- `app/` — App Router pages, layouts, and API routes.
- `app/actions.ts` — Server-side helpers (simulate usage, call billing endpoints).
- `components/` — UI primitives (tenant switcher, usage cards).
- `lib/api.ts` — Fetch helpers that call the core service or fall back to mocks.

Extend with tRPC or GraphQL clients once backend contracts stabilize.
