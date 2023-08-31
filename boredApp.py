import requests
import sqlite3 as sq
import json

BASE_URL = "https://www.boredapi.com/api/activity"

PARAMS = {
    "type": "education",
    "participants": 1,
    "minprice": 0.1,
    "maxprice": 30,
    "minaccessibility": 0.1,
    "minaccessibility": 0.5
}


class BoredAPIWrapper:
    def __init__(self, url):
        self.url = url

    def get_activity(self, params=[]):
        request_url = self.create_url_with_params(self.url, params)
        request = requests.get(request_url)
        print(request_url)
        print(request.text)
        return json.loads(request.text)

    def create_url_with_params(self, url, params):
        if not params:
            return url

        param_string = '&'.join([f'{key}={value}' for key, value in params.items()])
        full_url = f'{url}?{param_string}'
        return full_url


class ActivityDataBase:
    def __init__(self, db_file):
        self.db_file = db_file
        self.insert_querry = '''
                INSERT INTO activities (activity, type, participants, price, link, key, accessibility)
                VALUES (:activity, :type, :participants, :price, :link, :key, :accessibility)
            '''
        self.get_querry = '''SELECT * FROM activities ORDER BY id DESC LIMIT 5'''

    def save_activity(self, activity):
        try:
            db = sq.connect(self.db_file)
            db_cursor = db.cursor()
            db_cursor.execute(self.insert_querry, activity)
            db.commit()

        except sq.Error as e:
            if db: db.rollback()
            print("Error saving activity to the database")
            print(e)
        finally:
            if db: db.close()

    def get_last_saved_activity(self):
        try:
            db = sq.connect(self.db_file)
            db.row_factory = sq.Row
            db_cursor = db.cursor()
            db_cursor.execute(self.get_querry)
            last_activities = db_cursor.fetchall()
            print(last_activities)
            db.commit()


        except sq.Error as e:
            if db: db.rollback()
            print("Error getting activity to the database")
            print(e)
        finally:
            if db: db.close()





if __name__ == "__main__":
    API = BoredAPIWrapper(BASE_URL)
    BASE = ActivityDataBase("ActivitiesDB.db")
    activity = API.get_activity()
    BASE.save_activity(activity)
    BASE.get_last_saved_activity()