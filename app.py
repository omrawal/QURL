from flask import Flask, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import redirect
import string, random

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


def shorten_url():
    letters = string.ascii_lowercase + string.ascii_uppercase
    while True:
        rand_letters = random.choices(letters, k=3)
        rand_letters = "".join(rand_letters)
        short_url = Urls.query.filter_by(short=rand_letters).first()
        if not short_url:
            return rand_letters


@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        url_received = request.form["nm"]
        # check if url exists
        found_url = Urls.query.filter_by(long=url_received).first()
        if found_url:
            # return found_url.short
            return redirect(url_for("display_short_url", url=found_url.short))
        else:
            short_url = shorten_url()
            new_url = Urls(long=url_received, short=short_url)
            db.session.add(new_url)
            db.session.commit()
            # return short_url
            return redirect(url_for("display_short_url", url=short_url))
    else:
        return render_template("home.html")


@app.route("/display/<url>")
def display_short_url(url):
    return render_template("shorturl.html", short_url_display=url)


@app.route("/<short_url>")
def redirection(short_url):
    long_url = Urls.query.filter_by(short=short_url).first()
    if long_url:
        return redirect(long_url.long)
    else:
        return "Url Doesn't Exist"


if __name__ == "__main__":
    app.run(debug=True)
