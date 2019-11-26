from flask import Flask, render_template, redirect, url_for, request, session, flash, g
from functools import wraps
import sqlite3
from sqlite3 import Error as sql_error
from sql import db_reset, user_find
from flask_cas import CAS
from flask_cas import logout
from flask_cas import login_required as cas_login_required
#import ldap
# from .utils import get_ldap_connection

app = Flask(__name__)

#CAS
cas = CAS(app, '/cas')
app.config['CAS_AFTER_LOGOUT'] = 'welcome'
app.config['CAS_SERVER'] = 'https://cas-auth.rpi.edu/cas'
app.config['CAS_AFTER_LOGIN'] = 'dkasasdfasdffba'

# Flask Login
"""Needs Additional Security"""
app.secret_key = 'my precious'

#SQLite3
app.database = "sample.db"


# login required decorator
def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('You need to login first.')
            return redirect(url_for('login'))
    return wrap


@app.route('/')
@login_required
def home():
    g.db = connect_db(app.database)
    cur = g.db.execute('select * from credentials')
    existing_users = [dict(username=row[0], password=row[1]) for row in cur.fetchall()]
    g.db.close()
    return render_template('index.html',existing_users=existing_users)

@app.route('/welcome')
def welcome():
    return render_template("welcome.html")

@app.route('/register',methods=['GET','POST'])
def register():
    error = None
    if request.method == 'POST':
        u_in = request.form['username']
        p_in = request.form['password']
        g.db = connect_db(app.database)
        cur = g.db.execute('select * from credentials')
        existing_users = [row[0] for row in cur.fetchall()]
        g.db.close()
        if p_in == sql_error:
            error = "Invalid Password. Please try another one."
        elif u_in in existing_users:
            error = 'Username already exists. Please try another one.'
        else:
            conn = connect_db(app.database)
            with conn:
                print(conn.execute('select * from credentials').fetchall())
                cur = conn.cursor()
                cur.execute("insert into credentials values (?, ?)",
                (u_in, p_in))
                print(conn.execute('select * from credentials').fetchall())
            flash('You were just registered!')
            return redirect(url_for('login'))
    return render_template('register.html',error=error)


@app.route('/login',methods=['GET','POST'])
def login():
    error = None
    if request.method == 'POST':
        # Check Username and Password in RPI API
        u_in = request.form['username']
        p_in = request.form['password']
        g.db = connect_db(app.database)
        cur = g.db.execute('select * from credentials')
        p_out = user_find(g.db,u_in)
        g.db.close()
        if p_out == sql_error:
            error = 'Invalid credentials. Please try again.'
        else:
            if p_in == p_out:
                session['logged_in'] = True
                flash('You were just logged in!')
                return redirect(url_for('home'))
            else:
                error = 'Invalid credentials. Please try again.'
    return render_template('login.html',error=error)

@app.route('/logout')
@login_required
def logout():
    session.pop('logged_in', None)
    flash('You were just logged out!')
    return redirect(url_for('cas.logout'))

@app.route('/cas_logged_in')
@cas_login_required
def cas_logged_in():
    session['logged_in'] = True
    flash('You were just logged in!')
    return redirect(url_for('home'))

@app.route('/reset')
@login_required
def reset():
    db_reset(app.database)
    flash('Database refreshed')
    return redirect(url_for('home'))

def connect_db(db):
    conn = None
    try:
        conn = sqlite3.connect(db)
    except sql_error as e:
        print(e)
    return conn
def create_user(conn, user):
    """
    Create a new user
    :param conn:
    :param user:
    :return:
    """
    sql = ''' INSERT INTO credentials(username,password)
              VALUES(?,?) '''
    cur = conn.cursor()
    cur.execute(sql,user)
    return cur.lastrowid




if __name__ == '__main__':
    app.run(debug=True)
