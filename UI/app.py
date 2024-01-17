from flask import Flask, render_template

app = Flask(__name__)


class Test:
    def hello_fun():
        print("Hello")

    hello_fun()


@app.route("/")
def index():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
