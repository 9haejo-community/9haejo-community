import requests
import uuid
from bs4 import BeautifulSoup
from pymongo import MongoClient
from flask import Flask, render_template, request, jsonify
app = Flask(__name__)

client = MongoClient('mongodb+srv://test:sparta@cluster0.cctcpnr.mongodb.net/?retryWrites=true&w=majority')
db = client.guhaejo
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
data = requests.get('https://news.daum.net/digital/#1', headers=headers)

soup = BeautifulSoup(data.text, 'html.parser')

@app.route('/')
def home():
    return render_template('index.html')

# @app.route('/test')
# def test():
#     return render_template('/test/test.html')

@app.route("/guhaejo", methods=["GET"])
def board_get():
    board_list = list(db.article.find({},{'_id':False}))
    return jsonify({'board_list': board_list})

@app.route("/guhaejo/news", methods=["GET"])
def news_get():
    news = soup.select('body > div.container-doc.cont-category > main > section > div.main-sub > div.box_g.box_news_major > ul > li')
    news_list = []
    for new in news:
        news_title = new.select_one('strong > a').text
        news_url = new.select_one('strong > a')['href']
        news_company = new.select_one('strong > span').text
        doc={
            'url': news_url,
            'title' : news_title,
            'company' : news_company}
        news_list.append(doc)
    return jsonify({'news_list': news_list})


@app.route("/guhaejo/todos", methods=["POST"])
def todo_post():
    todo_receive = request.form['todo_give']
    id_receive = request.form['id_give']

    todo_list = list(db.todos.find({},{'_id':False}))
    num = uuid.uuid4().hex
    doc = {
        'num':num,
        'todo':todo_receive,
        'id': id_receive,
        'done': 0
    }
    db.todos.insert_one(doc)
    return jsonify('msg',"등록 완료")

@app.route("/guhaejo/todos/done", methods=["POST"])
def todo_done():
    num_receive = request.form['num_give']
    done_receive = request.form['done_give']
    if int(done_receive) == 0:
        db.todos.update_one({'num': num_receive}, {'$set': {'done': 1}})
        return jsonify({'msg': '완료!'})
    else:
        db.todos.update_one({'num': num_receive}, {'$set': {'done': 0}})
        return jsonify({'msg': '다시!'})

@app.route("/guhaejo/todos", methods=["GET"])
def todo_get():
    todo_list = list(db.todos.find({},{'_id':False}))
    return jsonify({'todos': todo_list})

@app.route("/guhaejo/todos/delete", methods=["POST"])
def todo_delete():
    num_receive = request.form['num_give']
    db.todos.delete_one({'num': num_receive})
    return jsonify({'msg': '삭제 완료!'})

@app.route("/guhaejo/review", methods=["GET"])
def web_reivews_get():
    img_list = ['https://hanghae99.spartacodingclub.kr/_next/image?url=%2F_next%2Fstatic%2Fmedia%2Fhyundai_autoever-logo.4ac170ea.png&w=640&q=75',
                'https://hanghae99.spartacodingclub.kr/_next/image?url=%2F_next%2Fstatic%2Fmedia%2Fyeogi-logo.8550ea49.png&w=640&q=75',
                'https://hanghae99.spartacodingclub.kr/_next/image?url=%2F_next%2Fstatic%2Fmedia%2Fkbbank-logo.cc16ad1a.png&w=640&q=75',
                'https://hanghae99.spartacodingclub.kr/_next/image?url=%2F_next%2Fstatic%2Fmedia%2Fjinhak-logo.7b03c373.png&w=640&q=75',
                'https://hanghae99.spartacodingclub.kr/_next/image?url=%2F_next%2Fstatic%2Fmedia%2Fmegazonecloud-logo.5c1b17fe.png&w=2048&q=75',
                'https://hanghae99.spartacodingclub.kr/_next/image?url=%2F_next%2Fstatic%2Fmedia%2Ffinda-logo.2b20b042.png&w=256&q=75',
                'https://hanghae99.spartacodingclub.kr/_next/image?url=%2F_next%2Fstatic%2Fmedia%2Fhana-logo.4da14aa2.png&w=1920&q=75',
                'https://hanghae99.spartacodingclub.kr/_next/image?url=%2F_next%2Fstatic%2Fmedia%2Fbalaan-logo.ced9ed54.png&w=640&q=75',
                'https://hanghae99.spartacodingclub.kr/_next/image?url=%2F_next%2Fstatic%2Fmedia%2Fcafe24-logo.92bd253e.png&w=384&q=75',
                'https://hanghae99.spartacodingclub.kr/_next/image?url=%2F_next%2Fstatic%2Fmedia%2Fnewploy-logo.5ca6c380.png&w=3840&q=75',
                ]
    url = 'https://hanghae99.spartacodingclub.kr'
    headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
    data = requests.get(url,headers=headers)
    soup = BeautifulSoup(data.text, 'html.parser')
    reviews = soup.select('#__next > section > section.css-1pxpne5 > div > div.css-1y4ubqo > div.css-1ldg707')
    reviews_list = []
    for review in reviews:
        a = review.select_one('h3')
        if a is not None:
            title = review.select_one('h3').text
            company = review.select_one('p').text
            comment = review.select_one('p:last-child').text
            review_obj = {'title':title, 'company':company, 'comment':comment}
            reviews_list.append(review_obj)
    return jsonify({'reviews' : reviews_list, 'imgList': img_list})


@app.route("/guhaejo/view-count", methods=["POST"])
def view_count_post():
    post_num_receive = request.form['post_num']
    view_count_receive = request.form['view_count']
    db.article.update_one({'post_num': int(post_num_receive)},{'$set':{'view_count': int(view_count_receive)}})
    return jsonify('msg',"view-count+1 완료")


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
