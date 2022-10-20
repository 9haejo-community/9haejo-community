from flask import Flask, render_template, request, jsonify
app = Flask(__name__)

from pymongo import MongoClient
import certifi

ca = certifi.where()

client = MongoClient('mongodb+srv://test:sparta@cluster0.cctcpnr.mongodb.net/?retryWrites=true&w=majority', tlsCAFile=ca)
db = client.dbsparta

@app.route('/')
def home():
    return render_template('article.html')

@app.route("/article", methods=["POST"])
def web_mars_post():
    title_receive = request.form['title_give']
    tag_receive = request.form['tag_give']
    text_receive = request.form['text_give']

    doc ={
        'title':title_receive,
        'tag':tag_receive,
        'text':text_receive
    }

    db.article.insert_one(doc)
    return jsonify({'msg': '등록완료!'})

@app.route("/article", methods=["GET"])
def web_mars_get():
    return jsonify({'msg': 'GET 연결 완료!'})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)