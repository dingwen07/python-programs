import pyperclip
import sqlite3
import time
import platform
import os


def current_milli_time(): return int(round(time.time() * 1000))


DATABASE_FILE = 'cliplog.db'
node = platform.node()


def init_db(database_file='cliplog.db'):
    db = sqlite3.connect(database_file)
    db_cursor = db.cursor()
    db_cursor.execute('''CREATE TABLE "clipboard_log" (
	                    "id"	INTEGER NOT NULL UNIQUE,
	                    "time"	INTEGER,
	                    "node"	TEXT,
	                    "text"	TEXT,
	                    PRIMARY KEY("id" AUTOINCREMENT)
                    );''')


if __name__ == "__main__":
    if not os.path.exists(DATABASE_FILE):
        init_db(DATABASE_FILE)
    db = sqlite3.connect(DATABASE_FILE)
    db_cursor = db.cursor()
    old_clip = pyperclip.paste()
    while True:
        time.sleep(0.5)
        try:
            new_clip = pyperclip.paste()
        except Exception as e:
            continue
        if new_clip != old_clip and (not (new_clip.isspace() or new_clip.strip(' ') == '')):
            if new_clip.lower() == 'stop clipboard logger':
                pyperclip.copy('CLIPBOARD LOGGING STOPPED')
                exit()
            ctime = current_milli_time()
            db_cursor.execute('''INSERT INTO "main"."clipboard_log"("time","node","text") VALUES (?,?,?);''',
                              (ctime, node, new_clip.replace(os.linesep, '\n'),))
            db.commit()
        old_clip = new_clip
