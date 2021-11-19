import sqlite3
import time

def get_str_time(timestamp: int) -> str:
    url_time_arr = time.localtime(timestamp)
    t = time.strftime("%Y-%m-%d %H:%M:%S", url_time_arr)
    return t

db = sqlite3.connect('QQ.db')
db_cursor = db.cursor()

select = db_cursor.execute('''SELECT "SendUin", "MsgTime", "strMsg", "nickName" FROM "main"."tb_TroopMsg_952121202" ORDER BY "MsgTime"''').fetchall()
# select = db_cursor.execute('''SELECT "SendUin", "MsgTime", "strMsg", "nickName" FROM "main"."tb_TroopMsg_1012562264" ORDER BY "MsgTime"''').fetchall()


with open('export.txt', 'a+', encoding="utf-8") as f:
    print(len(select))
    counter = 0
    for msg in select:
        counter += 1
        if counter % 10000 == 0:
            print(counter)
        if msg[0] == 0 or msg[2] == None:
            continue
        sender_info = get_str_time(msg[1]) + ' ' + msg[3] + '(' + str(msg[0]) + ')'
        msg_text = msg[2]
        f.write(sender_info + '\n' + msg_text + '\n\n')



input('FINISHED')