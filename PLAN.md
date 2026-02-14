# Authentimed – Implementation Plan

## 1. Remove “Combined” Image (Template + QR Only)

**Goal:** Only merge the QR with the template. Do not overlay the hidden/PAN image onto the packaging.

| Action | Details |
|--------|--------|
| Remove combined/final image flow | Delete `overlay_hidden_on_packaged`, `GENERATED_COMBINED`, and all logic that creates or returns a “combined” (template + QR + hidden) image. |
| Keep single packaging image | **Packaged image** = template + QR only (existing `replace_qr` in `qr_overlay.py`). This is the only “merged” image; store and serve it as the main product image. |
| Keep other artifacts as-is | Continue generating and storing: QR image, hidden (PAN) code image, red/blue/green reveal images. Use them only for verification, not for merging onto the pack. |
| Frontend | Remove “Combined image” / “Final” from UI. Show only **Packaged** (template+QR), plus optional links to hidden/reveals for debugging. |

**Files to touch:** `backend/app.py`, `backend/qr_overlay.py`, `frontend/src/components/ResultCard.jsx`.

---

## 2. Manufacturer Flow (Unchanged Intent, Clearer Steps)

**Flow:**

1. Manufacturer uploads **template** (image).
2. Backend saves template (e.g. `templates/{OWNER_ADDRESS}.png`).
3. Backend generates:
   - **Product ID** (e.g. `MEDICINEX-{uuid8}`).
   - **QR** image encoding product_id; save in `generated/qr/`.
   - **Embedded (PAN) code** via `generate_code()`; store in Supabase (see §4) linked to `product_id`.
   - **Hidden code image** (PAN format); save in `generated/hidden/`.
   - **Reveal images** (red/blue/green); save in `generated/reveals/`.
4. **Merge template + QR only** → save as **packaged** image in `generated/packaged/` (no hidden overlay).
5. **Register product on-chain** (`register_product(product_id)`).
6. Return to client: product_id, packaged image URL, hidden/reveal URLs, PAN code (for reference). No “combined” URL.

---

## 3. Supabase DB: Schema for Verification and Single-Scan Rules

Use **Supabase (PostgreSQL)** via existing `DATABASE_URL` in backend. Add/ensure these concepts:

### 3.1 Product–Code Link (for QR + embedded code verification)

- **Table `products`** (or extend existing usage):
  - `product_id` (PK) – e.g. `MEDICINEX-xxxxxxxx`.
  - `pan_code` – PAN-format code tied to this product (used for “strip” verification).
  - `created_at` (optional).
- When manufacturer generates a product: insert/update `product_id` and `pan_code` so pharmacist/consumer can verify both QR (→ product_id) and embedded code (→ look up product_id from `pan_code`).

### 3.2 Pharmacist: One Scan Per Product (QR)

- **Table `pharmacist_scans`** (or equivalent):
  - `product_id` (PK).
  - `scanned_at` (timestamp).
  - Optionally: `pharmacist_id` if you add auth.
- **Rule:** At most one row per `product_id`. If a pharmacist scan already exists for this `product_id` → treat as **replay** and **flag** (do not allow second scan). First scan: record row + call contract `verifyProduct(product_id)` (state VALID → REPLAYED).

### 3.3 Consumer: One Scan Per Factor (QR and Strip)

- **Table `consumer_scans`** (or equivalent):
  - `product_id`.
  - `factor` – e.g. `'qr'` or `'strip'`.
  - `scanned_at`.
  - **Unique constraint** on `(product_id, factor)`.
- **Rule:** For each product, at most **one** scan per factor (one QR scan, one strip scan). If consumer scans QR again for the same product → flag. If consumer scans strip again for the same product → flag. New scan for a new factor (e.g. first strip scan after a QR scan) is allowed until that factor is used once.

### 3.4 Existing Tables

- **`code_mappings`** – Keep for PAN code uniqueness (manufacturer generation). Optionally also store `product_id` here or in `products` so that `pan_code` ↔ `product_id` is queryable.
- **`scans`** – Can be deprecated in favor of `pharmacist_scans` and `consumer_scans`, or reused with a `role` + `factor` column; plan assumes separate tables for clarity.

---

## 4. Pharmacist Verification (Authenticated, Supabase, One Scan)

**Goal:** Verify QR + embedded code; authenticate pharmacist; allow only one scan per product; check Supabase for code and QR; flag replays.

| Step | Description |
|------|-------------|
| Auth | Pharmacist must be **authenticated** (e.g. Supabase Auth, JWT, or API key). Reject unauthenticated requests. |
| Input | Upload image (or provide QR + code): extract **product_id** from QR and **embedded (PAN) code** from image/input. |
| DB: Product + code | In Supabase: ensure a row exists for this `product_id` (e.g. in `products`) and that the stored `pan_code` matches the submitted/scanned code. If no row or code mismatch → **COUNTERFEIT / Invalid**. |
| DB: One scan | Check `pharmacist_scans` for this `product_id`. If a row already exists → **flag** (replay), return “Already scanned” / COUNTERFEIT. Do not call contract again. |
| Chain | If first scan: call `verifyProduct(product_id)` on-chain (VALID → REPLAYED). On success, insert into `pharmacist_scans(product_id, scanned_at)`. |
| Response | Return GENUINE + product_id on first successful scan; return COUNTERFEIT + “Replay” when already scanned. |

---

## 5. Consumer Verification (Scan Strip OR QR, One Scan Per Factor)

**Goal:** Consumer can verify by **either** scanning the **strip** (embedded code) **or** the **QR**. Authenticity is checked at this level; only one scan allowed per factor (per product) for uniqueness.

| Step | Description |
|------|-------------|
| Option A – QR | Consumer uploads image with QR. Extract **product_id** from QR. Look up product in Supabase; verify pharmacist has already scanned (on-chain state REPLAYED or `pharmacist_scans` has row). Check **consumer_scans**: if `(product_id, 'qr')` exists → **flag** (replay). Else insert `(product_id, 'qr', scanned_at)` and return VERIFIED. |
| Option B – Strip | Consumer uploads image of strip (or enters code). Extract or receive **PAN code**. Look up **product_id** in Supabase from `pan_code` (e.g. from `products` or `code_mappings`). Same as above: verify pharmacist scan, then check **consumer_scans** for `(product_id, 'strip')`. If exists → **flag**. Else insert and return VERIFIED. |
| Uniqueness | Enforce **one scan per factor per product**: at most one row in `consumer_scans` per `(product_id, factor)`. More than one scan for the same factor → flag. |
| Response | VERIFIED + product_id (and optionally first scan time) on first scan for that factor; clear “Replay”/flag message when the same factor is scanned again. |

---

## 6. Summary Checklist

| # | Item |
|---|------|
| 1 | Remove combined image: only merge template + QR; store packaged, QR, hidden, reveals separately. |
| 2 | Manufacturer: upload template → generate QR + embedded code → merge template+QR only → store artifacts; register on-chain; link product_id ↔ pan_code in Supabase. |
| 3 | Supabase: `products` (product_id, pan_code), `pharmacist_scans` (product_id, one row per product), `consumer_scans` (product_id, factor, one row per (product_id, factor)). |
| 4 | Pharmacist: authenticate; verify QR + embedded code via Supabase; allow only 1 scan per product; flag replays. |
| 5 | Consumer: option to scan strip or QR; verify authenticity; allow 1 scan per factor per product; flag duplicate scans. |

This plan keeps the packaging as “template + QR” only, uses Supabase for code and scan limits, and enforces one pharmacist scan and one scan per consumer factor (QR and strip) for uniqueness and replay protection.
