from flask import Flask, render_template, request, make_response, redirect, flash, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, logout_user, login_required, UserMixin, current_user
import json


app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///food.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = "675tyugheufft6ytgdvshtygvhsgv" #notsecret


lm = LoginManager(app)
lm.init_app(app) 
lm.login_view = "login"   

db = SQLAlchemy(app)

class Food(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(100))
    name = db.Column(db.String(100))
    price = db.Column(db.Integer)
    image = db.Column(db.String(200))
    description = db.Column(db.Text)
class Cart(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    food_id = db.Column(db.Integer, db.ForeignKey('food.id'))
    quantity = db.Column(db.Integer, default=1)
    food = db.relationship('Food')

class User(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(15), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    number = db.Column(db.String(15))
    password = db.Column(db.String(100), nullable=False)


with app.app_context():
    db.create_all()


@lm.user_loader
def user_loader(id):
    return User.query.get(int(id))

@app.route("/")
def home():
    return render_template("home.html")


@app.route("/menu")
@login_required
def menu(): 

    search = request.args.get("search","")
    if search:
         data = Food.query.filter(Food.name.contains(search))
    else:
         data = Food.query.all()
    data = Food.query.all()
    return render_template("menu.html", fe_data=data, search=search)


@app.route("/categories")
@login_required
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
@login_required
def cart():
    return render_template("cart.html")


@app.route("/register", methods=["GET","POST"])
def register():

    if request.method == "POST":
         
            first_name = request.form["first_name"]
            email = request.form["email"]
            number = request.form["number"]
            password = request.form["password"]  

            new_user = User(
                first_name = first_name,
                email=email,
                number=number,
                password=password )
            
            db.session.add(new_user)
            db.session.commit()
            flash("registration sucessfull")
            return redirect(url_for("login"))

    return render_template("register.html")



@app.route("/login" ,methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
         return redirect("/")
    
    if request.method == "GET":
        return render_template("login.html")
        
    user = User.query.filter_by(email=request.form.get("email"),
                                password=request.form.get("password")).first() 
        
    if user :
            login_user(user)
            flash ("login sucessfull")
            return redirect("/")
    else :
            flash ("invalid email or password ")
            return redirect("/login")
    

@app.route("/add_item", methods=["GET", "POST"])
@login_required
def add_item():
    if request.method == "POST":
        name = request.form.get("name")
        price = request.form.get("price")
        image = request.form.get("image")
        description = request.form.get('description')
        category = request.form.get("category")

        item = Food(
            name=name,
            price=price,
            image=image,
            category=category,
            description=description 
        )

        db.session.add(item)
        db.session.commit()
        flash("adding food sucessfull")
        return redirect(url_for("add_item"))
    return render_template("add_item.html")

@app.route("/logout")
@login_required
def logout():
     logout_user()
     flash ("user logout")
     return redirect("/")



@app.errorhandler(401)
def page_not_found(error):
     return render_template("/login.html")


