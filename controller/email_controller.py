# controller/usuario_controller.py
from app import app
from flask import  request, jsonify
from services.email_service import send_email



@app.route('/send-email', methods=['POST'])
def send_email_to_user():
    data = request.get_json()
    email = data.get('email')
    subject = 'Bem-vindo!'
    body = 'Obrigado por se registrar no nosso sistema.'

    try:
        send_email(subject, [email], body)
        return jsonify({'message': 'E-mail enviado com sucesso!'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500