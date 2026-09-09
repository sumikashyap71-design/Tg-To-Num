# -*- coding: utf-8 -*-
# TG ID to Number Lookup API
# Credit: @Qfrexx (Sumi Hacker)

import requests
import json
import re
from flask import Flask, request, jsonify

app = Flask(__name__)

# ==========================================
# CONFIGURATION
# ==========================================
API_KEY = "UNIQVERCEL"
TELEGRAM_API = "https://api.telegram.org/bot"
BOT_TOKEN = "8875372741:AAHmNtvFEvupgCtFmC53RPyZMWf4S6wYWJ4"

# ==========================================
# MAIN API ENDPOINT
# ==========================================
@app.route('/api/tg2num', methods=['GET'])
def tg_to_number():
    key = request.args.get('key')
    if key != API_KEY:
        return jsonify({
            'status': 'error',
            'message': 'Invalid API key',
            'credit': '@Qfrexx'
        }), 401

    tg_id = request.args.get('id')
    if not tg_id:
        return jsonify({
            'status': 'error',
            'message': 'Missing Telegram ID or Username',
            'usage': '/api/tg2num?key=UNIQVERCEL&id=123456789',
            'credit': '@Qfrexx'
        }), 400

    tg_id = tg_id.strip()
    result = fetch_number_from_tg(tg_id)

    if result:
        return jsonify({
            'status': 'success',
            'data': result,
            'credit': '@Qfrexx',
            'developer': '@Qfrexx (Sumi Hacker)'
        })
    else:
        return jsonify({
            'status': 'error',
            'message': 'No data found for this Telegram ID',
            'credit': '@Qfrexx'
        }), 404

def fetch_number_from_tg(tg_id):
    results = {}

    # Method 1: Telegram API
    try:
        url = f"{TELEGRAM_API}{BOT_TOKEN}/getChat"
        params = {'chat_id': tg_id}
        response = requests.get(url, params=params, timeout=10)
        if response.status_code == 200:
            data = response.json()
            if data.get('ok') and data.get('result'):
                chat = data['result']
                results['name'] = chat.get('first_name', 'N/A')
                results['username'] = chat.get('username', 'N/A')
                results['last_name'] = chat.get('last_name', 'N/A')
                results['type'] = chat.get('type', 'N/A')
                if 'phone_number' in chat:
                    results['phone'] = chat['phone_number']
    except:
        pass

    # Method 2: External API
    try:
        url = f"https://tg-info-api.vercel.app/api?user={tg_id}"
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            if data.get('status') == 'success':
                results['tg_info'] = data.get('data', {})
    except:
        pass

    return results if results else None

@app.route('/')
def home():
    return jsonify({
        'status': 'success',
        'message': '🚀 TG to Number API is live!',
        'endpoints': {'/api/tg2num': 'GET - Convert Telegram ID to Number'},
        'usage': '/api/tg2num?key=UNIQVERCEL&id=YOUR_TG_ID',
        'example': '/api/tg2num?key=UNIQVERCEL&id=8661022214',
        'credit': '@Qfrexx'
    })

# ==========================================
# VERCEL SERVERLESS HANDLER
# ==========================================
# For Vercel deployment
def handler(event, context):
    return app(event, context)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
