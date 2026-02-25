# Joe Django's Art Emporium

A modern full-stack Django e-commerce application for artist Joe Django, selling limited-edition art prints and offering private custom commission services in a distinctive chibi-gothic-surreal style.

**Live demo:** [https://joe-django-art.herokuapp.com](https://joe-django-art.herokuapp.com) *(update after deployment)*

---

## Table of Contents

- [Project Overview](#project-overview)
- [Value to Users](#value-to-users)
- [User Stories](#user-stories)
- [UX & Design](#ux--design)
- [Database Schema](#database-schema)
- [Features](#features)
- [Technologies Used](#technologies-used)
- [Apps Structure](#apps-structure)
- [Local Setup](#local-setup)
- [Deployment](#deployment)
- [Testing](#testing)
- [Credits](#credits)

---

## Project Overview

Joe Django's Art Emporium is a real-world Full Stack MVC web application built with Django and PostgreSQL. It features multiple reusable apps, user authentication with purpose (persistent wishlists, commission tracking, download access), Stripe-powered e-commerce, CRUD functionality beyond authentication, JavaScript enhancements, and secure deployment.

This project was built to fulfil the requirements of the Code Institute / Gateway Qualifications Diploma in Web Application Development (Unit 4).

---

## Value to Users

| User Type | Value Proposition |
|-----------|-------------------|
| **Visitors / Collectors** | Discover and buy unique, emotionally resonant art prints instantly via Stripe checkout. Browse a curated gallery. |
| **Commission Clients** | Request fully custom bespoke artwork in Joe's signature style, with a live JS price calculator and status tracking. |
| **Joe Django (Admin)** | Manage print inventory, commission requests, order fulfilment, and file delivery via Django admin. |

### Why Authentication?

Users register/login to:
- **Persist a wishlist** of favourite prints across sessions.
- **Submit and track** custom commission requests (status updates from artist).
- **Access downloads** of purchased digital art prints (protected URLs).

---

## User Stories

1. As a **visitor**, I want to view a responsive homepage showcasing Joe Django's signature art style so I can understand the aesthetic and explore further.
2. As a **potential buyer**, I want to browse a categorized gallery of available art prints so I can find pieces that resonate with me.
3. As a **visitor**, I want to see detailed views of individual art prints (zoomable images, price) so I can evaluate before purchasing.
4. As a **registered user**, I want to add art prints to a persistent wishlist so I can return later without losing my selections.
5. As a **shopper**, I want a cart system with Stripe checkout for purchasing prints so I can complete secure test-mode payments.
6. As a **client**, I want to fill out a commission request form with a client-side quote preview (JS calculator) so I can get an instant estimate.
7. As a **logged-in client**, I want to view the status of my commissions and see updates from the artist.
8. As a **logged-in client**, I want full CRUD on my commissions -- create, view, edit, and delete requests while they are still pending.
9. As the **artist (admin)**, I want a secure dashboard to manage all commission requests, print orders, upload files, and update statuses.
10. As **any user**, I want accessible navigation, responsive design, and clear calls-to-action on any device.

---

## UX & Design

### Colour Palette

| Colour | Hex | Use |
|--------|-----|-----|
| Dark Base | `#1a1a2e` / `#0f0f1a` | Background, navbar, footer |
| Accent Rose | `#c71585` | Primary buttons, highlights |
| Accent Teal | `#00f5d4` | Prices, success states, links |
| Accent Gold | `#d4a017` | Warnings, limited edition badges |
| Text Light | `#e0e0e0` | Body text on dark backgrounds |

### Typography

- **Headings:** System serif stack / Playfair Display
- **Body:** Segoe UI, Roboto, Open Sans

### Wireframe Structure

- **Homepage** (`/`): Hero with CTAs, feature cards, CTA section.
- **Gallery** (`/gallery/`): Filterable card grid by category, click to detail page.
- **Print Detail** (`/gallery/<slug>/`): Lightbox image, price, Add to Cart, Wishlist toggle, related prints.
- **Cart** (`/shop/cart/`): HTMX-powered quantity adjustment, Stripe checkout button.
- **Commission Form** (`/commissions/new/`): Login required, JS live quote calculator.
- **Dashboard** (`/account/dashboard/`): Tabbed view - Commissions, Orders, Wishlist.

### Accessibility

- ARIA labels on navigation and interactive elements
- Alt text on all images
- Sufficient colour contrast (4.5:1 minimum)
- Keyboard-navigable interface

---

## Database Schema

### Entity Relationship Summary

```
Category (1) ----< (M) ArtPrint
User (1) ----< (M) CommissionRequest
User (1) ----< (M) Order
Order (1) ----< (M) OrderItem (M) >---- (1) ArtPrint
User (1) ---- (1) Profile
Profile (M) >----< (M) ArtPrint (wishlist)
Profile (M) >----< (M) ArtPrint (purchased_prints)
```

### Models Detail

| Model | App | Key Fields | Relationships |
|-------|-----|------------|---------------|
| **Category** | gallery | name, slug, description | Has many ArtPrints |
| **ArtPrint** | gallery | title, slug, description, image, price, is_available, limited_edition | Belongs to Category (FK) |
| **CommissionRequest** | commissions | title, commission_type, size, description, reference_images, estimated_price, status, final_file | Belongs to User (FK) |
| **Order** | shop | stripe_session_id, total_amount, status, is_completed | Belongs to User (FK) |
| **OrderItem** | shop | quantity, price (snapshot) | Belongs to Order (FK), references ArtPrint (FK) |
| **Profile** | users | wishlist (M2M ArtPrint), purchased_prints (M2M ArtPrint) | One-to-One with User |

---

## Features

### Implemented

- **Multi-app Django structure** - home, gallery, shop, commissions, users
- **User authentication** (django-allauth) with meaningful purpose
- **Gallery** - Filterable by category, detail pages with Lightbox2 image zoom
- **Wishlist** - Persistent per-user favourites (ManyToMany via Profile)
- **Shopping cart** - Session-based, HTMX-powered quantity updates without page reload
- **Stripe Checkout** - Secure test-mode payment
- **Stripe Webhook** - Reliable async payment confirmation with signature verification
- **Order confirmation email** - Sent via Django send_mail after successful payment
- **Protected downloads** - Purchased prints available via protected URL (ownership verified)
- **Commission form** - Full CRUD with crispy-forms, real-time JavaScript quote calculator
- **Commission status tracking** - View status, edit/delete while pending, download final files
- **User dashboard** - Tabbed view (Bootstrap 5 tabs) for Commissions, Orders, Wishlist
- **Responsive design** - Bootstrap 5, mobile-first, sticky navbar
- **Dark theme** - Custom CSS with chibi-gothic colour palette
- **Accessible navigation** - ARIA labels, alt text, contrast ratios, keyboard nav
- **Django admin** - Extended with list displays, filters, inline editing for all models

### Future Enhancements

- Real-time commission status notifications
- Multiple reference image uploads per commission
- Print size variant pricing
- Testimonial slider on homepage

---

## Technologies Used

### Languages

- Python 3.12
- HTML5
- CSS3
- JavaScript (ES6+)

### Frameworks & Libraries

- Django 6.0.2 (MVC web framework)
- Bootstrap 5.3.3 (responsive UI)
- HTMX 2.0.1 (immediate cart updates without reload)
- Lightbox2 (image zoom in gallery)
- Stripe.js (client-side checkout)
- Font Awesome 6.5 (iconography)

### Backend Packages

- django-allauth (authentication)
- django-environ (environment variable management)
- django-crispy-forms + crispy-bootstrap5 (form rendering)
- stripe (payment processing)
- Pillow (image handling)
- psycopg2-binary (PostgreSQL adapter)
- whitenoise (static file serving in production)
- gunicorn (WSGI HTTP server for deployment)

### Database

- SQLite3 (development)
- PostgreSQL (production)

### Tools

- Git / GitHub (version control)
- VS Code (IDE)
- Heroku / Render (deployment platform)

---

## Apps Structure

| App | Purpose | Key Models |
|-----|---------|------------|
| `home` | Homepage, static pages | -- |
| `gallery` | Art showcase, categories, detail views | Category, ArtPrint |
| `shop` | Cart, Stripe checkout, orders, webhook, downloads | Order, OrderItem |
| `commissions` | Custom request form, quote logic, CRUD | CommissionRequest |
| `users` | Profile extension, wishlist, dashboard | Profile |

---

## Local Setup

### Prerequisites

- Python 3.12+
- pip
- Git
- PostgreSQL (optional - SQLite works for development)

### Steps

```bash
# 1. Clone the repository
git clone https://github.com/yourusername/joe-django.git
cd joe-django

# 2. Create and activate a virtual environment
python -m venv venv
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Create a .env file with required variables:
# SECRET_KEY=your-secret-key
# DEBUG=True
# STRIPE_PUBLIC_KEY=pk_test_...
# STRIPE_SECRET_KEY=sk_test_...
# STRIPE_WEBHOOK_SECRET=whsec_...

# 5. Run migrations
python manage.py migrate

# 6. Create a superuser
python manage.py createsuperuser

# 7. Run the development server
python manage.py runserver
```

Visit `http://127.0.0.1:8000/` to see the site.

### Stripe Test Cards

| Card Number | Result |
|-------------|--------|
| 4242 4242 4242 4242 | Successful payment |
| 4000 0000 0000 0002 | Declined |

Use any future expiry date and any 3-digit CVC.

---

## Deployment

### Heroku

```bash
# 1. Login and create app
heroku login
heroku create joe-django-art

# 2. Add PostgreSQL
heroku addons:create heroku-postgresql:essential-0

# 3. Set environment variables
heroku config:set SECRET_KEY=your-production-secret-key
heroku config:set DEBUG=False
heroku config:set STRIPE_PUBLIC_KEY=pk_test_...
heroku config:set STRIPE_SECRET_KEY=sk_test_...
heroku config:set STRIPE_WEBHOOK_SECRET=whsec_...

# 4. Deploy
git push heroku main

# 5. Run migrations
heroku run python manage.py migrate
heroku run python manage.py createsuperuser

# 6. Open
heroku open
```

### Key Production Settings

- `DEBUG = False`
- `ALLOWED_HOSTS` includes deployment domain
- `SECRET_KEY` loaded from environment variable (not hard-coded)
- `STATIC_ROOT` configured for `collectstatic`
- WhiteNoise middleware for static file serving
- `DATABASE_URL` auto-configured by Heroku PostgreSQL add-on

---

## Testing

### Manual Testing

- All navigation links verified across pages
- Cart add/remove/update tested with HTMX
- Stripe checkout tested with test cards
- Commission CRUD tested - create, edit, delete verified
- Wishlist add/remove verified for authenticated users
- Protected download URLs verified (403 for non-purchasers)
- Responsive design tested across viewport sizes
- Django admin CRUD verified for all models

### Automated Testing

```bash
python manage.py test
```

---

## Development Diary

A chronological record of issues encountered, decisions made, and progress achieved throughout the build. Each entry is dated to provide an honest, traceable account of the development journey.

---

### Entry 1 — 13 February 2026

**Phase:** Project Initialisation
**Commit:** `fix(env): resolve pip not recognized by adding virtual environment setup`

#### Context

With the repository freshly created on GitHub and cloned locally, the first task was to install Django so that development work could begin. The course requires a Django-based full-stack application, so getting the framework installed was the essential first step.

#### Issue Encountered

When attempting to install Django from the terminal, PowerShell returned `pip : The term 'pip' is not recognized`. The `pip` package manager was not available as a standalone command on the system PATH, despite Python 3.14.2 being installed correctly.

#### Root Cause

On many Windows installations, Python is accessible via `python` or `py`, but `pip` is not automatically added to the system PATH as its own command. This is especially common when Python is installed from the Microsoft Store or when the "Add to PATH" option was not fully selected during installation.

#### Resolution

1. Confirmed Python was installed (`python --version` → Python 3.14.2).
2. Created a virtual environment using `python -m venv venv`.
3. Activated with `.\venv\Scripts\Activate.ps1`.
4. Installed Django (`pip install django` → Django 6.0.2).
5. Generated `requirements.txt` via `pip freeze`.
6. Created `.gitignore` for venv, `__pycache__`, db.sqlite3, etc.

#### Lesson Learned

Always use a virtual environment for Python projects. It solves PATH issues with `pip` and is standard professional practice — keeping dependencies project-specific, portable, and reproducible.

#### Files Changed

- `.gitignore` — created with Django/Python exclusion rules
- `requirements.txt` — generated from the virtual environment
- `Documents/` — course reference materials added

---

### Entry 2 — 13 February 2026

**Phase:** Project Initialisation
**Commit:** `fix(env): activate correct venv and create Django project`

#### Context

With Django installed (Entry 1), the next step was to scaffold the Django project using `django-admin startproject`. This generates the core project structure — settings, URL configuration, and WSGI/ASGI entry points.

#### Issue Encountered

`django-admin startproject joe_django` failed with `django-admin : The term 'django-admin' is not recognized`.

#### Root Cause

Two virtual environments existed — `venv/` (empty, manually created) and `.venv/` (containing Django, created by VS Code). The wrong one was being activated.

#### Resolution

1. Located `django-admin.exe` inside `.venv/Scripts/`.
2. Activated the correct environment (`.\.venv\Scripts\Activate.ps1`).
3. Created the Django project with `django-admin startproject joe_django .`.
4. Removed the redundant `venv/` folder.

#### Lesson Learned

When using VS Code with Python, always verify which virtual environment is active. VS Code may create `.venv` (with dot) while manual creation uses `venv` (without). Standardise on one and remove duplicates.

#### Files Changed

- `joe_django/` — Django project package created (settings.py, urls.py, wsgi.py, asgi.py, __init__.py)
- `manage.py` — Django management utility created
- `venv/` — redundant empty environment removed

---

### Entry 3 — 13 February 2026

**Phase:** Project Initialisation
**Commit:** `fix(env): activate venv before running manage.py commands`

#### Context

With the project scaffolded (Entry 2), the next steps were initial migrations and superuser creation.

#### Issue Encountered

`python manage.py createsuperuser` failed with `ModuleNotFoundError: No module named 'django'`. Same root cause as Entries 1 and 2 — `.venv` not activated in the new terminal session.

#### Resolution

1. Activated `.venv`, ran `python manage.py migrate` (18 default migrations applied, SQLite3 database created).
2. Created superuser via `python manage.py createsuperuser --noinput`.
3. Verified with `python manage.py check` — zero issues.

#### Lesson Learned

Virtual environment activation does not persist between terminal sessions. The `(.venv)` prefix confirms the environment is active — if missing, commands will fail.

#### Files Changed

- `db.sqlite3` — SQLite development database created (git-ignored)
- Superuser account created in the database

---

### Entry 4 — 13 February 2026

**Phase:** Project Initialisation
**Commit:** `fix(env): add VS Code workspace settings for automatic venv activation`

#### Context

After encountering the same venv activation issue three times (Entries 1–3), a permanent fix was needed.

#### Resolution

Created `.vscode/settings.json` with `python.defaultInterpreterPath`, `python.terminal.activateEnvironment: true`, and `terminal.integrated.env.windows` pointing to `.venv`. Updated `.gitignore` to track `.vscode/` so the fix benefits all contributors. Fresh terminal now shows `(.venv)` prefix automatically.

#### Lesson Learned

When a problem occurs three or more times, it is a workflow gap that needs a permanent fix. Configure the environment to handle it automatically rather than relying on memory.

#### Files Changed

- `.vscode/settings.json` — created with Python environment and auto-activation settings
- `.gitignore` — removed `.vscode/` from exclusions

---

### Entry 5 — 13 February 2026

**Phase:** Project Initialisation
**Commit:** `feat(auth): install django-allauth for user authentication`

#### Summary

Installed `django-allauth==0.50.0` — the industry-standard Django package for user registration, login, logout, email verification, and social authentication. First dependency install to run without environment issues, confirming the workspace configuration fix is working. Updated `requirements.txt`.

#### Files Changed

- `requirements.txt` — updated with `django-allauth==0.50.0` and its dependencies

---

### Entry 6 — 14 February 2026

**Phase:** Project Initialisation
**Commit:** `fix(auth): resolve duplicate auth app and typo in allauth config`

#### Problem

`python manage.py migrate` failed with `ImproperlyConfigured: Application labels aren't unique, duplicates: auth`.

#### Root Cause

1. `django.contrib.auth` and `django.contrib.messages` listed twice in `INSTALLED_APPS`.
2. Typo: `UTHENTICATION_BACKENDS` instead of `AUTHENTICATION_BACKENDS`.

#### Fix

Removed duplicate entries and corrected the typo. Migrations ran successfully — 7 new migrations for `account`, `sites`, and `socialaccount`.

#### Lesson Learned

When adding apps to `INSTALLED_APPS`, add below existing defaults — don't re-paste. Django won't warn about unrecognised setting names; it silently ignores them.

#### Files Changed

- `joe_django/settings.py` — removed duplicate apps, fixed `AUTHENTICATION_BACKENDS` typo

---

### Entry 7 — 14 February 2026

**Phase:** Project Initialisation
**Commit:** `feat(auth): complete allauth configuration with account settings`

#### Summary

Configured allauth account behaviour: console email backend for development, `username_email` authentication method, mandatory email with verification, signup email confirmation field, minimum username length of 4, login/redirect URLs. Verified login/signup pages render correctly.

#### Files Changed

- `joe_django/settings.py` — added allauth account configuration settings

---

### Entry 8 — 19 February 2026

**Phase:** Authentication Templates
**Commit:** `feat(templates): add allauth templates and Bootstrap base layout`

#### Summary

Copied the full set of allauth default templates into `templates/allauth/` for branding customisation. Created `templates/base.html` with auth-aware navigation and `templates/allauth/base.html` with Bootstrap 4.6 CDN. Updated `settings.py` TEMPLATES DIRS.

#### Files Changed

- `templates/base.html` — project-level base template with messages and auth-aware menu
- `templates/allauth/base.html` — Bootstrap 4.6 base layout for allauth pages
- `templates/allauth/account/` — all account templates
- `templates/allauth/socialaccount/` — all social account templates
- `joe_django/settings.py` — added template directories to TEMPLATES DIRS

---

### Entry 9 — 19 February 2026

**Phase:** Authentication Templates
**Commit:** `refactor(templates): restructure base.html with Django template blocks`

#### Summary

Refactored `templates/allauth/base.html` from flat HTML into properly block-structured Django template with named blocks for `meta`, `extra_meta`, `corecss`, `extra_css`, `corejs`, `extra_js`, and `extra_title`. Added fixed-top header container, messages container, and page-specific title support.

#### Files Changed

- `templates/allauth/base.html` — restructured with named template blocks

---

### Entry 10 — 19 February 2026

**Phase:** Home App & Page Structure
**Commit:** `feat(home): create home app with index view and wire up base template`

#### Summary

Created the `home` app using `python manage.py startapp home`. Set up the full request cycle: URL routing (`''` → `index` view → `home/index.html` template). Added `page_header`, `content`, and `postloadjs` blocks to `base.html`. Updated `settings.py` with `import os`, `os.path.join()` for DIRS, and `'home'` in `INSTALLED_APPS`. Verified homepage renders at `http://localhost:8000/`.

#### Files Changed

- `home/` — new Django app (8 files)
- `home/templates/home/index.html` — homepage template
- `joe_django/urls.py` — added home app URL include
- `joe_django/settings.py` — added `import os`, `os.path.join` for DIRS, `'home'` in INSTALLED_APPS
- `templates/base.html` — added `page_header`, `content`, `postloadjs` blocks

---

### Entry 11 — 23 February 2026

**Phase:** Project Structure Review & Fixes
**Commit:** `fix(templates): fix template inheritance chain and project config issues`

#### Summary

Full project structure evaluation resolving six issues:

1. **Template duplication eliminated** — `templates/allauth/base.html` replaced with `{% extends "base.html" %}`.
2. **Template inheritance chain fixed** — `templates/allauth/account/base.html` rebuilt to extend `base.html` with auth menu and `inner_content` block.
3. **Child templates updated** — All 20 allauth child templates updated from `{% block content %}` to `{% block inner_content %}`.
4. **`DEFAULT_AUTO_FIELD` added** — `BigAutoField` setting added for Django 6.0 compatibility.
5. **Static files directory created** — `STATICFILES_DIRS` configured, `static/` directory created.
6. **`requirements.txt` encoding fixed** — Regenerated with UTF-8 (was UTF-16 from PowerShell redirect).

#### Template Inheritance Chain (After Fix)

```
templates/base.html                          ← Root: Bootstrap CDN, nav, blocks
  └── templates/allauth/base.html            ← {% extends "base.html" %}
  └── templates/allauth/account/base.html    ← {% extends "base.html" %}, auth menu + inner_content
      └── account/login.html etc.            ← {% extends "account/base.html" %}, fills inner_content
  └── home/templates/home/index.html         ← {% extends "base.html" %}, fills content
```

#### Files Changed

- `templates/allauth/base.html` — replaced duplicate HTML with `{% extends "base.html" %}`
- `templates/allauth/account/base.html` — rebuilt with auth menu and `inner_content` block
- `templates/allauth/account/*.html` (15 files) — block name updated
- `templates/allauth/socialaccount/*.html` (5 files) — block name updated
- `joe_django/settings.py` — added `DEFAULT_AUTO_FIELD` and `STATICFILES_DIRS`
- `requirements.txt` — regenerated with UTF-8 encoding
- `static/.gitkeep` — created

---

### Entry 12 — 25 February 2026

**Phase:** Full Application Build
**Commit:** `feat: build complete e-commerce platform with gallery, shop, commissions, and user dashboard`

#### Context

With the project foundation in place (Django scaffold, allauth authentication, template inheritance chain, home app), the full application needed to be built. This entry covers the creation of all four remaining apps, all data models, views, templates, Stripe integration, HTMX cart behaviour, commission CRUD with JavaScript quote calculator, user dashboard, Bootstrap 5 upgrade, custom dark theme CSS, and deployment preparation. This was the largest single development session of the project.

**Note on commit practice:** Ideally, each feature below would have been its own atomic commit to create a traceable development journey. Building everything in a single session without incremental commits is not best practice — future work will return to smaller, focused commits. This entry documents the full scope of changes to maintain an honest development record.

#### What Was Built

**1. Four New Django Apps Created**

```bash
python manage.py startapp gallery
python manage.py startapp shop
python manage.py startapp commissions
python manage.py startapp users
```

Each app registered in `INSTALLED_APPS` with its own `urls.py`, `admin.py`, `models.py`, `views.py`, `forms.py` (where applicable), and templates directory.

**2. Data Models (6 models across 4 apps)**

| Model | App | Purpose | Key Fields |
|-------|-----|---------|------------|
| `Category` | gallery | Art categorisation | name, slug (auto-generated), description |
| `ArtPrint` | gallery | Print products | title, slug, image, price, category (FK), is_available, limited_edition, size_options |
| `CommissionRequest` | commissions | Custom art requests | user (FK), title, commission_type (5 choices), size, description, reference_images, estimated_price, status (6-state workflow), artist_notes, final_file |
| `Order` | shop | Purchase records | user (FK, nullable for guest), stripe_session_id, total_amount, status, is_completed |
| `OrderItem` | shop | Line items | order (FK), art_print (FK), quantity, price (snapshot at time of purchase) |
| `Profile` | users | User extension | user (OneToOne), wishlist (M2M → ArtPrint), purchased_prints (M2M → ArtPrint) |

Profile created automatically via `post_save` signal on User model. All models have Django admin configurations with `list_display`, `list_filter`, `search_fields`, and `list_editable` where appropriate. OrderItem uses `TabularInline` inside OrderAdmin.

All migrations created and applied successfully (`python manage.py makemigrations` + `python manage.py migrate`). `python manage.py check` returned zero issues.

**3. Gallery App — Views & Templates**

- **Gallery list** (`/gallery/`) — Filterable by category via query parameter (`?category=slug`). Uses `select_related('category')` for query optimisation. Category filter pills rendered dynamically. Responsive Bootstrap 5 card grid with hover zoom effect.
- **Art detail** (`/gallery/<slug>/`) — Full print detail with Lightbox2 image zoom, breadcrumb navigation, price display, Add to Cart form, wishlist toggle (authentication-aware — shows login prompt for anonymous users), and related prints grid (same category, excludes current print, limited to 4).
- **Wishlist** — `add_to_wishlist` and `remove_from_wishlist` views (both `@login_required`), operating on the Profile M2M field.

**4. Shop App — Cart, Stripe Checkout, Webhook, Downloads**

- **Session-based cart** (`shop/utils.py`) — Helper functions: `get_cart`, `add_to_cart`, `remove_from_cart`, `update_cart_quantity`, `get_cart_total`, `clear_cart`. Cart stored in `request.session['cart']` as `{art_id: {quantity, price, title, slug}}`.
- **Context processor** (`shop/contexts.py`) — Injects `cart_item_count`, `cart_total`, and `stripe_public_key` into every template. Registered in `settings.py` TEMPLATES context_processors.
- **Cart page** (`/shop/cart/`) — Table layout with HTMX-powered quantity inputs (`hx-post`, `hx-target`, `hx-swap`). Quantity changes update row totals and cart summary without page reload. Stripe.js checkout button with loading state.
- **HTMX partial** (`shop/includes/cart_table.html`) — Rendered server-side on quantity update, swapped into DOM via HTMX. Uses `hx-swap-oob` for out-of-band total update.
- **Stripe Checkout** — `create_checkout_session` view builds `stripe.checkout.Session` with line items from cart. Creates Order + OrderItems in database with `status='pending'`. Redirects to Stripe-hosted checkout page.
- **Payment success** (`/shop/success/`) — Retrieves Stripe session, verifies payment status, marks order as completed, grants download access (adds prints to `Profile.purchased_prints` M2M), sends confirmation email, clears cart.
- **Stripe webhook** (`/shop/webhook/`) — `@csrf_exempt`, verifies signature with `STRIPE_WEBHOOK_SECRET`, handles `checkout.session.completed` event as backup for the success view.
- **Email confirmation** — `_send_order_confirmation()` sends itemised order email via Django `send_mail`.
- **Protected downloads** (`/shop/download/<art_id>/`) — `@login_required`, verifies ownership via `purchased_prints` M2M, serves file via `FileResponse`.

**5. Commissions App — CRUD & JavaScript Quote Calculator**

- **Commission form** (`/commissions/new/`) — `@login_required`, crispy-forms rendering with `crispy_bootstrap5` template pack. ModelForm with custom widget attributes (CSS classes, IDs for JS binding, placeholders).
- **Server-side pricing** — `_calculate_price()` function: base price by type (icon £30, logo £50, poster £80, portrait £100, other £60), size multiplier (small ×1, medium ×1.5, large ×2, xl ×2.5), description complexity (length-based: +£10 at 200 chars, +£25 at 500 chars). Price stored on model at save time.
- **Client-side JS calculator** — Mirrors server-side logic exactly. Listens on `change`/`input` events for type, size, and description fields. Updates a sticky preview card showing base price, size multiplier, complexity add-on, and estimated total in real time.
- **Edit** (`/commissions/<pk>/edit/`) — `@login_required`, ownership check, editability check (only `pending`/`quoted` status).
- **Delete** (`/commissions/<pk>/delete/`) — `@login_required`, ownership check, editability check, POST confirmation page.

**6. Users App — Profile & Dashboard**

- **Profile model** — OneToOneField to User with `post_save` signal for automatic creation. M2M fields for wishlist and purchased prints.
- **Dashboard** (`/account/dashboard/`) — `@login_required`. Queries orders (completed, with `prefetch_related` for items and art prints), commissions (all user's), wishlist, and purchased prints.
- **Tabbed interface** — Bootstrap 5 nav-tabs with three panels:
  - **Commissions tab** — Table with title, type, status (colour-coded badges), date, and Edit/Delete action links (shown only for editable commissions). "Request Commission" CTA if no commissions exist.
  - **Orders tab** — Table with order number, date, total, status. Expandable item list with download links for purchased prints.
  - **Wishlist tab** — Card grid with Add to Cart and Remove from Wishlist buttons.

**7. Base Template & Homepage Overhaul**

- **Bootstrap 4 → 5 upgrade** — Replaced Bootstrap 4.6 CDN with Bootstrap 5.3.3 (CSS + JS bundle). Removed jQuery dependency. Updated navbar to BS5 syntax (`data-bs-toggle`, `navbar-expand-lg`).
- **Dark navbar** — `#1a1a2e` background, brand text, responsive collapse menu.
- **Auth-aware navigation** — Logged in: Dashboard, Logout. Anonymous: Register, Login. Always: Gallery, Commissions, Cart (with item count badge).
- **Cart badge** — Real-time item count from context processor, displayed as Bootstrap badge on nav cart link.
- **Footer** — Sticky footer with quick links (Gallery, Commissions, Dashboard), social media icon links (Font Awesome), copyright.
- **Messages** — Bootstrap 5 dismissible alerts for Django messages framework, auto-mapped message tags to alert classes.
- **External libraries loaded** — Font Awesome 6.5.1, HTMX 2.0.1, Lightbox2 CSS/JS (via CDN).
- **Homepage** (`home/index.html`) — Hero section with gradient text and dual CTAs (Browse Gallery, Request Commission), three feature cards (Limited Edition Prints, Custom Commissions, Your Collection), bottom CTA section.

**8. Custom CSS Dark Theme**

Created `static/css/custom.css` with:
- CSS custom properties: `--dark-base (#1a1a2e)`, `--accent-rose (#c71585)`, `--accent-teal (#00f5d4)`, `--accent-gold (#d4a017)`
- Hero gradient text effect
- Card hover lift/shadow animations
- Gallery image hover zoom (scale 1.05)
- Custom button colours matching palette
- Dark form control styling
- Quote preview card styling for commission calculator
- HTMX loading indicator
- Responsive media queries

**9. Settings & Configuration**

- **django-environ** integration — `.env` file with `SECRET_KEY`, `DEBUG`, `ALLOWED_HOSTS`, `STRIPE_PUBLIC_KEY`, `STRIPE_SECRET_KEY`, `STRIPE_WEBHOOK_SECRET`, `DEFAULT_FROM_EMAIL`.
- **New INSTALLED_APPS** — `gallery`, `shop`, `commissions`, `users`, `crispy_forms`, `crispy_bootstrap5`.
- **WhiteNoise** middleware added for production static file serving.
- **Context processors** — `shop.contexts.cart_contents` added to TEMPLATES.
- **Crispy forms** — `CRISPY_ALLOWED_TEMPLATE_PACKS = 'bootstrap5'`, `CRISPY_TEMPLATE_PACK = 'bootstrap5'`.
- **Stripe settings** — Keys loaded from environment variables.
- **Media files** — `MEDIA_URL = '/media/'`, `MEDIA_ROOT = os.path.join(BASE_DIR, 'media')`.
- **Delivery constants** — `FREE_DELIVERY_THRESHOLD = 50`, `STANDARD_DELIVERY_PERCENTAGE = 10`.
- **Database** — Conditional: `DATABASE_URL` env var for PostgreSQL in production, SQLite3 fallback for development.

**10. URL Configuration**

Root `joe_django/urls.py` updated with:
- `admin/` → Django admin
- `accounts/` → django-allauth
- `gallery/` → gallery app
- `shop/` → shop app
- `commissions/` → commissions app
- `account/` → users app (dashboard)
- `''` → home app
- Media file serving in DEBUG mode via `static(MEDIA_URL, document_root=MEDIA_ROOT)`

**11. Deployment Preparation**

- `Procfile` — `web: gunicorn joe_django.wsgi --log-file -`
- `runtime.txt` — `python-3.12.3`
- `.gitignore` — Added `.env` and `staticfiles/`
- `requirements.txt` — Frozen with all installed packages (django-environ, stripe, Pillow, psycopg2-binary, whitenoise, crispy-forms, crispy-bootstrap5)

**12. README Rewrite**

Complete README rewrite to document the finished application: Table of Contents, Project Overview, Value to Users, User Stories, UX & Design (colour palette, typography, wireframes, accessibility), Database Schema (ERD + relationships table), Features (implemented + future), Technologies Used, Apps Structure, Local Setup, Deployment (Heroku), Testing, Credits.

#### Dependencies Installed

```
django-environ, stripe, Pillow, psycopg2-binary, whitenoise,
django-crispy-forms, crispy-bootstrap5
```

Note: `gunicorn` listed in requirements.txt for deployment but not installed locally (Linux/macOS only).

#### Verification

- `python manage.py makemigrations gallery shop commissions users` — all 4 migration files created successfully
- `python manage.py migrate` — all migrations applied
- `python manage.py check` — "System check identified no issues (0 silenced)"
- Dev server started, homepage verified rendering (hero, features, CTA, nav, footer)
- Gallery page verified rendering (category filters, empty state)
- Cart page verified rendering (empty cart state, Stripe button)

#### Files Changed

**New apps (4 apps, ~40 files):**
- `gallery/` — `__init__.py`, `admin.py`, `apps.py`, `models.py`, `urls.py`, `views.py`, `migrations/`, `templates/gallery/gallery_list.html`, `templates/gallery/art_detail.html`
- `shop/` — `__init__.py`, `admin.py`, `apps.py`, `models.py`, `urls.py`, `views.py`, `utils.py`, `contexts.py`, `migrations/`, `templates/shop/cart_detail.html`, `templates/shop/includes/cart_table.html`, `templates/shop/payment_success.html`
- `commissions/` — `__init__.py`, `admin.py`, `apps.py`, `models.py`, `urls.py`, `views.py`, `forms.py`, `migrations/`, `templates/commissions/commission_form.html`, `templates/commissions/commission_confirm_delete.html`
- `users/` — `__init__.py`, `admin.py`, `apps.py`, `models.py`, `urls.py`, `views.py`, `migrations/`, `templates/users/dashboard.html`

**Modified files:**
- `joe_django/settings.py` — django-environ, new apps, WhiteNoise, Stripe, crispy-forms, media, context processors
- `joe_django/urls.py` — all app URL includes + media serving
- `templates/base.html` — complete rewrite (Bootstrap 5, dark theme, auth-aware nav, cart badge, footer)
- `home/templates/home/index.html` — hero section, feature cards, CTA
- `.gitignore` — added `.env`, `staticfiles/`
- `requirements.txt` — all new dependencies frozen

**New files:**
- `static/css/custom.css` — dark theme stylesheet
- `.env` — environment variables (git-ignored)
- `Procfile` — Heroku process file
- `runtime.txt` — Python version specification

---

### Entry 13 — 25 February 2026

**Phase:** Content & Data Population
**Commit:** `feat(gallery): add import_prints management command and populate gallery with 25 Molishi Mysticals prints`

#### Context

With the gallery app fully built (Entry 12), the next step was populating it with real artwork. The artist's image collection (91 files) was stored on an external hard drive at `F:\David Folders\Pictures\Molishi Collection`. Rather than manually adding each print through Django admin, a custom management command was the efficient approach for a bulk import.

#### What Was Built

Created `gallery/management/commands/import_prints.py` — a Django management command that:

1. Scans a specified source folder for image files (`.jpg`, `.jpeg`, `.png`, `.webp`, `.gif`, `.bmp`)
2. Cleans filenames into human-readable titles (strips `Molishi_Mysticals_` prefix, replaces underscores with spaces, removes trailing variant numbers, applies title case)
3. Creates a Category record if one doesn't exist
4. Copies each image into `media/prints/`
5. Creates an ArtPrint database record with title, auto-generated slug, description, price, and category
6. Skips duplicate slugs to avoid re-importing the same artwork twice
7. Supports `--dry-run` to preview what would be imported without making changes
8. Accepts `--category` and `--price` arguments for customisation

#### Import Results

```
Source: F:\David Folders\Pictures\Molishi Collection (root files only)
Total images found: 91
Unique prints imported: 25
Variant duplicates skipped: 66 (images with same base name, different variant number)
Category created: Molishi Mysticals
Default price: £50.00
```

The 66 skipped files were variant versions of the same artwork (e.g., `_0.jpg`, `_1.jpg`, `_2.jpg`) — the command correctly imported only the first variant for each unique title.

#### Verification

- Gallery page renders all 25 prints as Bootstrap cards with images
- Image URLs correctly point to `/media/prints/` served by Django's dev server
- Category filter pill "Molishi Mysticals" appears and filters correctly
- Art detail pages accessible via slug URLs

#### Files Changed

- `gallery/management/__init__.py` — package initialiser
- `gallery/management/commands/__init__.py` — package initialiser
- `gallery/management/commands/import_prints.py` — bulk import management command

---

### Entry 14 — 25 February 2026

**Phase:** Homepage Redesign & New Pages
**Commit:** `feat(home): redesign homepage with artist portfolio banner stack and add About + Contact pages`

#### Context

With the gallery populated (Entry 13), the site needed a homepage that looks and feels like an artist's portfolio — not a generic e-commerce landing page. Inspired by artist portfolio sites (stacked full-width image banners with bold text overlays linking to each section), the homepage was rebuilt from scratch.

#### What Was Built

**1. Homepage Banner Stack**

Replaced the hero + feature cards + CTA layout with four full-width stacked banner sections, each using a Molishi Mysticals artwork as the background:

| Banner | Links To | Background Image |
|--------|----------|------------------|
| W O R K | Gallery (artwork showcase) | Castaway in a dark eerie ocean |
| S T O R E | Gallery (print shop) | Butterfly spirits on the water |
| A B O U T | About page | Shaman in a circle of stone |
| C O N T A C T | Contact page | Vibrant birthday celebration |

Each banner features: background image with dark overlay, bold spaced-letter white text, hover effects (image scale 1.05, overlay lightens, letter-spacing expands, rose glow on text shadow). Fully responsive — banners shrink on mobile.

**2. About Page** (`/about/`)

- Hero section with artwork background and gradient overlay
- Artist bio with featured artwork image alongside text
- "The Process" section — 4-step visual breakdown (Concept → Sketch → Render → Print)
- Stats/facts row (25+ prints, infinite imagination, 100% original, 1 artist)

**3. Contact Page** (`/contact/`)

- Hero section with lanterns artwork background
- Contact form (name, email, subject, message) with Django form handling and messages
- Sidebar with commission link, email, response time info
- Social media icon buttons with hover effects

**4. Navigation Overhaul**

- Nav links updated: Work, Store, About, Contact (right: Cart, Dashboard/Login)
- Brand text restyled: uppercase with letter-spacing, rose colour (matching Tom Lewis portfolio style)
- Removed Font Awesome icons from nav links for cleaner typography
- Footer updated with new page links

**5. CSS Overhaul**

- Body background changed from flat colour to 3-part gradient (`#1a1a2e → #2d1b3a → #16213e`), fixed attachment
- Navbar glass effect: semi-transparent with backdrop blur and subtle rose border
- New banner stack styles with hover animations
- About/Contact hero sections with gradient overlays
- Contact form card, social link buttons, process step cards — all with glass-morphism effect
- Responsive breakpoints for banner height and letter-spacing

#### Files Changed

- `home/templates/home/index.html` — complete rewrite with banner stack layout
- `home/templates/home/about.html` — **new** About page template
- `home/templates/home/contact.html` — **new** Contact page template
- `home/views.py` — added `about()` and `contact()` views (contact handles POST)
- `home/urls.py` — added `about/` and `contact/` URL paths
- `templates/base.html` — navbar brand restyled, nav links updated (Work/Store/About/Contact), footer links updated
- `static/css/custom.css` — major overhaul: 3-part gradient body, glass navbar, banner stack, about/contact page styles, responsive adjustments

---

### Entry 15 — 25 February 2026

**Phase:** Store Page, Navbar & Footer Visual Refinement
**Commit:** `feat(ui): redesign store grid, navbar typography and footer layout for clean portfolio aesthetic`

#### Context

With the homepage banner stack complete, the store/gallery page still looked like a generic Bootstrap card grid. Inspired by professional artist portfolio shops (clean image grids, minimal chrome, elegant typography), the store page, navbar, and footer were all redesigned for a cohesive, refined look.

#### What Was Built

**1. Store Page Redesign**

Replaced Bootstrap card grid with a custom CSS Grid store layout:

- Clean 3-column grid with 1:1 aspect ratio images
- No card borders, shadows, or buttons — images speak for themselves
- Title and price displayed beneath each image in clean Inter font
- Limited edition count shown subtly in gold
- Category filter tabs at top (underline-style, not pill buttons)
- Page header with Playfair Display serif title and uppercase subtitle
- Hover effect: subtle image scale (1.04) with slight opacity fade
- Fully responsive: 2 columns on tablet, 1 on mobile

**2. Navbar Redesign**

- Brand name "Joe Django" set in Playfair Display serif font at 2rem, white, with subtle letter-spacing
- Hover on brand transitions to rose colour
- All nav links moved to the right (ms-auto) in a single unified list
- Links styled in Inter font, 0.85rem, uppercase with wide letter-spacing
- Hover underline animation (scaleX transform) on each link
- Removed Font Awesome icons from Cart and Dashboard links for cleaner look
- Removed pink border-bottom from navbar

**3. Footer Redesign**

- Horizontal flexbox layout: brand left, links center, social icons right
- Brand in Playfair Display serif, tagline in Inter uppercase
- Links displayed horizontally with generous spacing (2.5rem gap)
- Social icons displayed inline with subtle hover to white
- Bottom bar with copyright in small, light, spaced text
- Responsive: stacks vertically and centers on mobile

**4. Typography System**

- Added Google Fonts: Playfair Display (brand, headings) + Inter (body, UI elements)
- Body font changed from Segoe UI to Inter with font-weight 300 for lighter feel
- Consistent letter-spacing and text-transform across all UI elements

#### Files Changed

- `templates/base.html` — Google Fonts added, navbar restructured (single nav list, Playfair brand, clean links), footer rebuilt (flex layout, brand/links/social horizontal)
- `gallery/templates/gallery/gallery_list.html` — complete rewrite: CSS Grid store layout, category tabs, clean image items with title/price below
- `static/css/custom.css` — new `.site-navbar`, `.site-brand`, `.site-nav-links` styles; new `.store-page`, `.store-grid`, `.store-item`, `.store-tabs` styles; new `.site-footer`, `.footer-main`, `.footer-links`, `.footer-social` styles; responsive breakpoints updated for store grid and footer

---

*Further entries will be added as development continues.*

---

## Credits

### Technologies & Libraries

- [Django](https://www.djangoproject.com/)
- [Bootstrap 5](https://getbootstrap.com/)
- [HTMX](https://htmx.org/)
- [Stripe](https://stripe.com/)
- [Lightbox2](https://lokeshdhakar.com/projects/lightbox2/)
- [Font Awesome](https://fontawesome.com/)
- [django-allauth](https://django-allauth.readthedocs.io/)
- [django-crispy-forms](https://django-crispy-forms.readthedocs.io/)
- [WhiteNoise](http://whitenoise.evans.io/)

### Content & Media

- All artwork by Joe Django (used with permission)
- Code written by David Wells for Code Institute Diploma project

### Acknowledgements

- Code Institute for project guidance and learning materials
- Django documentation community
