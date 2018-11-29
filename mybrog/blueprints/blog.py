from flask import Blueprint, request, current_app, render_template, url_for,flash, redirect
from mybrog.models import Category, Post, Comment
from mybrog.forms import AdminCommentForm, CommentForm, LoginForm, LinkForm
from mybrog.extensions import db
from flask_login import current_user

blog_bp = Blueprint('blog', __name__)


@blog_bp.route('/', defaults={'page': 1})
@blog_bp.route('/page/<int:page>')
def index(page):
    pagination = Post.query.order_by(Post.timestamp.desc()).paginate(
        page, per_page=current_app.config['BLUELOG_POST_PER_PAGE'])
    posts = pagination.items
    return render_template('blog/index.html',posts=posts, pagination=pagination)


@blog_bp.route('/about')
def about():
    return render_template('blog/about.html')


@blog_bp.route('/category/<int:category_id>')
def show_category(category_id):
    category = Category.query.get_or_404(category_id)
    page = request.args.get('page', 1, type=int)
    pagination = Post.query.with_parent(category).order_by(Post.timestamp.desc()).paginate(
        page, per_page=current_app.config['BLUELOG_POST_PER_PAGE'])
    posts = pagination.items
    return render_template('blog/category.html', category=category, pagination=pagination, posts=posts)





@blog_bp.route('/post/<int:post_id>', methods=['GET', 'POST'])
def show_post(post_id):
    post = Post.query.get_or_404(post_id)
    page = request.args.get('page', 1, type=int)
    per_page = current_app.config['BLUELOG_POST_PER_PAGE']
    pagination = Comment.query.with_parent(post).order_by(Comment.timestamp.desc()).paginate(page, per_page)
    comments = pagination.items
    if current_user.is_authenticated:
        form = AdminCommentForm()
        form.author.data = current_user.name
        form.email.data = current_app.config['BLUELOG_EMAIL']
        form.site.data = url_for('.index')
        from_admin = True
        reviewed = True
    else:
        form = CommentForm()
        from_admin = False
        reviewed = False

    if form.validate_on_submit():
        author = form.author.data
        email = form.email.data
        site = form.site.data
        body = form.body.data
        comment = Comment(
            author=author, email=email, site=site, body=body,
            from_admin=from_admin, post=post, reviewed=reviewed)
        replied_id = request.args.get('reply')
        if replied_id:
            replied_comment = Comment.query.get_or_404(replied_id)
            comment.replied = replied_comment
        db.session.add(comment)
        db.session.commit()
        if current_user.is_authenticated:
            flash('Comment published.', 'success')
        else:
            flash('Thanks, your comment will be published after reviewed.', 'info')
        return redirect(url_for('.show_post', post_id=post_id))
    return render_template('blog/post.html', post=post, current_user=current_user, pagination=pagination, comments=comments, form=form)


@blog_bp.route('/reply/comment/<int:comment_id>')
def reply_comment(comment_id):
    comment = Comment.query.get_or_404(comment_id)
    if not comment.post.can_comment:
        flash('禁止评论', 'warning')
        return redirect(url_for('.show_post', post_id=comment.post_id))
    return redirect(url_for('.show_post', post_id=comment.post_id, reply=comment_id, author=comment.author) + '#comment-form')




