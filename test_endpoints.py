import urllib.request
import urllib.error
import json
import time

BASE_URL = "http://127.0.0.1:5000/api"

def test_endpoint(name, endpoint, method="GET", data=None, expected_status=200):
    url = f"{BASE_URL}/{endpoint}"
    print(f"\n--- Testing: {name} ---")
    try:
        req = urllib.request.Request(url, method=method)
        if data:
            req.add_header('Content-Type', 'application/json')
            req.data = json.dumps(data).encode('utf-8')
            
        with urllib.request.urlopen(req) as response:
            status = response.status
            body = json.loads(response.read().decode())
            print(f"Status: {status} (Expected: {expected_status})")
            print(f"Response: {body}")
            if status == expected_status:
                print("[SUCCESS] PASS")
                return True
            else:
                print("[ERROR] FAIL")
                return False
    except urllib.error.HTTPError as e:
        status = e.code
        body = json.loads(e.read().decode())
        print(f"Status: {status} (Expected: {expected_status})")
        print(f"Response: {body}")
        if status == expected_status:
            print("[SUCCESS] PASS")
            return True
        else:
            print("[ERROR] FAIL")
            return False
    except Exception as e:
        print(f"[ERROR] FAIL (Exception: {e})")
        return False

def main():
    success = True
    
    # 5.2 Backend Endpoint Testing
    # Test health endpoint
    success &= test_endpoint("Health check", "health")
    
    # Test Contact endpoint with valid data
    success &= test_endpoint("Contact (Valid)", "contact", "POST", {
        "name": "John Test",
        "email": "test@test.com",
        "topic": "General",
        "message": "Hello"
    }, 201)
    
    # Test Contact endpoint with missing required field
    success &= test_endpoint("Contact (Missing Field)", "contact", "POST", {
        "name": "John Test",
        "email": "test@test.com"
    }, 400)
    
    # Test Contact endpoint with invalid email
    success &= test_endpoint("Contact (Invalid Email)", "contact", "POST", {
        "name": "John Test",
        "email": "invalid-email",
        "topic": "General",
        "message": "Hello"
    }, 400)
    
    # Test Reservation endpoint with valid data
    success &= test_endpoint("Reservation (Valid)", "reservations", "POST", {
        "customer_name": "Jane Test",
        "email": "jane@test.com",
        "phone": "1234567890",
        "reservation_date": "2026-10-10",
        "reservation_time": "7:00 PM",
        "guest_count": 4,
        "occasion": "Birthday"
    }, 201)
    
    # Test Reservation endpoint with invalid guest count
    success &= test_endpoint("Reservation (Invalid Guests)", "reservations", "POST", {
        "customer_name": "Jane Test",
        "email": "jane@test.com",
        "phone": "1234567890",
        "reservation_date": "2026-10-10",
        "reservation_time": "7:00 PM",
        "guest_count": "four",
        "occasion": "Birthday"
    }, 400)
    
    # Test Catering endpoint with valid data
    success &= test_endpoint("Catering (Valid)", "catering", "POST", {
        "customer_name": "Cater Test",
        "email": "cater@test.com",
        "event_date": "2026-11-11",
        "guest_count": 50,
        "event_type": "Wedding",
        "request_details": "Vegan options"
    }, 201)
    
    # Test Curbside endpoint with valid data
    success &= test_endpoint("Curbside (Valid)", "curbside", "POST", {
        "customer_name": "Curb Test",
        "phone": "1234567890",
        "pickup_time": "6:00 PM",
        "order_details": "1 Steak Frites"
    }, 201)

    # Test Delivery endpoint with valid data
    success &= test_endpoint("Delivery (Valid)", "delivery", "POST", {
        "customer_name": "Delivery Test",
        "phone": "09171234567",
        "delivery_address": "124 Ember Street, Apt 4B",
        "delivery_time": "7:00 PM",
        "order_details": "1x Prime Ribeye, 1x Old Fashioned",
        "delivery_notes": "Leave at lobby reception"
    }, 201)

    # Test Delivery endpoint with missing address
    success &= test_endpoint("Delivery (Missing Address)", "delivery", "POST", {
        "customer_name": "Delivery Test",
        "phone": "09171234567",
        "delivery_time": "7:00 PM",
        "order_details": "1x Prime Ribeye"
    }, 400)

    # Test Menu endpoint
    success &= test_endpoint("Menu Items (GET)", "menu", "GET", None, 200)
    
    # Test each endpoint with malformed JSON
    print("\n--- Testing: Malformed JSON ---")
    url = f"{BASE_URL}/contact"
    try:
        req = urllib.request.Request(url, method="POST")
        req.add_header('Content-Type', 'application/json')
        req.data = b"{ invalid json "
        urllib.request.urlopen(req)
        print("[ERROR] FAIL (Should have thrown 400)")
        success = False
    except urllib.error.HTTPError as e:
        if e.code == 400:
            print("[SUCCESS] PASS")
        else:
            print(f"[ERROR] FAIL (Status {e.code})")
            success = False
            
    # Duplicate submission test
    print("\n--- Testing: Duplicate Submission Prevention ---")
    print("This is primarily a frontend test, but we can verify multiple identical requests are handled by backend (usually they just insert new records with different timestamps, unless explicitly deduplicated). Let's just insert one more Contact request.")
    success &= test_endpoint("Contact (Duplicate)", "contact", "POST", {
        "name": "John Test",
        "email": "test@test.com",
        "topic": "General",
        "message": "Hello"
    }, 201)

    print(f"\nOVERALL RESULT: {'PASS' if success else 'FAIL'}")

if __name__ == '__main__':
    # wait a bit for server to fully start
    time.sleep(1)
    main()
