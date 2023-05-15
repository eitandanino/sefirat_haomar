import os
import requests
from pyluach import dates
from datetime import datetime


apiToken = os.environ["API_TOKEN"]
apiURL = f'https://api.telegram.org/bot{apiToken}/sendMessage'

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


    def get_hebrew_sentence(sefira_day, weeks):
        if weeks == 0:
            if sefira_day % 7 == 1:
                return f"היום יום אחד לעומר"
            else:
                return f"היום {sefira_day} ימים לעומר"
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
                return f"היום {sefira_day} יום לעומר שהם {weeks} שבוע אחד ו" \
                       f" {sefira_day % 7} ימים"
        else:
            if sefira_day % 7 == 0:
                return f"היום {sefira_day} יום לעומר שהם {weeks} שבועות"
            elif sefira_day % 7 == 1:
                return f"היום {sefira_day} יום לעומר שהם {weeks} שבועות ו" \
                       f" {sefira_day % 7} יום"
            else:
                return f"היום {sefira_day} יום לעומר שהם {weeks} שבועות ו" \
                       f" {sefira_day % 7} ימים"
        
             
    def get_user_chat_ids():
        try:
            response = requests.get(f"https://api.telegram.org/bot{apiToken}/getUpdates")
            data = response.json()
            users_chat_ids = set()
            for result in data["result"]:
                if "message" in result:
                    chat_id = result["message"]["chat"]["id"]
                    users_chat_ids.add(chat_id)
            return list(users_chat_ids)
        except Exception as ee:
            print(f"Error getting user chat IDs: {ee}")
            return []

        
    user_chat_ids = get_user_chat_ids()
    all_sentence_english = get_english_sentence(sefira_day, weeks)
    all_sentence_hebrew = get_hebrew_sentence(sefira_day, weeks)


    #     print(get_english_sentence(sefira_day, weeks))
    #     print(get_hebrew_sentence(sefira_day, weeks))
    for user_chat_id in user_chat_ids:
        try:
            response = requests.post(apiURL, json={'chat_id': user_chat_id,
                                                   'text': f'{all_sentence_hebrew} \n {all_sentence_english}'})
        except Exception as e:
            print(e)

