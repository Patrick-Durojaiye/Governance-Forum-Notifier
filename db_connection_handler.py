import mysql.connector
from db_details import get_keys

def connect_to_db():
    db_host, db_user, db_pass, db_name = get_keys()
    mydb = mysql.connector.connect(
        host=db_host,
        user=db_user,
        password=db_pass,
        database=db_name
    )
    return mydb
