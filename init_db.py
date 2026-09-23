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
