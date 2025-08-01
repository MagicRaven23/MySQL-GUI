from flask import Flask, render_template, request, make_response, redirect, url_for
import mysql.connector

def mysql_init(usr, password):
    global mydb
    mydb = mysql.connector.connect(
      host="localhost",
      user=usr,
      password=password
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
           #return redirect(url_for('database'))

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
    mysql_init(user_cookie, pass_cookie)
    mycursor = mydb.cursor()
    mycursor.execute("SHOW DATABASES")

    data = mycursor.fetchall()

    for i in data:
        print(i[0])

    if request.method == 'POST':
        selected = request.form.getlist('selected_items')
        print("Ausgewählt:", selected)
        return f"Du hast diese ID ausgewählt: {', '.join(selected)}"

    return render_template('database.html', mycursor=data)

@app.route("/table", methods=["GET", "POST"])
def table():
    return render_template('table.html')

if __name__ == "__main__":
    app.run(port=8080, debug=True)
