from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from .models import Post, User, Comment
from . import db

views = Blueprint("views", __name__)

# Home
@views.route("/")
@views.route("/home")
def home():
    posts = Post.query.all()
    return render_template("index.html",user=current_user,posts=posts)

# Post
@views.route("/post/<int:post_id>", methods=['GET', 'POST'])
def post(post_id):
    post = Post.query.filter_by(id=post_id).first()
    comment = Comment.query.filter_by(post_id=post_id).all()
    return render_template("post.html", user=current_user, post=post, comment=comment)

# Create a post
@views.route("/create-post", methods=['GET', 'POST'])
@login_required
def create_post():
    if request.method == "POST":
        title = request.form.get('title')
        text = request.form.get('text')

        if not text:
            flash('Post cannot be empty', category='error')
        elif not title:
            flash('Title cannot be empty', category='error')
        else:
            post = Post(text=text, author=current_user.id, title=title)
            db.session.add(post)
            db.session.commit()
            flash('Post created!', category='success')
            return redirect(url_for('views.home'))

    return render_template('create_post.html', user=current_user)

# Edit post
@views.route("/edit-post/<int:post_id>",methods=['POST', 'GET'])
@login_required
def edit(post_id):
    post= Post.query.filter_by(id=post_id).first()
    if current_user.id != post.user.id:
        flash("You don't have permission to edit this", category='error')
        return redirect(url_for('views.post', post_id=post.id))
    if request.method == "POST":
        title = request.form.get('title')
        text = request.form.get('text')

        if not text:
            flash('Post cannot be empty', category='error')
        if not title:
            flash('Title cannot be empty', category='error')
        else:
            post.text = text
            post.title = title
            db.session.commit()
            flash('Post edited!', category='success')
            return redirect(url_for('views.post', post_id=post.id))
    return render_template('edit_post.html', user=current_user, post=post)

# Delete post
@views.route("/delete-post/<int:post_id>")
@login_required
def delete_post(post_id):
    post = Post.query.filter_by(id=post_id).first()
    if current_user.id != post.user.id:
        flash("You don't have permission to Delete this", category='error')
        return redirect(url_for('views.post', post_id=post.id))
    

    if not post:
        flash("Post does not exist.", category='error')
    else:
        db.session.delete(post)
        db.session.commit()
        flash('Post deleted.', category='success')

    return redirect(url_for('views.home'))

# Create Comment
@views.route("/create-comment/<int:post_id>", methods=['POST'])
@login_required
def create_comment(post_id):
    text = request.form.get('text')

    if not text:
        flash('Comment cannot be empty.', category='error')
    else:
        post = Post.query.filter_by(id=post_id)
        if post:
            comment = Comment(
                text=text, author=current_user.id, post_id=post_id)
            db.session.add(comment)
            db.session.commit()
        else:
            flash('Post does not exist.', category='error')

    return redirect(url_for('views.post', post_id=post_id))


# Delete comment route
@views.route("/delete-comment/<comment_id>")
@login_required
def delete_comment(comment_id):
    comment = Comment.query.filter_by(id=comment_id).first()

    if not comment:
        flash('Comment does not exist.', category='error')
    elif current_user.id != comment.author and current_user.id != comment.post.author:
        flash('You do not have permission to delete this comment.', category='error')
    else:
        db.session.delete(comment)
        db.session.commit()

    return redirect(url_for('views.home'))
