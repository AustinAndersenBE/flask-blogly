"""Blogly application."""

from flask import Flask, render_template, redirect, url_for, request, flash
from models import db, User, Post, Tag, PostTag
from helpers import is_valid_img_url

app = Flask(__name__)

app.config['SECRET_KEY'] = "secretkey"
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False


db.init_app(app)

with app.app_context():
    db.create_all()

# List all users. 
@app.route('/')
def list_users():
    users = User.query.all()
    return render_template('user_list.html', users=users)

# List all tags
@app.route('/tags')
def list_tags():
    tags = Tag.query.all()
    return render_template('tag_list.html', tags=tags)


# Form to create a new user
@app.route('/users/new')
def new_user_form():
    return render_template('new_user_form.html')

# Form to create a new post
@app.route('/users/<int:user_id>/posts/new')
def new_post_form(user_id):
    user = User.query.get_or_404(user_id)
    tags = Tag.query.all()
    return render_template('new_post_form.html', user=user, tags=tags)

# Form to create a new tag
@app.route('/tags/new')
def new_tag_form():
    return render_template('new_tag_form.html')

# Post route to process form and create new user
@app.route('/users/new', methods=['POST'])
def create_user():
    first_name = request.form.get('first_Name').strip()
    last_name = request.form.get('last_Name').strip()
    image_url = request.form.get('image_URL')

    if first_name and last_name and is_valid_img_url(image_url):
        new_user = User(first_name=first_name, last_name=last_name, image_url=image_url)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('list_users'))

    if not is_valid_img_url(image_url):
        flash('Invalid img URL')
    
    if not first_name:
        flash('First name is required')

    if not last_name:
        flash('Last name is required')

    return redirect(url_for('new_user_form'))

#Post route to create new post
@app.route('/users/<int:user_id>/posts/new', methods=['POST'])
def create_post(user_id):
    title = request.form.get('title').strip()
    content = request.form.get('content').strip()
    selected_tag_names = request.form.getlist('tags') #fetch list of selected tag names


    if title and content:
        new_post = Post(title=title, content=content, user_id=user_id) #create instance of post
        db.session.add(new_post)
        db.session.commit()

        for tag_name in selected_tag_names:
            tag = Tag.query.filter_by(tag_name=tag_name).first() #find tag by name
            if tag:
                new_post_tag = PostTag(post_id=new_post.id, tag_id=tag.id) #create instance of post_tag (creating the connection between post and tag)
                db.session.add(new_post_tag)

        db.session.commit()

        return redirect(url_for('user_detail', user_id=user_id))
    
    if not title or not content:
        flash('Title and content are required')
        return redirect(url_for('new_post_form', user_id=user_id))
    
    return redirect(url_for('new_post_form', user_id=user_id))


# Post route to create new tag
@app.route('/tags/new', methods=['POST'])
def create_tag():
    tag_name = request.form.get('tag_name').strip()

    existing_tag = Tag.query.filter_by(tag_name=tag_name).first()
    if existing_tag:
        flash('Tag name already exists')
        return redirect(url_for('new_tag_form'))
    
    if tag_name:
        new_tag = Tag(tag_name=tag_name)
        db.session.add(new_tag)
        db.session.commit()
        return redirect(url_for('list_tags'))
    
    flash('Tag name is required')
    return redirect(url_for('new_tag_form'))


    
# Shows detail for a single user
@app.route('/users/<int:user_id>')
def user_detail(user_id):
    user = User.query.get_or_404(user_id)  # Query to fetch user by ID
    return render_template('user_detail.html', user=user)

# Show details for the post associated with the user
@app.route('/posts/<int:post_id>')
def post_detail(post_id):
    post = Post.query.get_or_404(post_id)
    user = post.author
    return render_template('post_detail.html', user=user, post=post)

# Show details for a single tag (and all posts associated with it)
@app.route('/tags/<int:tag_id>')
def tag_detail(tag_id):
    tag = Tag.query.get_or_404(tag_id) 
    post_tags = tag.posts.all() #find all post_tags with tag_id
    posts = [post_tag.post for post_tag in post_tags] #for each post_tag, get the post object
    return render_template('tag_detail.html', tag=tag, posts=posts)

# Edit user form
@app.route('/users/<int:user_id>/edit')
def edit_user_form(user_id):
    user = User.query.get_or_404(user_id)  
    return render_template('edit_user.html', user=user)

# Edit post form
@app.route('/posts/<int:post_id>/edit')
def edit_post_form(post_id):
    post = Post.query.get_or_404(post_id)
    tags = Tag.query.all()
    selected_tag_ids = [post_tag.tag_id for post_tag in PostTag.query.filter_by(post_id=post.id).all()]
    return render_template('edit_post.html', post=post, tags=tags, selected_tag_ids=selected_tag_ids)

# Edit tag form
@app.route('/tags/<int:tag_id>/edit')
def edit_tag_form(tag_id):
    tag = Tag.query.get_or_404(tag_id)
    return render_template('edit_tag.html', tag=tag)

# Updating a single user
@app.route('/users/<int:user_id>/edit', methods=['POST'])
def update_user(user_id):
    user = User.query.get_or_404(user_id)
    first_name = request.form.get('first_Name')
    last_name = request.form.get('last_Name')
    image_url = request.form.get('image_URL')

    if first_name and last_name and is_valid_img_url(image_url):
        user.first_name = first_name
        user.last_name = last_name
        user.image_url = image_url
        db.session.commit()
        return redirect(url_for('user_detail', user_id=user.id))

    if not is_valid_img_url(image_url):
        flash('Invalid image URL')
        
    if not first_name:
        flash('First name is required')
        
    if not last_name:
        flash('Last name is required')
    
    return redirect(url_for('edit_user_form', user_id=user_id))

# Updating a single post
@app.route('/posts/<int:post_id>/edit', methods=['POST'])
def update_post(post_id):
    post = Post.query.get_or_404(post_id)

    title = request.form.get('title')
    content = request.form.get('content')
    tag_ids = request.form.getlist('tags') #fetch list of selected tag IDs

    if title and content:
        post.title = title
        post.content = content

        # Delete all existing post tags
        PostTag.query.filter_by(post_id=post.id).delete()

        for tag_id in tag_ids:
            new_post_tag = PostTag(post_id=post.id, tag_id=tag_id)
            db.session.add(new_post_tag)

        db.session.commit()
        return redirect(url_for('post_detail', post_id=post.id))
    else:
        flash('Title and content are required')
        return redirect(url_for('edit_post_form', post_id=post.id))
    


# Updating a single tag
@app.route('/tags/<int:tag_id>/edit', methods=['POST'])
def update_tag(tag_id):
    tag = Tag.query.get_or_404(tag_id)

    tag_name = request.form.get('tag_name').strip()

    if tag_name:
        tag.tag_name = tag_name
        db.session.commit()
        return redirect(url_for('tag_detail', tag_id=tag.id))
    
    flash('Tag name is required')
    return redirect(url_for('edit_tag_form', tag_id=tag.id))

# Delete a user
@app.route('/users/<int:user_id>/delete', methods=['POST'])
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for('list_users'))

# Delete a post
@app.route('/posts/<int:post_id>/delete', methods=['POST'])
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)

    PostTag.query.filter_by(post_id=post.id).delete()

    db.session.delete(post)
    db.session.commit()
    return redirect(url_for('user_detail', user_id=post.user_id))

# Delete a tag
@app.route('/tags/<int:tag_id>/delete', methods=['POST'])
def delete_tag(tag_id):
    tag = Tag.query.get_or_404(tag_id)
    db.session.delete(tag)
    db.session.commit()
    flash('Tag deleted successfully', 'success')
    return redirect(url_for('list_tags'))







