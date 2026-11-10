import sqlite3
import json
from pathlib import Path

# Path to your database
DB_PATH = Path('database/valois.db')

TABLES = [
    "contact_inquiries",
    "reservations",
    "catering_requests",
    "curbside_orders",
    "delivery_orders",
    "menu_items"
]

def view_all_tables():
    if not DB_PATH.exists():
        print(f"Error: Database not found at {DB_PATH}")
        return

    # Connect to the database
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # This allows us to access columns by name
    cursor = conn.cursor()

    try:
        for table in TABLES:
            print(f"\n{'='*50}")
            print(f"--- {table.replace('_', ' ').upper()} ---")
            print(f"{'='*50}")
            
            # menu_items doesn't have created_at if not initialized, but it does according to schema.sql
            # We'll use a generic SELECT * just in case, but ORDER BY created_at where available
            try:
                cursor.execute(f"SELECT * FROM {table} ORDER BY created_at DESC")
            except sqlite3.Error:
                # Fallback if created_at doesn't exist for some reason
                cursor.execute(f"SELECT * FROM {table}")
                
            records = cursor.fetchall()
            
            if not records:
                print(f"No records found in {table}.")
            else:
                for record in records:
                    # Convert row to dictionary for nice printing
                    record_dict = dict(record)
                    print(json.dumps(record_dict, indent=2))
                    print("-" * 40)
                    
    except sqlite3.Error as e:
        print(f"Database error: {e}")
    finally:
        conn.close()

if __name__ == '__main__':
    view_all_tables()
