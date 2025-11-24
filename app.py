"""
Flask Web Application for Traceroute
WSL / Windows compatible version
"""

from flask import Flask, render_template, request, jsonify
from traceroute_core import simple_traceroute
import json
import os
from datetime import datetime

app = Flask(__name__)

# Results folder তৈরি করুন
RESULTS_DIR = 'results'
if not os.path.exists(RESULTS_DIR):
    os.makedirs(RESULTS_DIR)


@app.route('/')
def index():
    """Home page"""
    return render_template('index.html')


@app.route('/about')
def about():
    """About page"""
    return render_template('about.html')


@app.route('/trace', methods=['POST'])
def trace():
    """Traceroute run করুন"""
    try:
        data = request.get_json()
        destination = data.get('destination', '')
        max_hops = int(data.get('max_hops', 30))

        if not destination:
            return jsonify({'success': False, 'error': 'Please enter a destination'})

        # Core traceroute call
        result = simple_traceroute(destination, max_hops)

        # Save JSON result
        if result.get('success'):
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"{RESULTS_DIR}/trace_{destination.replace('.', '_')}_{timestamp}.json"
            with open(filename, 'w') as f:
                json.dump(result, f, indent=2)

        return jsonify(result)

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})


@app.route('/history')
def history():
    """Previous results দেখান"""
    try:
        files = []
        for filename in os.listdir(RESULTS_DIR):
            if filename.endswith('.json') and filename != '.gitkeep':
                filepath = os.path.join(RESULTS_DIR, filename)
                with open(filepath, 'r') as f:
                    data = json.load(f)
                    files.append({
                        'filename': filename,
                        'destination': data.get('destination'),
                        'timestamp': filename.split('_')[-2] + '_' + filename.split('_')[-1].replace('.json', '')
                    })

        # Sort by timestamp (newest first)
        files.sort(key=lambda x: x['timestamp'], reverse=True)

        return jsonify({'success': True, 'files': files[:10]})

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})


if __name__ == '__main__':
    print("=" * 50)
    print("🚀 Traceroute Web App Starting...")
    print("=" * 50)
    print("📍 Open browser: http://localhost:5000")
    print("⚠️  Note: Run in WSL/Linux or Windows terminal")
    print("=" * 50)

    app.run(debug=True, host='0.0.0.0', port=5000)
