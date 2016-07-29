import sqlite3
import os

def getConn():
    conn = sqlite3.connect('./DataBase/data.db')
    return conn

def getCursor(conn):
    if conn is not None:
        return conn.cursor()

def close_all(conn, cu):
    try:
        if cu is not None:
            cu.close()
    finally:
        if cu is not None:
            cu.close()

def createTable():
    sql = '''CREATE TABLE IF NOT EXISTS UserInfo(
                'Name'        VARCHAR(50) NOT NULL,
                'Password'    VARCHAR(16) NOT NULL,
                'Avatar'      VARCHAR(50) NOT NULL,
                PRIMARY KEY('Name')
                )'''
    conn = getConn()
    cu = getCursor(conn)
    cu.execute(sql)
    conn.commit()
    print 'Create Table Success!'
    close_all(conn,cu)

def insert(data):
    sql = 'INSERT INTO UserInfo VALUES (?,?,?)'
    conn = getConn()
    cu = getCursor(conn)
    cu.execute(sql,data)
    conn.commit()
    print 'Insert Success!'
    close_all(conn,cu)

def fetchAll(sql):
    conn = getConn()
    cu = getCursor(conn)
    cu.execute(sql)
    r = cu.fetchall()
    return r

def execute(sql):
    conn = getConn()
    cu = getCursor(conn)
    cu.execute(sql)
    conn.commit()
    close_all(conn,cu)
    print 'Execute success'

