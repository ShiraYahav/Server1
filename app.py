from datetime import timedelta
from flask import Flask, render_template, redirect, request, url_for, jsonify, session

app = Flask(__name__)

app.secret_key = '123'
app.config['SESSION_PERMANENT'] = True
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=20)

racquet_dic = {
    'Wilson': ['Roland Gross Blade', 305, 249],
    'Head': ['Speed Pro', 310, 230],
    'Prince': ['Textreme Warrier', 315, 179],
    'Babolat': ['Pure Aero', 320, 279],
    'Dunlop': ['CX 200 Tour', 332, 249]
}

user_dict = {
    'shira@gmail.com': ['0311','Shira'],
    'michal@gmail.com': ['9098','Michal'],
    'talya@gmail.com':['1322', 'Talya'],
    'ofir@gmail.com':['1801', 'Ofir'],
    'rafael@gmail.com':['1359','Rafael']
}

@app.route('/')
def home():
    return render_template('Home.html')


@app.route('/contact_page')
def contact_page():
    return render_template('ContactPage.html')


@app.route('/assignment3_1')
def assignment3_1():
    user_info = {'name': 'Shira', 'last_name': 'Yahav', 'gender': 'female', 'age': 26}
    hobbies = ['Tennis', 'Science', 'Languages']
    return render_template('assignment3_1.html', user_info=user_info, hobbies=hobbies)


@app.route('/assignment3_2')
def assignment3_2():
    return render_template('assignment3_2.html')


@app.route('/login',  methods=['GET', 'POST'])
def login_func():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        firstname = request.form['firstname']
        if username in user_dict:
            pas_in_dict = user_dict[username][0]
            firstname_in_dict = user_dict[username][1]
            if pas_in_dict == password and firstname_in_dict == firstname:
                session['username'] = user_dict[username][1]
                session['logedin'] = True
                return render_template('assignment3_2.html', message='Successfully logged in', username=username, users=user_dict)
            else:
                if pas_in_dict != password:
                    return render_template('assignment3_2.html', message='Wrong password',  users=user_dict)
                elif firstname_in_dict != firstname:
                    return render_template('assignment3_2.html', message='Wrong first name', users=user_dict)
        else:
                user_dict[username][0] = password
                user_dict[username][1] = firstname
                session['username']= user_dict[username][1]
                session['logedin'] = True
                return render_template('assignment3_2.html', message='Thank you ' + session['username'][1] + ' for registering to our site!',  users=user_dict)
    return render_template('assignment3_2.html', users=user_dict)


@app.route('/logout')
def logout_func():
    session['logedin'] = False
    session.clear()
    return redirect(url_for('login_func'))


@app.route('/catalog')
def racquet_catalog():
    if 'product_company' in request.args:
        product_company = request.args['product_company']
        if product_company:
            if product_company in racquet_dic:
                return render_template('assignment3_2.html',
                                       product_company=product_company,
                                       product_model=racquet_dic[product_company][0],
                                       product_weight=racquet_dic[product_company][1],
                                       product_price=racquet_dic[product_company][2])
            else:
                return render_template('assignment3_2.html', message_catalog='Product not found.')
    return render_template('assignment3_2.html', racquet_dic=racquet_dic)


@app.route('/session')
def session_func():
    return jsonify(dict(session))

##assignment_4
from Pages.assignment_4.assignment_4 import assignment_4
app.register_blueprint(assignment_4)

if __name__ == '__main__':
    app.run()
