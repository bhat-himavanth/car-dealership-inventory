# AutoVault – Car Dealership Inventory System

A full-stack inventory system for a car dealership. Users register and log in, browse and search the showroom, and purchase vehicles. Admins can add, edit, restock and delete vehicles.

Built test-first (TDD) as part of the Software Craftsman kata.

| Layer     | Tech                                                  |
|-----------|-------------------------------------------------------|
| Backend   | Python 3.11+, FastAPI, SQLAlchemy, SQLite, JWT, bcrypt |
| Frontend  | React 19, Vite, Tailwind CSS v4, React Router         |
| Tests     | pytest + pytest-cov (backend), Vitest + Testing Library (frontend) |

## Architecture

```
React SPA (Vite, :5173)
   │  fetch /api/...  + "Authorization: Bearer <JWT>"
   ▼
FastAPI (:8000)
   routers/      → HTTP layer: parse request, pick status code
   dependencies  → "is this user logged in / an admin?"
   services/     → business rules (search, purchase, restock…)
   models        → SQLAlchemy tables
   ▼
SQLite file (dealership.db)
```

Routes stay thin and contain no business logic; services contain no HTTP code. That separation makes each layer easy to test and change on its own.

## API

| Method | Endpoint | Access |
|---|---|---|
| POST | `/api/auth/register` | Public |
| POST | `/api/auth/login` | Public – returns a JWT |
| POST | `/api/vehicles` | Logged in |
| GET | `/api/vehicles` | Logged in |
| GET | `/api/vehicles/search?make=&model=&category=&min_price=&max_price=` | Logged in |
| PUT | `/api/vehicles/:id` | Logged in |
| DELETE | `/api/vehicles/:id` | **Admin** |
| POST | `/api/vehicles/:id/purchase` | Logged in |
| POST | `/api/vehicles/:id/restock` `{ "amount": 5 }` | **Admin** |

Interactive docs are available at **http://localhost:8000/docs** while the backend runs.

## Running locally

**Prerequisites:** Python 3.11+, Node.js 20+, Git.

### Backend

```bash
cd backend
python -m venv .venv
# Windows: .venv\Scripts\activate     macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

The API runs on http://localhost:8000 and creates `dealership.db` on first start.

### Frontend (new terminal)

```bash
cd frontend
npm install
npm run dev
```

Open http://localhost:5173.

### Making an admin

Register through the UI, then:

```bash
cd backend
python -m app.make_admin you@example.com
```

Log out and back in to see the admin controls.

## Tests

```bash
cd backend && pytest --cov=app --cov-report=term-missing
cd frontend && npm test
```

### Test report

<!-- Paste the output of the two commands above here. -->

```
Backend:  52 passed – 100% coverage
Frontend: 7 passed
```

## Screenshots

| Login | Showroom (admin) |
|---|---|
| ![Login](docs/screenshots/login.png) | ![Dashboard](docs/screenshots/dashboard.png) |

## Design decisions

- **SQLite** – a real on-disk database with zero setup. Swapping to PostgreSQL only needs a different `DATABASE_URL`.
- **Race-safe purchase** – stock is checked and decremented in a single `UPDATE … WHERE quantity > 0`, so two buyers can't both get the last car.
- **Same error for wrong email and wrong password** – stops attackers from discovering which emails are registered.
- **Admin role** – delete and restock are admin-only, as the spec requires. Add/update are open to any logged-in user per the spec, while the UI only shows those forms to admins.

## My AI Usage

<!-- Write this section in your own words – the interviewers will ask about it. -->

**Tools used:** Claude (Anthropic) via claude.ai.

**How I used it:**
- …
- …

**Reflection:**
…