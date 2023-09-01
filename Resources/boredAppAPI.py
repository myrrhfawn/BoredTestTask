import requests
import sqlite3 as sq
import json


"""
Activity type = {
                    "activity": String,
                    "type": String,
                    "participants": Integer,
                    "price": Float,
                    "link": String,
                    "key": Integer,
                    "accessibility": Float
                }
Params type = {
                    "type": String,             -optional
                    "participants": Integer,    -optional
                    "minprice": Float,          -optional
                    "maxprice": Float,          -optional
                    "price": Float,             -optional, used only without minprice and maxprice
                    "minaccessibility": Float,  -optional
                    "maxaccessibility":Float,   -optional
                    "accessibility": Float      -optional, used only without minaccessibility and maxaccessibility
                }               
                

"""


class BoredAPIWrapper:
    """
    class for working with the database.
    :param url: String - base API url.

    """

    def __init__(self, url):
        self.url = url

    def get_activity(self, params={}):
        """

        :param params: Dictionary - an object of type Params to filter the activities by type,
                        number of participants, price range,
                        and accessibility range.

        :return: Dictionary - an object of Activity type.
        """

        request_url = self.create_url_with_params(params)
        request = requests.get(request_url)
        return json.loads(request.text)

    def create_url_with_params(self, params):
        """
        A function that combines filtering parameters with the base url.

        :param params: Dictionary - an object of type Params with the required filtering parameters.
        :return: String - full url with parameters included.
        """

        if not params:
            return self.url

        param_string = '&'.join([f'{key}={value}' for key, value in params.items() if value is not None])
        full_url = f'{self.url}?{param_string}'
        return full_url




class ActivityDataBase:
    """
    class for working with the database.
    :param db_file: String - name of database file.

    """

    def __init__(self, db_file):
        self.db_file = db_file
        self.insert_querry = '''
                INSERT INTO activities (activity, type, participants, price, link, key, accessibility)
                VALUES (:activity, :type, :participants, :price, :link, :key, :accessibility)
            '''
        self.get_querry = '''SELECT * FROM activities ORDER BY id DESC LIMIT 5'''

    def save_activity(self, activity):
        """
        a function that saves activity to the database.

        :param activity: Dictionary - an object of Activity type.
        :return: Void.
        """

        try:
            db = sq.connect(self.db_file)
            db_cursor = db.cursor()
            db_cursor.execute(self.insert_querry, activity)
            db.commit()

        except sq.Error as e:
            if db: db.rollback()
            if not activity["error"]:
                print("Error saving activity to the database")
                print(e)
        finally:
            if db: db.close()

    def get_last_saved_activity(self):
        """
        A function that returns the last 5 records from the database.

        :param: Void.
        :return: Array -  an array of 5 values of Activity type.
        """
        try:
            db = sq.connect(self.db_file)
            db.row_factory = self.dict_factory
            db_cursor = db.cursor()
            db_cursor.execute(self.get_querry)
            last_activities = db_cursor.fetchall()
            db.commit()
            return last_activities

        except sq.Error as e:
            if db: db.rollback()
            print("Error getting activity to the database")
            print(e)
        finally:
            if db: db.close()

    def dict_factory(self, cursor, row):
        """
        function to conver sql.Row to dictionary.

        :param cursor: database cursor to work with data.
        :param row: database row.
        :return: Dictionary - an object of Activity type.
        """

        dict = {}
        for idx, col in enumerate(cursor.description):
            dict[col[0]] = row[idx]
        return dict





if __name__ == "__main__":
    API = BoredAPIWrapper(BASE_URL)
    BASE = ActivityDataBase("ActivitiesDB.db")
    activity = API.get_activity()
    BASE.save_activity(activity)
    last = BASE.get_last_saved_activity()
    print(last)