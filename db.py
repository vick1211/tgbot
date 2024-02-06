import sqlite3 as sq

class BotDB:
    def __init__(self, db_file):
        self.con = sq.connect(db_file)
        self.cur = self.con.cursor()

        self.cur.execute("""CREATE TABLE IF NOT EXISTS students(
                         id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                         user_id TEXT NOT NULL UNIQUE,
                         ФИО TEXT NOT NULL,
                         класс TEXT NOT NULL
        )""")

        self.cur.execute("""CREATE TABLE IF NOT EXISTS teachers(
                         id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                         user_id TEXT NOT NULL UNIQUE,
                         ФИО TEXT NOT NULL
        )""")

    def add_student(self, user_id, name, grade):
        self.cur.execute("INSERT INTO students(user_id, ФИО, класс) VALUES (?,?,?)",(user_id, name, grade))
        return self.con.commit()

    def add_teacher(self, user_id, name):
        self.cur.execute("INSERT INTO teachers(user_id, ФИО) VALUES (?,?)",(user_id, name))
        return self.con.commit()

    def student_exists(self, user_id):
        result = self.cur.execute("SELECT id FROM students WHERE user_id = ?", (user_id,))
        return bool(len(result.fetchall()))

    def teacher_exists(self, user_id):
        result = self.cur.execute("SELECT id FROM teachers WHERE user_id = ?", (user_id,))
        return bool(len(result.fetchall()))

    def show_data(self, user_id):
        if self.student_exists(user_id):
            result = self.cur.execute("SELECT ФИО, класс FROM students WHERE user_id = ?", (user_id,))
            studentData = result.fetchone()
            return 'Имя: ' + studentData[0] + '\n' + 'Должность: Ученик\n' + 'Класс: ' + studentData[1]
        elif self.teacher_exists(user_id):
            result = self.cur.execute("SELECT ФИО FROM teachers WHERE user_id = ?", (user_id,))
            teacherData = result.fetchone()
            return 'Имя: ' + teacherData[0] + '\n' + 'Должность: Учитель'

    def select_id_to_send_message(self, grade):
        result = self.cur.execute('SELECT user_id FROM students WHERE класс = ?',(grade,))
        return result.fetchall()

    def delete_user(self,user_id):
        if self.student_exists(user_id):
            self.cur.execute("DELETE FROM students WHERE user_id = ?",(user_id,))
        elif self.teacher_exists(user_id):
            self.cur.execute("DELETE FROM teachers WHERE user_id = ?", (user_id,))
        return self.con.commit()

    def close_db(self):
        self.con.close()