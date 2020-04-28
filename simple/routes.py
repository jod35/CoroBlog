from . import app,db
from flask import render_template,request,redirect,url_for,flash
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import login_user,logout_user,current_user
from .models import User,Post

@app.route('/')
def index():
   return render_template('index.html')


@app.route('/signup',methods=['GET', 'POST'])
def create_account():
   if request.method == 'POST':
      username=request.form.get('username')
      email=request.form.get('email')
      password=request.form.get('password')
      confirm=request.form.get('confirm')
      print(confirm)
      print(password)

      existing_user=(User.query.filter_by(username=username).first() or
      User.query.filter_by(email=email).first())

      if existing_user:
         flash("The account already exists")
         return redirect(url_for('create_account'))

      if confirm != password:
         flash("Passwords do not match")
         return redirect(url_for("create_account"))


      new_user=User(username = username, email = email,password = generate_password_hash(password))

      db.session.add(new_user)
      db.session.commit()
      flash("Account created Succcessfully")
      return redirect(url_for('login'))

   return render_template('signup.html')


@app.route('/login',methods=['GET', 'POST'])
def login():
   prompt=request.form.get('prompt')
   password=request.form.get('password')

   existing_user=(User.query.filter_by(username=prompt).first() or
     User.query.filter_by(email=prompt).first()
   )

   if existing_user and check_password_hash(existing_user.password,password):
      login_user(existing_user)
      return redirect(url_for('home_page'))

   return render_template('login.html')

@app.route('/about')
def about():
   return render_template('about.html')

@app.route('/home')
def home_page():

   return render_template('homepage.html')

@app.route('/logout')
def log_out():
   logout_user()
   return redirect(url_for('index'))

@app.route('/post',methods=['POST'])
def create_post():
   post_content=request.form.get('post_content')
   new_post=Post(post_comment=post_content,author=current_user)
   db.session.add(new_post)
   db.session.commit()
   flash("Your post is now live")
   return redirect(url_for('home_page'))

@app.route('/posts')
def posts():
     posts=Post.query.order_by(Post.id.desc()).all()
     context={
        'posts':posts
     }
     return render_template('posts.html',**context)

@app.errorhandler(404)
def not_fount(error):
   return render_template('404.html'),404
