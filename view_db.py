import sqlite3
import json
from pathlib import Path

# Path to your database
DB_PATH = Path('database/valois.db')

def view_curbside_orders():
    print("--- CURBSIDE ORDERS IN DATABASE ---")
    
    if not DB_PATH.exists():
        print(f"Error: Database not found at {DB_PATH}")
        return

    # Connect to the database
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # This allows us to access columns by name
    cursor = conn.cursor()

    try:
        # Fetch all orders
        cursor.execute("SELECT * FROM curbside_orders ORDER BY created_at DESC")
        orders = cursor.fetchall()
        
        if not orders:
            print("No curbside orders found in the database yet.")
        else:
            for order in orders:
                # Convert row to dictionary for nice printing
                order_dict = dict(order)
                print(json.dumps(order_dict, indent=2))
                print("-" * 40)
                
    except sqlite3.Error as e:
        print(f"Database error: {e}")
    finally:
        conn.close()

if __name__ == '__main__':
    view_curbside_orders()
