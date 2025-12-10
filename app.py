from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import os
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

app = Flask(__name__)
CORS(app)

# Configuration
app.config['JSON_SORT_KEYS'] = False
app.config['JSON_AS_ASCII'] = False

# Data storage (in production, use a database)
services = [
    {
        'id': 1,
        'title': 'Diagnostyka i naprawa pojazdów',
        'description': 'Nowoczesna diagnostyka komputerowa wszystkich marek pojazdów transportowych',
        'icon': '🔍'
    },
    {
        'id': 2,
        'title': 'Przeglądy techniczne',
        'description': 'Kompleksowe przeglądy zgodne z wymogami CIRED',
        'icon': '✓'
    },
    {
        'id': 3,
        'title': 'Wymiana opon i konserwacja',
        'description': 'Wymiana opon, balansowanie, naprawa felg',
        'icon': '🛞'
    },
    {
        'id': 4,
        'title': 'Serwis hydrauliki',
        'description': 'Naprawa i konserwacja systemów hydraulicznych',
        'icon': '⚙️'
    },
    {
        'id': 5,
        'title': 'Naprawa silnika i skrzyni biegów',
        'description': 'Profesjonalna naprawa silników i skrzyń biegów',
        'icon': '🔧'
    }
]

contact_info = {
    'email': 'iAlmid.poznan2024@gmail.l',
    'phone': '+731531092',
    'address': 'mączniki 25 64-460 nowe skalmierzyce'
    'hours': {
        'weekday': '8 - 20'
        'saturday': '09:00 - 14:00',
        'sunday': 'Zamknięte'
    }
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/services', methods=['GET'])
def get_services():
    return jsonify(services)

@app.route('/api/contact-info', methods=['GET'])
def get_contact_info():
    return jsonify(contact_info)

@app.route('/api/contact', methods=['POST'])
def send_contact_message():
    try:
        data = request.get_json()
        name = data.get('name', '')
        email = data.get('email', '')
        phone = data.get('phone', '')
        message = data.get('message', '')
        
        if not all([name, email, message]):
            return jsonify({'success': False, 'message': 'Brak wymaganych pól'}), 400
        
        # Validation
        if len(name) < 2:
            return jsonify({'success': False, 'message': 'Imię musi mieć co najmniej 2 znaki'}), 400
        
        if len(message) < 10:
            return jsonify({'success': False, 'message': 'Wiadomość musi mieć co najmniej 10 znaków'}), 400
        
        # In production, send actual email
        # For now, just log it
        print(f'\nNowa wiadomość z kontaktu:')
        print(f'Imię: {name}')
        print(f'Email: {email}')
        print(f'Telefon: {phone}')
        print(f'Wiadomość: {message}')
        print(f'Data: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')
        
        return jsonify({
            'success': True,
            'message': 'Wiadomość została wysłana. Odezwiemy się do Ciebie wkrótce!'
        }), 200
    
    except Exception as e:
        print(f'Error: {str(e)}')
        return jsonify({'success': False, 'message': 'Błąd podczas wysyłania wiadomości'}), 500

@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({'status': 'ok', 'timestamp': datetime.now().isoformat()})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
