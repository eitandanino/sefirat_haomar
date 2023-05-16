import os
import requests
from pyluach import dates
from datetime import datetime


apiToken = os.environ["API_TOKEN"]
apiURL = f'https://api.telegram.org/bot{apiToken}/sendMessage'

user_name = os.environ["USER_NAME"]
mongo_db_password = os.environ["MONGO_DB_PASSWORD"]

# Connect to MongoDB
cluster = MongoClient(f"mongodb+srv://{user_name}:{mongo_db_password}@safirat-haomer.ynxy0yo.mongodb.net/")
db = cluster["chat_ids"]
collection = db["telegram_chat_ids"]

def add_user_chat_id(chat_id):
    # Check if the chat ID already exists in the database
    result = collection.find_one({"_id": chat_id})
    if result is None:
        # Insert the chat ID if it doesn't exist
        post = {"_id": chat_id}
        collection.insert_one(post)


def get_users_chat_ids_mongo():
    # Retrieve all user chat IDs from the database
    results = collection.find({})
    chat_ids = [result["_id"] for result in results]
    return chat_ids


CURRENT_DAY = dates.HebrewDate.today().day
CURRENT_MONTH = dates.HebrewDate.today().month

if (CURRENT_MONTH == 1 and CURRENT_DAY >= 14 or
        (CURRENT_MONTH == 2) or
        (CURRENT_MONTH == 3 and CURRENT_DAY <= 7)):
    def get_passover_date():
        current_year = datetime.now().year
        heb_year = current_year + 3760
        passover = dates.HebrewDate(heb_year, 1, 14)
        greg_passover = (passover.to_greg() + 1)
        the_date = (greg_passover.tuple())
        this_year = the_date[0]
        this_month = the_date[1]
        this_day = the_date[2]
        return this_year, this_month, this_day


    year, month, day = get_passover_date()

    # Get the current date and time
    now = datetime.now()

    # Calculate the sefirat haomer day and the number of weeks
    start_date = datetime(year, month, day)  # or the first night of Passover
    days = (now - start_date).days
    sefira_day = days + 1
    weeks = sefira_day // 7


    def number_to_hebrew_words(number):
        units = ["אפס", "אחד", "שני", "שלשה", "ארבעה", "חמשה", "ששה", "שבעה", "שמונה", "תשעה", "עשרה", "אחד עשר",
                 "שנים עשר", "שלשה עשר", "ארבעה עשר", "חמשה עשר", "ששה עשר", "שבעה עשר", "שמונה עשר", "תשעה עשר",
                 "עשרים", "אחד ועשרים", "שנים ועשרים", "שלשה ועשרים", "ארבעה ועשרים", "חמשה ועשרים",
                 "ששה ועשרים", "שבעה ועשרים", "שמונה ועשרים", "תשעה ועשרים", "שלשים", "אחד ושלשים", "שנים ושלשים",
                 "שלושה ושלשים", "ארבעה ושלשים", "חמשה ושלשים", "ששה ושלשים", "שבעה ושלשים", "שמונה ושלשים",
                 "תשעה ושלשים", "ארבעים", "אחד וארבעים", "שנים וארבעים", "שלשה וארבעים", "ארבעה וארבעים",
                 "חמשה וארבעים", "ששה וארבעים", "שבעה וארבעים", "שמונה וארבעים", "תשעה וארבעים"]
        return units[number]


    def get_english_sentence(sefira_day, weeks):
        if weeks == 0:
            if sefira_day % 7 == 1:
                return f"Today is {sefira_day} day of the Omer."
            else:
                return f"Today is {sefira_day} days of the Omer."
        elif weeks == 1:
            if sefira_day % 7 == 0:
                return f"Today is {sefira_day} days, which is {weeks} week of the Omer."
            elif sefira_day % 7 == 1:
                return f"Today is {sefira_day} days, which is {weeks} week and" \
                       f" {sefira_day % 7} day of the Omer."
            else:
                return f"Today is {sefira_day} days, which is {weeks} week and" \
                       f" {sefira_day % 7} days of the Omer."
        else:
            if sefira_day % 7 == 0:
                return f"Today is {sefira_day} days, which is {weeks} weeks of the Omer."
            elif sefira_day % 7 == 1:
                return f"Today is {sefira_day} days, which is {weeks} weeks and" \
                       f" {sefira_day % 7} day of the Omer."
            else:
                return f"Today is {sefira_day} days, which is {weeks} weeks and" \
                       f" {sefira_day % 7} days of the Omer."


    def get_hebrew_sentence_safaradi(sefira_day, weeks):
        if weeks == 0:
            if sefira_day % 7 == 1:
                return f"היום יום אחד לעומר"
            else:
                return f"היום {number_to_hebrew_words(sefira_day)} ימים לעומר"
        elif weeks == 1:
            if sefira_day % 7 == 0:
                return f"היום שבעה ימים לעומר שהם שבוע אחד"
            elif sefira_day % 7 == 1:
                return f"היום שמונה ימים לעומר שהם שבוע אחד ויום אחד"
            elif sefira_day % 7 == 2:
                return f"היום תשעה ימים לעומר שהם שבוע אחד ושני ימים"
            elif sefira_day % 7 == 3:
                return f"היום עשרה ימים לעומר שהם שבוע אחד ושלשה ימים"
            else:
                return f"היום {number_to_hebrew_words(sefira_day)} יום לעומר שהם {number_to_hebrew_words(weeks)} " \
                       f"שבוע אחד ו{number_to_hebrew_words(sefira_day % 7)} ימים"
        else:
            if sefira_day % 7 == 0:
                return f"היום {number_to_hebrew_words(sefira_day)} יום לעומר שהם {number_to_hebrew_words(weeks)} שבועות"
            elif sefira_day % 7 == 1:
                return f"היום {number_to_hebrew_words(sefira_day)} יום לעומר שהם {number_to_hebrew_words(weeks)}" \
                       f" שבועות ויום {number_to_hebrew_words(sefira_day % 7)}"
            else:
                return f"היום {number_to_hebrew_words(sefira_day)} יום לעומר שהם {number_to_hebrew_words(weeks)} " \
                       f"שבועות ו{number_to_hebrew_words(sefira_day % 7)} ימים"


    def get_hebrew_sentence_ashkenaz(sefira_day, weeks):
        if weeks == 0:
            if sefira_day % 7 == 1:
                return f"היום יום אחד לעומר"
            else:
                return f"היום {number_to_hebrew_words(sefira_day)} ימים לעומר"
        elif weeks == 1:
            if sefira_day % 7 == 0:
                return f"היום שבעה ימים שהם שבוע אחד לעומר"
            elif sefira_day % 7 == 1:
                return f"היום שמונה ימים שהם שבוע אחד ויום אחד לעומר"
            elif sefira_day % 7 == 2:
                return f"היום תשעה ימים שהם שבוע אחד ושני ימים לעומר"
            elif sefira_day % 7 == 3:
                return f"היום עשרה ימים שהם שבוע אחד ושלשה ימים לעומר"
            else:
                return f"היום {number_to_hebrew_words(sefira_day)} יום שהם {number_to_hebrew_words(weeks)} " \
                       f"שבוע אחד ו{number_to_hebrew_words(sefira_day % 7)} ימים לעומר"
        else:
            if sefira_day % 7 == 0:
                return f"היום {number_to_hebrew_words(sefira_day)} יום שהם {number_to_hebrew_words(weeks)} שבועות לעומר"
            elif sefira_day % 7 == 1:
                return f"היום {number_to_hebrew_words(sefira_day)} יום שהם {number_to_hebrew_words(weeks)}" \
                       f" שבועות ויום {number_to_hebrew_words(sefira_day % 7)} לעומר"
            else:
                return f"היום {number_to_hebrew_words(sefira_day)} יום שהם {number_to_hebrew_words(weeks)} " \
                       f"שבועות ו{number_to_hebrew_words(sefira_day % 7)} ימים לעומר"


    def get_and_add_user_chat_ids():
        try:
            response = requests.get(f"https://api.telegram.org/bot{apiToken}/getUpdates")
            data = response.json()
            users_chat_ids = set()
            for result in data["result"]:
                if "message" in result:
                    chat_id = result["message"]["chat"]["id"]
                    add_user_chat_id(chat_id)
        except Exception as ee:
            print(f"Error getting user chat IDs: {ee}")
            return []


    # Add new ids to the db
    get_and_add_user_chat_ids()
    # Get all the Chat ids from the db
    all_users_chat_ids = get_users_chat_ids_mongo()

    # Get all teh sentences
    all_sentence_english = get_english_sentence(sefira_day, weeks)
    all_sentence_hebrew_safaradi = get_hebrew_sentence_safaradi(sefira_day, weeks)
    all_sentence_hebrew_ashkenaz = get_hebrew_sentence_ashkenaz(sefira_day, weeks)

    # Send to each chat id
    for user_chat_id in all_users_chat_ids:
        try:
            response = requests.post(apiURL, json={'chat_id': user_chat_id,
                                                   'text': f'עדות המזרח - {all_sentence_hebrew_safaradi} \n אשכנז - '
                                                           f'{all_sentence_hebrew_ashkenaz} \n '
                                                           f'English - {all_sentence_english}'})
        except Exception as e:
            print(e)
