from flask import Flask, render_template, request, redirect, url_for
#import hinnad as h
import flask_login
from flask_login import LoginManager, UserMixin

login_manager = LoginManager()

app = Flask(__name__)
app.secret_key = 'võti'

login_manager.init_app(app)

users = {'kennar':{'pw':'pass1'}, 
         'marie':{'pw':'pass1'}, 
         'user3':{'pw':'pass3'}}

class User(UserMixin):
    pass

@app.errorhandler(401)
def not_logged_in(error):
    return redirect(url_for('login'))

@app.errorhandler(405)
def not_allowed(error):
    return redirect(url_for('index'))

@login_manager.user_loader
def user_loader(username):
    if username not in users:
        return

    user = User()
    user.id = username
    return user

@login_manager.request_loader
def request_loader(request):
    username = request.form.get('username')
    if username not in users:
        return

    user = User()
    user.id = username

    user.is_authenticated = request.form['pw'] == users[username]['pw']

    return user

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        try:
            if request.form.get('pw') == users[username]['pw']:
                user = User()
                user.id = username
                flask_login.login_user(user)
                if username == 'marie':
                    return redirect(url_for('books'))
                #return redirect(url_for('index'))
        except:
            render_template('login.html')
    return render_template('login.html')

@app.route('/logout')
def logout():
    flask_login.logout_user()
    return redirect(url_for('login'))




if __name__ == '__main__':
    app.run(debug=True)
