import sqlite3


class UrlModel():

    def __init__(self, name_db, url_list):
        self.url_list = url_list

        self.connect_sql = sqlite3.connect(f"./{name_db}.sqlite")
        self.cursor_sql = self.connect_sql.cursor()

        self.__first_add_in_db()


    def __first_add_in_db(self):
            if self.__execute_query(
                    """
                    CREATE TABLE url(
                        id INTEGER PRIMARY KEY,
                        url TEXT UNIQUE NOT NULL, 
                        data_yandex TEXT, 
                        current_yandex BOOLEAN NOT NULL,
                        data_google TEXT,
                        current_google BOOLEAN NOT NULL,
                        checked BOOLEAN NOT NULL
                    )
                    """
                    ):
                for url in self.url_list:
                    self.__execute_query(
                        f"""
                        INSERT INTO url(
                            url, 
                            current_yandex, 
                            current_google, 
                            checked
                            ) 

                        VALUES (
                            '{url}', 
                            {False}, 
                            {False}, 
                            {False}
                            )
                        """
                        )


    def __execute_query(self, query):
        try:
            self.cursor_sql.execute(query)
            self.connect_sql.commit()
            return True

        except sqlite3.Error as err:
            print(f"The error '{err}' occurred")
            return False


    def __execute_read_query(self, query):
        result = None
        try:
            self.cursor_sql.execute(query)
            result = self.cursor_sql.fetchall()
            return result
        except sqlite3.Error as err:
            print(f"The error '{err}' occurred")

    
    def select_url(self):
        res = self.__execute_read_query(f"SELECT url FROM url")
        return res


    def select_checked_url(self, checked=False):
        res = self.__execute_read_query(
            f"""
            SELECT url 
            FROM url 
            WHERE checked = {checked}
            """
            )
        return res


    def select_all(self):
        res = self.__execute_read_query(f"SELECT * FROM url")
        return res


    def add_result(self, url, field, data):
        self.__execute_query(
            f"""
            UPDATE url 
            SET {field} = '{data}' 
            WHERE url = '{url}'
            """
            )


    def delete_table(self):
        pass

