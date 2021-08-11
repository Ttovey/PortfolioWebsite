from flask import render_template, request, redirect, url_for, flash
from flask_mail import Mail, Message
from website.forms import ContactForm, LoginForm
from website.models import Post
from website import mail, app

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

@app.route('/blog', methods=['GET', 'POST'])
def blog():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=4)
    return render_template('blog.html', title='Blog', posts=posts)

@app.route('/login', methods=['GET'])
def login():
    form = LoginForm()

    return render_template('login.html', title='Login', form=form)

@app.route('/media')
def media():
    return render_template('media.html', title='Media')