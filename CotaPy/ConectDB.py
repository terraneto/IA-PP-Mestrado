import sqlite3

from sqlalchemy import create_engine


def Conecte():
    #   sqlEngine       = create_engine('mysql+pymysql://siasg:siasg@192.168.2.135/siasg', pool_recycle=3600)
    #   dbConnection    = sqlEngine.connect()

   e = create_engine('sqlite:..//Novembro-2022//siasg.db')  # pass your db url')  # pass your db url

   return e