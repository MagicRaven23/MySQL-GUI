from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # Getting input with name = user  in HTML form
        user = request.form.get("user")
        # Getting input with name = password in HTML form
        password = request.form.get("password")
        return f"mysql -u'{user}' -p'{password}'"

    return render_template('index.html')

if __name__ == "__main__":
    app.run(port=8080, debug=True)
