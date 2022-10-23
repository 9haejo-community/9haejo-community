import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient
from flask import Flask, render_template, request, jsonify
app = Flask(__name__)

client = MongoClient('mongodb+srv://test:sparta@cluster0.cctcpnr.mongodb.net/?retryWrites=true&w=majority')
db = client.guhaejo


@app.route('/')
def home():
    return render_template('index.html')
    
@app.route("/guhaejo", methods=["GET"])
def board_get():
    board_list = list(db.board.find({},{'_id':False}))
    return jsonify({'board_list': board_list})\

@app.route("/guhaejo/news", methods=["GET"])
def news_get():
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
    data = requests.get('https://news.daum.net/digital/#1', headers=headers)

    soup = BeautifulSoup(data.text, 'html.parser')
    news = soup.select('body > div.container-doc.cont-category > main > section > div.main-sub > div.box_g.box_news_major > ul > li')
    news_list = [];
    for new in news:
        news_title = new.select_one('strong > a').text
        news_url = new.select_one('strong > a')['href']
        news_company = new.select_one('strong > span').text
        doc={
            'url': news_url,
            'title' : news_title,
            'company' : news_company}
        news_list.append(doc);
    return jsonify({'news_list': news_list})
