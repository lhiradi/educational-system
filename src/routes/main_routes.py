from flask import Blueprint, render_template, request
from flask_login import login_required, current_user
from src.models.post import Post

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
@login_required
def index():
    page = request.args.get("page", 1, type=int)
    posts = Post.query.paginate(page=page, per_page=5)
    return render_template('index.html', user=current_user, posts=posts)

@main_bp.route("/post/<int:post_id>")
@login_required
def show_post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template("post.html", post=post)