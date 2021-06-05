from flask import Flask, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import redirect


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///urls.db"
db = SQLAlchemy(app)


class Urls(db.Model):
    id_ = db.Column("id_", db.Integer, primary_key=True)
    long = db.Column("long", db.String())
    short = db.Column("short", db.String(3))

    def __init__(self, long, short):
        self.long = long
        self.short = short


@app.before_first_request
def create_table():
    db.create_all()


@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        url_received = request.form["nm"]
        # check if url exists
        found_url = Urls.query.filter_by(long=url_received).first()
        if found_url:
            return redirect(url_for("display_short_url", url=found_url.short))
        return url_received
    else:
        return render_template("home.html")


if __name__ == "__main__":
    app.run(debug=True)


# 24:19
