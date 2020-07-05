from flask_mail import Mail, Message
from models import app

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = 'YOUR_ID'
app.config['MAIL_PASSWORD'] = 'YOUR_PASSWORD'
app.config['MAIL_DEFAULT_SENDER'] = 'YOUR_ID'
app.config['MAIL_MAX_EMAILS'] = None
app.config['MAIL_ASCII_ATTACHMENTS'] = False

mail = Mail(app)

def send_mail(address):
    msg = Message('Aapka Swagaat hae!!')

    msg.recipients.append(str(address))

    msg.html = '<h1>Welcome to <b style = "color : red;">Bijli ke dukaan!</b></h1>'

    with app.open_resource('static/images/giphy.gif') as image:
        msg.attach('giphy.gif', 'image/gif', image.read())

    mail.send(msg)
