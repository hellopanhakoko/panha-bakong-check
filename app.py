from flask import Flask, jsonify
from bakong_khqr import KHQR
import os

app = Flask(__name__)

# API Token for Bakong (load from environment variable for security)
api_token_bakong = os.getenv('BAKONG_API_TOKEN', 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJkYXRhIjp7ImlkIjoiY2U3NTMwODdiMjQ5NDQzZSJ9LCJpYXQiOjE3NjE1MzU0MjgsImV4cCI6MTc2OTMxMTQyOH0.e3w8uD5-GEtN_K_tFK0dydN8M0f4bxh_Qj3Y0AMaIzk')
khqr = KHQR(api_token_bakong)

@app.route('/check_payment/<md5>', methods=['GET'])
def check_payment(md5):
    try:
        # Check the payment status using the Bakong KHQR API
        status = khqr.check_payment(md5)
        
        # Normalize status to uppercase
        normalized_status = status.upper() if status else "UNKNOWN"
        
        # Return response compatible with check_payment_cart
        if normalized_status in ['PAID', 'PENDING', 'EXPIRED']:
            return jsonify({"success": True, "status": normalized_status})
        else:
            # If status is unknown, treat as PENDING
            return jsonify({"success": True, "status": "PENDING"})
    except Exception as e:
        # Handle errors (e.g., invalid MD5, API failure)
        return jsonify({"success": False, "error": "Invalid MD5 or API error", "details": str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)
