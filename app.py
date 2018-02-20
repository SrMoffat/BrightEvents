from flask import Flask, render_template, request, flash, redirect, url_for, session
import userClass
import eventsClass
import re


app = Flask(__name__)


app.config['SECRET_KEY'] = "4fr0c0d3things"


user_handler = userClass.UserManager()
event_handler = eventsClass.EventsManager()


def loginRequired():
    if "username" not in session:
        flash("Please log in to continue", "error")
        return "fail"
    else:
        return "pass"


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        username = request.form['username']
        confirm_pass = request.form['cpassword']
        if not re.match(r"(^[a-zA-Z0-9_.]+@[a-zA-Z0-9-]+\.[a-z.]+$)", email):
            flash('Invalid email', 'error')
            return render_template('register.html')
        if len(password) < 6 and len(confirm_pass) < 6:
            flash('The password should be 6 characters long', 'error')
            return render_template("register.html")

        form_submit = user_handler.registerUser(
            username,
            email,
            password,
            confirm_pass)

        if form_submit:
            flash('You have been successfully registered!', 'success')
            return redirect(url_for('signin'))
        elif form_submit == 'password_mismatch':
            flash('The passwords do not match!')
            return render_template('register.html')
        elif form_submit == 'existing_user':
            flash('Username or Email already exists', 'error')
            return render_template('register.html')
    elif request.method == 'GET':
        return render_template('register.html')
    else:
        flash('Invalid request', 'error')
        return render_template('register.html')


@app.route('/signin', methods=['GET', 'POST'])
def signin():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = user_handler.signin(username, password)
        if user == 'successful_login':
            session['username'] = request.form['username']
            global new_user
            new_user = username
            return redirect(url_for('dashboard'))
        return render_template('register.html')
    return render_template('signin.html')


@app.route('/dashboard', methods=["GET", "POST"])
def dashboard():
    if loginRequired() == "fail":
        return redirect(url_for("signin"))
    else:
        if new_user == session['username']:
            user_events = event_handler.return_events()
    return render_template('viewEvents.html' , user_events=user_events)

@app.route('/dashboard/add-event', methods=["GET", "POST"])
def add_event():
    if loginRequired() == "fail":
        return redirect(url_for("signin"))
    else:
        if request.method == "POST":
            event = request.form['event']
            category = request.form['category']
            location = request.form['location']
            date = request.form['date']
            owner = session ['username']

            event_submit = event_handler.createEvent(
                event,
                location,
                category,
                date,
                owner)

            if event_submit == "event_created":
                return render_template("dashboard.html")

          

            #if event_submit:
             #   return render_template('dashboard.html', events=event_submit)

    #return render_template('viewEvents.html', user_events=user_events)

        
        


@app.route('/editProfile')
def editProfile():
    return render_template('editProfile.html')


@app.route('/viewEvents')
def viewEvents():
    return render_template('viewEvents.html')


@app.route('/logout')
def logout():
    session.pop('username', None)
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
