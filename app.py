from flask import Blueprint,  Flask, render_template, \
    request, redirect, url_for, session, flash
from flask_bootstrap import Bootstrap
from datetime import timedelta


app = Flask(__name__, template_folder='templates', static_folder='static')
Bootstrap(app)
app.secret_key = "hello"
app.permanent_session_lifetime = timedelta(minutes=5)
bp = Blueprint('auth', __name__, url_prefix='/auth')


@app.route('/')
def home():
    return render_template('warehouse_templates/home.html')


@app.route('/sign_in_form')
def sign_in_form():
    return render_template('auth/sign_in_form.html')


@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        session.permanent = True
        user_name = (request.form["username"])
        session["user"] = user_name

        flash('Login Successful!')
        return redirect(url_for("user"))
    else:
        if "user" in session:
            flash('Already Logged In')
            return redirect(url_for("user"))
    return render_template("auth/login.html")


@app.route("/user")
def user():
    if "user" in session:
        user_name = session["user"]
        return render_template('auth/user.html', user_name=user_name)
    else:
        flash('You are not Logged In')
        return redirect(url_for("login"))


@app.route("/logout")
def logout():
    if "user" in session:
        flash('You have been logged out.', category='info')
    session.pop("user", None)

    return redirect(url_for("login"))


@app.route('/add_product')
def add_product():

    return render_template('warehouse_templates/add_product.html')


@app.route('/added_product', methods=['POST', 'GET'])
def added_product():
    result = request.form
    data = result.to_dict()
    data_to_display = str(data)
    warehouse[data['Name']] = data
    print('-----FUNCTION CALL: \"ADDED_PRODUCT\" ON ITEM: \"' + data['Name'] + '\"' +
          '\n PORDUCT DESCTIPTION: \"' + data_to_display + '\"' +
          '\n MADE BY: ' + session['user'])
    return render_template('warehouse_templates/added_product.html', result=result)


@app.route('/show_products', methods=['POST', 'GET'])
def show_products():
    return render_template('warehouse_templates/show_products.html', products=warehouse)


@app.route('/delete_product/<position_to_delete>', methods=['POST', 'GET'])
def delete_product(position_to_delete):
    position_to_delete_description = warehouse[position_to_delete].__str__()
    print('-----FUNCTION CALL: \"DELETE\" ON ITEM: \"' + position_to_delete + '\"' +
          '\n PORDUCT DESCTIPTION: \"' + position_to_delete_description + '\"' +
          '\n MADE BY: ' + session['user'])
    warehouse.pop(position_to_delete)
    return show_products()


if __name__ == '__main__':
    app.run()

warehouse = {'Wkurwix': {'Name': 'Wkurwix',
                         'Descripton': 'Głośnik który brzmi jak wkurwiony kogut o 5:20, porze Judaszowej rano',
                         'Quantity': '1', 'Position': 'W dupe se wsadź'},
             'Wino': {'Name': 'Wino', 'Descripton': 'winko', 'Quantity': '1', 'Position': 'A-1'}}

users = {'admin': {'username': 'admin', 'password': 'root', 'hierarchy': 'manager'},
         'user': {'username': 'user', 'password': 'root', 'hierarchy': 'user'}}
