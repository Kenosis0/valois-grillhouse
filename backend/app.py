"""
Valois Grillhouse Backend - Flask Application
Handles form submissions and database persistence.
"""

import sqlite3
import json
import os
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from pathlib import Path
from datetime import datetime

# Application Factory
def create_app():
    app = Flask(__name__)
    CORS(app)  # Enable CORS for local development
    
    # Configuration
    BASE_DIR = Path(__file__).parent.parent
    DB_PATH = BASE_DIR / 'database' / 'valois.db'
    
    app.config['DB_PATH'] = DB_PATH
    app.config['JSON_SORT_KEYS'] = False
    
    # Database helper functions
    def get_db():
        """Get database connection."""
        conn = sqlite3.connect(str(app.config['DB_PATH']))
        conn.row_factory = sqlite3.Row
        return conn
    
    def dict_from_row(row):
        """Convert sqlite3.Row to dict."""
        return dict(row) if row else None
    
    # Validation helper
    def validate_required(data, required_fields):
        """Validate that all required fields are present and non-empty."""
        errors = []
        for field in required_fields:
            if field not in data or not str(data.get(field, '')).strip():
                errors.append(f"'{field}' is required")
        return errors
    
    # Error response helper
    def error_response(message, status_code=400):
        """Return standardized error response."""
        return jsonify({'success': False, 'error': message}), status_code
    
    # Success response helper
    def success_response(data=None, message="Success", status_code=200):
        """Return standardized success response."""
        return jsonify({
            'success': True,
            'message': message,
            'data': data
        }), status_code
    
    # Health check endpoint
    @app.route('/api/health', methods=['GET'])
    def health():
        return success_response(message="Backend is running")
    
    # ========== CONTACT INQUIRIES ENDPOINT ==========
    @app.route('/api/contact', methods=['POST'])
    def submit_contact():
        """Store contact inquiry."""
        try:
            data = request.get_json(silent=True)
            
            if not data:
                return error_response("No data provided")
            
            # Validate required fields
            required = ['name', 'email', 'topic', 'message']
            errors = validate_required(data, required)
            if errors:
                return error_response('; '.join(errors))
            
            # Basic email validation
            if '@' not in data.get('email', ''):
                return error_response("Invalid email address")
            
            # Insert into database
            conn = get_db()
            cursor = conn.cursor()
            
            cursor.execute(
                """INSERT INTO contact_inquiries 
                   (name, email, topic, message, status, created_at)
                   VALUES (?, ?, ?, ?, 'new', datetime('now'))""",
                (
                    data['name'].strip(),
                    data['email'].strip(),
                    data['topic'].strip(),
                    data['message'].strip()
                )
            )
            conn.commit()
            inquiry_id = cursor.lastrowid
            conn.close()
            
            return success_response(
                data={'inquiry_id': inquiry_id},
                message="Thank you for contacting us. We will get back to you soon.",
                status_code=201
            )
        
        except Exception as e:
            return error_response(f"Server error: {str(e)}", 500)
    
    # ========== RESERVATIONS ENDPOINT ==========
    @app.route('/api/reservations', methods=['POST'])
    def submit_reservation():
        """Store reservation request."""
        try:
            data = request.get_json(silent=True)
            
            if not data:
                return error_response("No data provided")
            
            # Validate required fields
            required = ['customer_name', 'email', 'phone', 'reservation_date', 
                       'reservation_time', 'guest_count']
            errors = validate_required(data, required)
            if errors:
                return error_response('; '.join(errors))
            
            # Validate email
            if '@' not in data.get('email', ''):
                return error_response("Invalid email address")
            
            # Validate guest count (must be positive integer)
            try:
                guest_count = int(data['guest_count'])
                if guest_count <= 0:
                    return error_response("Guest count must be greater than 0")
            except ValueError:
                return error_response("Guest count must be a number")
            
            # Insert into database
            conn = get_db()
            cursor = conn.cursor()
            
            cursor.execute(
                """INSERT INTO reservations
                   (customer_name, email, phone, reservation_date, 
                    reservation_time, guest_count, occasion, status, created_at)
                   VALUES (?, ?, ?, ?, ?, ?, ?, 'pending', datetime('now'))""",
                (
                    data['customer_name'].strip(),
                    data['email'].strip(),
                    data['phone'].strip(),
                    data['reservation_date'].strip(),
                    data['reservation_time'].strip(),
                    guest_count,
                    data.get('occasion', '').strip() or None
                )
            )
            conn.commit()
            reservation_id = cursor.lastrowid
            conn.close()
            
            return success_response(
                data={'reservation_id': reservation_id},
                message="Your reservation request has been received. We will confirm shortly.",
                status_code=201
            )
        
        except Exception as e:
            return error_response(f"Server error: {str(e)}", 500)
    
    # ========== CATERING ENDPOINT ==========
    @app.route('/api/catering', methods=['POST'])
    def submit_catering():
        """Store catering request."""
        try:
            data = request.get_json(silent=True)
            
            if not data:
                return error_response("No data provided")
            
            # Validate required fields
            required = ['customer_name', 'email', 'event_date', 'guest_count']
            errors = validate_required(data, required)
            if errors:
                return error_response('; '.join(errors))
            
            # Validate email
            if '@' not in data.get('email', ''):
                return error_response("Invalid email address")
            
            # Validate guest count
            try:
                guest_count = int(data['guest_count'])
                if guest_count <= 0:
                    return error_response("Guest count must be greater than 0")
            except ValueError:
                return error_response("Guest count must be a number")
            
            # Insert into database
            conn = get_db()
            cursor = conn.cursor()
            
            cursor.execute(
                """INSERT INTO catering_requests
                   (customer_name, email, event_date, guest_count, 
                    event_type, request_details, status, created_at)
                   VALUES (?, ?, ?, ?, ?, ?, 'pending', datetime('now'))""",
                (
                    data['customer_name'].strip(),
                    data['email'].strip(),
                    data['event_date'].strip(),
                    guest_count,
                    data.get('event_type', '').strip() or None,
                    data.get('request_details', '').strip() or None
                )
            )
            conn.commit()
            catering_id = cursor.lastrowid
            conn.close()
            
            return success_response(
                data={'catering_id': catering_id},
                message="Thank you for your catering inquiry. We will contact you soon.",
                status_code=201
            )
        
        except Exception as e:
            return error_response(f"Server error: {str(e)}", 500)
    
    # ========== CURBSIDE ENDPOINT ==========
    @app.route('/api/curbside', methods=['POST'])
    def submit_curbside():
        """Store curbside pickup order."""
        try:
            data = request.get_json(silent=True)
            
            if not data:
                return error_response("No data provided")
            
            # Validate required fields
            required = ['customer_name', 'phone', 'pickup_time', 'order_details']
            errors = validate_required(data, required)
            if errors:
                return error_response('; '.join(errors))
            
            # Insert into database
            conn = get_db()
            cursor = conn.cursor()
            
            cursor.execute(
                """INSERT INTO curbside_orders
                   (customer_name, phone, pickup_time, order_details, status, created_at)
                   VALUES (?, ?, ?, ?, 'pending', datetime('now'))""",
                (
                    data['customer_name'].strip(),
                    data['phone'].strip(),
                    data['pickup_time'].strip(),
                    data['order_details'].strip()
                )
            )
            conn.commit()
            order_id = cursor.lastrowid
            conn.close()
            
            return success_response(
                data={'order_id': order_id},
                message="Your curbside pickup order has been received.",
                status_code=201
            )
        
        except Exception as e:
            return error_response(f"Server error: {str(e)}", 500)
    
    # ========== DELIVERY ENDPOINT ==========
    @app.route('/api/delivery', methods=['POST'])
    def submit_delivery():
        """Store delivery order."""
        try:
            data = request.get_json(silent=True)
            
            if not data:
                return error_response("No data provided")
            
            # Validate required fields
            required = ['customer_name', 'phone', 'delivery_address', 'delivery_time', 'order_details']
            errors = validate_required(data, required)
            if errors:
                return error_response('; '.join(errors))
            
            # Insert into database
            conn = get_db()
            cursor = conn.cursor()
            
            cursor.execute(
                """INSERT INTO delivery_orders
                   (customer_name, phone, delivery_address, delivery_time, order_details, delivery_notes, status, created_at)
                   VALUES (?, ?, ?, ?, ?, ?, 'pending', datetime('now'))""",
                (
                    data['customer_name'].strip(),
                    data['phone'].strip(),
                    data['delivery_address'].strip(),
                    data['delivery_time'].strip(),
                    data['order_details'].strip(),
                    data.get('delivery_notes', '').strip() or None
                )
            )
            conn.commit()
            delivery_id = cursor.lastrowid
            conn.close()
            
            return success_response(
                data={'delivery_id': delivery_id},
                message="Your delivery order has been received. We will prepare it fresh and deliver it to your address.",
                status_code=201
            )
        
        except Exception as e:
            return error_response(f"Server error: {str(e)}", 500)
    
    # ========== MENU ENDPOINT (OPTIONAL) ==========
    @app.route('/api/menu', methods=['GET'])
    def get_menu():
        """Retrieve all menu items (for future use)."""
        try:
            conn = get_db()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM menu_items WHERE is_available = 1 ORDER BY category, name")
            items = [dict_from_row(row) for row in cursor.fetchall()]
            conn.close()
            
            return success_response(data={'items': items})
        
        except Exception as e:
            return error_response(f"Server error: {str(e)}", 500)
    
    # ========== STATIC FRONTEND SERVING (FOR DESKTOP & MOBILE BROWSERS) ==========
    @app.route('/')
    def serve_index():
        return send_from_directory(str(BASE_DIR), 'index.html')
    
    @app.route('/<path:filename>')
    def serve_static_files(filename):
        target = BASE_DIR / filename
        if target.exists() and target.is_file():
            return send_from_directory(str(BASE_DIR), filename)
        return error_response("Endpoint not found", 404)
    
    # Error handlers
    @app.errorhandler(404)
    def not_found(error):
        return error_response("Endpoint not found", 404)
    
    @app.errorhandler(500)
    def internal_error(error):
        return error_response("Internal server error", 500)
    
    return app

# Entry point
if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5000)
