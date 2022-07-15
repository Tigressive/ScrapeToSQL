# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
import pymysql
import csv


def connect_sql(bname, bkeyword, baddress, bcity, bstate, bzip, bwebsite, bphone, bemail):
    connection = pymysql.connect(host="localhost",
                                 user="aatkinson",
                                 password="test",
                                 database="schema_name",
                                 cursorclass=pymysql.cursors.DictCursor)

    connection.begin()
    cursor = connection.cursor()

    cursor.execute("INSERT INTO business (business_name, business_keyword, business_address, business_city, "
                   "business_state, business_zip, business_website, business_phone, business_email) VALUES (%s, %s, "
                   "%s, %s, %s, %s, %s, %s, %s )", (bname, bkeyword, baddress, bcity, bstate, bzip, bwebsite, bphone,
                                                    bemail))
    connection.commit()
    rows = cursor.fetchall()
    for row in rows:
        print(row)
    connection.close()


def read_csv():
    with open('Arizona Furniture stores.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        next(csv_reader)

        for row in csv_reader:
            if row[11] is "":
                next(csv_reader)
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


if __name__ == '__main__':
    read_csv()
