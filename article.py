from flask import Flask, render_template, request, jsonify
app = Flask(__name__)

from datetime import datetime
now = datetime.now()

from pymongo import MongoClient
import certifi

ca = certifi.where()

client = MongoClient('mongodb+srv://test:sparta@cluster0.cctcpnr.mongodb.net/?retryWrites=true&w=majority', tlsCAFile=ca)
db = client.guhaejo

@app.route('/')
def home():
    return render_template('article.html')

@app.route("/article", methods=["POST"])
def web_article_post():
    title_receive = request.form['title_give']
    name_receive = request.form['name_give']
    tag_receive = request.form['tag_give']
    content_receive = request.form['content_give']
    article_list = list(db.article.find({},{'_id':False}))
    count = len(article_list) + 1
    now = datetime.now()
    current_time = now.strftime("%Y/%m/%d, %H:%M:%S")


    doc ={
        'title':title_receive,
        'nickname':name_receive,
        'tag':tag_receive,
        'content':content_receive,
        'post_num': count,
        'time':current_time
    }

    db.article.insert_one(doc)
    return jsonify({'msg': '등록완료!'})

@app.route("/article", methods=["GET"])
def web_article_get():

    return jsonify({'articles': 'GET 연결 완료!'})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)