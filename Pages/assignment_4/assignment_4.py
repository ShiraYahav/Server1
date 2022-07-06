import requests as requests
from flask import Blueprint, render_template
import mysql.connector
from flask import request, redirect
from flask import jsonify


assignment_4 = Blueprint('assignment_4', __name__,
                         static_folder='static',
                         template_folder='templates')

@assignment_4.route('/assignment_4')
def assignment4_req():
    query = 'select * from users'
    user_list = interact_db(query, query_type='fetch')
    return render_template('assignment_4.html', users=user_list)

#---------------Part A---------------------
@assignment_4.route('/insert', methods=['POST'])
def insert_user():
    firstname = request.form['firstname']
    password = request.form['password']
    username = request.form['username']
    query = 'select * from users'
    users = interact_db(query, query_type='fetch')
    for user in users:
        if username == user.username:
            Upquery = 'select * from users'
            Upusers = interact_db(Upquery, query_type='fetch')
            return render_template('assignment_4.html',message2='User already exists in our database',users=Upusers)
    else:
        query = "INSERT INTO users(username,password,firstname) VALUES ('%s','%s','%s')" % (username,password,firstname)
        interact_db(query=query, query_type='commit')
        Upquery = 'select * from users'
        Upusers = interact_db(Upquery, query_type='fetch')
        return render_template('assignment_4.html',message2='Potential tennis player added successfully!', users=Upusers)

# update
@assignment_4.route('/update', methods=['POST'])
def update_user():
    firstname = request.form['firstname']
    password = request.form['password']
    username = request.form['username']
    query = 'select * from users'
    users = interact_db(query, query_type='fetch')
    for user in users:
        if username == user.username:
            if password != "" and (firstname== user.firstname or firstname=="") :
                query = "UPDATE users SET password='%s' WHERE username='%s' " % (password, username)
                interact_db(query=query, query_type='commit')
                Upquery = 'select * from users'
                Upusers = interact_db(Upquery, query_type='fetch')
                return render_template('assignment_4.html',message1='Password successfully updated',users=Upusers)
            elif firstname != "" and (password== user.password or password==""):
                query = "UPDATE users SET firstname='%s' WHERE username='%s' " % (firstname, username)
                interact_db(query=query, query_type='commit')
                Upquery = 'select * from users'
                Upusers = interact_db(Upquery, query_type='fetch')
                return render_template('assignment_4.html',message1='firstname successfully updated',users=Upusers)
            elif (firstname != "" and password != ""):
                query = "UPDATE users SET firstname='%s', password='%s' WHERE username='%s' " % (firstname,password, username)
                interact_db(query=query, query_type='commit')
                Upquery = 'select * from users'
                Upusers = interact_db(Upquery, query_type='fetch')
                return render_template('assignment_4.html',
                                message1='First name and Password successfully updated',
                               users=Upusers)
    else:
        Upquery = 'select * from users'
        Upusers = interact_db(Upquery, query_type='fetch')
        return render_template('assignment_4.html',
                               message1='User does not exist in our system, please insert first.',
                               users=Upusers)

@assignment_4.route('/delete', methods=['POST'])
def delete_user():
    username = request.form['username']
    password = request.form['password']
    query = 'select * from users'
    users = interact_db(query, query_type='fetch')
    for user in users:
        if username == user.username:
            if password==user.password:
                query = "DELETE FROM users WHERE username='%s'" % username
                interact_db(query=query, query_type='commit')
                Upquery = 'select * from users'
                Upusers = interact_db(Upquery, query_type='fetch')
                return render_template('assignment_4.html', message3='User deleted!', users=Upusers)
            else:
                Upquery = 'select * from users'
                Upusers = interact_db(Upquery, query_type='fetch')
                return render_template('assignment_4.html', message3='incorrect password, not deleted',
                               users=Upusers)
    Upquery = 'select * from users'
    Upusers = interact_db(Upquery, query_type='fetch')
    return render_template('assignment_4.html',message3='User does not exist in our systems, cannot delete', users=Upusers)

#---------------Part B---------------------
@assignment_4.route('/assignment_4/users')
def user_response():
    query = 'select * from users'
    list = interact_db(query, query_type='fetch')
    return jsonify(list)

@assignment_4.route('/assignment_4/outer_source')
def outer_source():
    return render_template('outer_source.html')

@assignment_4.route('/assignment_4/outer_source/fetch_backend')
def fetch_outer_source():
    user_id = request.args['user_id']
    res = requests.get(f"https://reqres.in/api/users/{user_id}")
    return render_template('outer_source.html', request_data=res.json()['data'])



#---------------Part C---------------------
@assignment_4.route('/assignment_4/restapi_users/', defaults={'user_id': -1})
@assignment_4.route('/assignment_4/restapi_users/<user_id>')
def get_user(user_id):
    if user_id == -1:
        query = f'SELECT * FROM users'
        users_list = interact_db(query, query_type='fetch')
        return_list = []
        for user in users_list:
            user_dict = {
                'name': user.firstname,
                'email': user.username
            }
            return_list.append(user_dict)
        return jsonify(return_list)

    else:
        query = f'SELECT * FROM users WHERE id={user_id}'
        users_list = interact_db(query, query_type='fetch')
        if len(users_list) == 0:
            return_dict = {
                'message': 'user was not found, try again.'
            }
        else:
            user = users_list[0]
            return_dict = {
                'name': user.firstname,
                'email': user.username
            }
    return jsonify(return_dict)

#--------interact db--------------

def interact_db(query, query_type: str):
    return_value = False
    connection = mysql.connector.connect(host='localhost',
                                         user='root',
                                         passwd='ROOT',
                                         database='schema1')
    cursor = connection.cursor(named_tuple=True)
    cursor.execute(query)
    # CREATE, UPDATE, DELETE
    if query_type == 'commit':
        connection.commit()
        return_value = True

        # READ
    if query_type == 'fetch':
        query_result = cursor.fetchall()
        return_value = query_result

    connection.close()
    cursor.close()
    return return_value

