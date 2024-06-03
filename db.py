from dotenv import load_dotenv
import os
from flask import Flask
from flask_mysqldb import MySQL

load_dotenv()

def setup_db(app : Flask) :
    app.config['MYSQL_HOST'] = os.environ['MYSQL_HOST']
    app.config['MYSQL_USER'] = os.environ['MYSQL_USER']
    app.config['MYSQL_PASSWORD'] = os.environ['MYSQL_PASSWORD']
    app.config['MYSQL_DB'] = os.environ['MYSQL_DB']


class MysqlDB:

    mysql = None 
    
    @staticmethod
    def init_app(app):
        setup_db(app)
        MysqlDB.mysql = MySQL(app)

    @staticmethod
    def  get_db()-> MySQL: 
        if MysqlDB.mysql is None:
            raise Exception('Database not initialized')
        return MysqlDB.mysql

    @staticmethod
    def get_cursor():
        if MysqlDB.mysql is None:
            raise Exception('Database not initialized')
        return MysqlDB.mysql.connection.cursor()
    
    @staticmethod
    def commit() -> None:
        if MysqlDB.mysql is None:
            raise Exception('Database not initialized')
        MysqlDB.mysql.connection.commit()

    @staticmethod
    def close():
        if MysqlDB.mysql is None:
            raise Exception('Database not initialized')
        MysqlDB.mysql.connection.close()



