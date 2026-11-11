# Khatabook Backend (Django + MySQL)

REST API backend for the Dukaan Khata app, matching the prototype's features:
multi-business ledgers, customers & entries, inventory, GST billing, staff,
devices, notifications, and settings.

## Stack

- Python 3.10, Django 4.2 LTS, Django REST Framework
- MySQL (XAMPP's MariaDB 10.4, accessed via PyMySQL)
- JWT auth (`djangorestframework-simplejwt`)

Django 4.2 is pinned deliberately — Django 5.x requires MariaDB 10.5+, but
XAMPP ships MariaDB 10.4.

## Setup

```
cd backend
venv\Scripts\activate          # Windows
pip install -r requirements.txt
```

Make sure XAMPP's MySQL is running, then the `khatabook` database (already
created) and `.env` (already present with default XAMPP root/no-password
creds) are picked up automatically.

```
python manage.py migrate
python manage.py createsuperuser --mobile <mobile>
python manage.py runserver
```

API base URL: `http://127.0.0.1:8000/api/`
Admin panel: `http://127.0.0.1:8000/admin/`

## Auth

- `POST /api/auth/register/` — `{mobile, password, name, business_name?, business_type?}` → creates user + first business, returns `{user, access, refresh}`
- `POST /api/auth/login/` — `{mobile, password}` → `{access, refresh}`
- `POST /api/auth/login/refresh/` — `{refresh}` → `{access}`
- `GET/PATCH /api/auth/me/` — profile & settings (name, language, app_lock, pin, auto_backup, current_business)
- `POST /api/auth/verify-pin/` — `{pin}` → `{valid}`

All other endpoints require `Authorization: Bearer <access>`.

## Businesses

- `GET/POST /api/businesses/`
- `GET/PATCH/DELETE /api/businesses/{id}/`
- `POST /api/businesses/{id}/switch/` — sets as the user's current business
- `GET /api/businesses/{id}/summary/` — `{given, received, due, advance}`
- `GET /api/businesses/{id}/report/` — summary + customer count + top due customer
- `GET /api/businesses/{id}/outstanding_summary/` — per-customer balances, sorted

## Staff (business members)

- `GET/POST /api/businesses/{id}/staff/`
- `GET/PATCH/DELETE /api/businesses/{id}/staff/{id}/` (owner only for write)

## Customers & Ledger

- `GET/POST /api/businesses/{id}/customers/` (supports `?q=` search)
- `GET/PATCH/DELETE /api/businesses/{id}/customers/{id}/`
- `GET /api/businesses/{id}/customers/{id}/statement/` — full entry history + totals
- `GET/POST /api/businesses/{id}/customers/{cid}/entries/` — `{type: given|received, amount, note, date}`
- `GET/PATCH/DELETE /api/businesses/{id}/customers/{cid}/entries/{id}/`

## Inventory

- `GET/POST /api/businesses/{id}/inventory/`
- `GET/PATCH/DELETE /api/businesses/{id}/inventory/{id}/`
- `GET /api/businesses/{id}/inventory/report/` — items + low stock count

## Billing

- `GET/POST /api/businesses/{id}/bills/` — `{customer?, gst_percent, items: [{inventory_item?, name, qty, price}]}`
  (creating a bill auto-deducts stock for any item linked to `inventory_item`)
- `GET/DELETE /api/businesses/{id}/bills/{id}/`

## Devices & Notifications (per logged-in user)

- `GET/POST/DELETE /api/devices/`
- `GET/POST /api/notifications/`, `POST /api/notifications/{id}/mark_read/`, `POST /api/notifications/mark-all-read/`

## Access control

A user can access a business if they own it or have a `BusinessMembership`
row for it. Only the owner can edit/delete the business or manage staff.
All nested resources (customers, entries, inventory, bills, staff) are
scoped to businesses the requesting user can access — enforced in every
viewset's `get_queryset`/`get_business`, not just at the URL level.

## Next steps (not yet built)

- Real OTP SMS login (currently mobile + password)
- Reminders (SMS/WhatsApp send) — model not yet added
- UPI QR payment integration — needs a payment gateway account
- Cloud backup/export job — `auto_backup`/`last_backup_at` fields exist on
  the user but no backend job triggers them yet
- Wiring the React/vanilla-JS frontend (`dukaan-khata.html`,
  `latest update/dukaan-khata-react-apk/`) to call this API instead of
  `localStorage`
