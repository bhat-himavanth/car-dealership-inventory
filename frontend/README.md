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

| Login | Admin dashboard |
|---|---|
| ![Login](docs/screenshots/login.png) | ![Admin dashboard](docs/screenshots/admin-dashboard.png) |

| Add vehicle (admin) | User dashboard | User search |
|---|---|---|
| ![Add vehicle](docs/screenshots/add-vehicle.png) | ![User dashboard](docs/screenshots/user-dashboard.png) | ![User search](docs/screenshots/user-search.png) |

## Design decisions

- **SQLite** – a real on-disk database with zero setup. Swapping to PostgreSQL only needs a different `DATABASE_URL`.
- **Race-safe purchase** – stock is checked and decremented in a single `UPDATE … WHERE quantity > 0`, so two buyers can't both get the last car.
- **Same error for wrong email and wrong password** – stops attackers from discovering which emails are registered.
- **Admin role** – delete and restock are admin-only, as the spec requires. Add/update are open to any logged-in user per the spec, while the UI only shows those forms to admins.

## My AI Usage

### Tools used
- **Claude (Anthropic, via claude.ai)** – the only AI tool I used. Raw chat links are in [PROMPTS.md](PROMPTS.md).

### How I used it

**1. As a pair-programming mentor, not just a code generator**
Full-stack development was new to me, so I used Claude to learn as I built. For each file
I asked *why* it was designed that way: why routers and services are separate, why
passwords are hashed with bcrypt, how JWT stateless auth works, why CORS is needed, and how
React state and context drive the UI. I didn't move to the next step until I could explain
the current one.

**2. To follow Test-Driven Development**
Claude drafted the test suites from the kata requirements, including edge cases I would
have missed (expired and tampered tokens, duplicate emails in different letter case,
buying the last unit twice). I committed each test file **before** its implementation, ran
it to watch it fail (Red), then added the code until it passed (Green). My commit history
shows these `test:` → `feat:` pairs for every backend feature and for the frontend
components. The backend has 52 tests at 100% coverage.

**3. For clean, SOLID design**
I asked Claude to keep each module to one responsibility:
- `routers/` only translate HTTP ⇄ Python and choose status codes
- `services/` hold the business rules and know nothing about HTTP
- `dependencies.py` provides reusable auth guards (`get_current_user`, `require_admin`)
- `api/client.js` is the only frontend file that talks to the backend

Because of this, each layer can be tested on its own, and new features extend the code
without rewriting it.

**4. For a security-first review**
With my cybersecurity background, I paid particular attention to auth and asked Claude to
check those decisions: passwords are only stored as salted bcrypt hashes, login returns the
same error for an unknown email and a wrong password (so attackers can't find which accounts
exist), the response schema never exposes password hashes, admin-only routes return 403
(not 401), and the purchase endpoint uses a single conditional `UPDATE` to prevent a race
condition that would sell the same last car twice.

**5. For debugging my environment**
Claude helped me get past real setup problems on Windows: Application Control blocking
`pip.exe` (fixed by using `python -m pip`), GitHub rejecting my push over email privacy
(switched to my noreply address), and pytest failing to import `app` (added `pythonpath`
to `pytest.ini`).

### Reflection
- **Speed with understanding:** AI let me deliver a complete, tested full-stack app in a
  stack I hadn't used before. Asking "why" at every step turned it into a learning exercise
  rather than copy-paste.
- **Tests are how I trust AI code:** AI output isn't automatically correct. Some setup steps
  failed on my machine. Writing tests first gave me an objective check: if the tests pass
  against the spec, the code does what it should, regardless of who wrote it.
- **Craft still matters:** AI can produce code quickly, but whether that code is
  well-designed, secure and readable depends on the questions you ask and what you
  accept. I learned to ask for small, single-purpose modules and meaningful names, and to
  review security decisions myself.
- **Transparency:** every commit where AI helped has a `Co-authored-by` trailer, and my full,
  unedited chats are linked in PROMPTS.md.
- **Next time:** I'd add a proper Refactor commit after each Green step and set up CI to
  run the tests on every push.

**How I used it:**
- …
- …

**Reflection:**
…
