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
    result = customers_coll.update_one(
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
        "coords": [0, 0],  # Add actual coords if available
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
