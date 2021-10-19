from flask import render_template, request, redirect, url_for, flash
from flask_mail import Mail, Message
from flask_login import login_user, current_user, logout_user, login_required
from website.forms import ContactForm, LoginForm, NewPost, UpdatePost, NewMedia
from website.models import Post, User, Media
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


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/blog', methods=['GET', 'POST'])
def blog():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(
        Post.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template('blog.html', title='Blog', posts=posts)


@app.route('/blog/<int:post_id>')
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', title=post.title, post=post)


@app.route('/blog/<int:post_id>/update', methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    form = UpdatePost()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        return redirect(url_for('post', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content

    return render_template('update_post.html', form=form, title='Update Post')


@app.route('/blog/<int:post_id>/delete', methods=['POST'])
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()
    return redirect('blog')


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


@app.route('/medias')
def medias():
    page = request.args.get('page', 1, type=int)
    medias = Media.query.order_by(
        Media.date_posted.desc()).paginate(page=page, per_page=8)
    return render_template('medias.html', title='Media', medias=medias)


@app.route('/medias/new', methods=['GET', 'POST'])
def new_media():
    form = NewMedia()
    if form.validate_on_submit():
        media = Media(title=form.title.data, type=form.type.data)
        db.session.add(media)
        db.session.commit()
        return redirect(url_for('media'))
    return render_template('new_media.html', title='New Media Post', form=form)


@app.route('/medias/<int:media_id>/delete', methods=['POST'])
def delete_media(media_id):
    media = Media.query.get_or_404(media_id)
    db.session.delete(media)
    db.session.commit()
    return redirect(url_for('medias'))


@app.route('/medias/<int:media_id>')
def media(media_id):
    media = Media.query.get_or_404(media_id)
    return render_template('media.html', media=media)
