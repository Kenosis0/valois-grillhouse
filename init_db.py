#!/usr/bin/env python3
"""
Initialize SQLite database for Valois Grillhouse.
Safe to run repeatedly; idempotent.
"""

import sqlite3
import os
import sys
from pathlib import Path

def init_database():
    """Create database and schema if not present."""
    db_path = Path(__file__).parent / 'database' / 'valois.db'
    schema_path = Path(__file__).parent / 'database' / 'schema.sql'
    
    # Ensure database directory exists
    db_path.parent.mkdir(parents=True, exist_ok=True)
    
    if not schema_path.exists():
        print(f"ERROR: schema.sql not found at {schema_path}")
        sys.exit(1)
    
    # Connect to database (creates file if not exists)
    conn = sqlite3.connect(str(db_path))
    cursor = conn.cursor()
    
    try:
        # Read and execute schema
        with open(schema_path, 'r') as f:
            schema = f.read()
        
        cursor.executescript(schema)
        
        # Seed menu_items if empty
        cursor.execute("SELECT COUNT(*) FROM menu_items;")
        if cursor.fetchone()[0] == 0:
            seed_items = [
                # Steaks
                ("Prime Ribeye", "Steaks", "Charcoal crust, roasted garlic butter, house jus", 42.00, "assets/images/foods/Prime Ribeye.png"),
                ("Classic T-Bone", "Steaks", "Dry-aged, cracked pepper, rosemary jus", 48.00, "assets/images/foods/Classic T-Bone.png"),
                ("Garlic Butter Tenderloin", "Steaks", "Silky butter, grilled shallot, sea salt", 46.00, "assets/images/foods/Garlic Butter Tenderloin.png"),
                ("Smoked Tomahawk", "Steaks", "Oak smoke, market weight, served to share", 78.00, "assets/images/foods/Smoked Tomahawk.png"),
                ("Black Pepper Striploin", "Steaks", "Coarse black peppercorn crust, brandy-pepper jus, charred herb sprig", 44.00, "assets/images/foods/Black Pepper Striploin.png"),
                ("Slow-Grilled Short Ribs", "Steaks", "Bone-in beef short ribs, espresso-chili glaze, pickled shallots", 39.00, "assets/images/foods/Slow-Grilled Short Ribs.png"),
                # Seafood
                ("Charred Salmon Fillet", "Seafood", "Lemon herb oil, grilled greens", 32.00, "assets/images/foods/Charred Salmon Fillet.png"),
                ("Garlic Butter Prawns", "Seafood", "Chili, parsley, toasted sourdough", 28.00, "assets/images/foods/Garlic Butter Prawns.png"),
                ("Grilled Calamari", "Seafood", "Tender fire-kissed squid, charred lemon, smoked paprika oil, wild rocket", 24.00, "assets/images/foods/Grilled Calamari.png"),
                ("Seafood Grill Platter", "Seafood", "Charred salmon, tiger prawns, grilled calamari, herb butter, grilled lemon", 64.00, "assets/images/foods/Seafood Grill Platter.png"),
                # From the Fire
                ("Charcoal Pork Ribs", "From the Fire", "Smoky glaze, pickled apple, herb salad", 30.00, "assets/images/foods/Charcoal Pork Ribs.png"),
                ("Herb-Grilled Chicken", "From the Fire", "Green peppercorn sauce, crispy skin", 27.00, "assets/images/foods/Herb-Grilled Chicken.png"),
                ("Lamb Chops", "From the Fire", "Double-cut rack of lamb, rosemary-garlic crust, mint chimichurri", 40.00, "assets/images/foods/Lamb Chops.png"),
                ("Steakhouse Beef Skewers", "From the Fire", "Marinated tenderloin cubes, blistered peppers, red onion, chimichurri", 29.00, "assets/images/foods/Steakhouse Beef Skewers.png"),
                ("Mixed Grill Platter", "From the Fire", "Steak, ribs, prawns, house sauces", 56.00, "assets/images/foods/Mixed Grill Platter.png"),
                # Sides
                ("Steak Frites", "Sides", "Garlic butter, parsley, sea salt", 12.00, "assets/images/foods/Steak Frites.png"),
                ("Grilled Market Vegetables", "Sides", "Seasonal vegetables, smoked lemon", 10.00, "assets/images/foods/Grilled Market Vegetables.png"),
                ("House Salad", "Sides", "Baby greens, shaved radish, mustard vinaigrette", 9.00, "assets/images/foods/House Salad.png"),
                # Drinks
                ("Old Fashioned", "Drinks", "Small-batch bourbon, aromatic bitters, raw sugar, orange peel, subtle oak smoke", 16.00, "assets/images/drinks/Old Fashioned.png"),
                ("Red Wine Sangria", "Drinks", "Vibrant house red wine, fresh citrus wheels, seasonal fruits, brandy splash", 14.00, "assets/images/drinks/Red Wine Sangria.png"),
                ("Classic Mojito", "Drinks", "White rum, fresh green mint leaves, lime wedges, cane sugar over crushed ice", 14.00, "assets/images/drinks/Classic Mojito.png"),
                ("Cabernet Sauvignon", "Drinks", "Full-bodied house pour, deep red berry notes, smooth oak finish", 15.00, "assets/images/drinks/Cabernet Sauvignon.png"),
                ("Berry Lemonade", "Drinks", "Sparkling house lemonade mixed with fresh lemons and dark mixed berries", 8.00, "assets/images/drinks/Berry Lemonade.png"),
                ("Smoked Peach Iced Tea", "Drinks", "Slow-brewed iced tea with fresh peach slices and a subtle hint of smoke", 8.00, "assets/images/drinks/Smoked Peach Iced Tea.png"),
                ("Citrus Cooler", "Drinks", "Bright sparkling mocktail cooler with layered orange, lemon, and lime slices", 9.00, "assets/images/drinks/Citrus Cooler.png")
            ]
            cursor.executemany(
                """INSERT INTO menu_items (name, category, description, price, image_path, is_available)
                   VALUES (?, ?, ?, ?, ?, 1)""",
                seed_items
            )
        
        conn.commit()
        
        # Verify tables created
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        
        if tables:
            print(f"[SUCCESS] Database initialized successfully at {db_path}")
            print(f"[SUCCESS] Created tables: {', '.join([t[0] for t in tables])}")
        else:
            print("[ERROR] Database created but no tables found")
            sys.exit(1)
    
    except Exception as e:
        print(f"[ERROR] Error initializing database: {e}")
        sys.exit(1)
    
    finally:
        conn.close()

if __name__ == '__main__':
    init_database()
