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
    'shira': '3425',
    'mor': '9098'
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
        if username in user_dict:
            pas_in_dict = user_dict[username]
            if pas_in_dict == password:
                session['username'] = username
                session['logedin'] = True
                return render_template('assignment3_2.html', message='Successfully logged in', usernamr=username, users=user_dict)
            else:
                return render_template('assignment3_2.html', message='Wrong password',  users=user_dict)
        else:
            user_dict[username] = password
            session['username'] = username
            session['logedin'] = True

            return render_template('assignment3_2.html', message='Thank you ' + session['username'] + ' for registering to our site!',  users=user_dict)
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


if __name__ == '__main__':
    app.run()
