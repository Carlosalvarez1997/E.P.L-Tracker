from flask_app import app
from flask import render_template, redirect, request, session
from flask_app.models import user, team# import entire file, rather than class, to avoid circular imports

import requests
#agaOMC0Z18MGoYFp1y8JKqdGGWliND6OydauLoJ2x56ODdjZyQoudYaoCfIV

# Create Users Controller
@app.route('/')
def create_page():
    return render_template('register.html')

@app.route('/create', methods = ["POST"])
def create_user():
    if user.User.create_user(request.form):

        return redirect('/home')
    return redirect ('/')

#login
@app.route('/login')
def user_login_page():
    return render_template('login.html')

@app.route('/users/login' , methods = ['POST'])
def login():
    if user.User.login(request.form):
        print(session['user_id'])
        return redirect('/home')
    return redirect('/login')

#Logout
@app.route('/users/logout')
def logout():
    session.clear()
    return redirect('/login')

# Read Users Controller
@app.route('/home', methods = ['GET', 'POST'])
def index():
    if 'user_id' not in session :
        return redirect('/login')
    else:
        if request.method == 'POST':
            team.Team.get_team(request.form)
        all_teams = team.Team.get_all_teams_with_user()
        team.Team.refresh_data()
        return render_template('index.html', all_teams = all_teams)


# Update Users Controller
@app.route('/team/update/<id>', methods = ["GET", "POST"])
def update_team(id):
    if request.method == "GET":
        this_team = team.Team.get_team_with_id(id)
        return render_template("update.html", this_team = this_team)
    if request.method == "POST":
        this_team = team.Team.update_team(request.form)

        return redirect("/home")

# Delete Users Controller
@app.route('/delete/<id>')
def delete_team(id):
    team.Team.delete_team_from_list(id)
    return redirect('/home')

# Notes:
# 1 - Use meaningful names
# 2 - Do not overwrite function names
# 3 - No matchy, no worky
# 4 - Use consistent naming conventions
# 5 - Keep it clean
# 6 - Test every little line before progressing
# 7 - READ ERROR MESSAGES!!!!!!
# 8 - Error messages are found in the browser and terminal




# How to use path variables:
# @app.route('/<int:id>')
# def index(id):
#     user_info = user.User.get_user_by_id(id)
#     return render_template('index.html', user_info)

# Converter -	Description
# string -	Accepts any text without a slash (the default).
# int -	Accepts integers.
# float -	Like int but for floating point values.
# path 	-Like string but accepts slashes.
