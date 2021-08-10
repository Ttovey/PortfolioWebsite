from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mail import Mail, Message
from forms import ContactForm
import os

app = Flask(__name__)
mail = Mail(app)

app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ.get('gmail_user')
app.config['MAIL_PASSWORD'] = os.environ.get('gmail_pass')


mail = Mail(app)


def send_email(content, email):
    msg = Message('Personal Website Message',
                   sender='Personal Website Admin',
                   recipients=[os.environ.get('gmail_user')])
    msg.body = f'From: {email}, {content}'
    mail.send(msg)

@app.route('/', methods=['GET', 'POST'])
def index():
    form = ContactForm()
    if request.method == 'POST':
        content = form.content.data
        email = form.email.data
        send_email(content, email)
        flash('Message Successfully Sent', 'success')
        return redirect('/#contact')
    return render_template('index.html', title='Home', form=form)

if __name__ == '__main__':
    app.run(debug=True)