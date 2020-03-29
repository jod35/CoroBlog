from . import db,login_manager
from flask_login import UserMixin



class User(db.Model,UserMixin):
    id=db.Column(db.Integer(),primary_key=True)
    username=db.Column(db.String(255),nullable=False)
    email=db.Column(db.String(255),nullable=False)
    password=db.Column(db.Text,nullable=False)
    posts=db.relationship('Post',backref='author',lazy=True)

    def __repr__(self):
        return self.username

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))


class Post(db.Model):
    id=db.Column(db.Integer(),primary_key=True)
    post_comment=db.Column(db.String(140),nullable=False)
    user_id=db.Column(db.Integer(),db.ForeignKey('user.id'))

    def __repr__(self):
        return "{}".format(self.post_comment)