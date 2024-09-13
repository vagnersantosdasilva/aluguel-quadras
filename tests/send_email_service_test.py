from services.email_service import send_email


def send_email_to_user():
    email = 'vagnersantosdasilva@gmail.com'
    subject = 'Bem-vindo!'
    body = 'Obrigado por se registrar no nosso sistema.'

    try:
        send_email(subject, [email], body)

    except Exception as e:
        print (e)

send_email_to_user()