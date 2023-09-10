
from flask_app import app
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash, session
import re
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)
# import re
# from flask_bcrypt import Bcrypt
# bcrypt = Bcrypt(app)
# The above is used when we do login registration, be sure to install flask-bcrypt: pipenv install flask-bcrypt


class User:
    db = "sample" #which database are you using for this project
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.teams = []
        # What changes need to be made above for this project?
        #What needs to be added her for class association?



    # Create Users Models
    @classmethod
    def create_user(cls, data):
        if not cls.validate_user(data):
            return False
        data = cls.parsed_data(data)
        query = """
        INSERT INTO user (first_name, last_name, email, password)
        VALUES(%(first_name)s, %(last_name)s, %(email)s, %(password)s)
        ;"""
        user_id = connectToMySQL(cls.db).query_db(query,data)
        session['user_id'] = user_id
        session['first_name']= data['first_name']
        session['user_name'] = f'{data["first_name"]} {data["last_name"]}'
        session['email'] = data['email']
        return user_id



    # Read Users Models
    @classmethod
    def get_user_by_email(cls, email):
        data = {'email': email}
        query = """
        SELECT *
        FROM user
        WHERE email = %(email)s
        ;"""
        user_id = connectToMySQL(cls.db).query_db(query,data)
        if user_id:
            return cls(user_id[0])
        return False

    @classmethod
    def get_user_by_id(cls, id):
        data = {'id' : id}
        query = """
        SELECT *
        FROM user
        WHERE id = %(id)s
        ;"""
        user_id = connectToMySQL(cls.db).query_db(query,data)
        this_user = user_id[0]
        return this_user





    # Update Users Models
    @classmethod
    def update_user(cls,id):
        query = """
        UPDATE user
        SET first_name = %(first_name)s, last_name = %(last_name)s, email = %(email)s
        WHERE id = %(id)s
        """
        result = cconnectToMySQL(cls.db).query_db(query,data)
        return result



    # Delete Users Models



    #Helper
    @staticmethod
    def validate_user(data):
        is_valid = True
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if len(data['first_name']) < 2 :
            flash('First name has to be longer than 2 characters')
            is_valid = False
        if len(data['last_name']) <2 :
            flash('last Name has to be longer than 2 characters')
            is_valid= False
        if 'id' not in data or data['email'] != User.get_user_by_id(data['id']).email:
            if not EMAIL_REGEX.match(data['email']):
                flash("email address format incomplete")
                is_valid= False
            if User.get_user_by_email(data['email']):
                flash('Email Address is already Taken')
                is_valid= False
        if 'id' not in data:
            if len(data['password']) <8:
                flash('Password has to be longer than 8 Characters')
            if data['password'] != data['confirm_password']:
                flash('Password do not match')
                is_valid= False
        return is_valid

    @staticmethod
    def parsed_data(data):
        parsed_data = {
        'email' : data['email'],
        'first_name' :data['first_name'],
        'last_name' : data['last_name'],
        'password' : bcrypt.generate_password_hash(data['password'])
    }
        return parsed_data

    @staticmethod
    def login(data):
        this_user = User.get_user_by_email(data['email'])
        if this_user:
            if bcrypt.check_password_hash(this_user.password, data['password']):
                session['user_id'] = this_user.id
                session['first_name']= this_user.first_name
                session['user_name'] = f'{this_user.first_name} {this_user.last_name}'
                session['email'] = this_user.email
                return True
        flash('Email or Password is Incorrect')
        return False
