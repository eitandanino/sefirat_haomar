Sefirat HaOmer Telegram and WhatsApp Reminder
=============================================

This code is a Python script that sends daily reminders for counting the Sefirat HaOmer (the Counting of the Omer) to Telegram and WhatsApp groups. The script retrieves the current date and calculates the number of days and weeks that have passed since the beginning of the counting, based on the Passover date of the current year.

Dependencies
------------

The script requires the following dependencies:

•	`os`: Used to access environment variables.

•	`requests`: Used for making HTTP requests to the Telegram Bot API and the WhatsApp API.

•	`pyluach`: A Python library for Hebrew calendar calculations.

•	`datetime`: Used for working with dates and times.

•	`pymongo`: A Python library for interacting with MongoDB.

Setup
-----

Before running the script, you need to set up the following:

1.	Set environment variables:

	•	`API_TOKEN`: Your Telegram Bot API token.
  
	•	`user`: Your MongoDB Atlas username.
  
	•	`MONGO_DB_PASSWORD`: Your MongoDB Atlas password.
  
	•	`GID`: The WhatsApp group ID.
  
	•	`RAPID_API_KEY`: Your RapidAPI key for the first WhatsApp API.
  
	•	`RAPID_API_KEY_2`: Your RapidAPI key for the second WhatsApp API.

2.	Connect to MongoDB:

	•	The script connects to a MongoDB Atlas cluster using the provided username and password.

3.	Create a collection in the MongoDB database:

	•	The script creates a collection called `telegram_chat_ids` in the `chat_ids` database to store the chat IDs of Telegram users.

Functionality
-------------

The script performs the following tasks:

1.	Retrieves the Passover date for the current year using the Hebrew calendar.
2.	Calculates the number of days and weeks that have passed since the beginning of the counting.
3.	Retrieves and adds the chat IDs of Telegram users to the MongoDB collection `telegram_chat_ids`.
4.	Generates sentences in English, Safaradi Hebrew, and Ashkenaz Hebrew representing the current day of the Omer count.
5.	Sends the generated sentences as messages to all Telegram users.
6.	Sends the generated sentences as a WhatsApp message to the specified group using the RapidAPI service. The API key used depends on the current day.

Usage
-----

To use this script, follow these steps:

1.	Set up the dependencies and environment variables as described above.
2.	Run the script. It will automatically send the daily reminders to the Telegram users and the WhatsApp group.

Note: The script should be scheduled to run daily to send the reminders on time.

License
-------

This code is released under the **[MIT License](https://opensource.org/license/mit/)**. Feel free to modify and distribute it according to your needs.
