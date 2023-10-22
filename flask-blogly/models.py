"""Models for Blogly."""
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


# Initialize SQLAlchemy object
db = SQLAlchemy()

class User(db.Model):
    """User Model"""
    
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    image_url = db.Column(db.String(500), nullable=True, default=None)

    posts = db.relationship("Post", back_populates="author", lazy='dynamic') #dynamic means instead of loading items, SQLAlchemy will return another query object to further refine
    
    def __repr__(self):
        return f"<User id={self.id} first_name={self.first_name} last_name={self.last_name}>"
    

class Post(db.Model):

    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(500), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    author = db.relationship("User", back_populates="posts")
    tags = db.relationship('PostTag', back_populates='post', lazy='dynamic')

class PostTag(db.Model):
    
    __tablename__ = 'post_tags'

    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), primary_key=True)
    tag_id = db.Column(db.Integer, db.ForeignKey('tags.id'), primary_key=True)

    post = db.relationship('Post', back_populates='tags', lazy='joined')
    tag = db.relationship('Tag', back_populates='posts', lazy='joined')

class Tag(db.Model):
    __tablename__ = 'tags'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    tag_name = db.Column(db.String(50), nullable=False, unique=True)

    posts = db.relationship('PostTag', back_populates='tag', lazy='dynamic')