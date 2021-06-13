from flask import Flask, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import redirect
import string, random
import os
from .qrCode import detectFromImage, validateURL, detectLiveFeed, createQRcode


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///urls.db"
db = SQLAlchemy(app)
UPLOAD_FOLDER = "./static"
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg"}
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


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


@app.route("/qrcode", methods=["GET", "POST"])
def qrPage():
    context = None
    if request.method == "POST":
        # print(request.form["cam"])
        if request.files:
            # print("File Found")
            f = request.files["file"]
            path = os.path.join(app.config["UPLOAD_FOLDER"], f.filename)
            f.save(path)
            saved_filename = path
            result = detectFromImage(path=saved_filename)

            if not result:
                context = "No QR Code Found"
            else:
                context = {
                    "url": None,
                    "data": None,
                    "cam": False,
                    "file": True,
                    "create": False,
                }
                if validateURL(result):
                    context["url"] = result
                else:
                    context["data"] = result
        elif request.form["data"]:
            if request.form["data"] != "none":
                # print("Creating QR")
                # print(request.form["data"])
                received_data = request.form["data"]
                if len(received_data) < 1:
                    context = None
                else:
                    createQRcode(received_data)

                    context = {
                        "url": None,
                        "data": None,
                        "cam": False,
                        "file": False,
                        "create": True,
                    }
            elif request.form["cam"] == "cam":
                context = {
                    "url": None,
                    "data": None,
                    "cam": True,
                    "file": False,
                    "create": False,
                }
                # print("Opening cam")
                # print("cam_val", request.form["cam"])
                res = detectLiveFeed()
                for i in res:
                    if validateURL(i):
                        if context["url"] == None:
                            context["url"] = [i]
                        else:
                            context["url"].append(i)
                    else:
                        if context["data"] == None:
                            context["data"] = [i]
                        else:
                            context["data"].append(i)
            else:
                print("In Else")
        return render_template("qrCode.html", context=context)
    else:
        return render_template("qrCode.html", context=context)


if __name__ == "__main__":
    # app.run()
    app.run(debug=True)
