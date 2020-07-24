from flask import Flask, render_template, request, flash, redirect, url_for, session
from sqlalchemy import create_engine, text


# DataBase Initialization

eng = create_engine('postgresql://user_name:password@127.0.0.1/db_name')


with eng.connect() as con:
    print("Opened database successfully")

    query = text('''
    CREATE TABLE IF NOT EXISTS users(
        id SERIAL PRIMARY KEY, 
        name TEXT NOT NULL, 
        email Text NOT NULL UNIQUE,
        password TEXT NOT NULL
        );
    ''')

    con.execute(query)

    query = text('''
    CREATE TABLE IF NOT EXISTS gym(id SERIAL PRIMARY KEY, 
        name TEXT NOT NULL,
        contact TEXT NOT NULL,
        foundation TEXT NOT NULL,
        phone TEXT NOT NULL,
        description TEXT NOT NULL,
        instagram TEXT DEFAULT '',
        facebook TEXT DEFAULT ''
        );
    ''')

    con.execute(query)

    con.execute(query)

    query = text('''
    CREATE TABLE IF NOT EXISTS review(
        id SERIAL PRIMARY KEY,
        gid INTEGER NOT NULL,
        gname TEXT NOT NULL,
        uid INTEGER NOT NULL,
        uname TEXT NOT NULL,
        message TEXT NOT NULL
    );
    ''')

    con.execute(query)

    print("Table created successfully")


# Application Initialization


app = Flask(__name__)
app.config['SECRET_KEY'] = "random_string"


# Routes Start


@app.route('/')
@app.route('/login')
def login():

    if 'user_id' not in session:
        return render_template('login.html')

    else:
        return redirect(url_for('index'))


@app.route('/logging_in', methods=["POST"])
def logging_in():

    email = request.form["email"]
    password = request.form["password"]

    with eng.connect() as con:
        data = {"email": email}
        query = text("SELECT * From users WHERE email = :email;")
        cur = con.execute(query, **data)
        row = cur.fetchone()

        if row is None:
            flash('Invalid Login')
            return redirect(url_for('login'))

        elif password == row[3]:
            session.permanent = True
            session['user_id'] = row[0]
            flash('Logged in')
            return redirect(url_for('index'))

        else:
            flash('Incorrect Login Credentials')
            return redirect(url_for('login'))


@app.route('/signup')
def signup():

    if 'user_id' not in session:
        return render_template('signup.html')

    else:
        return redirect(url_for('index'))


@app.route('/signing_up', methods=["POST"])
def signing_up():

    name = request.form['name']
    email = request.form['email']
    password = request.form['password']

    with eng.connect() as con:
        data = {"email": email}
        query = text("SELECT * From users WHERE email = :email;")
        cur = con.execute(query, **data)
        rows = cur.fetchall()

        if rows:
            flash("Email Already Exist")
            return redirect(url_for('signup'))
        else:
            data = {"name": name, "email": email, "password": password}
            query = text("INSERT INTO users(name,email,password) VALUES(:name, :email, :password);")
            con.execute(query, **data)
            flash("Account Created Successfully. Log in to Continue.")
            return redirect(url_for('login'))


@app.route('/logout')
def logout():

    if 'user_id' not in session:
        return render_template('login.html')

    else:
        session.pop('user_id', None)
        return redirect(url_for('login'))


@app.route('/index')
def index():

    if 'user_id' not in session:
        return render_template('login.html')

    else:
        return render_template('index.html')


@app.route('/search', methods=["POST"])
def search():

    if 'user_id' not in session:
        return render_template('login.html')

    else:

        search_keyword = request.form['search']
        rows = []

        with eng.connect() as con:
            query = text("SELECT * From gym WHERE LOWER(REPLACE(name, ' ', '')) LIKE '%{0}%' ;".format(
                search_keyword.replace(" ", "%").lower()))
            cur = con.execute(query)
            rows_filter_by_name = cur.fetchall()
            for row in rows_filter_by_name:
                if row not in rows:
                    rows.append(row)

            query = text("SELECT * From gym WHERE LOWER(REPLACE(contact, ' ', '')) LIKE '%{0}%' ;".format(
                search_keyword.replace(" ", "%").lower()))
            cur = con.execute(query)
            rows_filter_by_contact = cur.fetchall()
            for row in rows_filter_by_contact:
                if row not in rows:
                    rows.append(row)

            query = text("SELECT * From gym WHERE LOWER(REPLACE(foundation, ' ', '')) LIKE '%{0}%' ;".format(
                search_keyword.replace(" ", "%").lower()))
            cur = con.execute(query)
            rows_filter_by_foundation = cur.fetchall()
            for row in rows_filter_by_foundation:
                if row not in rows:
                    rows.append(row)

            query = text("SELECT * From gym WHERE LOWER(REPLACE(phone, ' ', '')) LIKE '%{0}%' ;".format(
                search_keyword.replace(" ", "%").lower()))
            cur = con.execute(query)
            rows_filter_by_phone = cur.fetchall()
            for row in rows_filter_by_phone:
                if row not in rows:
                    rows.append(row)

            query = text("SELECT * From gym WHERE LOWER(REPLACE(description, ' ', '')) LIKE '%{0}%' ;".format(
                search_keyword.replace(" ", "%").lower()))
            cur = con.execute(query)
            rows_filter_by_description = cur.fetchall()
            for row in rows_filter_by_description:
                if row not in rows:
                    rows.append(row)

        return render_template('search_result.html', rows=rows)


@app.route('/result', methods=["GET", "POST"])
def result():

    if 'user_id' not in session:
        return render_template('login.html')

    else:

        if request.method == "POST":
            id = request.form['id']
        else:
            id = request.args.get('id')

        with eng.connect() as con:
            data = {"id": id}

            query = text("SELECT * From gym WHERE id = :id ;")
            cur = con.execute(query, **data)
            row = cur.fetchone()

            query = text("SELECT * From review WHERE gid = :id ;")
            cur = con.execute(query, **data)
            reviews = cur.fetchall()

        return render_template('result.html', row=row, reviews=reviews, reviews_count=len(reviews))


@app.route('/add_review', methods=["POST"])
def add_review():

    if 'user_id' not in session:
        return render_template('login.html')

    else:

        gid = request.form['gid']
        gname = request.form['gname']
        review = request.form['review']

        uid = session['user_id']

        with eng.connect() as con:
            data = {"uid": uid, "gid": gid}

            query = text("SELECT * From review WHERE uid = :uid and gid = :gid;")
            cur = con.execute(query, **data)
            rows = cur.fetchall()

            if rows:
                flash("Per User One Review is allowed for One Gym")
            else:

                data = {"uid": uid}
                query = text("SELECT * From users WHERE id = :uid;")
                cur = con.execute(query, **data)
                row = cur.fetchone()
                uname = row[1]

                data = {"gid": gid, "gname": gname, "uid": uid, "uname": uname, "review": review}
                query = text(
                    "INSERT INTO review(gid,gname,uid,uname,message) values (:gid,:gname,:uid,:uname,:review);")
                con.execute(query, **data)
                flash('Review Added Successfully.')

            return redirect(url_for('result', id=gid))


if __name__ == "__main__":
    app.run(debug=True)
