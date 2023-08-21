from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService
from messenger import send_to_tg
from db_connection_handler import connect_to_db

class Scraper:
    def __init__(self, dao):
        self.mydb = connect_to_db()
        self.dao = dao

    def get_dao_details(self):
        mycursor = self.mydb.cursor()
        sql = "Select post_name, forum_url, pinned FROM forum_links WHERE name_of_dao = %s"
        dao_name = (self.dao,)
        mycursor.execute(sql, dao_name)
        result = mycursor.fetchall()[0]
        return result[0], result[1], result[2]

    def fetch_new_post(self, last_post_title, url, pinned):
        self.driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
        self.driver.get(url)

        elements = self.driver.find_elements(By.CLASS_NAME, 'topic-list-body')
        for i in elements:
            if pinned:
                name = i.find_elements(By.TAG_NAME, 'tr')[1]
            else:
                name = i.find_element(By.TAG_NAME, 'tr')
            post_name = name.find_element(By.TAG_NAME, 'a').text
            link = name.find_element(By.TAG_NAME, 'a').get_attribute("href")
            post_link = link

            if last_post_title != post_name:
                last_post_title = post_name
                send_to_tg(post_title=last_post_title, post_link=post_link)
                self.update_db(post_name=post_name, post_link=post_link)
            else:
                self.mydb.cursor().close()

    def update_db(self, post_name, post_link):
        mycursor = self.mydb.cursor()
        sql = "Update forum_links set post_name=%s, links=%s WHERE name_of_dao=%s"
        values = (post_name, post_link, self.dao)
        mycursor.execute(sql, values)
        self.mydb.commit()
        mycursor.close()
