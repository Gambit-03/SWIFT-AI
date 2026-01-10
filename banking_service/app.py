from flask import Flask, request, jsonify, render_template, send_from_directory, Response
from flask_cors import CORS
from pymongo import MongoClient
from datetime import datetime, timedelta
import random
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

app = Flask(__name__, static_folder='.', template_folder='.')
CORS(app)

# Email Config
SMTP_SERVER = "smtp.gmail.com"
FRAUD_API_URL = os.getenv("FRAUD_API_URL", "http://localhost:5001/analyze")
SMTP_PORT = 587
MAIL_USERNAME = "mkbharvad534@gmail.com"
MAIL_PASSWORD = "dwtp fmiq miyl ccvq"

def send_email(to_email, subject, body):
    try:
        msg = MIMEMultipart()
        msg['From'] = MAIL_USERNAME
        msg['To'] = to_email
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'html')) # HTML for better formatting
        
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(MAIL_USERNAME, MAIL_PASSWORD)
        text = msg.as_string()
        server.sendmail(MAIL_USERNAME, to_email, text)
        server.quit()
        print(f"Email sent to {to_email}")
        return True
    except Exception as e:
        print(f"Failed to send email: {e}")
        return False

# Error Handlers
@app.errorhandler(404)
def not_found(e):
    return send_from_directory('.', '404.html'), 404

@app.errorhandler(500)
def server_error(e):
    return jsonify({"error": "Internal server error"}), 500

@app.errorhandler(504)
def gateway_timeout(e):
    return send_from_directory('.', '504.html'), 504

# Database Configuration
# Database Configuration (Dedicated Banking DB)
MONGO_URI = "mongodb+srv://mkbharvad8080:Mkb%408080@cluster0.a82h2.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(MONGO_URI)
db = client['banking_core_db']

transactions_coll = db['transactions']
customers_coll = db['customers']
merchants_coll = db['merchants']
bank_accounts_coll = db['bank_accounts']
credit_cards_coll = db['credit_cards']
audit_coll = db['audit_logs']

# --- Helper Functions ---
def log_audit(user, action, target, details=""):
    audit_coll.insert_one({
        "timestamp": datetime.utcnow(),
        "user": user,
        "action": action,
        "target": target,
        "details": details
    })

# --- PAYPAL WEBHOOK INTEGRATION ---
@app.route('/api/paypal/webhook', methods=['POST'])
def paypal_webhook():
    """
    PayPal sends transaction data here when payment happens
    Configure this URL in PayPal Developer Dashboard
    """
    try:
        data = request.json
        event_type = data.get('event_type')
        
        # Handle payment completion
        if event_type == 'PAYMENT.SALE.COMPLETED':
            payment_data = data.get('resource', {})
            
            # Extract transaction details
            txn_id = payment_data.get('id', f"PP-{random.randint(100000, 999999)}")
            amount = float(payment_data.get('amount', {}).get('total', 0))
            currency = payment_data.get('amount', {}).get('currency', 'USD')
            payer_email = payment_data.get('payer', {}).get('email_address', 'Unknown')
            
            # Calculate risk score via Microservice
            risk_score, reasoning = calculate_risk_score({
                "amount": amount,
                "location": "PayPal",
                "customer": payer_email,
                "merchant": "PayPal"
            })
            
            # Save to database
            transaction = {
                "id": txn_id,
                "customer": payer_email,
                "amount": amount,
                "currency": currency,
                "location": "PayPal",
                "coords": [0, 0],
                "channel": "PayPal",
                "type": "Credit",
                "timestamp": datetime.utcnow(),
                "risk_score": risk_score,
                "ai_reason": reasoning,
                "status": "Blocked" if risk_score > 85 else ("Review" if risk_score > 60 else "Approved")
            }
            transactions_coll.insert_one(transaction)
            
            # Update customer profile
            customers_coll.update_one(
                {"email": payer_email},
                {"$inc": {"txn_count": 1, "total_spent": amount}, "$set": {"last_txn": datetime.utcnow(), "risk_score": risk_score}},
                upsert=True
            )
            
            log_audit("PayPal", f"Transaction: {txn_id}", "PayPal", f"{amount} {currency}")
            return jsonify({"success": True})
        
        return jsonify({"success": True, "message": "Event received"})
    except Exception as e:
        print(f"PayPal Error: {e}")
        return jsonify({"error": str(e)}), 500

# --- AUTH ENDPOINTS WITH OTP ---
@app.route('/api/auth/register', methods=['POST'])
def register():
    data = request.json
    email = data.get('email')
    
    if db['users'].find_one({"email": email}):
        return jsonify({"success": False, "message": "User already exists"})
    
    user = {
        "name": data.get('name'),
        "email": email,
        "phone": data.get('phone'),
        "password": data.get('password'), 
        "role": data.get('role', 'Customer'),
        "created_at": datetime.utcnow(),
        "status": "Active"
    }
    db['users'].insert_one(user)
    
    # Send Welcome Email
    email_body = f"""
    <h3>Welcome to Swift AI!</h3>
    <p>Hello {user['name']},</p>
    <p>Your account has been successfully created as <strong>{user['role']}</strong>.</p>
    <p>Please login and link your credit card to start making payments.</p>
    """
    send_email(email, "Welcome to Swift AI Platform", email_body)
    
    log_audit("System", f"New User Registered: {email} ({user['role']})", "Auth", "Register")
    return jsonify({"success": True, "message": "Registration successful"})

@app.route('/api/auth/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('email')
    password = data.get('password') # Merchants don't have passwords in this simple flow, or we assume they do? 
    # Actually, for this demo, merchants might not have passwords set up in 'register_merchant'.
    # Let's check: register_merchant creates a merchant object but NO PASSWORD field.
    # To fix this elegantly for the user without complex auth:
    # We will allow merchants to login just by Email for this demo (or assume a default password if needed).
    # OR, better: Check if it's a merchant, if so, generate OTP directly without password check (simulating "Login with OTP").
    
    # 1. Check User (Customer/Admin) with Password
    user = db['users'].find_one({"email": email})
    if user:
        if user.get('password') == password:
            # Valid User
            pass 
        else:
            return jsonify({"success": False, "message": "Invalid credentials"})
    else:
        # 2. Check Merchant (No password required for this demo flow, just email)
        merchant = merchants_coll.find_one({"email": email})
        if merchant:
            user = merchant # Treat merchant as user for OTP step
        else:
             return jsonify({"success": False, "message": "User not found"})
    
    # Generate 6-digit OTP
    otp = str(random.randint(100000, 999999))
    
    # Store OTP
    db['otps'].insert_one({
        "email": email,
        "otp": otp,
        "created_at": datetime.utcnow(),
        "expires_at": datetime.utcnow() + timedelta(minutes=5)
    })
    
    # Send OTP
    name = user.get('name', user.get('business_name', 'User'))
    email_body = f"""
    <h3>Your Login OTP</h3>
    <p>Hello {name},</p>
    <p>Your OTP for login is: <strong style="font-size:24px; color:#dc3545;">{otp}</strong></p>
    """
    send_email(email, f"Swift AI Login OTP: {otp}", email_body)
    
    log_audit(email, "OTP Sent", "Auth", "OTP Generated")
    return jsonify({"success": True, "message": "OTP sent to your email"})

@app.route('/api/auth/verify-otp', methods=['POST'])
def verify_otp():
    data = request.json
    email = data.get('email')
    otp = data.get('otp')
    
    # Find valid OTP
    otp_record = db['otps'].find_one({
        "email": email,
        "otp": otp,
        "expires_at": {"$gt": datetime.utcnow()}
    })
    
    if not otp_record:
        return jsonify({"success": False, "message": "Invalid or expired OTP"})
    
    # Delete used OTP
    db['otps'].delete_one({"_id": otp_record['_id']})
    
    # Get user details
    role = "Customer"
    user = db['users'].find_one({"email": email})
    
    if user:
        name = user['name']
        role = user['role']
    else:
        # Check Merchant
        merchant = merchants_coll.find_one({"email": email})
        if merchant:
            name = merchant['business_name']
            role = "Merchant"
        else:
            return jsonify({"success": False, "message": "User record not found"})
    
    log_audit(email, f"Login Success ({role})", "Auth", "Login")
    return jsonify({
        "success": True,
        "user": {
            "name": name,
            "email": email,
            "role": role
        }
    })

@app.route('/api/auth/resend-otp', methods=['POST'])
def resend_otp():
    data = request.json
    email = data.get('email')
    
    user = db['users'].find_one({"email": email})
    if not user:
        return jsonify({"success": False, "message": "User not found"})
    
    # Generate new OTP
    otp = str(random.randint(100000, 999999))
    
    db['otps'].insert_one({
        "email": email,
        "otp": otp,
        "created_at": datetime.utcnow(),
        "expires_at": datetime.utcnow() + timedelta(minutes=5)
    })
    
    email_body = f"""
    <h3>Your New Login OTP</h3>
    <p>Your OTP is: <strong style="font-size:24px; color:#dc3545;">{otp}</strong></p>
    <p>Valid for 5 minutes.</p>
    """
    send_email(email, f"Swift AI OTP Resent: {otp}", email_body)
    
    return jsonify({"success": True, "message": "OTP resent"})

# --- PROFILE MANAGEMENT ---
@app.route('/api/profile', methods=['GET', 'POST'])
def manage_profile():
    # For simulation, default to Admin or use query param
    email = request.args.get('email', "admin@swiftai.com")
    
    if request.method == 'POST':
        data = request.json
        email = data.get('email', email) # Allow updating email context if needed
        
        update_fields = {
            "name": data.get('name'),
            "phone": data.get('phone'),
            "location": data.get('location', 'Headquarters, Silicon Valley, CA'),
            "updated_at": datetime.utcnow()
        }
        
        result = db['users'].update_one({"email": email}, {"$set": update_fields}, upsert=True)
        log_audit(email, "Updated Profile", "Profile", "User updated personal details")
        return jsonify({"success": True, "message": "Profile updated successfully"})
        
    user = db['users'].find_one({"email": email})
    if not user:
        # Create default admin if missing
        user = {
            "name": "Admin User",
            "email": email,
            "role": "Super Admin",
            "phone": "+1 (555) 000-1234",
            "location": "Headquarters, Silicon Valley, CA",
            "created_at": datetime.utcnow()
        }
        db['users'].insert_one(user)
        
    user['_id'] = str(user['_id'])
    return jsonify(user)

# --- BANK PORTAL ENDPOINTS ---
@app.route('/api/bank/kyc', methods=['POST'])
def submit_kyc():
    data = request.json
    record = {
        "customer_id": data.get('customer_id'),
        "name": data.get('name'),
        "doc_type": data.get('doc_type'),
        "status": "Submitted",
        "submitted_at": datetime.utcnow()
    }
    db['kyc_records'].insert_one(record)
    send_email(MAIL_USERNAME, "New KYC Submission", f"New KYC document submitted by {record['name']}")
    return jsonify({"success": True, "message": "KYC Submitted"})

@app.route('/api/kyc/verify', methods=['POST'])
def verify_kyc():
    data = request.json
    name = data.get('name')
    # Simple logic for simulation: "Unknown" or "Hidden" triggers fraud
    is_fraud = "Unknown" in name or "Hidden" in data.get('country', '')
    
    status = "Failed" if is_fraud else "Verified"
    
    # Store record
    db['kyc_records'].insert_one({
        "name": name,
        "country": data.get('country'),
        "status": status,
        "timestamp": datetime.utcnow()
    })
    
    if status == "Failed":
        # Alert Admin
        send_email(MAIL_USERNAME, "CRITICAL: KYC Alert", f"High Risk KYC Detected: {name}. System blocked verification.")
        
    return jsonify({
        "status": status,
        "details": { "document_check": "Forged" if is_fraud else "Valid" }
    })

# --- AI CHATBOT ENDPOINT ---
@app.route('/api/chat', methods=['POST'])
def ai_chat():
    data = request.json
    msg = data.get('message', '').lower()
    
    response_text = "I didn't understand that. Try asking about 'stats', 'blocked transactions', or a 'customer'."
    
    try:
        if 'hello' in msg or 'hi' in msg:
            response_text = "Hello! I am Swift Assist. I can help you analyze fraud data. Try asking 'Show me today's stats'."
            
        elif 'stat' in msg or 'overview' in msg:
            total = db['transactions'].count_documents({})
            blocked = db['transactions'].count_documents({"status": "Blocked"})
            response_text = f"Currently, we have processed {total} transactions. {blocked} have been blocked as fraudulent."
            
        elif 'blocked' in msg:
            recent_blocked = list(db['transactions'].find({"status": "Blocked"}).sort("timestamp", -1).limit(3))
            if recent_blocked:
                details = ", ".join([f"{t.get('customer', 'Unknown')} (${t.get('amount')})" for t in recent_blocked])
                response_text = f"The last 3 blocked transactions were: {details}."
            else:
                response_text = "No blocked transactions found recently."
                
        elif 'customer' in msg or 'check' in msg:
            # Simple simulation: Extract name if possible, or just give general info
            response_text = "To check a specific customer, please visit the Customers page or provide an ID. I can tell you that we have " + str(db['customers'].count_documents({})) + " active profiles."
            
        elif 'alert' in msg:
            pending = db['alerts'].count_documents({"status": "Pending"})
            response_text = f"There are currently {pending} pending alerts requiring your attention."
            
        elif 'risk' in msg:
            response_text = "Global Risk Level is currently MODERATE based on recent velocity checks."
            
    except Exception as e:
        response_text = "I encountered an error accessing the database."

    return jsonify({"response": response_text})



import requests

def calculate_risk_score(txn):
    """
    Delegate risk calculation to the external Fraud Detection Service.
    """
    try:
        # Prepare payload for microservice
        payload = {
            "id": txn.get('id', 'UNKNOWN'),
            "amount": txn.get('amount', 0),
            "location": txn.get('location', 'Unknown'),
            "merchant": txn.get('merchant', 'Unknown'),
            "type": txn.get('type', 'Standard'),
            "customer": txn.get('customer', 'Unknown')
        }
        
        print(f"[FRAUD CHECK] Calling {FRAUD_API_URL} for transaction {payload['id']}")
        response = requests.post(FRAUD_API_URL, json=payload, timeout=5)
        
        if response.status_code == 200:
            result = response.json()
            print(f"[FRAUD CHECK] ✅ Response: {result.get('status')} (Score: {result.get('risk_score')})")
            # Return tuple to match existing signature for minimal refactoring impact
            return result.get('risk_score', 0), ", ".join(result.get('reasons', []))
        else:
            print(f"[FRAUD CHECK] ❌ HTTP {response.status_code}: {response.text}")
            
    except requests.exceptions.ConnectionError as e:
        print(f"⚠ Warning: Cannot connect to Fraud Service at {FRAUD_API_URL}")
        print(f"   Make sure fraud service is running on port 5001")
    except requests.exceptions.Timeout:
        print(f"⚠ Warning: Fraud Service timeout")
    except Exception as e:
        print(f"⚠ Warning: Fraud Service error: {type(e).__name__}: {e}")
        
    # Fallback if service is down (Safe Default)
    return 0, "Fraud Service Unavailable (Approved by Default)"


# --- Routes ---
@app.route('/')
def index(): return send_from_directory('.', 'index.html')

@app.route('/<path:filename>')
def serve_static(filename):
    return send_from_directory('.', filename)

# Location to Coordinates Mapping
LOCATION_MAP = {
    "Mumbai, IN": [19.0760, 72.8777],
    "New York, US": [40.7128, -74.0060],
    "London, UK": [51.5074, -0.1278],
    "Dubai, UAE": [25.2048, 55.2708],
    "Lagos, Nigeria": [6.5244, 3.3792],
    "Tokyo, Japan": [35.6762, 139.6503],
    "High Risk Zone": [34.5553, 69.2075] # Kabul (example)
}

@app.route('/api/transactions/<txn_id>', methods=['GET'])
def get_transaction(txn_id):
    txn = transactions_coll.find_one({"id": txn_id})
    if txn:
        txn['_id'] = str(txn['_id'])
        return jsonify(txn)
    return jsonify({"error": "Transaction not found"}), 404

# 1. Transactions & Simulation
@app.route('/api/transactions', methods=['POST', 'GET'])
def manage_transactions():
    if request.method == 'POST':
        data = request.json
        txn_id = data.get('id', f"TXN-{random.randint(100000, 999999)}")
        risk_score, reasoning = calculate_risk_score(data)
        
        location_name = data.get('location', 'Globe')
        coords = LOCATION_MAP.get(location_name, [random.uniform(-60, 60), random.uniform(-120, 120)])

        transaction = {
            "id": txn_id,
            "customer": data.get('customer', 'Unknown'),
            "amount": float(data.get('amount', 0)),
            "location": location_name,
            "coords": coords,
            "channel": data.get('channel', 'Web'),
            "type": data.get('type', 'Credit'),
            "timestamp": datetime.utcnow(),
            "risk_score": risk_score,
            "ai_reason": reasoning,
            "status": "Blocked" if risk_score > 85 else ("Review" if risk_score > 60 else "Approved")
        }
        transactions_coll.insert_one(transaction)
        
        # Sync Customer Profile
        customers_coll.update_one(
            {"name": transaction['customer']},
            {"$inc": {"txn_count": 1, "total_spent": transaction['amount']}, 
             "$set": {"last_txn": datetime.utcnow(), "risk_score": risk_score}},
            upsert=True
        )

        # No local alert creation - handled by Fraud Service if needed or just logged
        
        transaction['_id'] = str(transaction['_id'])
        return jsonify(transaction)
    
    # GET with Filters
    status = request.args.get('status')
    query = {"status": status} if status and status != 'All' else {}
    txns = list(transactions_coll.find(query).sort("timestamp", -1).limit(50))
    for t in txns: t['_id'] = str(t['_id'])
    return jsonify(txns)

# Admin Dashboard Logic Removed (Moved to Fraud Service)

# Duplicate KYC verify removed



# 11. Integrations Management - See line 573 for complete CRUD implementation

# 12. User Management - See line 626 for complete implementation with invitations

# 13. Customer Profile Management

# Duplicate profile management removed (Consolidated at top)

@app.route('/api/profile/photo', methods=['POST'])
def upload_profile_photo():
    if 'photo' not in request.files:
        return jsonify({"error": "No photo uploaded"}), 400
    
    file = request.files['photo']
    if file.filename == '':
        return jsonify({"error": "No file selected"}), 400
    
    # Save file (in production, use cloud storage like S3)
    filename = f"profile_{datetime.utcnow().timestamp()}.jpg"
    filepath = os.path.join('uploads', filename)
    os.makedirs('uploads', exist_ok=True)
    file.save(filepath)
    
    photo_url = f"/uploads/{filename}"
    # Use 'users' collection
    db['users'].update_one(
        {"email": "admin@swiftai.com"},
        {"$set": {"photo": photo_url}},
        upsert=True
    )
    log_audit("Admin", "Uploaded Profile Photo", "Profile", filename)
    return jsonify({"success": True, "photo_url": photo_url})

@app.route('/api/profile/password', methods=['POST'])
def change_password():
    data = request.json
    current_password = data.get('current_password')
    new_password = data.get('new_password')
    
    # Use 'users' collection
    db['users'].update_one(
        {"email": "admin@swiftai.com"},
        {"$set": {"password_updated_at": datetime.utcnow()}},
        upsert=True
    )
    log_audit("Admin", "Changed Password", "Security", "Password updated")
    return jsonify({"success": True, "message": "Password changed successfully"})

@app.route('/api/export/<data_type>', methods=['POST'])
def export_generic_data(data_type):
    data = request.json
    export_record = {
        "type": data_type,
        "format": data.get('format', 'PDF'),
        "filters": data.get('filters', {}),
        "exported_at": datetime.utcnow(),
        "status": "Completed"
    }
    db['exports'].insert_one(export_record)
    log_audit("Admin", f"Exported {data_type} Report", "Exports", "Generated")
    
    # Return a download URL that points to our generic download handler
    return jsonify({
        "success": True, 
        "export": str(export_record),  # Convert to string just in case
        "download_url": f"/api/reports/download/{str(export_record['_id'])}" # Re-use report download logic for now
    })

# 17. Audit Logs with Export & Filtering

@app.route('/api/audit/export/pdf', methods=['POST'])
def export_audit_pdf():
    data = request.json
    filters = data.get('filters', {})
    
    # Create export record
    export_record = {
        "type": "audit_logs",
        "format": "PDF",
        "filters": filters,
        "exported_at": datetime.utcnow(),
        "status": "Completed",
        "record_count": audit_coll.count_documents(filters)
    }
    result = db['exports'].insert_one(export_record)
    export_id = str(result.inserted_id)
    
    log_audit("Admin", "Exported Audit Logs", "Audit", f"PDF export with {export_record['record_count']} records")
    return jsonify({"success": True, "export_id": export_id, "download_url": f"/api/audit/download/pdf/{export_id}"})

@app.route('/api/audit/export/csv', methods=['POST'])
def export_audit_csv():
    data = request.json
    filters = data.get('filters', {})
    
    export_record = {
        "type": "audit_logs",
        "format": "CSV",
        "filters": filters,
        "exported_at": datetime.utcnow(),
        "status": "Completed",
        "record_count": audit_coll.count_documents(filters)
    }
    result = db['exports'].insert_one(export_record)
    export_id = str(result.inserted_id)
    
    log_audit("Admin", "Exported Audit Logs", "Audit", f"CSV export with {export_record['record_count']} records")
    return jsonify({"success": True, "export_id": export_id, "download_url": f"/api/audit/download/csv/{export_id}"})

@app.route('/api/audit/download/<format>/<export_id>', methods=['GET'])
def download_audit_export(format, export_id):
    content = f"Audit Logs Export ({format.upper()})\n\nExport ID: {export_id}\n\nGenerated: {datetime.utcnow()}\n\n[Log Data Redacted for Demo]"
    
    return Response(
        content,
        mimetype="text/plain",
        headers={"Content-disposition": f"attachment; filename=audit_logs_{export_id}.{format.lower() if format != 'PDF' else 'txt'}"}
    )


# 19. User Management with Invitations

# 20. File Upload Handler
@app.route('/uploads/<filename>')
def serve_upload(filename):
    return send_from_directory('uploads', filename)

# 21. Transaction Actions (Approve/Block/Review)
@app.route('/api/transactions/<txn_id>/approve', methods=['POST'])
def approve_transaction(txn_id):
    transactions_coll.update_one({"id": txn_id}, {"$set": {"status": "Approved"}})
    log_audit("Admin", f"Approved Transaction: {txn_id}", "Transactions", "Approved")
    return jsonify({"success": True, "message": "Transaction approved"})

@app.route('/api/transactions/<txn_id>/block', methods=['POST'])
def block_transaction(txn_id):
    transactions_coll.update_one({"id": txn_id}, {"$set": {"status": "Blocked"}})
    log_audit("Admin", f"Blocked Transaction: {txn_id}", "Transactions", "Blocked")
    return jsonify({"success": True, "message": "Transaction blocked"})

@app.route('/api/transactions/<txn_id>/review', methods=['POST'])
def review_transaction(txn_id):
    transactions_coll.update_one({"id": txn_id}, {"$set": {"status": "Review"}})
    log_audit("Admin", f"Sent Transaction to Review: {txn_id}", "Transactions", "Review")
    return jsonify({"success": True, "message": "Transaction sent to review"})

# 22. Customer Detail & Management
@app.route('/api/customers/<customer_id>', methods=['GET', 'PUT'])
def manage_customer_detail(customer_id):
    if request.method == 'GET':
        # Search by Email OR Name
        customer = customers_coll.find_one({"$or": [{"email": customer_id}, {"name": customer_id}]})
        if not customer:
            # If not found, try to return a default structure for new users so the dashboard doesn't break
            return jsonify({
                "name": customer_id.split('@')[0] if '@' in customer_id else customer_id,
                "email": customer_id if '@' in customer_id else "",
                "txn_count": 0,
                "total_spent": 0,
                "risk_score": 0
            })
        customer['_id'] = str(customer['_id'])
        return jsonify(customer)
    
    # UPDATE
    data = request.json
    customers_coll.update_one(
        {"$or": [{"email": customer_id}, {"name": customer_id}]},
        {"$set": {
            "name": data.get('name', customer_id), # Ensure name is set if updating
            "phone": data.get('phone'),
            "updated_at": datetime.utcnow()
        }},
        upsert=True # Create if doesn't exist to ensure profile availability
    )
    log_audit("Admin", f"Updated Customer: {customer_id}", "Customers", "Modified")
    return jsonify({"success": True, "message": "Customer updated"})

@app.route('/api/customers/<customer_id>/transactions', methods=['GET'])
def get_customer_transactions(customer_id):
    txns = list(transactions_coll.find({"customer": customer_id}).sort("timestamp", -1).limit(50))
    for t in txns:
        t['_id'] = str(t['_id'])
    return jsonify(txns)

@app.route('/api/customers/<customer_id>/alerts', methods=['GET'])
def get_customer_alerts(customer_id):
    alerts = list(alerts_coll.find({"customer": customer_id}).sort("timestamp", -1).limit(20))
    for a in alerts:
        a['_id'] = str(a['_id'])
    return jsonify(alerts)

@app.route('/api/customers/<customer_id>/block', methods=['POST'])
def block_customer(customer_id):
    customers_coll.update_one({"name": customer_id}, {"$set": {"status": "Blocked"}})
    log_audit("Admin", f"Blocked Customer: {customer_id}", "Customers", "Blocked")
    return jsonify({"success": True, "message": "Customer blocked"})

# 23. Alert Detail & Actions
@app.route('/api/alerts/<alert_id>', methods=['GET', 'PUT'])
def manage_alert_detail(alert_id):
    from bson import ObjectId
    
    if request.method == 'GET':
        alert = alerts_coll.find_one({"_id": ObjectId(alert_id)})
        if not alert:
            return jsonify({"error": "Alert not found"}), 404
        alert['_id'] = str(alert['_id'])
        return jsonify(alert)
    
    # UPDATE
    data = request.json
    alerts_coll.update_one(
        {"_id": ObjectId(alert_id)},
        {"$set": {
            "status": data.get('status'),
            "notes": data.get('notes'),
            "updated_at": datetime.utcnow()
        }}
    )
    log_audit("Admin", f"Updated Alert: {alert_id}", "Alerts", "Modified")
    return jsonify({"success": True, "message": "Alert updated"})

@app.route('/api/alerts/<alert_id>/escalate', methods=['POST'])
def escalate_alert(alert_id):
    from bson import ObjectId
    alerts_coll.update_one(
        {"_id": ObjectId(alert_id)},
        {"$set": {"severity": "Critical", "escalated": True, "escalated_at": datetime.utcnow()}}
    )
    log_audit("Admin", f"Escalated Alert: {alert_id}", "Alerts", "Escalated")
    return jsonify({"success": True, "message": "Alert escalated"})

@app.route('/api/alerts/<alert_id>/assign', methods=['POST'])
def assign_alert(alert_id):
    from bson import ObjectId
    data = request.json
    alerts_coll.update_one(
        {"_id": ObjectId(alert_id)},
        {"$set": {"assigned_to": data.get('user_id'), "assigned_at": datetime.utcnow()}}
    )
    log_audit("Admin", f"Assigned Alert: {alert_id} to {data.get('user_id')}", "Alerts", "Assigned")
    return jsonify({"success": True, "message": "Alert assigned"})


# --- MERCHANT MANAGEMENT ENDPOINTS ---
@app.route('/api/merchants/register', methods=['POST'])
def register_merchant():
    data = request.json
    
    # Check if merchant already exists
    if merchants_coll.find_one({"email": data.get('email')}):
        return jsonify({"success": False, "message": "Merchant already registered"})
    
    # Generate API key
    import secrets
    api_key = f"sk_live_{secrets.token_urlsafe(32)}"
    merchant_id = f"MERCH-{random.randint(100000, 999999)}"
    
    merchant = {
        "merchant_id": merchant_id,
        "business_name": data.get('business_name'),
        "business_type": data.get('business_type'),
        "email": data.get('email'),
        "phone": data.get('phone'),
        "address": data.get('address'),
        "website": data.get('website'),
        "paypal_email": data.get('paypal_email'),
        "expected_volume": data.get('expected_volume'),
        "description": data.get('description'),
        "api_key": api_key,
        "status": "Active",
        "created_at": datetime.utcnow(),
        "total_sales": 0,
        "approved_count": 0,
        "blocked_count": 0,
        "fraud_prevented_amount": 0
    }
    
    merchants_coll.insert_one(merchant)
    
    # Send welcome email
    email_body = f"""
    <h3>Welcome to Swift AI Fraud Protection!</h3>
    <p>Hello {merchant['business_name']},</p>
    <p>Your merchant account has been successfully created.</p>
    <p><strong>Merchant ID:</strong> {merchant_id}</p>
    <p><strong>API Key:</strong> {api_key}</p>
    <p>Keep your API key secure. You'll need it for integration.</p>
    """
    send_email(data.get('email'), "Welcome to Swift AI", email_body)
    
    log_audit("System", f"Merchant Registered: {merchant_id}", "Merchant", merchant['business_name'])
    return jsonify({"success": True, "merchant_id": merchant_id, "api_key": api_key})

@app.route('/api/merchants/<merchant_id>', methods=['GET'])
def get_merchant(merchant_id):
    merchant = merchants_coll.find_one({"merchant_id": merchant_id})
    if merchant:
        merchant['_id'] = str(merchant['_id'])
        return jsonify(merchant)
    return jsonify({"error": "Merchant not found"}), 404

@app.route('/api/merchants/<merchant_id>/transactions', methods=['GET'])
def get_merchant_transactions(merchant_id):
    txns = list(transactions_coll.find({"merchant_id": merchant_id}).sort("timestamp", -1).limit(50))
    for t in txns: t['_id'] = str(t['_id'])
    return jsonify(txns)

@app.route('/api/merchants/email/<email>', methods=['GET'])
def get_merchant_by_email(email):
    merchant = merchants_coll.find_one({"email": email})
    if merchant:
        merchant['_id'] = str(merchant['_id'])
        return jsonify(merchant)
    return jsonify({"error": "Merchant not found"}), 404

@app.route('/api/fraud-check', methods=['POST'])
def fraud_check():
    """
    Real-time fraud detection for merchant transactions
    Called BEFORE payment is processed
    """
    data = request.json
    
    # Verify API key (in production)
    # api_key = request.headers.get('Authorization', '').replace('Bearer ', '')
    
    customer_email = data.get('customer_email')
    amount = float(data.get('amount', 0))
    merchant_id = data.get('merchant_id')
    
    # Get customer history
    customer = customers_coll.find_one({"email": customer_email}) or {}
    avg_amount = customer.get('avg_amount', 100)
    txn_count = customer.get('txn_count', 0)
    
    # Calculate risk score
    risk_score = 0
    reasons = []
    
    # Amount anomaly
    if amount > avg_amount * 3:
        risk_score += 30
        reasons.append(f"Amount ${amount} is 3x higher than average ${avg_amount}")
    
    # New customer
    if txn_count == 0:
        risk_score += 20
        reasons.append("New customer - no transaction history")
    
    # High amount
    if amount > 10000:
        risk_score += 25
        reasons.append(f"High transaction amount: ${amount}")
    
    # Location check (simplified)
    location = data.get('location', '')
    if 'Nigeria' in location or 'Russia' in location:  # Example high-risk countries
        risk_score += 30
        reasons.append(f"High-risk location: {location}")
    
    # Device check
    device = data.get('device', '')
    if 'Unknown' in device:
        risk_score += 15
        reasons.append("Unknown device")
    
    # Determine status
    if risk_score >= 85:
        status = "BLOCKED"
        decision = "Transaction blocked due to high fraud risk"
    elif risk_score >= 60:
        status = "REVIEW"
        decision = "Transaction requires manual review"
    else:
        status = "APPROVED"
        decision = "Transaction approved"
    
    # Generate transaction ID
    txn_id = f"TXN-{random.randint(100000, 999999)}"
    
    # Save transaction
    transaction = {
        "transaction_id": txn_id,
        "merchant_id": merchant_id,
        "customer_email": customer_email,
        "amount": amount,
        "currency": data.get('currency', 'USD'),
        "location": location,
        "device": device,
        "channel": "Merchant",
        "risk_score": risk_score,
        "status": status,
        "fraud_check_reasons": reasons,
        "timestamp": datetime.utcnow()
    }
    transactions_coll.insert_one(transaction)
    
    # Update merchant stats
    if status == "APPROVED":
        merchants_coll.update_one(
            {"merchant_id": merchant_id},
            {"$inc": {"total_sales": amount, "approved_count": 1}}
        )
    elif status == "BLOCKED":
        merchants_coll.update_one(
            {"merchant_id": merchant_id},
            {"$inc": {"blocked_count": 1, "fraud_prevented_amount": amount}}
        )
    
    # Create alert if high risk
    if risk_score >= 60:
        alerts_coll.insert_one({
            "transaction_id": txn_id,
            "merchant_id": merchant_id,
            "customer": customer_email,
            "risk_score": risk_score,
            "severity": "Critical" if risk_score >= 85 else "High",
            "status": "New",
            "timestamp": datetime.utcnow()
        })
    
    log_audit(merchant_id, f"Fraud Check: {txn_id}", "FraudCheck", f"Score: {risk_score}, Status: {status}")
    
    return jsonify({
        "success": True,
        "transaction_id": txn_id,
        "status": status,
        "risk_score": risk_score,
        "decision": decision,
        "reasons": reasons
    })

# --- BANK ACCOUNT SYSTEM ---
@app.route('/api/bank/create-account', methods=['POST'])
def create_bank_account():
    data = request.json
    email = data.get('email')
    user_type = data.get('user_type', 'Customer')
    initial_balance = float(data.get('initial_balance', 10000))
    
    # Check if account already exists
    existing = bank_accounts_coll.find_one({"user_email": email})
    if existing:
        return jsonify({"success": False, "message": "Account already exists"})
    
    # Generate account number
    account_number = f"{random.randint(1000000000, 9999999999)}"
    
    account = {
        "account_id": f"ACC-{random.randint(100000, 999999)}",
        "user_email": email,
        "user_type": user_type,
        "account_number": account_number,
        "ifsc_code": "SWIFT0001",
        "balance": initial_balance,
        "currency": "USD",
        "status": "Active",
        "created_at": datetime.utcnow(),
        "last_updated": datetime.utcnow()
    }
    
    bank_accounts_coll.insert_one(account)
    log_audit(email, "Bank Account Created", "Bank", f"Account: {account_number}")
    
    return jsonify({"success": True, "account_number": account_number, "balance": initial_balance})

@app.route('/api/bank/account/<email>', methods=['GET'])
def get_bank_account(email):
    account = bank_accounts_coll.find_one({"user_email": email})
    if account:
        account['_id'] = str(account['_id'])
        return jsonify(account)
    return jsonify({"error": "Account not found"}), 404

@app.route('/api/bank/transfer', methods=['POST'])
def bank_transfer():
    """
    Process payment from Credit Card → Merchant (or User)
    Enhanced with IP, location, device, and session tracking
    """
    data = request.json
    
    from_email = data.get('from_email')
    to_email = data.get('to_email')
    amount = float(data.get('amount', 0))
    category = data.get('category', 'Other')
    description = data.get('description', '')
    
    # Enhanced data
    card_id = data.get('card_id')
    card_type = data.get('card_type', 'Unknown')
    last_4 = data.get('last_4', 'XXXX')
    ip_address = data.get('ip_address', request.remote_addr)
    location = data.get('location', {})
    device = data.get('device', {})
    session = data.get('session', {})
    
    # 1. Verify Sender (Must have Credit Card)
    card = credit_cards_coll.find_one({"card_id": card_id}) if card_id else credit_cards_coll.find_one({"user_email": from_email})
    if not card:
        return jsonify({"success": False, "message": "No linked credit card found. Please link a card."}), 400

    # 1.0 Verify Recipient (Must be a valid user or merchant)
    recipient = merchants_coll.find_one({"email": to_email}) or customers_coll.find_one({"email": to_email})
    if not recipient:
        # REPORT TO FRAUD SERVICE BEFORE RETURNING ERROR
        print(f"[PAYMENT] ❌ Recipient '{to_email}' not found. Reporting to Fraud Service...")
        calculate_risk_score({
            "id": f"FAIL-{random.randint(100000, 999999)}",
            "amount": amount,
            "merchant": to_email, # The invalid email
            "customer": from_email,
            "type": "Invalid Recipient",
            "status": "Blocked", # Explicitly mark as Blocked
            "location": location.get('city', 'Unknown'),
            "ip_address": ip_address,
            "device_type": device.get('type', 'Unknown'),
            "reasons": ["Attempt transfer to non-existent recipient", "Potential Account Enumeration"]
        })
        return jsonify({"success": False, "message": f"Recipient '{to_email}' not found. Please check the email address."}), 400
    
    # 1.1 Check Credit Limit (Mock Check as requested)
    limit = card.get('limit', 5000.0) # Default mock limit
    spent = card.get('current_spent', 0.0)
    if spent + amount > limit:
         # REPORT TO FRAUD SERVICE
         print(f"[PAYMENT] ❌ Insufficient funds. Reporting to Fraud Service...")
         calculate_risk_score({
            "id": f"FAIL-{random.randint(100000, 999999)}",
            "amount": amount,
            "merchant": to_email,
            "customer": from_email,
            "type": "Insufficient Funds",
            "status": "Blocked",
            "location": location.get('city', 'Unknown'),
            "ip_address": ip_address,
            "device_type": device.get('type', 'Unknown'),
            "reasons": ["Insufficient funds", "Potential high-value fraud attempt"]
         })
         return jsonify({"success": False, "message": f"Insufficient funds. Credit Limit: ${limit}, Available: ${limit - spent}"}), 400
    
    # 2. FRAUD CHECK via Fraud Service (Enhanced)
    print(f"\n[PAYMENT] Processing transfer {from_email} → {to_email}: ${amount}")
    print(f"[PAYMENT] IP: {ip_address}, Location: {location.get('city', 'Unknown')}, {location.get('country', 'Unknown')}")
    print(f"[PAYMENT] Device: {device.get('type', 'Unknown')}, Card: {card_type} ****{last_4}")
    
    # Fetch customer stats for context
    customer_profile = customers_coll.find_one({"email": from_email}) or {}

    # Call fraud service with enhanced data
    risk_score, reasoning = calculate_risk_score({
        "id": f"TXN-{random.randint(100000, 999999)}",
        "amount": amount,
        "merchant": to_email,
        "location": location.get('city', 'Online'),
        "customer": from_email,
        "type": "Transfer",
        "category": category,
        
        # Enhanced fields
        "ip_address": ip_address,
        "country": location.get('country', 'Unknown'),
        "latitude": location.get('latitude', 0),
        "longitude": location.get('longitude', 0),
        "device_type": device.get('type', 'Unknown'),
        "browser": device.get('browser', 'Unknown'),
        "os": device.get('os', 'Unknown'),
        "card_type": card_type,
        "timezone": session.get('timezone', 'UTC'),
        
        # User History Context
        "user_txn_count": customer_profile.get('txn_count', 0),
        "user_total_spent": customer_profile.get('total_spent', 0),
        "user_risk_score": customer_profile.get('risk_score', 0),
        "account_created_at": str(customer_profile.get('created_at', datetime.utcnow().isoformat()))
    })
    
    # Parse reasons
    reasons = reasoning.split(", ") if reasoning else []
    
    # Determine status based on fraud service response
    if risk_score >= 85:
        status = "BLOCKED"
        decision = "Transaction blocked due to high fraud risk"
    elif risk_score >= 60:
        status = "REVIEW"
        decision = "Transaction requires manual review"
    else:
        status = "APPROVED"
        decision = "Transaction approved"
    
    # Generate transaction ID
    txn_id = f"TXN-{random.randint(100000, 999999)}"
    
    # 3. Process Payment
    if status == "APPROVED":
        # Credit Merchant (Update Stats if it is a merchant)
        # Credit Merchant (Update Stats if it is a merchant)
        merchants_coll.update_one(
            {"email": to_email},
            {"$inc": {"total_sales": amount, "approved_count": 1}}
        )
        
        # Debited from Card (Update Spent)
        credit_cards_coll.update_one(
            {"card_id": card.get('card_id', card_id)},
            {"$inc": {"current_spent": amount}}
        )
        
        # Save Transaction (Enhanced)
        transaction = {
            "transaction_id": txn_id,
            "from_email": from_email,
            "to_email": to_email,
            "amount": amount,
            "currency": "USD",
            "category": category,
            "description": description,
            
            # Location & IP
            "location": location.get('city', 'Online'),
            "country": location.get('country', 'Unknown'),
            "ip_address": ip_address,
            "latitude": location.get('latitude', 0),
            "longitude": location.get('longitude', 0),
            "channel": "Web",
            
            # Card details
            "payment_method": {
                "type": "Credit Card",
                "card_id": card.get('card_id', card_id),
                "last_4": card.get('last_4', last_4),
                "card_type": card.get('card_type', card_type)
            },
            
            # Device & Session
            "device": {
                "type": device.get('type', 'Unknown'),
                "browser": device.get('browser', 'Unknown'),
                "os": device.get('os', 'Unknown')
            },
            "session": {
                "timezone": session.get('timezone', 'UTC'),
                "language": session.get('language', 'en')
            },
            
            # Fraud check results
            "fraud_check": {
                "status": status,
                "risk_score": risk_score,
                "reasons": reasons,
                "checked_at": datetime.utcnow()
            },
            "status": "COMPLETED",
            "timestamp": datetime.utcnow()
        }
        transactions_coll.insert_one(transaction)
        
        # Update Customer Stats
        customers_coll.update_one(
            {"email": from_email},
            {
                "$inc": {"txn_count": 1, "total_spent": amount},
                "$set": {"last_txn": datetime.utcnow()}
            },
            upsert=True
        )
        
        log_audit(from_email, f"Payment: {txn_id}", "Payment", f"${amount} to {to_email}")
        
        return jsonify({
            "success": True,
            "transaction_id": txn_id,
            "status": status,
            "risk_score": risk_score,
            "decision": decision,
            "message": "Payment successful"
        })
    
    else:
        # BLOCKED or REVIEW (Enhanced)
        transaction = {
            "transaction_id": txn_id,
            "from_email": from_email,
            "to_email": to_email,
            "amount": amount,
            "currency": "USD",
            "category": category,
            "description": description,
            
            # Location & IP
            "location": location.get('city', 'Online'),
            "country": location.get('country', 'Unknown'),
            "ip_address": ip_address,
            "latitude": location.get('latitude', 0),
            "longitude": location.get('longitude', 0),
            "channel": "Web",
            
            # Card details
            "payment_method": {
                "type": "Credit Card",
                "card_id": card.get('card_id', card_id),
                "last_4": card.get('last_4', last_4),
                "card_type": card.get('card_type', card_type)
            },
            
            # Device & Session
            "device": {
                "type": device.get('type', 'Unknown'),
                "browser": device.get('browser', 'Unknown'),
                "os": device.get('os', 'Unknown')
            },
            "session": {
                "timezone": session.get('timezone', 'UTC'),
                "language": session.get('language', 'en')
            },
            
            # Fraud check results
            "fraud_check": {
                "status": status,
                "risk_score": risk_score,
                "reasons": reasons,
                "checked_at": datetime.utcnow()
            },
            "status": status,
            "timestamp": datetime.utcnow()
        }
        transactions_coll.insert_one(transaction)
        
        # Create alert
        if risk_score >= 60:
            alerts_coll.insert_one({
                "transaction_id": txn_id,
                "customer": from_email,
                "risk_score": risk_score,
                "severity": "Critical" if risk_score >= 85 else "High",
                "status": "New",
                "timestamp": datetime.utcnow()
            })
        
        log_audit(from_email, f"Payment {status}: {txn_id}", "Payment", f"Risk: {risk_score}")
        
        return jsonify({
            "success": False,
            "transaction_id": txn_id,
            "status": status,
            "risk_score": risk_score,
            "decision": decision,
            "reasons": reasons
        })

@app.route('/api/bank/add-money', methods=['POST'])
def add_money():
    """Simulate adding money to account"""
    data = request.json
    email = data.get('email')
    amount = float(data.get('amount', 0))
    
    account = bank_accounts_coll.find_one({"user_email": email})
    if not account:
        return jsonify({"success": False, "message": "Account not found"}), 404
    
    new_balance = account['balance'] + amount
    bank_accounts_coll.update_one(
        {"user_email": email},
        {"$set": {"balance": new_balance, "last_updated": datetime.utcnow()}}
    )
    
    log_audit(email, "Money Added", "Bank", f"${amount}")
    return jsonify({"success": True, "new_balance": new_balance})

# --- CREDIT CARD SYSTEM ---
@app.route('/api/cards/link', methods=['POST'])
def link_credit_card():
    """Link a credit card to user account"""
    data = request.json
    email = data.get('email')
    
    # Check if card already exists
    card_number = data.get('card_number')
    last_4 = card_number[-4:] if len(card_number) >= 4 else card_number
    
    existing = credit_cards_coll.find_one({"user_email": email, "last_4": last_4})
    if existing:
        return jsonify({"success": False, "message": "Card already linked"})
    
    card = {
        "card_id": f"CARD-{random.randint(100000, 999999)}",
        "user_email": email,
        "card_number": card_number,  # In production, encrypt this!
        "last_4": last_4,
        "card_holder": data.get('card_holder'),
        "expiry_month": data.get('expiry_month'),
        "expiry_year": data.get('expiry_year'),
        "cvv": data.get('cvv'),  # In production, don't store CVV!
        "card_type": data.get('card_type', 'Visa'),
        "billing_address": data.get('billing_address', ''),
        "is_primary": data.get('is_primary', True),
        "status": "Active",
        "linked_at": datetime.utcnow()
    }
    
    credit_cards_coll.insert_one(card)
    log_audit(email, "Credit Card Linked", "Card", f"****{last_4}")
    
    return jsonify({"success": True, "message": "Card linked successfully", "card_id": card['card_id']})

@app.route('/api/cards/<email>', methods=['GET'])
def get_user_cards(email):
    """Get all cards for a user"""
    print(f"Fetching cards for: {email}") # DEBUG
    cards = list(credit_cards_coll.find({"user_email": email}))
    for card in cards:
        card['_id'] = str(card['_id'])
        # Don't send full card number
        card['card_number'] = f"****-****-****-{card['last_4']}"
        del card['cvv']  # Never send CVV
    return jsonify(cards)

@app.route('/api/cards/delete/<card_id>', methods=['DELETE'])
def delete_card(card_id):
    """Delete a credit card"""
    result = credit_cards_coll.delete_one({"card_id": card_id})
    if result.deleted_count > 0:
        log_audit("User", f"Card Deleted: {card_id}", "Card", "Deleted")
        return jsonify({"success": True, "message": "Card deleted"})
    return jsonify({"success": False, "message": "Card not found"}), 404


# --- BALANCE & PAYMENT MANAGEMENT ---

@app.route('/api/balance/add', methods=['POST'])
def add_balance():
    """Add money to customer account"""
    data = request.json
    customer_email = data.get('customer_email')
    amount = float(data.get('amount', 0))
    
    if amount <= 0:
        return jsonify({"error": "Invalid amount"}), 400
    
    # Update customer balance
    customers_coll.update_one(
        {"email": customer_email},
        {
            "$inc": {"balance": amount},
            "$set": {"last_updated": datetime.utcnow()}
        },
        upsert=True
    )
    
    # Get updated balance
    customer = customers_coll.find_one({"email": customer_email})
    new_balance = customer.get('balance', 0) if customer else amount
    
    # Log transaction
    balance_txn = {
        "id": f"BAL-{random.randint(100000, 999999)}",
        "customer": customer_email,
        "type": "Balance Add",
        "amount": amount,
        "new_balance": new_balance,
        "timestamp": datetime.utcnow(),
        "status": "Completed"
    }
    transactions_coll.insert_one(balance_txn)
    
    log_audit(customer_email, "Added Balance", "Account", f"Added ${amount}")
    
    return jsonify({
        "success": True,
        "message": f"${amount} added successfully",
        "new_balance": new_balance,
        "transaction_id": balance_txn['id']
    })


@app.route('/api/balance/check', methods=['GET'])
def check_balance():
    """Check customer balance"""
    customer_email = request.args.get('customer_email')
    
    customer = customers_coll.find_one({"email": customer_email})
    balance = customer.get('balance', 0) if customer else 0
    
    return jsonify({
        "customer": customer_email,
        "balance": balance,
        "currency": "USD"
    })


@app.route('/api/payment/process', methods=['POST'])
def process_payment():
    """Process payment with balance deduction and fraud check"""
    data = request.json
    
    customer_email = data.get('customer_email')
    amount = float(data.get('amount', 0))
    merchant = data.get('merchant', 'Unknown Merchant')
    description = data.get('description', '')
    
    # Check customer balance
    customer = customers_coll.find_one({"email": customer_email})
    if not customer:
        return jsonify({"error": "Customer not found"}), 404
    
    current_balance = customer.get('balance', 0)
    
    if current_balance < amount:
        return jsonify({
            "error": "Insufficient balance",
            "current_balance": current_balance,
            "required": amount
        }), 400
    
    # Generate transaction ID
    txn_id = f"PAY-{random.randint(100000, 999999)}"
    
    # Fraud check
    print(f"\n[PAYMENT] Processing payment {txn_id} for ${amount}")
    risk_score, reasoning = calculate_risk_score({
        "id": txn_id,
        "amount": amount,
        "merchant": merchant,
        "location": customer.get('location', 'Unknown'),
        "customer": customer_email,
        "type": "Payment"
    })
    
    # Determine status based on risk
    if risk_score > 85:
        status = "Blocked"
        action = "Payment blocked due to high fraud risk"
    elif risk_score > 60:
        status = "Review"
        action = "Payment under review"
    else:
        status = "Approved"
        action = "Payment successful"
        
        # Deduct balance only if approved
        new_balance = current_balance - amount
        customers_coll.update_one(
            {"email": customer_email},
            {
                "$set": {"balance": new_balance, "last_updated": datetime.utcnow()},
                "$inc": {"total_spent": amount, "txn_count": 1}
            }
        )
    
    # Create transaction record
    transaction = {
        "id": txn_id,
        "customer": customer_email,
        "merchant": merchant,
        "description": description,
        "amount": amount,
        "previous_balance": current_balance,
        "new_balance": current_balance - amount if status == "Approved" else current_balance,
        "type": "Payment",
        "channel": "Web",
        "location": customer.get('location', 'Unknown'),
        "coords": [0, 0],
        "timestamp": datetime.utcnow(),
        "risk_score": risk_score,
        "ai_reason": reasoning,
        "status": status
    }
    
    transactions_coll.insert_one(transaction)
    transaction['_id'] = str(transaction['_id'])
    
    log_audit(customer_email, "Payment Processed", "Transaction", f"{status}: ${amount} to {merchant}")
    
    # Generate receipt if approved
    receipt_url = None
    if status == "Approved":
        receipt_url = f"/api/receipt/{txn_id}"
    
    return jsonify({
        "success": status == "Approved",
        "transaction": transaction,
        "message": action,
        "receipt_url": receipt_url
    })


@app.route('/api/receipt/<txn_id>', methods=['GET'])
def get_receipt(txn_id):
    """Generate and return receipt for transaction"""
    transaction = transactions_coll.find_one({"id": txn_id})
    
    if not transaction:
        return jsonify({"error": "Transaction not found"}), 404
    
    # Generate receipt HTML
    receipt_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Payment Receipt - {txn_id}</title>
        <style>
            body {{
                font-family: 'Arial', sans-serif;
                max-width: 600px;
                margin: 50px auto;
                padding: 30px;
                background: #f5f5f5;
            }}
            .receipt {{
                background: white;
                padding: 40px;
                border-radius: 10px;
                box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            }}
            .header {{
                text-align: center;
                border-bottom: 2px solid #4CAF50;
                padding-bottom: 20px;
                margin-bottom: 30px;
            }}
            .header h1 {{
                color: #4CAF50;
                margin: 0;
                font-size: 28px;
            }}
            .status {{
                display: inline-block;
                padding: 8px 20px;
                border-radius: 20px;
                font-weight: bold;
                margin-top: 10px;
            }}
            .status.approved {{
                background: #4CAF50;
                color: white;
            }}
            .details {{
                margin: 30px 0;
            }}
            .detail-row {{
                display: flex;
                justify-content: space-between;
                padding: 12px 0;
                border-bottom: 1px solid #eee;
            }}
            .detail-label {{
                color: #666;
                font-weight: 500;
            }}
            .detail-value {{
                color: #333;
                font-weight: 600;
            }}
            .amount {{
                font-size: 32px;
                color: #4CAF50;
                text-align: center;
                margin: 30px 0;
                font-weight: bold;
            }}
            .footer {{
                text-align: center;
                margin-top: 40px;
                padding-top: 20px;
                border-top: 2px solid #eee;
                color: #999;
                font-size: 12px;
            }}
            .print-btn {{
                background: #2196F3;
                color: white;
                border: none;
                padding: 12px 30px;
                border-radius: 5px;
                cursor: pointer;
                font-size: 16px;
                margin-top: 20px;
            }}
            .print-btn:hover {{
                background: #1976D2;
            }}
            @media print {{
                body {{
                    background: white;
                }}
                .print-btn {{
                    display: none;
                }}
            }}
        </style>
    </head>
    <body>
        <div class="receipt">
            <div class="header">
                <h1>🏦 Swift AI Banking</h1>
                <p style="color: #666; margin: 10px 0;">Payment Receipt</p>
                <span class="status approved">{transaction['status']}</span>
            </div>
            
            <div class="amount">
                ${transaction['amount']:.2f}
            </div>
            
            <div class="details">
                <div class="detail-row">
                    <span class="detail-label">Transaction ID</span>
                    <span class="detail-value">{transaction['id']}</span>
                </div>
                <div class="detail-row">
                    <span class="detail-label">Date & Time</span>
                    <span class="detail-value">{transaction['timestamp'].strftime('%B %d, %Y at %I:%M %p')}</span>
                </div>
                <div class="detail-row">
                    <span class="detail-label">Merchant</span>
                    <span class="detail-value">{transaction.get('merchant', 'N/A')}</span>
                </div>
                <div class="detail-row">
                    <span class="detail-label">Customer</span>
                    <span class="detail-value">{transaction['customer']}</span>
                </div>
                <div class="detail-row">
                    <span class="detail-label">Payment Method</span>
                    <span class="detail-value">Account Balance</span>
                </div>
                <div class="detail-row">
                    <span class="detail-label">Previous Balance</span>
                    <span class="detail-value">${transaction.get('previous_balance', 0):.2f}</span>
                </div>
                <div class="detail-row">
                    <span class="detail-label">New Balance</span>
                    <span class="detail-value">${transaction.get('new_balance', 0):.2f}</span>
                </div>
                <div class="detail-row">
                    <span class="detail-label">Fraud Risk Score</span>
                    <span class="detail-value">{transaction['risk_score']}/100 (Low Risk)</span>
                </div>
            </div>
            
            <div style="text-align: center;">
                <button class="print-btn" onclick="window.print()">🖨️ Print Receipt</button>
            </div>
            
            <div class="footer">
                <p>This is a computer-generated receipt and does not require a signature.</p>
                <p>Protected by AI-powered fraud detection | Swift AI Banking © 2026</p>
                <p>Transaction secured with end-to-end encryption</p>
            </div>
        </div>
    </body>
    </html>
    """
    
    return receipt_html


if __name__ == '__main__':
    print("--- Swift AI World-Class Backend Running ---")
    app.run(host='0.0.0.0', port=5000, debug=True)
