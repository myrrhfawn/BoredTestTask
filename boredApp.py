import argparse
from Resources import boredAppAPI as API

#CONSTANTS
BASE_URL = "https://www.boredapi.com/api/activity"
DB_NAME = "./Resources/ActivitiesDB.db"

"""
Description of used types:

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

class CommandLineProgram:
    """
    the class responsible for the operation of the program

    :param parser: <class 'argparse.ArgumentParser'> - parser for args
    """

    def __init__(self, parser, api, database):
        self.parser = parser
        self.api = api
        self.database = database


    def parse_command_line(self):
        """
        a function that parses commands with the help of argsparse module.

        :return: Void.
        """

        # Add command line arguments
        self.parser.add_argument('command', help='Команда')
        self.parser.add_argument('--type', help='Тип')
        self.parser.add_argument('--participants', type=int, help='Кількість учасників')
        self.parser.add_argument('--price_min', type=float, help='Мінімальна ціна')
        self.parser.add_argument('--price_max', type=float, help='Максимальна ціна')
        self.parser.add_argument('--price', type=float, help='Визначена ціна')
        self.parser.add_argument('--accessibility_min', type=float, help='Мінімальна доступність')
        self.parser.add_argument('--accessibility_max', type=float, help='Максимальна доступність')
        self.parser.add_argument('--accessibility', type=float, help='Визначена доступність')

        args = parser.parse_args()

        # Deligate command
        if args.command == "new":
            self.command_new_processor(args)

        if args.command == "list":
            self.command_list_processor()

    def command_new_processor(self, args):
        """
        a function that processes the "new" command.

        :param args: Namespace -  namespace from argsparse.
        :return: Void.
        """

        dict = self.convert_to_dict(args)
        activity = self.api.get_activity(dict)
        self.output_controller([activity])
        self.database.save_activity(activity)

    def command_list_processor(self):
        """
        a function that processes the "list" command

        :return: Void.
        """
        activities = self.database.get_last_saved_activity()
        self.output_controller(activities)

    def output_controller(self, activities):
        """
        a function that controls the output of activities to the console.

        :param activities: Dictionary - an object of Activity type.
        :return: Void.
        """
        if len(activities) > 0:
            for i in range(0, len(activities)):
                if len(activities) == 1:
                    self.activity_output(activities[i])
                else:
                    self.activity_output(activities[i], i+1)
        else:
            print("=============================")
            print("Тhere are no saved activities")
            print("=============================")



    def activity_output(self, activity, number=0):
        """
        a function for outputting activity to the console.


        :param activity: Dictionary - an object of Activity type.
        :param number: Integer - sequence number for the activity
        :return: Void.
        """

        try:
            if number != 0:
                print("Activity #" + str(number))
            print("=" * len("What do you want to do today? - " + activity["activity"]))
            print("What do you want to do today? - " + activity["activity"])
            print("What type of activity is this? - " + activity["type"])
            print("How many participants will be with you? - "
                  + (str(activity["participants"]) if activity["participants"] > 0 else "You will be alone"))
            print("How much it will cost? - "
                  + ("It is free!" if activity["price"] == 0 else
                     "Very cheap" if activity["price"] < 0.25 else
                     "Cheap" if activity["price"] < 0.5 else
                     "Moderately" if activity["price"] < 0.75 else
                     "Expensive" if activity["price"] < 1 else
                     "Very expensive"))
            print("How accessible is it? - "
                  + ("Easy" if activity["accessibility"] < (1 / 3) else
                     "Medium" if activity["accessibility"] < (2 / 3) else
                     "Hard"))
            if activity["link"]:
                print("Follow the link: " + activity["link"])
            print("=" * len("What do you want to do today? - " + activity["activity"]))


        except Exception as e:
            print("=" * len(activity["error"]))
            print(activity["error"])
            print("=" * len(activity["error"]))


    def convert_to_dict(self, namespace_obj):
        """
        the function of converting us sleep into an object of Params type.


        :param namespace_obj: Namespace - namespace from argsparse.
        :return: Dictionary - an object of Params type.
        """
        return {
            "type": str(namespace_obj.type) if namespace_obj.type else None,
            "participants": int(namespace_obj.participants) if namespace_obj.participants is not None else None,
            "minprice": float(namespace_obj.price_min) if namespace_obj.price_min is not None else None,
            "maxprice": float(namespace_obj.price_max) if namespace_obj.price_max is not None else None,
            "price": float(namespace_obj.price) if namespace_obj.price is not None else None,
            "minaccessibility": float(
                namespace_obj.accessibility_min) if namespace_obj.accessibility_min is not None else None,
            "maxaccessibility": float(
                namespace_obj.accessibility_max) if namespace_obj.accessibility_max is not None else None,
            "accessibility": float(
                namespace_obj.accessibility) if namespace_obj.accessibility is not None else None
        }



# Виводимо значення аргументів
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="My Program")  # We create an argument parser
    api = API.BoredAPIWrapper(BASE_URL)                         # We create a API for program
    database = API.ActivityDataBase(DB_NAME)                    # We connect a SQLLite3 database
    program = CommandLineProgram(parser, api, database)         # We create a program controller
    program.parse_command_line()                                # Start parsing command line arguments




