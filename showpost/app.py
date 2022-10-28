from flask import Flask, render_template, request, jsonify
app = Flask(__name__)
from datetime import datetime
now = datetime.now()


from pymongo import MongoClient
client = MongoClient('mongodb+srv://test:sparta@cluster0.cctcpnr.mongodb.net/?retryWrites=true&w=majority')
db = client.guhaejo

@app.route('/')
def home():
    return render_template('index.html')

@app.route("/comment", methods=["POST"])
def comment_post():
    comment_receive = request.form['comment_give']
    now = datetime.now()
    current_time = now.strftime("%Y/%m/%d, %H:%M:%S")
    all_comment = list(db.comment.find({},{'_id':False}))
    no_of_comment = len(all_comment) + 1
    doc = {
        'id': 1,
        'comment': comment_receive,
        'time': current_time,
        'total_comment': no_of_comment
    }
    db.comment.insert_one(doc)
    return jsonify({'msg': '작성완료!'})

@app.route("/comment", methods=["GET"])
def comment_get():
    comment_list = list(db.comment.find({}, {'_id': False}))
    return jsonify({'comments': comment_list})

@app.route("/article", methods=["GET"])
def article_get():
    article_list = list(db.article.find({}, {'_id': False}))
    return jsonify({'articles': article_list})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)