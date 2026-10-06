import csv
import os
import sqlite3

# Resolve the resources folder relative to this file, so paths work
# no matter what directory the script is run from.
_RESOURCES_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'resources')

# Connect to the SQLite in-memory database
conn = sqlite3.connect(':memory:')

# A cursor object to execute SQL commands
cursor = conn.cursor()


def main():

    # users table
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                        userId INTEGER PRIMARY KEY,
                        firstName TEXT,
                        lastName TEXT
                      )'''
                   )

    # callLogs table (with FK to users table)
    cursor.execute('''CREATE TABLE IF NOT EXISTS callLogs (
        callId INTEGER PRIMARY KEY,
        phoneNumber TEXT,
        startTime INTEGER,
        endTime INTEGER,
        direction TEXT,
        userId INTEGER,
        FOREIGN KEY (userId) REFERENCES users(userId)
    )''')

    # You will implement these methods below. They just print TO-DO messages for now.
    load_and_clean_users(os.path.join(_RESOURCES_DIR, 'users.csv'))
    load_and_clean_call_logs(os.path.join(_RESOURCES_DIR, 'callLogs.csv'))
    write_user_analytics(os.path.join(_RESOURCES_DIR, 'userAnalytics.csv'))
    write_ordered_calls(os.path.join(_RESOURCES_DIR, 'orderedCalls.csv'))

    # Helper method that prints the contents of the users and callLogs tables. Uncomment to see data.
    select_from_users_and_call_logs()

    # Close the cursor and connection. main function ends here.
    cursor.close()
    conn.close()


# TODO: Implement the following 4 functions. The functions must pass the unit tests to complete the project.


# This function will load the users.csv file into the users table, discarding any records with incomplete data
def load_and_clean_users(file_path):
    USERS_FIELDS = 2
    FIRST_FIELD = 'firstName'

    with open(file_path, 'r') as users_file:
        for line in users_file:
            values = line.replace(' ', '').strip(',\n').split(',')
            
            if len(values) != USERS_FIELDS or values[0] == FIRST_FIELD or '' in values:
                continue

            cursor.execute('INSERT INTO users (firstName, lastName) VALUES (?, ?)', values)



# This function will load the callLogs.csv file into the callLogs table, discarding any records with incomplete data
def load_and_clean_call_logs(file_path):
    CALLLOGS_FIELDS = 5
    FIRST_FIELD = 'phoneNumber'

    with open(file_path, 'r') as calllogs_file:
        for line in calllogs_file:
            values = line.replace(' ', '').strip(',\n').split(',')

            if len(values) != CALLLOGS_FIELDS or values[0] == FIRST_FIELD or '' in values:
                continue

            cursor.execute('''
            INSERT INTO callLogs (phoneNumber, startTime, endTime, direction, userId)
            VALUES (?, ?, ?, ?, ?)
            ''', values)


# This function will write analytics data to testUserAnalytics.csv - average call time, and number of calls per user.
# You must save records consisting of each userId, avgDuration, and numCalls
# example: 1,105.0,4 - where 1 is the userId, 105.0 is the avgDuration, and 4 is the numCalls.
def write_user_analytics(csv_file_path):
    cursor.execute('''
    SELECT userId, startTime, endTime
    FROM callLogs
    ''')

    user_data = {}

    for user_id, start_time, end_time in cursor.fetchall():
        call_duration = end_time - start_time

        if user_id in user_data:
            old_data = user_data[user_id]
            user_data[user_id] = (old_data[0] + call_duration, old_data[1] + 1)
        else:
            user_data[user_id] = (call_duration, 1)

    with open(csv_file_path, 'w') as analytics_file:
        analytics_file.write('userId,avgDuration,numCalls\n')

        for id, data in user_data.items():
            avg_duration = data[0] / data[1]
            analytics_file.write(f'{id},{avg_duration},{data[1]}\n')



# This function will write the callLogs ordered by userId, then start time.
# Then, write the ordered callLogs to orderedCalls.csv
def write_ordered_calls(csv_file_path):

    print("TODO: write_ordered_calls")



# No need to touch the functions below!------------------------------------------

# This function is for debugs/validation - uncomment the function invocation in main() to see the data in the database.
def select_from_users_and_call_logs():

    print()
    print("PRINTING DATA FROM USERS")
    print("-------------------------")

    # Select and print users data
    cursor.execute('''SELECT * FROM users''')
    for row in cursor:
        print(row)

    # new line
    print()
    print("PRINTING DATA FROM CALLLOGS")
    print("-------------------------")

    # Select and print callLogs data
    cursor.execute('''SELECT * FROM callLogs''')
    for row in cursor:
        print(row)


def return_cursor():
    return cursor


if __name__ == '__main__':
    main()