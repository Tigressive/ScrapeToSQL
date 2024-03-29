import csv
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


def read_csv(start, done):
    entries = os.listdir('test/')
    for files in entries:
        if len(entries) > 0:
            with open(f'{start}/{files}') as csv_file:
                csv_reader = csv.reader(csv_file, delimiter=',')
                next(csv_reader)
                next(csv_reader)

                for row in csv_reader:
                    if not row[11]:
                        print("No Email - Skipping")
                    else:
                        bname = row[2]
                        bkeyword = row[1]
                        baddress = row[3]
                        bcity = row[5]
                        bstate = row[6]
                        bzip = row[7]
                        bwebsite = row[9]
                        bphone = row[10]
                        singleEmail = row[11].split(',')
                        bemail = singleEmail[0]

                        connect_sql(bname, bkeyword, baddress, bcity, bstate, bzip, bwebsite, bphone, bemail)

                print(f"Successfully Imported {files}")
                print("Next Import will run at 2:00 PM!")
                os.replace(f'{start}/{files}', f'{done}/{files.replace(".csv", "_done.csv")}')
        else:
            print("Empty - Time to start a new scrape!")


if __name__ == '__main__':
    start = input("Enter the starting directory")
    done = input("Enter the directory for the finished files")
    print()
    read_csv(start, done)
    schedule.every().day.at("02:00").do(read_csv)

    while True:
        schedule.run_pending()
        time.sleep(1)
