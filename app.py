#https://tech-diary.net/flask-introduction/
#https://qiita.com/fghyuhi/items/b1d74198012152ab0458
#https://knt60345blog.com/flaskhtmlcss/#toc3
#https://www.esz.co.jp/blog/2847.html

# sqlite3 score.sqlite
# .table
# .schema oeda
# select * from oeda;

from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
import csv
import random

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///score.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

item = []
item_id = random.randint(1,210)
battle_point = 192012
rest_count = 0
        
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    book_name = db.Column(db.String(256), nullable=False)
    item_no = db.Column(db.Integer, nullable=False)
    question_ct = db.Column(db.Integer, nullable=False)
    answer_ct = db.Column(db.Integer, nullable=False)
    anxiety_ct = db.Column(db.Integer, nullable=False)
    mistake_ct = db.Column(db.Integer, nullable=False)
    __table_args__ = {'extend_existing': True}

def set_table_name(model, table_name):
    model.__table__.name = table_name
    
@app.route('/')
def index():
    return render_template('index.html', title = 'oboeruuno', battle_point = battle_point)

@app.route('/question', methods=['GET', 'POST'])
def question():
    global item_id
    if request.method == 'POST':
        print("##########")
        #post = db.session.get(Post, 10)
        post = Post.query.get(item_id)
        print(post)
        print("@@@@@@@@@@")
        radio = request.form.get('radio')
        print(radio)
        print(type(radio))

        post.question_ct = post.question_ct + 1
        if radio=='1':
            post.answer_ct = post.answer_ct + 1
        elif radio=='2':
            post.anxiety_ct = post.anxiety_ct + 1
        else:
            post.mistake_ct = post.mistake_ct + 1
        db.session.add(post)
        db.session.commit()
    
        item_id = random.randint(1,210)
        item_id = 200
        item = item_data[item_id]
        
        if radio=='1': #正解1, 不正解2
            global rest_count
            rest_count -= 1
            
        if rest_count==0:
            return render_template('index.html', title = 'oboeruuno', battle_point = battle_point)
 
    else:
        rest_count = 10
        item = item_data[item_id]
    return render_template('question.html', title = '出題（日本語）', message = item[1], rest_count = rest_count)

@app.route('/answer')
def answer():
    item = item_data[item_id]
    return render_template('answer.html', title = '解答（英語）', message = item[2], rest_count = rest_count)

def load_item_data(file_name):
    data = []
    with open(file_name, 'r', encoding='utf-8') as file:
        reader = csv.reader(file, delimiter='|')
        for row in reader:
            data.append((row[0].strip(), row[1].strip(), row[2].strip()))            
    return data

if __name__ == "__main__":
    file_name = "../englishbook_data/80patterns.txt"
    item_data = load_item_data(file_name)
    username = 'oeda'
    set_table_name(Post, username)

    app.run(debug=True)





'''    
# アプリケーションコンテキストを設定してデータベースを作成
from app import app, db
with app.app_context():
  db.create_all()
'''
