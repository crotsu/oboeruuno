#https://tech-diary.net/flask-introduction/
#https://qiita.com/fghyuhi/items/b1d74198012152ab0458
#https://knt60345blog.com/flaskhtmlcss/#toc3
#https://www.esz.co.jp/blog/2847.html

# sqlite3 score.sqlite
# .table
# .schema oeda
# select * from oeda;

from flask import Flask, render_template, request, redirect, g
from flask_sqlalchemy import SQLAlchemy
import csv
import random

REST_COUNT = 10 # 1回の問題数

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///score.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
item_id = random.randint(1,211)
item_set = []

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
    global item_set
    item_set = random.sample(range(1, 211), REST_COUNT)
    return render_template('index.html', title = 'oboeruuno', battle_point = battle_point)

@app.route('/question', methods=['GET', 'POST'])
def question():
    global item_id
    global item_set
    if request.method == 'POST':
        post = Post.query.get(item_id)
        radio = request.form.get('radio')

        post.question_ct = post.question_ct + 1
        if radio=='1':
            post.answer_ct = post.answer_ct + 1
        elif radio=='2':
            post.anxiety_ct = post.anxiety_ct + 1
        else:
            post.mistake_ct = post.mistake_ct + 1
        db.session.add(post)
        db.session.commit()
        print("##########################")
        print(item_set)
        item_id = random.choice(item_set)
        print(item_id)
        item = item_data[item_id]
        
        if radio=='1': #正解1, 不正解2
            global rest_count
            item_set.remove(item_id)
            rest_count -= 1
            
        if rest_count==0:
            return redirect('/')
 
    else:
        rest_count = REST_COUNT
        item = item_data[item_id]
    return render_template('question.html', title = '出題（日本語）', message = item[1], rest_count = rest_count)

@app.route('/answer')
def answer():
    post = Post.query.get(item_id)
    item = item_data[item_id]
    return render_template('answer.html', title = '解答（英語）', message = item[2], rest_count = rest_count, book_name=book_name, number=item[0], accuracy=post.answer_ct/(post.question_ct+1), question_ct=post.question_ct, answer_ct=post.answer_ct, anxiety_ct=post.anxiety_ct, mistake_ct=post.mistake_ct)

def load_item_data(file_name):
    data = []
    with open(file_name, 'r', encoding='utf-8') as file:
        reader = csv.reader(file, delimiter='|')
        for row in reader:
            data.append((row[0].strip(), row[1].strip(), row[2].strip()))            
    return data

if __name__ == "__main__":
    book_name = "80patterns.txt"    
    file_name = "../englishbook_data/"+book_name
    item_data = load_item_data(file_name)
    username = 'oeda'
    set_table_name(Post, username)
    battle_point = 234
    rest_count = REST_COUNT

    app.run(debug=True)