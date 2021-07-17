from __future__ import print_function

import mysql.connector
from mysql.connector import errorcode

import random   
import time 
from time import localtime, strftime




DB_NAME = 'temperature'

TABLES = {}

TABLES['chamber_probe_green'] = (
    "CREATE TABLE `chamber_probe_green`("
    "   `id` INT unsigned NOT NULL AUTO_INCREMENT,"
    "   `time` TIME NOT NULL,"
    "   `temp` FLOAT NOT NULL,"
    "   PRIMARY KEY (ID)"
    ") ENGINE=InnoDB")



TABLES['chamber_probe_blue'] = (
    "CREATE TABLE `chamber_probe_blue`("
    "   `id` INT unsigned NOT NULL AUTO_INCREMENT,"
    "   `time` TIME NOT NULL,"
    "   `temp` FLOAT NOT NULL,"
    "   PRIMARY KEY (ID)"
    ") ENGINE=InnoDB")



TABLES['food_probe_yellow'] = (
    "CREATE TABLE `food_probe_yellow`("
    "   `id` INT unsigned NOT NULL AUTO_INCREMENT,"
    "   `time` TIME NOT NULL,"
    "   `temp` FLOAT NOT NULL,"
    "   PRIMARY KEY (ID)"
    ") ENGINE=InnoDB")



TABLES['food_probe_red'] = (
    "CREATE TABLE `food_probe_red`("
    "   `id` INT unsigned NOT NULL AUTO_INCREMENT,"
    "   `time` TIME NOT NULL,"
    "   `temp` FLOAT NOT NULL,"
    "   PRIMARY KEY (ID)"
    ") ENGINE=InnoDB")


clock = strftime("%I:%M", localtime())

data = "{:.2f}".format(random.random()*100)


cnx = mysql.connector.connect(user='root',password='Mason.830')
cursor = cnx.cursor()

def create_database(cursor):
    try:
        cursor.execute(
            "CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8'".format(DB_NAME))
    except mysql.connector.Error as err:
        print("Failed creating database: {}".format(err))
        exit(1)
try:
    cursor.execute("USE {}".format(DB_NAME))
except mysql.connector.Error as err:
    print("Database {} does not exist.".format(DB_NAME))
    if err.errno == errorcode.ER_BAD_DB_ERROR:
        create_database(cursor)
        print("Database {} created successfully.".format(DB_NAME))
        cnx.database = DB_NAME
    else:
        print(err)
        exit(1)

for table_name in TABLES:
    table_description = TABLES[table_name]
    try:
        print("Creating table {}: ".format(table_name), end=' ')
        cursor.execute(table_description)
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
            print("Already exists.")
        else:
            print(err.msg)
    else:
        print("OK")




def insertData():

    while(True):

        AddDataBlue = ("INSERT INTO chamber_probe_blue "
                        "(time, temp)"
                        "VALUES (%s, %s)") 

        AddDataGreen = ("INSERT INTO chamber_probe_green "
                        "(time, temp)"
                        "VALUES (%s, %s)") 

        AddDataYellow = ("INSERT INTO food_probe_yellow "
                        "(time, temp)"
                        "VALUES (%s, %s)") 

        AddDataRed = ("INSERT INTO chamber_probe_blue "
                        "(time, temp)"
                        "VALUES (%s, %s)") 
        
        dataBlue = (clock, data)

        dataGreen = (clock, data)

        dataYellow = (clock, data)

        dataRed = (clock, data)
        print("Adding Blue Data")
        cursor.execute(AddDataBlue, dataBlue)
        print("Adding Green Data")
        cursor.execute(AddDataGreen, dataGreen)
        print("Adding Yellow Data")
        cursor.execute(AddDataYellow, dataYellow)
        print("Adding Red ddata")
        cursor.execute(AddDataRed, dataRed)

        cnx.commit()

        time.sleep(2)

insertData()

cursor.close()
cnx.close()
