from flask import Flask, render_template, request, redirect, url_for
from models.user import Db, User
from modules.userform import UserForm

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost/usersdb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = "s14a-key"
Db.init_app(app)


@app.route('/')
def index():
    # Query all
    users = User.query.order_by(User.user_id).all()

    # Iterate and print
    for user in users:
        User.tostring(user)

    return render_template("index.html", users=users)


# @route /adduser - GET, POST
@app.route('/adduser', methods=['GET', 'POST'])
def addUser():
    form = UserForm()
    # If GET
    if request.method == 'GET':
        return render_template('adduser.html', form=form)
    # If POST
    else:
        if form.validate_on_submit():
            first_name = request.form['first_name']
            age = request.form['age']
            new_user = User(first_name=first_name, age=age)
            Db.session.add(new_user)
            Db.session.commit()
            return redirect(url_for('index'))
        else:
            return render_template('adduser.html', form=form)


# @route /adduser/<first_name>/<age>
@app.route('/adduser/<first_name>/<age>')
def addUserFromUrl(first_name, age):
    Db.session.add(User(first_name=first_name, age=age))
    Db.session.commit()
    return redirect(url_for('index'))

# @route /user/<user_id
@app.route('/user/<uid>')
def readUser(uid):
    # Query by user_id
    users = User.query.filter_by(user_id=uid)
    return render_template("index.html", users=users)

# @route /deleteuser/<uid>
@app.route('/deleteuser/<uid>')
def removeUserFromUrl(uid):
    user = User.query.filter_by(user_id=uid).first()
    Db.session.delete(user)
    Db.session.commit()
    return redirect(url_for('index'))

# @route /updateuser/<uid>/<fn>/<a>
@app.route('/updateuser/<uid>/<fn>/<a>')
def updateUserFromUrl(uid, fn, a):
    user = User.query.filter_by(user_id=uid).first()
    user.first_name = fn
    user.age = a
    Db.session.commit()
    return redirect(url_for('index'))


