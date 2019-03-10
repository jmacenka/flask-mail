from flask import Flask, request, url_for
from flask_mail import Mail, Message
from itsdangerous import URLSafeTimedSerializer, SignatureExpired, BadTimeSignature

app = Flask(__name__)
app.config.from_pyfile('config.cfg')
app.config['SECRET_KEY'] = 'Verry_Secret!'
mail = Mail(app)

serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])

@app.route('/', methods=['POST','GET'])
def index():
    if request.method == 'GET':
        return '<form action="/" method="POST"><input name="email"><input type="submit"></form>'

    email = request.form["email"]
    token = serializer.dumps(email, salt='email-confirmation')
    link = url_for('confirm_email', token=token, _external=True)
    msg = Message(
    'Confirm Email',
    sender='no-reply.nbdf@gmx.de',
    recipients=[email]
    )
    msg.body = f'Your link is {link}\nBitte nicht auf diese Mail antworten!'
    mail.send(msg)

    return f'<h1>The email you entered is {email}. The token is {token}</h1>'

@app.route('/confirm_email/<token>')
def confirm_email(token):
    try:
        email = serializer.loads(token, salt='email-confirmation', max_age=10)
    except SignatureExpired:
        return 'The token is expired'
    return 'The token works'

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=8080,debug=True)
