from flask import render_template, request, redirect, url_for, flash
from flask_mail import Mail, Message
from flask_login import login_user, current_user, logout_user, login_required
from website.forms import ContactForm, LoginForm, NewPost
from website.models import Post, User
from website import mail, app, db
import os

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
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template('blog.html', title='Blog', posts=posts)

@app.route('/blog/new', methods=['GET', 'POST'])
@login_required
def new_blog():
    form = NewPost()
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data)
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('blog'))
    return render_template('new_post.html', title='New Post', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        print(form.username.data)
        if user:
            login_user(user)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('blog'))
    return render_template('login.html', title='Login', form=form)

@app.route('/media')
def media():
    return render_template('media.html', title='Media')