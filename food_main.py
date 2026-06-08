from flask import Flask, render_template, request, make_response, redirect, flash, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, logout_user, login_required, UserMixin, current_user
import json


app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///food.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = "675tyugheufft6ytgdvshtygvhsgv" #notsecret

db = SQLAlchemy(app)

class Food(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    price = db.Column(db.Integer)
    image = db.Column(db.String(200))

class Cart(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    food_id = db.Column(db.Integer, db.ForeignKey('food.id'))
    quantity = db.Column(db.Integer, default=1)
    food = db.relationship('Food')




@app.route("/")
def home():
    return render_template("home.html")


@app.route("/menu")
def menu(): 
    return render_template("menu.html")

@app.route("/categories")
def categories():
    return render_template("categories.html")


@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        subject = request.form["subject"]
        message = request.form["message"]
        print(name, email, subject, message)

    return render_template("contact.html")


@app.route("/cart")
def cart():
    return render_template("cart.html")

@app.route("/login" ,methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        print(email, password)  

        return redirect(url_for("menu"))

    return render_template("login.html")
