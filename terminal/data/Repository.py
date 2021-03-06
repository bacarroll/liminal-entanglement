import random
import sqlite3


def create_connection(db_file):
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except sqlite3.Error as e:
        print(e)
    return None


class Repository:
    def __init__(self, con):
        self.connection = con
        self.connection.row_factory = self.__dict_factory
        self.cur = self.connection.cursor()
        self.categories = self.__retrieve_categories()

    # Builds dictionary from cursor result
    def __dict_factory(self, cursor, row):
        res_dict = {}
        for i, col in enumerate(cursor.description):
            res_dict[col[0]] = row[i]
        return res_dict

    def __retrieve_categories(self):
        self.cur.execute("SELECT * FROM CATEGORY")
        categories = self.cur.fetchall()
        return categories

    def choose_categories(self):
        chosen_cats = {}
        random.shuffle(self.categories)
        for x in range(1, 4):
            chosen_cats[x] = self.categories[x-1]
        return chosen_cats

    def get_random_question(self, category_id):
        self.cur.execute("select * from question where category_id = ? ORDER BY RANDOM() LIMIT 1",
                         str(category_id))
        return self.cur.fetchone()

    def insert_answer(self, answer):
        sql = '''INSERT INTO answer(question_id,text) VALUES(?,?)'''
        self.cur.execute(sql, answer)
        self.connection.commit()
        return self.cur.lastrowid

    def get_random_anwer(self):
        sql = '''SELECT a.text as 'answer', q.text as 'question' 
                    FROM answer a JOIN question q 
                    ON a.question_id = q.id 
                    ORDER BY RANDOM() LIMIT 1'''
        self.cur.execute(sql)
        return self.cur.fetchone()
