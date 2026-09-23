# Midterm Test Checklist

**Test Date:** 2026-09-23
**Tester Name:** QA Team (Automated & Manual)
**Overall Result:** PASS

## 5.1 Database Testing
- [x] Verify database file exists: `database/valois.db` (✓ PASS)
- [x] Verify all 5 tables exist: contact_inquiries, reservations, catering_requests, curbside_orders, menu_items (✓ PASS)
- [x] Verify all tables have correct columns and types (✓ PASS)
- [x] Verify indexes created on appropriate fields (✓ PASS)

## 5.2 Backend Endpoint Testing
- [x] Test health endpoint: `GET http://127.0.0.1:5000/api/health` → should return JSON success (✓ PASS)
- [x] Test Contact endpoint with valid data → should return 201 and insert into contact_inquiries (✓ PASS)
- [x] Test Contact endpoint with missing required field → should return 400 with error message (✓ PASS)
- [x] Test Contact endpoint with invalid email → should return 400 with email error (✓ PASS)
- [x] Test Reservation endpoint with valid data → should return 201 and insert into reservations (✓ PASS)
- [x] Test Reservation endpoint with invalid guest count → should return 400 with error (✓ PASS)
- [x] Test Catering endpoint with valid data → should return 201 and insert into catering_requests (✓ PASS)
- [x] Test Curbside endpoint with valid data → should return 201 and insert into curbside_orders (✓ PASS)
- [x] Test each endpoint with malformed JSON → should return 400 (✓ PASS)
- [x] Verify all error responses are JSON formatted and user-friendly (✓ PASS)
- [x] Verify duplicate submissions to same endpoint work (✓ PASS)

## 5.3 Frontend Form Testing
*(Verified manually by User)*
- [x] Open Contact.html in browser and submit valid contact form (✓ PASS)
- [x] Open Contact.html and try to submit with empty name (✓ PASS)
- [x] Open Reservation.html and submit valid reservation (✓ PASS)
- [x] Open Reservation.html and try invalid guest count (✓ PASS)
- [x] Open Catering.html and submit valid catering request (✓ PASS)
- [x] Open Valois's Curbside.html and submit valid curbside order (✓ PASS)

## 5.4 Duplicate Submission Prevention Testing
*(Verified manually by User)*
- [x] Submit a form successfully and verify button disabled (✓ PASS)

## 5.5 Page & Navigation Testing
*(Verified manually by User)*
- [x] Verify all 8 HTML pages still load correctly (✓ PASS)
- [x] Verify navigation links work (✓ PASS)
- [x] Verify responsive design intact on mobile/tablet screen sizes (✓ PASS)
- [x] Verify no visual regressions or styling issues (✓ PASS)

## Bugs Found
1. **JSON Parsing Error Handling**: Initially, malformed JSON returned a 500 error instead of a 400 error.
   - **Resolution**: Fixed in `backend/app.py` by passing `silent=True` to `request.get_json()`. (Fixed)
