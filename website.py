from flask import Flask

app = Flask(__name__)

@app.route("/")
def index():
    with open("calendar.ics", "r") as file:
        return file.read()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80, debug=False)