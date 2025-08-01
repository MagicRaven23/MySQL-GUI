from flask import Flask, render_template, request, make_response, redirect, url_for
import mysql.connector

def mysql_init(usr, password, database):
    global mydb
    mydb = mysql.connector.connect(
      host="localhost",
      user=usr,
      password=password,
      database=database
    )

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # Getting input with name = user  in HTML form
        user = request.form.get("user")
        # Getting input with name = password in HTML form
        password = request.form.get("password")

        try:
           mysql_init(user, password)
           print(mydb)
           mycursor = mydb.cursor()
           mycursor.execute("SHOW DATABASES")
           print(mycursor)

           for i in mycursor:
              print(i)

           # Send the User and Password to the next side
           resp = make_response(redirect(url_for('database')))
           resp.set_cookie('user', user)
           resp.set_cookie('pass', password)
           return resp

        except mysql.connector.errors.ProgrammingError as e:
           print(e)
           return "Wrong Password or User"

    return render_template('index.html')

@app.route("/database", methods=["GET", "POST"])
def database():
    # Catch the User and Password from the Cookie
    user_cookie = request.cookies.get('user')
    pass_cookie = request.cookies.get('pass')
    print(user_cookie, pass_cookie)
    mysql_init(user_cookie, pass_cookie, '')
    mycursor = mydb.cursor()
    mycursor.execute("SHOW DATABASES")

    data = mycursor.fetchall()

    for i in data:
        print(i[0])

    if request.method == 'POST':
        database = request.form.getlist('selected_items')
        print("Ausgewählt:", database[0])
        #return f"Du hast diese ID ausgewählt: {', '.join(database)}"
        # Send the selection to the next sides
        resp = make_response(redirect(url_for('table')))
        resp.set_cookie('selection', database[0])
        return resp

    return render_template('database.html', mycursor=data)

@app.route("/table", methods=["GET", "POST"])
def table():
    # Catch the Database selected
    database_cookie = request.cookies.get('selection')
    # Catch the User and Password from the Cookie
    user_cookie = request.cookies.get('user')
    pass_cookie = request.cookies.get('pass')
    print(user_cookie, pass_cookie)

    mysql_init(user_cookie, pass_cookie, database_cookie)
    mycursor = mydb.cursor()
    mycursor.execute("SHOW TABLES")

    data = mycursor.fetchall()

    for i in data:
        print(i[0])
    #print(database_cookie)

    return render_template('table.html', database=database_cookie, table=data)

if __name__ == "__main__":
    app.run(port=8080, debug=True)
