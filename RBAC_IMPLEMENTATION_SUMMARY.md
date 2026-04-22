# RBAC Implementation Summary

## Original Task

The test task asked to add role-based access control to the FastAPI full-stack template.

Required roles:

- `admin`
- `manager`
- `member`

Required permission matrix:

| Action | admin | manager | member |
| --- | --- | --- | --- |
| List all users | yes | yes | no |
| Create user | yes | no | no |
| View metrics | yes | yes | no |
| View/update own profile | yes | yes | yes |
| View/update/delete any profile | yes | no | no |

The implementation should enforce permissions in the backend, reflect them in the frontend UI, hide unauthorized controls, show a friendly forbidden/access-denied state, add focused tests, and update README documentation.

## Plan We Chose

- Replace the existing `is_superuser` flag with a single `role` field.
- Migrate existing superusers to `admin` and all other users to `member`.
- Default new signups to `member`.
- Keep backend authorization as the source of truth.
- Use frontend capability helpers only to improve UX.
- Add a simple protected metrics page and backend endpoint.
- Update only the root README for documentation.

## What Was Implemented

Backend:

- Added `UserRole` enum with `admin`, `manager`, and `member`.
- Replaced `is_superuser` with `role` in user models and API schemas.
- Added role helpers in `backend/app/api/deps.py`:
  - `require_roles(...)`
  - `is_admin(...)`
  - `get_current_active_admin`
- Updated user routes:
  - `admin` and `manager` can list users.
  - only `admin` can create, update, or delete other users.
  - all authenticated users can view/update their own profile.
- Updated item routes so only `admin` keeps global item access.
- Added `/api/v1/metrics/`, available to `admin` and `manager`.
- Added an Alembic migration that adds `role`, backfills it from `is_superuser`, and drops `is_superuser`.
- Updated initial seed data so `FIRST_SUPERUSER` is created as `admin`.

Frontend:

- Added role capability helpers in `frontend/src/authz.ts`.
- Updated sidebar visibility:
  - `admin` and `manager` see Users and Metrics.
  - `member` does not see protected links.
- Updated the Users page:
  - managers can view the user list.
  - only admins see Add/Edit/Delete user controls.
  - role badges now display `role`.
- Added a `/metrics` page.
- Added friendly Access Denied handling for unauthorized direct navigation.
- Updated generated API client types/services for `role` and `MetricsService`.

Tests and docs:

- Updated backend user tests from `is_superuser` to `role`.
- Added manager/member authorization coverage.
- Added metrics route tests.
- Updated root `README.md` with:
  - permission matrix
  - local run instructions
  - migration instructions
  - test instructions
  - seed data notes
  - authorization architecture notes

## Verification Performed

Frontend build:

```bash
npm run build --workspace frontend
```

Result: passed.

Notes:

- Vite warned that Node.js `20.15.0` is below the preferred `20.19+`, but the build completed successfully.
- Vite also reported the existing large chunk warning.

Backend syntax check:

```bash
python -m compileall app tests
```

Result: passed.

Full backend tests were not run in this environment because the local Python environment did not have the FastAPI dependencies installed, and Docker daemon access was unavailable.

## How To Run Locally

Start Docker Desktop first, then run:

```bash
docker compose up -d
```

Apply migrations:

```bash
docker compose exec backend alembic upgrade head
```

Open:

- Frontend: http://localhost
- Backend API docs: http://localhost/docs
- Mailcatcher: http://localhost:1080

Default admin credentials come from `.env`:

```env
FIRST_SUPERUSER=admin@example.com
FIRST_SUPERUSER_PASSWORD=changethis
```

Run backend tests:

```bash
docker compose exec backend bash scripts/test.sh
```

## Important Files Changed

- `backend/app/models.py`
- `backend/app/api/deps.py`
- `backend/app/api/routes/users.py`
- `backend/app/api/routes/items.py`
- `backend/app/api/routes/metrics.py`
- `backend/app/alembic/versions/5f6a1b2c3d4e_replace_is_superuser_with_role.py`
- `frontend/src/authz.ts`
- `frontend/src/routes/_layout/admin.tsx`
- `frontend/src/routes/_layout/metrics.tsx`
- `frontend/src/components/Sidebar/AppSidebar.tsx`
- `frontend/src/components/Admin/AddUser.tsx`
- `frontend/src/components/Admin/EditUser.tsx`
- `frontend/src/components/Admin/UserActionsMenu.tsx`
- `frontend/src/components/Common/ErrorComponent.tsx`
- `backend/tests/api/routes/test_users.py`
- `backend/tests/api/routes/test_metrics.py`
- `README.md`

