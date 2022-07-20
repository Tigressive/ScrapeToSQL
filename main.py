# This is a sample Python script.

import csv
# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
import os
import time

import pymysql
import schedule as schedule


def connect_sql(bname, bkeyword, baddress, bcity, bstate, bzip, bwebsite, bphone, bemail):
    connection = pymysql.connect(host="localhost",
                                 user="aatkinson",
                                 password="test",
                                 database="schema_name",
                                 cursorclass=pymysql.cursors.DictCursor)

    connection.begin()
    cursor = connection.cursor()
    cursor.execute(f"SELECT * FROM business WHERE (business_name) = %s", bname)
    entry = cursor.fetchone()

    if entry is None:
        cursor.execute("INSERT INTO business (business_name, business_keyword, business_address, "
                       "business_city, "
                       "business_state, business_zip, business_website, business_phone, business_email) VALUES (%s, "
                       "%s, "
                       "%s, %s, %s, %s, %s, %s, %s )",
                       (bname, bkeyword, baddress, bcity, bstate, bzip, bwebsite, bphone,
                        bemail))
        connection.commit()
    else:
        print("Entry Found")

    connection.close()


def read_csv():
    entries = os.listdir('test/')
    if len(entries) > 0:
        with open(f'test/{entries[0]}') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            next(csv_reader)

            for row in csv_reader:
                if not row[11]:
                    print("No Email")
                else:
                    bname = row[2]
                    bkeyword = row[1]
                    baddress = row[3]
                    bcity = row[5]
                    bstate = row[6]
                    bzip = row[7]
                    bwebsite = row[9]
                    bphone = row[10]
                    bemail = row[11]

                    connect_sql(bname, bkeyword, baddress, bcity, bstate, bzip, bwebsite, bphone, bemail)

            print(f"Successfully Imported {entries[0]} ")
            os.replace(f'test/{entries[0]}', f'done/{entries[0].replace(".csv", "_done.csv" )}')

    else:
        print("Empty - Time to start a new scrape!")


if __name__ == '__main__':
    read_csv()
    # schedule.every().day.at("02:00").do(read_csv)
    #
    # while True:
    #     schedule.run_pending()
    #     time.sleep(1)
