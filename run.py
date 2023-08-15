from scraper import Scraper
import mysql.connector
from multiprocessing import Pool
import time
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

def get_daos(mydb):
    mycursor = mydb.cursor()
    sql = "Select name_of_dao FROM forum_links"
    mycursor.execute(sql)
    results = mycursor.fetchall()
    mycursor.close()

    list_of_daos = []
    for dao in results:
        list_of_daos.append(dao[0])
    return list_of_daos

def scrape(dao):
    time.sleep(2)
    p = Scraper(dao=dao)
    pname, plink, ppinned = p.get_dao_details()
    p.fetch_new_post(last_post_title=pname, url=plink, pinned=ppinned)

def run():
    mydb = connect_to_db()
    daos = get_daos(mydb=mydb)

    pool = Pool()
    pool.map(scrape, daos)
    pool.close()


if __name__ == '__main__':
    run()
