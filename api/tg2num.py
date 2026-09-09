# -*- coding: utf-8 -*-
# TG ID to Number Lookup API
# Credit: @Qfrexx (Sumi Hacker)

import json
from flask import Flask, request, jsonify

app = Flask(__name__)

# 🔥 CONFIG
API_KEY = "UNIQVERCEL"

# ==========================================
# ROOT ENDPOINT (TEST KE LIYE)
# ==========================================
@app.route('/')
def home():
    return jsonify({
        'status': 'success',
        'message': '🚀 API is live!',
        'endpoints': {
            '/api/tg2num': 'GET - Convert Telegram ID to Number'
        },
        'usage': '/api/tg2num?key=UNIQVERCEL&id=YOUR_TG_ID',
        'example': '/api/tg2num?key=UNIQVERCEL&id=8661022214',
        'credit': '@Qfrexx'
    })

# ==========================================
# MAIN API ENDPOINT
# ==========================================
@app.route('/api/tg2num', methods=['GET'])
def tg_to_number():
    # 🔥 1. API Key Check
    key = request.args.get('key')
    if key != API_KEY:
        return jsonify({
            'status': 'error',
            'message': 'Invalid API key',
            'credit': '@Qfrexx'
        }), 401

    # 🔥 2. ID Check
    tg_id = request.args.get('id')
    if not tg_id:
        return jsonify({
            'status': 'error',
            'message': 'Missing Telegram ID or Username',
            'usage': '/api/tg2num?key=UNIQVERCEL&id=123456789',
            'credit': '@Qfrexx'
        }), 400

    tg_id = tg_id.strip()

    # 🔥 3. Mock Data (Real API call ke liye replace karo)
    mock_data = {
        '8661022214': {
            'phone': '+919999999999',
            'name': 'Qfrexx',
            'username': '@Qfrexx'
        },
        '123456789': {
            'phone': '+919876543210',
            'name': 'Demo User',
            'username': '@demouser'
        }
    }

    # 🔥 4. Check karo agar ID data me hai
    if tg_id in mock_data:
        return jsonify({
            'status': 'success',
            'data': mock_data[tg_id],
            'credit': '@Qfrexx',
            'developer': '@Qfrexx (Sumi Hacker)'
        })
    else:
        return jsonify({
            'status': 'error',
            'message': 'No data found for this Telegram ID',
            'credit': '@Qfrexx'
        }), 404

# ==========================================
# VERCEL SERVERLESS HANDLER
# ==========================================
# 🔥 YEH IMPORTANT HAI — Vercel ke liye
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

# Vercel serverless handler
handler = app
