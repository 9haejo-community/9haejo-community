from flask import Flask, render_template, request, jsonify
app = Flask(__name__)

from pymongo import MongoClient
# client = MongoClient('')
# db = client.dbsparta

@app.route('/')
def home():
   return render_template('index.html')

@app.route("/homework", methods=["POST"])
def home_post():
    # name_receive = request.form['name_give']
    return jsonify({'msg':'저장 완료!'})

@app.route("/homework", methods=["GET"])
def home_get():
    # comment_list = list(db.fanbook.find({}, {'_id': False}))
    return jsonify({'comments': 'GET 완료!'})

if __name__ == '__main__':
   app.run('0.0.0.0', port=5000, debug=True)