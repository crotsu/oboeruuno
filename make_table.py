# 成績
import sqlite3

#データフォーマット
#id, 書籍,   問題番号,  出題回数,     正解回数,   不安回数,    間違い回数
#id, book_name, item_num, question_ct, answer_ct, anxiety_ct, mistake_ct

# ユーザー名
user_name = 'oeda'

#データベースに接続
filepath = 'score.sqlite'
connect = sqlite3.connect(filepath)
#filepathと同名のファイルがなければ，ファイルが作成されます

#テーブルを作成
cur = connect.cursor()
cur.execute('DROP TABLE IF EXISTS ' + user_name)

create_table = 'CREATE TABLE '+ user_name + '(id INTEGER PRIMARY KEY,book_name TEXT,item_no INTEGER,question_ct INTEGER,answer_ct INTEGER,anxiety_ct INTEGER,mistake_ct INTEGER)'
cur.execute(create_table)
connect.commit()

#連続でデータを挿入
data = []
for i in range(210):
    data.append(['80patterns.txt', i+1, 0, 0, 0, 0])

cur = connect.cursor()
cur.executemany('INSERT INTO ' + user_name + '(book_name, item_no, question_ct, answer_ct, anxiety_ct, mistake_ct) VALUES (?,?,?,?,?,?)', data)
connect.commit()
