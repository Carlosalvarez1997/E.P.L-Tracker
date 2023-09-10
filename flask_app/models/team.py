from flask_app import app
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash, session,request
from flask_app.models import user

import requests


class Team:
    db = "sample" #which database are you using for this project
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.short_code = data['short_code']
        self.image = data['image_path']
        self.last_played = data['last_played_at']
        self.upcoming = data['upcoming']
        self.starting_at = data['starting_at']
        self.user_id = data
        self.fan = ''


    @classmethod
    def get_team(cls, data):
        url =  "https://api.sportmonks.com/v3/football/teams?api_token=agaOMC0Z18MGoYFp1y8JKqdGGWliND6OydauLoJ2x56ODdjZyQoudYaoCfIV&include=upcoming;"
        response = requests.get(url)
        this_response = response.json()
        teams = this_response['data']
        data = data.copy()
        # print(data)
        for team in teams:
            if team['name'] == data['search']:
                data = team
                data['user_id'] = session['user_id']
                data_starting = data['upcoming'][0]['starting_at']
                # print(data_starting)
                data['upcoming'] = data['upcoming'][0]['name']
                data['starting_at'] = data_starting
                query = """
                INSERT INTO team (id, name, short_code, user_id, last_played_at, image_path, upcoming, starting_at)
                VALUES(%(id)s, %(name)s, %(short_code)s, %(user_id)s, %(last_played_at)s, %(image_path)s, %(upcoming)s, %(starting_at)s)
                """
                team_id = connectToMySQL(cls.db).query_db(query,data)
                return team_id
        return flash("Team not available")

    @classmethod
    def get_team_with_id(cls, id):
        data = {'id' : id}
        query = """
        SELECT *
        FROM team
        WHERE id = %(id)s
        ;"""
        team_id = connectToMySQL(cls.db).query_db(query,data)
        this_team = team_id[0]
        return this_team

    @classmethod
    def get_all_teams_with_user(cls):
        data = {'id': id}
        query = """
        SELECT *
        FROM team
        JOIN user
        ON user.id = team.user_id
        ;"""
        results = connectToMySQL(cls.db).query_db(query)
        all_teams = []
        for row in results:
            one_team = cls(row)
            data = cls.refresh_data()
            # print(data)
            for team in data:
                if len(team['upcoming']) == 0:
                    pass
                else:
                    datas = team
                    data_starting = team['upcoming'][0]['starting_at']
                    team['upcoming'] = team['upcoming'][0]['name']
                    team['starting_at'] = data_starting
                    query = """
                    UPDATE team
                        SET id = %(id)s, name = %(name)s, short_code = %(short_code)s, last_played_at = %(last_played_at)s, image_path = %(image_path)s, upcoming = %(upcoming)s, starting_at = %(starting_at)s
                        WHERE id = %(id)s
                    """
                    refreshed = connectToMySQL(cls.db).query_db(query,datas)
            one_team_user = {
                'id': row['user_id'],
                'first_name' : row['first_name'],
                'last_name': row['last_name'],
                "user_id": row['user_id'],
                'email': row['email'],
                'password': row['password'],
                'created_at': row['created_at'],
                'updated_at' : row['updated_at']
            }
            fan = user.User(one_team_user)
            one_team.fan = fan
            all_teams.append(one_team)
        return all_teams

    @classmethod
    def update_team(cls,data):
        old_id = int(data['id'])
        url =  "https://api.sportmonks.com/v3/football/teams?api_token=agaOMC0Z18MGoYFp1y8JKqdGGWliND6OydauLoJ2x56ODdjZyQoudYaoCfIV&include=upcoming;"
        response = requests.get(url)
        this_response = response.json()
        teams = this_response['data']
        for team in teams:
            if team['name'] == data['search']:
                data = team
                data["old_id"] = old_id
                data_starting = data['upcoming'][0]['starting_at']
                data['upcoming'] = data['upcoming'][0]['name']
                data['starting_at'] = data_starting
                query = """
                UPDATE team
                SET id = %(id)s, name = %(name)s, short_code = %(short_code)s, last_played_at = %(last_played_at)s, image_path = %(image_path)s, upcoming = %(upcoming)s, starting_at = %(starting_at)s
                WHERE id = %(old_id)s
                """
                result = connectToMySQL(cls.db).query_db(query,data,)
                return result

    @classmethod
    def delete_team_from_list(cls, id):
        data = {'id' : id}
        query = """
            DELETE FROM team
            WHERE id = %(id)s
        """
        deleted = connectToMySQL(cls.db).query_db(query,data)
        return


    @classmethod
    def refresh_data(cls):
        url =  "https://api.sportmonks.com/v3/football/teams?api_token=agaOMC0Z18MGoYFp1y8JKqdGGWliND6OydauLoJ2x56ODdjZyQoudYaoCfIV&include=upcoming;"
        response = requests.get(url)
        this_response = response.json()
        team_list = []
        for team in this_response['data']:
            team_list.append(team)
        return team_list
