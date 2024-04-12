from flask import Blueprint,render_template,request,flash,redirect,url_for
from .models import User
from .import db
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import login_user, login_required, logout_user, current_user


auth=Blueprint('auth',__name__)

@auth.route('/signup',methods=['GET','POST'])
def signup():
    if request.method=='POST':
        email=request.form.get('email')
        firstName=request.form.get('firstName')
        password1=request.form.get('password1')
        password2=request.form.get('password2')
        print(firstName)
        print(password1)
        print(password2)

        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already exists.', category='error')
        elif len(email) <4:
            flash('Email must be longer',category='error')
        elif len(firstName) <4:
            flash('Name is to Short' ,category='error')
        elif password1!=password2:
            flash('password doesnot match',category='error')
        elif len(password1) <4:
            flash('password is to short')
        else:

            new_user = User(email=email,firstName=firstName,password=generate_password_hash(password1, method='pbkdf2:sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('Account created Successfully',category='Sucsess')
            return redirect(url_for('views.home'))

    return render_template("signup.html",user=current_user)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('Email does not exist.', category='error')

    return render_template("login.html", user=current_user)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


